import asyncio
import json
import sys
from pathlib import Path
from unittest.mock import AsyncMock, patch, MagicMock
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.notebooklm_ingest import (
    check_local_pdf,
    inspect_notebook_sources,
    prove_source_retrieval,
    ensure_source_ingested,
    get_extract_tab,
)

def test_check_local_pdf_success_and_missing(tmp_path):
    # Missing file fails closed
    with pytest.raises(FileNotFoundError, match="Local source PDF file not found"):
        check_local_pdf(str(tmp_path / "nonexistent.pdf"))
        
    # Too small / empty file fails closed
    empty_file = tmp_path / "empty.pdf"
    empty_file.write_bytes(b"short")
    with pytest.raises(ValueError, match="too small or corrupt"):
        check_local_pdf(str(empty_file))
        
    # Valid file returns metadata and correct SHA-256
    valid_file = tmp_path / "valid.pdf"
    content = b"%PDF-1.5 " + b"X" * 2000
    valid_file.write_bytes(content)
    meta = check_local_pdf(str(valid_file))
    assert meta["exists"] is True
    assert meta["size_bytes"] == len(content)
    assert meta["sha256"]
    assert meta["filename"] == "valid.pdf"

@pytest.mark.anyio
async def test_inspect_notebook_sources_extraction():
    mock_ws = AsyncMock()
    mock_state = {
        "title": "SDP-B001-EXTRACT",
        "sources": ["sanday_headlam_1895_romans_icc.pdf"],
        "source_count": 1,
        "has_error": False,
        "is_indexing": False,
        "has_checkbox": True,
        "dialog_open": False
    }
    with patch("scripts.notebooklm_ingest.evaluate_cdp", new=AsyncMock(return_value=mock_state)):
        res = await inspect_notebook_sources(mock_ws)
        assert res["title"] == "SDP-B001-EXTRACT"
        assert res["sources"] == ["sanday_headlam_1895_romans_icc.pdf"]
        assert not res["has_error"]
        assert not res["is_indexing"]

@pytest.mark.anyio
async def test_prove_source_retrieval_success_and_timeout():
    mock_ws = AsyncMock()
    
    # 1. Successful probe
    eval_mock = AsyncMock()
    eval_mock.side_effect = [
        0,       # init_count
        True,    # typed
        True,    # submitted
        {"settled": True, "text_len": 120, "markers": 3} # settled
    ]
    with patch("scripts.notebooklm_ingest.evaluate_cdp", new=eval_mock), \
         patch("scripts.notebooklm_ingest.asyncio.sleep", new=AsyncMock()):
        proven = await prove_source_retrieval(mock_ws, "sanday_headlam_1895_romans_icc.pdf", timeout=10.0)
        assert proven is True

    # 2. Probe timeout
    async def mock_timeout_eval(ws, msg_id, expr):
        if msg_id == 201: return 0
        if msg_id in (202, 203): return True
        return {"settled": False, "text_len": 10, "markers": 0}

    with patch("scripts.notebooklm_ingest.evaluate_cdp", new=mock_timeout_eval), \
         patch("scripts.notebooklm_ingest.asyncio.sleep", new=AsyncMock()):
        proven = await prove_source_retrieval(mock_ws, "sanday_headlam_1895_romans_icc.pdf", timeout=0.05)
        assert proven is False

@pytest.mark.anyio
async def test_ingest_category_a_already_ingested_skips_upload(tmp_path):
    """
    Reviewer Requirement: Category A / Idempotent Recovery
    If exactly one source tile exists and retrieval probe succeeds, skip upload and return verified.
    """
    mock_pdf = tmp_path / "sanday_headlam_1895_romans_icc.pdf"
    mock_pdf.write_bytes(b"%PDF-1.5 " + b"A" * 5000)
    
    mock_tab = {"webSocketDebuggerUrl": "ws://dummy", "url": "https://notebook.google.com/notebook/b3cd453a"}
    existing_state = {
        "title": "SDP-B001-EXTRACT",
        "sources": ["sanday_headlam_1895_romans_icc.pdf"],
        "source_count": 1,
        "has_error": False,
        "is_indexing": False,
        "dialog_open": False
    }
    
    mock_ws = AsyncMock()
    mock_ws_ctx = MagicMock()
    mock_ws_ctx.__aenter__.return_value = mock_ws
    mock_ws_ctx.__aexit__.return_value = None

    with patch("scripts.notebooklm_ingest.check_local_pdf", return_value={"filename": "sanday_headlam_1895_romans_icc.pdf", "size_mb": 45, "sha256": "dummy"}), \
         patch("scripts.notebooklm_ingest.get_extract_tab", new=AsyncMock(return_value=mock_tab)), \
         patch("scripts.notebooklm_ingest.websockets.connect", return_value=mock_ws_ctx), \
         patch("scripts.notebooklm_ingest.inspect_notebook_sources", new=AsyncMock(return_value=existing_state)), \
         patch("scripts.notebooklm_ingest.prove_source_retrieval", new=AsyncMock(return_value=True)):
        res = await ensure_source_ingested(source_id="S02F")
        assert res["status"] == "ALREADY_INGESTED_AND_VERIFIED"
        assert res["expected_filename"] == "sanday_headlam_1895_romans_icc.pdf"

@pytest.mark.anyio
async def test_ingest_delayed_spinner_progression(tmp_path):
    """
    Reviewer Requirement:
    Absence of spinner at first poll followed by later DOM update.
    The detector must handle delayed spinner appearance and settle properly without premature exit.
    """
    mock_tab = {"webSocketDebuggerUrl": "ws://dummy", "url": "https://notebook.google.com/notebook/b3cd453a"}
    
    progression = [
        {"title": "SDP-B001-EXTRACT", "sources": [], "has_error": False, "is_indexing": False, "dialog_open": True}, # initial
        {"title": "SDP-B001-EXTRACT", "sources": [], "has_error": False, "is_indexing": False},                       # poll 1
        {"title": "SDP-B001-EXTRACT", "sources": ["sanday_headlam_1895_romans_icc.pdf"], "has_error": False, "is_indexing": True}, # poll 2 (indexing)
        {"title": "SDP-B001-EXTRACT", "sources": ["sanday_headlam_1895_romans_icc.pdf"], "has_error": False, "is_indexing": False}, # poll 3 (settled!)
    ]
    
    inspect_mock = AsyncMock(side_effect=progression)
    mock_ws = AsyncMock()
    mock_ws_ctx = MagicMock()
    mock_ws_ctx.__aenter__.return_value = mock_ws
    mock_ws_ctx.__aexit__.return_value = None
    
    with patch("scripts.notebooklm_ingest.check_local_pdf", return_value={"filename": "sanday_headlam_1895_romans_icc.pdf", "size_mb": 45, "sha256": "dummy"}), \
         patch("scripts.notebooklm_ingest.get_extract_tab", new=AsyncMock(return_value=mock_tab)), \
         patch("scripts.notebooklm_ingest.websockets.connect", return_value=mock_ws_ctx), \
         patch("scripts.notebooklm_ingest.inspect_notebook_sources", new=inspect_mock), \
         patch("scripts.notebooklm_ingest.evaluate_cdp", new=AsyncMock(return_value={"x": 100, "y": 200, "w": 50, "h": 20})), \
         patch("scripts.notebooklm_ingest.send_cdp", new=AsyncMock()), \
         patch("asyncio.wait_for", new=AsyncMock(return_value=json.dumps({"method": "Page.fileChooserOpened", "params": {"backendNodeId": 99}}))), \
         patch("scripts.notebooklm_ingest.asyncio.sleep", new=AsyncMock()), \
         patch("scripts.notebooklm_ingest.prove_source_retrieval", new=AsyncMock(return_value=True)):
        res = await ensure_source_ingested(source_id="S02F", max_wait_seconds=50.0, heartbeat_seconds=0.01)
        assert res["status"] == "INGESTED_AND_VERIFIED"
        assert res["expected_filename"] == "sanday_headlam_1895_romans_icc.pdf"

@pytest.mark.anyio
async def test_ingest_successful_source_with_no_spinner(tmp_path):
    """
    Reviewer Requirement:
    Fast indexing where spinner is never observed, but source appears, has no error,
    and settles with successful retrieval proof.
    """
    mock_tab = {"webSocketDebuggerUrl": "ws://dummy", "url": "https://notebook.google.com/notebook/b3cd453a"}
    progression = [
        {"title": "SDP-B001-EXTRACT", "sources": [], "has_error": False, "is_indexing": False, "dialog_open": True}, # initial
        {"title": "SDP-B001-EXTRACT", "sources": ["sanday_headlam_1895_romans_icc.pdf"], "has_error": False, "is_indexing": False}, # appears settled
    ]
    inspect_mock = AsyncMock(side_effect=progression)
    mock_ws = AsyncMock()
    mock_ws_ctx = MagicMock()
    mock_ws_ctx.__aenter__.return_value = mock_ws
    mock_ws_ctx.__aexit__.return_value = None
    
    with patch("scripts.notebooklm_ingest.check_local_pdf", return_value={"filename": "sanday_headlam_1895_romans_icc.pdf", "size_mb": 45, "sha256": "dummy"}), \
         patch("scripts.notebooklm_ingest.get_extract_tab", new=AsyncMock(return_value=mock_tab)), \
         patch("scripts.notebooklm_ingest.websockets.connect", return_value=mock_ws_ctx), \
         patch("scripts.notebooklm_ingest.inspect_notebook_sources", new=inspect_mock), \
         patch("scripts.notebooklm_ingest.evaluate_cdp", new=AsyncMock(return_value={"x": 100, "y": 200, "w": 50, "h": 20})), \
         patch("scripts.notebooklm_ingest.send_cdp", new=AsyncMock()), \
         patch("asyncio.wait_for", new=AsyncMock(return_value=json.dumps({"method": "Page.fileChooserOpened", "params": {"backendNodeId": 99}}))), \
         patch("scripts.notebooklm_ingest.asyncio.sleep", new=AsyncMock()), \
         patch("scripts.notebooklm_ingest.prove_source_retrieval", new=AsyncMock(return_value=True)):
        res = await ensure_source_ingested(source_id="S02F", max_wait_seconds=50.0, heartbeat_seconds=0.01)
        assert res["status"] == "INGESTED_AND_VERIFIED"
        assert res["expected_filename"] == "sanday_headlam_1895_romans_icc.pdf"

@pytest.mark.anyio
async def test_ingest_duplicate_or_wrong_source_triggers_cleanup_quarantine():
    """
    Reviewer Requirement: Category D
    Duplicate sources or wrong/residual source (e.g. S01F Aageson) triggers cleanup.
    If cleanup fails to restore 0-source invariant, fails closed with RuntimeError.
    """
    mock_tab = {"webSocketDebuggerUrl": "ws://dummy", "url": "https://notebook.google.com/notebook/b3cd453a"}
    # Dirty state with residual Aageson
    dirty_state = {
        "title": "SDP-B001-EXTRACT",
        "sources": ["aageson_1984_pauls_use_of_scripture.pdf"],
        "has_error": False,
        "is_indexing": False,
        "dialog_open": False
    }
    mock_ws = AsyncMock()
    mock_ws_ctx = MagicMock()
    mock_ws_ctx.__aenter__.return_value = mock_ws
    mock_ws_ctx.__aexit__.return_value = None
    
    # After cleanup attempt, sources still not empty -> raises RuntimeError
    inspect_mock = AsyncMock(return_value=dirty_state)

    with patch("scripts.notebooklm_ingest.check_local_pdf", return_value={"filename": "sanday_headlam_1895_romans_icc.pdf", "size_mb": 45, "sha256": "dummy"}), \
         patch("scripts.notebooklm_ingest.get_extract_tab", new=AsyncMock(return_value=mock_tab)), \
         patch("scripts.notebooklm_ingest.websockets.connect", return_value=mock_ws_ctx), \
         patch("scripts.notebooklm_ingest.inspect_notebook_sources", new=inspect_mock), \
         patch("scripts.notebooklm_ingest.evaluate_cdp", new=AsyncMock()), \
         patch("scripts.notebooklm_ingest.send_cdp", new=AsyncMock()), \
         patch("scripts.notebooklm_ingest.asyncio.sleep", new=AsyncMock()):
        with pytest.raises(RuntimeError, match="Could not restore clean 0-source invariant"):
            await ensure_source_ingested(source_id="S02F", max_wait_seconds=10.0, heartbeat_seconds=0.01)

@pytest.mark.anyio
async def test_ingest_terminal_error_fails_closed():
    """
    Reviewer Requirement:
    Terminal error indicator on source card fails closed immediately.
    """
    mock_tab = {"webSocketDebuggerUrl": "ws://dummy", "url": "https://notebook.google.com/notebook/b3cd453a"}
    error_state = {
        "title": "SDP-B001-EXTRACT",
        "sources": ["sanday_headlam_1895_romans_icc.pdf"],
        "has_error": True,
        "is_indexing": False,
        "dialog_open": True
    }
    
    inspect_mock = AsyncMock(side_effect=[
        {"title": "SDP-B001-EXTRACT", "sources": [], "has_error": False, "is_indexing": False, "dialog_open": True},
        error_state
    ])
    mock_ws = AsyncMock()
    mock_ws_ctx = MagicMock()
    mock_ws_ctx.__aenter__.return_value = mock_ws
    mock_ws_ctx.__aexit__.return_value = None
    
    with patch("scripts.notebooklm_ingest.check_local_pdf", return_value={"filename": "sanday_headlam_1895_romans_icc.pdf", "size_mb": 45, "sha256": "dummy"}), \
         patch("scripts.notebooklm_ingest.get_extract_tab", new=AsyncMock(return_value=mock_tab)), \
         patch("scripts.notebooklm_ingest.websockets.connect", return_value=mock_ws_ctx), \
         patch("scripts.notebooklm_ingest.inspect_notebook_sources", new=inspect_mock), \
         patch("scripts.notebooklm_ingest.evaluate_cdp", new=AsyncMock(return_value={"x": 100, "y": 200, "w": 50, "h": 20})), \
         patch("scripts.notebooklm_ingest.send_cdp", new=AsyncMock()), \
         patch("asyncio.wait_for", new=AsyncMock(return_value=json.dumps({"method": "Page.fileChooserOpened", "params": {"backendNodeId": 99}}))), \
         patch("scripts.notebooklm_ingest.asyncio.sleep", new=AsyncMock()):
        with pytest.raises(RuntimeError, match="Terminal error indicator detected"):
            await ensure_source_ingested(source_id="S02F", max_wait_seconds=30.0, heartbeat_seconds=0.01)

@pytest.mark.anyio
async def test_ingest_stuck_indexing_times_out():
    """
    Reviewer Requirement:
    Monotonic timeout deadline prevents infinite polling when indexing hangs.
    """
    mock_tab = {"webSocketDebuggerUrl": "ws://dummy", "url": "https://notebook.google.com/notebook/b3cd453a"}
    stuck_state = {
        "title": "SDP-B001-EXTRACT",
        "sources": ["sanday_headlam_1895_romans_icc.pdf"],
        "has_error": False,
        "is_indexing": True, # Always indexing!
        "dialog_open": True
    }
    
    first_call = True
    async def mock_inspect(ws):
        nonlocal first_call
        if first_call:
            first_call = False
            return {"title": "SDP-B001-EXTRACT", "sources": [], "has_error": False, "is_indexing": False, "dialog_open": True}
        return stuck_state
    
    mock_ws = AsyncMock()
    mock_ws_ctx = MagicMock()
    mock_ws_ctx.__aenter__.return_value = mock_ws
    mock_ws_ctx.__aexit__.return_value = None
    
    # Simulate time advancing by 1 second on each sleep
    simulated_time = 1000.0
    def mock_time():
        nonlocal simulated_time
        return simulated_time
    async def mock_sleep(secs):
        nonlocal simulated_time
        simulated_time += 1.0

    with patch("scripts.notebooklm_ingest.check_local_pdf", return_value={"filename": "sanday_headlam_1895_romans_icc.pdf", "size_mb": 45, "sha256": "dummy"}), \
         patch("scripts.notebooklm_ingest.get_extract_tab", new=AsyncMock(return_value=mock_tab)), \
         patch("scripts.notebooklm_ingest.websockets.connect", return_value=mock_ws_ctx), \
         patch("scripts.notebooklm_ingest.inspect_notebook_sources", new=mock_inspect), \
         patch("scripts.notebooklm_ingest.evaluate_cdp", new=AsyncMock(return_value={"x": 100, "y": 200, "w": 50, "h": 20})), \
         patch("scripts.notebooklm_ingest.send_cdp", new=AsyncMock()), \
         patch("asyncio.wait_for", new=AsyncMock(return_value=json.dumps({"method": "Page.fileChooserOpened", "params": {"backendNodeId": 99}}))), \
         patch("time.time", side_effect=mock_time), \
         patch("scripts.notebooklm_ingest.asyncio.sleep", new=mock_sleep):
        with pytest.raises(TimeoutError, match="Monotonic deadline .* exceeded"):
            await ensure_source_ingested(source_id="S02F", max_wait_seconds=2.0, heartbeat_seconds=1.0)

@pytest.mark.anyio
async def test_get_extract_tab_parked_and_missing():
    """
    Reviewer Requirement:
    Check parked tab restoration and fail closed on missing/incorrect tab.
    """
    # 1. Missing tab fails closed
    with patch("urllib.request.urlopen") as mock_url:
        mock_resp = MagicMock()
        mock_resp.read.return_value = json.dumps([{"url": "https://google.com"}]).encode()
        mock_url.return_value.__enter__.return_value = mock_resp
        with pytest.raises(RuntimeError, match="tab matching .* not found"):
            await get_extract_tab(notebook_pattern="b3cd453a")

    # 2. Parked tab gets restored
    parked_tab = {
        "url": "chrome-extension://dummy/park.html#url=https://notebook.google.com/notebook/b3cd453a",
        "webSocketDebuggerUrl": "ws://dummy"
    }
    live_tab = {
        "url": "https://notebook.google.com/notebook/b3cd453a",
        "webSocketDebuggerUrl": "ws://dummy"
    }
    with patch("urllib.request.urlopen") as mock_url, \
         patch("scripts.notebooklm_ingest.websockets.connect", return_value=AsyncMock()), \
         patch("scripts.notebooklm_ingest.send_cdp", new=AsyncMock()), \
         patch("scripts.notebooklm_ingest.asyncio.sleep", new=AsyncMock()):
        mock_resp1 = MagicMock()
        mock_resp1.read.return_value = json.dumps([parked_tab]).encode()
        mock_resp2 = MagicMock()
        mock_resp2.read.return_value = json.dumps([live_tab]).encode()
        mock_url.return_value.__enter__.side_effect = [mock_resp1, mock_resp2]
        
        t = await get_extract_tab(notebook_pattern="b3cd453a")
        assert "park.html" not in t["url"]
        assert "b3cd453a" in t["url"]
