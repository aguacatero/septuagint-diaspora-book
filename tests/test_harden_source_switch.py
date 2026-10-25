import asyncio
import hashlib
import json
import sys
from pathlib import Path
from unittest.mock import AsyncMock, patch
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.queue_context import get_source_context, validate_output_path_isolation
from scripts.run_secondary_prompt import validate_notebook_state
from scripts.promote_to_sdp01 import promote_source, inspect_sdp01


def hash_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


# Cryptographic ledger of canonical SHA-256 digests for accepted S01F and S02F artifacts
CANONICAL_S01F_HASHES = {
    "argument_map.md": "6215386a3513ecdc8153cbabe6c16af6c5cbc91c3d018b5027dafe93155ee581",
    "bibliography_leads.md": "f03fe8d9838bcfcee6d527a1c48ecb92982eb25daf7824a4001f4bc1353247b0",
    "counterevidence.md": "cadc6204038f6efc311f0c9b89686b4b3e62ccf0cb3de73d891180473791988c",
    "extraction.md": "097c7a2fcb5562170ba54f04289e1d99d1ac857a089b48f448ae0c87d09993df",
    "metadata.md": "b1be23120dccf6df94dcb35cd6a71344d22b9333c2cfcf67a9aee81b50adc961",
    "notebooklm_self_audit.md": "e4dec66fcaa5325b09eb41721558bc22ec77089e54c9dadcc1ff360f878bfe0d",
    "relevance_scan.md": "2bb82483eeaea6a9fe32481826739d93ddf38f84dc23114b6c9960a3f15b2bbc",
    "citation_ledger.csv": "9929e628d2453eeda1f57c410189b53514b9771f694989588684f73c5e52980c",
}

CANONICAL_S02F_HASHES = {
    "argument_map.md": "40293df29dbf33829c47373325ee6f525a8b4d2c2bfbb706b92a10d2d3edeb33",
    "bibliography_leads.md": "63f803e7b7c64947ce7b506727a8616b08d871731341b71e3d82a2385045c17a",
    "counterevidence.md": "f5c267b8e45e8932cae33b35d3e5ce3da449e90ce10830ae763fc2cbcad1bf65",
    "excursus_extraction.md": "b084e5c988bbc9281beb802dacf0e75fd034ad0d72c9f0968e4377b5bb71ae9a",
    "extraction.md": "a3ab3836a42f362316ced84a472ca72e282806942beb6d2c1371c1962867a72a",
    "full_volume_search_log.md": "4f5c6f6cc518f0a0bd130a8c33ef37fc6f5c20c8accd099834b92f3be22b1359",
    "ingestion_diagnostic.md": "b08da58e274eaa61b1837da15758dd12e0d30ecafe2402255b0f1ccba80b6821",
    "metadata.md": "be44fed85fd31d461c2082e067b707a0f969becdc588e123d42380fe1b89c57f",
    "notebooklm_self_audit.md": "e3974d3e761db9bf498ecb4cd352581a2b6d18621faf83a86f8be9fdacf1af62",
    "relevance_scan.md": "9a91c8624f6dfd589ebbc2476db1234a40a5dc5378e48fecf5f481e713209589",
    "citation_ledger.csv": "feb9feeed92a3b885325700d9c7c9e68a4b7b0328eabc97796a5d3d70ed5377b",
    "provenance_manifest.json": "f884083d1e12cad55cb4c219f04a1e90b0cd2eaa5ac7c4c11c975900d02f459e",
}


def test_preserve_accepted_s01f_and_s02f_artifacts():
    """Verify that accepted S01F and S02F artifacts remain strictly identical and untouched."""
    repo_root = Path(__file__).resolve().parent.parent
    s01f_dir = repo_root / "research/inbox/B001-pauline-txt-pilot/sources/S01F"
    s02f_dir = repo_root / "research/inbox/B001-pauline-txt-pilot/sources/S02F"

    for fname, expected_hash in CANONICAL_S01F_HASHES.items():
        p = s01f_dir / fname
        assert p.is_file(), f"Missing S01F canonical artifact: {p}"
        actual = hash_file(p)
        assert actual == expected_hash, f"Cryptographic integrity violation on {p}: expected {expected_hash}, got {actual}"

    for fname, expected_hash in CANONICAL_S02F_HASHES.items():
        p = s02f_dir / fname
        assert p.is_file(), f"Missing S02F canonical artifact: {p}"
        actual = hash_file(p)
        assert actual == expected_hash, f"Cryptographic integrity violation on {p}: expected {expected_hash}, got {actual}"


def test_citation_ownership_isolation():
    """Verify validate_output_path_isolation blocks cross-source directory contamination."""
    # S03F writing into S03F succeeds
    validate_output_path_isolation("/path/to/sources/S03F/output.json", "S03F")

    # S03F writing into S02F or S01F fails closed
    with pytest.raises(RuntimeError, match="cross-source artifact overwrite blocked"):
        validate_output_path_isolation("/path/to/sources/S02F/output.json", "S03F")

    with pytest.raises(RuntimeError, match="cross-source artifact overwrite blocked"):
        validate_output_path_isolation("/path/to/sources/S01F/output.json", "S03F")


def test_ingest_duplicate_or_wrong_source_fails_closed():
    """Verify validate_notebook_state rejects multiple sources or wrong single source."""
    # Duplicate sources in extraction notebook
    with pytest.raises(RuntimeError, match="Expected exactly 1 source"):
        validate_notebook_state(
            title="SDP-B001-EXTRACT",
            sources=["robertson_plummer_1911_1corinthians_icc.pdf", "sanday_headlam_1895_romans_icc.pdf"],
            expected_source="robertson_plummer_1911_1corinthians_icc.pdf"
        )

    # 0 sources
    with pytest.raises(RuntimeError, match="Expected exactly 1 source"):
        validate_notebook_state(
            title="SDP-B001-EXTRACT",
            sources=[],
            expected_source="robertson_plummer_1911_1corinthians_icc.pdf"
        )

    # Wrong single source
    with pytest.raises(RuntimeError, match="Source identity invariant violated"):
        validate_notebook_state(
            title="SDP-B001-EXTRACT",
            sources=["sanday_headlam_1895_romans_icc.pdf"],
            expected_source="robertson_plummer_1911_1corinthians_icc.pdf"
        )

    # Correct single source passes
    validate_notebook_state(
        title="SDP-B001-EXTRACT",
        sources=["robertson_plummer_1911_1corinthians_icc.pdf"],
        expected_source="robertson_plummer_1911_1corinthians_icc.pdf"
    )


@pytest.mark.anyio
async def test_promote_to_sdp01_requires_successful_retrieval_probe():
    """
    Step 6 Hardening Gate:
    Verify promote_source fails closed with RuntimeError when prove_retrieval returns False.
    """
    mock_tabs = [{
        "id": "tab123",
        "url": "https://notebook.google.com/notebook/65d4bea4-7939-4754-bb7b-09d420e8ff19",
        "webSocketDebuggerUrl": "ws://dummy"
    }]

    mock_state_already_present = {
        "title": "SDP-01 Paul",
        "sources": ["robertson_plummer_1911_1corinthians_icc.pdf"],
        "is_indexing": False,
        "has_error": False
    }

    with patch("urllib.request.urlopen") as mock_url, \
         patch("websockets.connect") as mock_ws_conn, \
         patch("scripts.promote_to_sdp01.inspect_sdp01", new=AsyncMock(return_value=mock_state_already_present)), \
         patch("scripts.promote_to_sdp01.prove_retrieval", new=AsyncMock(return_value=False)):

        mock_url.return_value.__enter__.return_value.read.return_value = json.dumps(mock_tabs).encode()

        mock_ws = AsyncMock()
        mock_ws_conn.return_value.__aenter__.return_value = mock_ws

        with pytest.raises(RuntimeError, match="retrieval verification failed"):
            await promote_source(source_id="S03F", probe_timeout=1.0)


@pytest.mark.anyio
async def test_promote_to_sdp01_fails_on_unattributed_or_error_state():
    """Verify promote_source fails closed when notebook is indexing or has error state."""
    mock_tabs = [{
        "id": "tab123",
        "url": "https://notebook.google.com/notebook/65d4bea4-7939-4754-bb7b-09d420e8ff19",
        "webSocketDebuggerUrl": "ws://dummy"
    }]

    # 1. Source already present but is_indexing=True
    state_indexing = {
        "title": "SDP-01 Paul",
        "sources": ["robertson_plummer_1911_1corinthians_icc.pdf"],
        "is_indexing": True,
        "has_error": False
    }

    with patch("urllib.request.urlopen") as mock_url, \
         patch("websockets.connect") as mock_ws_conn, \
         patch("scripts.promote_to_sdp01.inspect_sdp01", new=AsyncMock(return_value=state_indexing)):

        mock_url.return_value.__enter__.return_value.read.return_value = json.dumps(mock_tabs).encode()
        mock_ws = AsyncMock()
        mock_ws_conn.return_value.__aenter__.return_value = mock_ws

        with pytest.raises(RuntimeError, match="currently indexing"):
            await promote_source(source_id="S03F")

    # 2. Source already present but has_error=True
    state_error = {
        "title": "SDP-01 Paul",
        "sources": ["robertson_plummer_1911_1corinthians_icc.pdf"],
        "is_indexing": False,
        "has_error": True
    }

    with patch("urllib.request.urlopen") as mock_url, \
         patch("websockets.connect") as mock_ws_conn, \
         patch("scripts.promote_to_sdp01.inspect_sdp01", new=AsyncMock(return_value=state_error)):

        mock_url.return_value.__enter__.return_value.read.return_value = json.dumps(mock_tabs).encode()
        mock_ws = AsyncMock()
        mock_ws_conn.return_value.__aenter__.return_value = mock_ws

        with pytest.raises(RuntimeError, match="has error state"):
            await promote_source(source_id="S03F")
