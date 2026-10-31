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


@pytest.mark.anyio
async def test_prove_retrieval_handles_streaming_progression():
    """Verify prove_retrieval does not fail early on 0 markers while text streams, succeeding once settled."""
    from scripts.promote_to_sdp01 import prove_retrieval

    mock_client = AsyncMock()
    # 1. init_count check -> returns 0
    # 2. type_js -> returns True
    # 3. submit_js -> returns True
    # 4. check_js loop:
    #    cycle 1: text_len=35, markers=0, generating=False (streaming start)
    #    cycle 2: text_len=366, markers=0, generating=False (streaming continue)
    #    cycle 3: text_len=2621, markers=13, generating=False (settled with citations)
    mock_client.evaluate.side_effect = [
        0,      # init_count
        True,   # type_js
        True,   # submit_js
        {"has_message": True, "is_generating": False, "text_len": 35, "markers": 0},
        {"has_message": True, "is_generating": False, "text_len": 366, "markers": 0},
        {"has_message": True, "is_generating": False, "text_len": 2621, "markers": 13},
    ]

    with patch("asyncio.sleep", new=AsyncMock(return_value=None)):
        ok = await prove_retrieval(mock_client, "dummy.pdf", "S03F", timeout=20.0)
        assert ok is True

    # Also verify that if text settles for >= 2 cycles without citations, it returns False
    mock_client_fail = AsyncMock()
    mock_client_fail.evaluate.side_effect = [
        0,      # init_count
        True,   # type_js
        True,   # submit_js
        {"has_message": True, "is_generating": False, "text_len": 200, "markers": 0},
        {"has_message": True, "is_generating": False, "text_len": 200, "markers": 0},
        {"has_message": True, "is_generating": False, "text_len": 200, "markers": 0},
    ]

    with patch("asyncio.sleep", new=AsyncMock(return_value=None)):
        ok_fail = await prove_retrieval(mock_client_fail, "dummy.pdf", "S03F", timeout=20.0)
        assert ok_fail is False


def test_verify_s03f_negative_search_rejects_tampered_text(tmp_path, monkeypatch):
    """
    Step 6 Hardening Gate (Finding S03F-R2-F3):
    Verify extract_and_validate_text fails closed with exit code 8 when
    extracted text does not match EXPECTED_TEXT_SHA256, unconditionally in CI.
    """
    from scripts.verify_s03f_negative_search import (
        extract_and_validate_text,
        EXPECTED_TEXT_SHA256
    )

    dummy_pdf = tmp_path / "dummy.pdf"
    dummy_bytes = b"%PDF-1.4 dummy pdf content for CI verification"
    dummy_pdf.write_bytes(dummy_bytes)
    dummy_sha = hashlib.sha256(dummy_bytes).hexdigest()

    monkeypatch.setattr("scripts.verify_s03f_negative_search.EXPECTED_RAW_PDF_SHA256", dummy_sha)
    monkeypatch.setattr("scripts.verify_s03f_negative_search.EXPECTED_RAW_PDF_BYTES", len(dummy_bytes))

    tampered_text_file = tmp_path / "tampered_text.txt"
    tampered_text_file.write_text("Corrupted or altered text from adversarial cache", encoding="utf-8")

    # Must fail closed with exit code 8
    text, sha, code = extract_and_validate_text(
        pdf_path=dummy_pdf,
        text_path=tampered_text_file,
        allow_text_digest_mismatch=False
    )
    assert code == 8
    assert sha != EXPECTED_TEXT_SHA256

    # When --allow-text-digest-mismatch is enabled, permits continuation (code 0)
    text, sha, code = extract_and_validate_text(
        pdf_path=dummy_pdf,
        text_path=tampered_text_file,
        allow_text_digest_mismatch=True
    )
    assert code == 0
    assert sha != EXPECTED_TEXT_SHA256


def test_verify_s03f_negative_search_dynamic_adjudication(monkeypatch):
    """
    Step 6 Hardening Gate (Findings S03F-R2-F1, S03F-R3-F1, S03F-R4-F1):
    Verify adjudicate_target and adjudicate_hit perform real evidence-grounded
    adjudication bound to authentic text digest and context witnesses, including
    on zero-hit decisions.
    """
    from scripts.verify_s03f_negative_search import (
        EXPECTED_TEXT_SHA256,
        TARGET_QUERIES,
        adjudicate_target,
        adjudicate_hit
    )

    queries_by_id = {q["id"]: q for q in TARGET_QUERIES}

    # 1. Target with 0 matches on unauthenticated text ("dummy full text" != EXPECTED_TEXT_SHA256)
    # MUST return UNVERIFIED_ZERO_MATCHES (authenticated=False), even if text_sha256 is spoofed!
    res_empty_unauth = adjudicate_target(queries_by_id["B001-1"], [], "dummy full text", text_sha256=EXPECTED_TEXT_SHA256)
    assert res_empty_unauth["classification"] == "UNVERIFIED_ZERO_MATCHES"
    assert res_empty_unauth["substantive"] is False
    assert res_empty_unauth["authenticated"] is False
    assert "cannot be certified" in res_empty_unauth["rationale"]

    res_empty_wrong_sha = adjudicate_target(queries_by_id["B001-1"], [], "dummy full text", text_sha256="wrong_sha")
    assert res_empty_wrong_sha["classification"] == "UNVERIFIED_ZERO_MATCHES"
    assert res_empty_wrong_sha["substantive"] is False
    assert res_empty_wrong_sha["authenticated"] is False

    # 2. Target with 0 matches on authenticated text (digest matches EXPECTED_TEXT_SHA256)
    # evaluates to NOT_DISCUSSED (authenticated=True)
    auth_text = "authenticated 504-page text fixture"
    auth_sha = hashlib.sha256(auth_text.encode("utf-8")).hexdigest()
    monkeypatch.setattr("scripts.verify_s03f_negative_search.EXPECTED_TEXT_SHA256", auth_sha)
    res_empty_auth = adjudicate_target(queries_by_id["B001-1"], [], auth_text, text_sha256=auth_sha)
    assert res_empty_auth["classification"] == "NOT_DISCUSSED"
    assert res_empty_auth["substantive"] is False
    assert res_empty_auth["authenticated"] is True
    assert "0 matches found under verified search patterns across all 504 pages." in res_empty_auth["rationale"]

    # 3. Out-of-catalog unverified hit fails closed to CONTEXT_REVIEW_REQUIRED
    unverified_hit = {
        "match": "Rom. iv. 3",
        "start": 500,
        "snippet": "Some text mentioning Rom. iv. 3 in passing..."
    }
    res_unverified = adjudicate_target(queries_by_id["B001-1"], [unverified_hit], "x" * 1000, text_sha256=auth_sha)
    assert res_unverified["classification"] == "CONTEXT_REVIEW_REQUIRED"
    assert res_unverified["substantive"] is False
    assert "require manual context review" in res_unverified["rationale"]


def test_verify_s03f_match_catalog_authentication_and_hash_binding(monkeypatch):
    """
    Step 6 Hardening Gate (Finding S03F-R3-F1):
    Verify that the verified match catalog is strictly cryptographically bound to
    EXPECTED_TEXT_SHA256 (both passed and computed from full_text), exact normalized
    match string, offset validity, and context witness.
    Wrong-text-at-known-offset, wrong hash, dummy full text, and altered witness MUST fail closed.
    """
    from scripts.verify_s03f_negative_search import (
        EXPECTED_TEXT_SHA256,
        TARGET_QUERIES,
        VERIFIED_MATCH_CATALOG,
        adjudicate_hit,
        adjudicate_target,
    )

    queries_by_id = {q["id"]: q for q in TARGET_QUERIES}

    # 0. Exact reviewer counterexample from S03F-R3-F1:
    # adjudicate_target(B001-6, [{"start":287850,"match":"Rom. xi. 34","snippet":"..."}], "dummy full text")
    # MUST fail closed to CONTEXT_REVIEW_REQUIRED (substantive=False), even if text_sha256 is passed!
    counterexample_hit = [{"start": 287850, "match": "Rom. xi. 34", "snippet": "..."}]
    res_counter_default = adjudicate_target(queries_by_id["B001-6"], counterexample_hit, "dummy full text")
    assert res_counter_default["classification"] == "CONTEXT_REVIEW_REQUIRED"
    assert res_counter_default["substantive"] is False

    res_counter_spoofed_sha = adjudicate_target(
        queries_by_id["B001-6"], counterexample_hit, "dummy full text", text_sha256=EXPECTED_TEXT_SHA256
    )
    assert res_counter_spoofed_sha["classification"] == "CONTEXT_REVIEW_REQUIRED"
    assert res_counter_spoofed_sha["substantive"] is False

    # Construct mock buffer containing exact authentic text at known offset 287850
    mock_context = "is clause is retained in Rom. xi. 34, while\nés συνβιβάσει αὐτ"
    match_str = "Rom. xi. 34"
    match_idx = mock_context.index(match_str)
    prefix_len = 287850 - match_idx
    mock_prefix = " " * prefix_len
    mock_text = mock_prefix + mock_context + (" " * 1000)
    assert mock_text[287850 : 287850 + len(match_str)] == match_str
    mock_sha = hashlib.sha256(mock_text.encode("utf-8")).hexdigest()

    hit_valid = {
        "match": match_str,
        "start": 287850,
        "snippet": mock_context
    }

    # 1. Before monkeypatching EXPECTED_TEXT_SHA256, mock_text's true SHA-256 differs from
    # EXPECTED_TEXT_SHA256, so even passing text_sha256=EXPECTED_TEXT_SHA256 MUST fail closed
    res_unauthenticated_buf = adjudicate_hit("B001-6", hit_valid, mock_text, text_sha256=EXPECTED_TEXT_SHA256)
    assert res_unauthenticated_buf["catalog_verified"] is False
    assert res_unauthenticated_buf["classification"] == "CONTEXT_REVIEW_REQUIRED"
    assert res_unauthenticated_buf["substantive"] is False

    # Bind EXPECTED_TEXT_SHA256 to mock_sha to test authenticated catalog lookup in CI
    monkeypatch.setattr("scripts.verify_s03f_negative_search.EXPECTED_TEXT_SHA256", mock_sha)

    # 2. Authentic text + valid hash -> PASSES with catalog verification
    res1 = adjudicate_hit("B001-6", hit_valid, mock_text, text_sha256=mock_sha)
    assert res1["catalog_verified"] is True
    assert res1["classification"] == "SUBSTANTIVE_CROSS_EPISTLE_COMPARISON"
    assert res1["substantive"] is True

    # 3. Wrong-hash regression: text_sha256 differs from EXPECTED_TEXT_SHA256
    # MUST fail closed to CONTEXT_REVIEW_REQUIRED with catalog_verified=False
    res_wrong_hash = adjudicate_hit("B001-6", hit_valid, mock_text, text_sha256="wrong_hash_1234567890abcdef")
    assert res_wrong_hash["catalog_verified"] is False
    assert res_wrong_hash["classification"] == "CONTEXT_REVIEW_REQUIRED"
    assert res_wrong_hash["substantive"] is False

    # 4. Wrong-text-at-known-offset regression: different match string at known offset 287850
    # MUST NOT receive the catalog verdict; MUST fail closed
    hit_wrong_match = {
        "match": "Rom. iv. 3",
        "start": 287850,
        "snippet": mock_context
    }
    res_wrong_match = adjudicate_hit("B001-6", hit_wrong_match, mock_text, text_sha256=mock_sha)
    assert res_wrong_match["catalog_verified"] is False
    assert res_wrong_match["classification"] == "CONTEXT_REVIEW_REQUIRED"
    assert res_wrong_match["substantive"] is False

    # 5. Altered context witness regression: context witness does not match catalog
    tampered_context = "is clause is retained in Rom. xi. 34, [ALTERED CONTEXT]"
    tampered_idx = tampered_context.index(match_str)
    tampered_prefix = " " * (287850 - tampered_idx)
    tampered_text = tampered_prefix + tampered_context + (" " * 1000)
    tampered_sha = hashlib.sha256(tampered_text.encode("utf-8")).hexdigest()
    monkeypatch.setattr("scripts.verify_s03f_negative_search.EXPECTED_TEXT_SHA256", tampered_sha)
    res_altered_witness = adjudicate_hit("B001-6", hit_valid, tampered_text, text_sha256=tampered_sha)
    assert res_altered_witness["catalog_verified"] is False
    assert res_altered_witness["classification"] == "CONTEXT_REVIEW_REQUIRED"
    assert res_altered_witness["substantive"] is False


def test_verify_s03f_search_patterns_reject_counterexamples():
    """
    Step 6 Hardening Gate (Finding S03F-R3-F2):
    Verify search regexes require unambiguous chapter/verse delimiters and complete
    numeral boundaries, rejecting counterexamples Hos. ix. 5, Isa. xix. 11, Rom. x. 12,
    Joel ii. 5, and missing delimiters while reliably matching legitimate citations and
    distinguishing direct Rom 10:13 hits from Rom 10:12, 13 cross-reference variants.
    """
    import re
    from scripts.verify_s03f_negative_search import POSITIVE_CONTROLS, TARGET_QUERIES

    queries_by_id = {q["id"]: q for q in TARGET_QUERIES}

    # 1. B001-3 (Hosea 1:10) MUST reject Hosea 9:5 (Hos. ix. 5) and missing delimiters
    pats_b001_3 = queries_by_id["B001-3"]["patterns"]
    assert not any(re.search(p, "Hos. ix. 5", re.I) for p in pats_b001_3), "Hos. ix. 5 falsely matched B001-3"
    assert not any(re.search(p, "Hos. ix", re.I) for p in pats_b001_3), "Hos. ix falsely matched B001-3"
    assert not any(re.search(p, "Hos 1 10", re.I) for p in pats_b001_3), "Missing delimiter Hos 1 10 matched B001-3"
    assert any(re.search(p, "Hos. i. 10", re.I) for p in pats_b001_3), "Legitimate Hos. i. 10 did not match"
    assert any(re.search(p, "Hosea 1:10", re.I) for p in pats_b001_3), "Legitimate Hosea 1:10 did not match"

    # 2. B001-7 (Isaiah 11:10) MUST reject Isaiah 19:11/12 (Isa. xix. 11) and missing delimiters
    pats_b001_7 = queries_by_id["B001-7"]["patterns"]
    assert not any(re.search(p, "Isa. xix. 11", re.I) for p in pats_b001_7), "Isa. xix. 11 falsely matched B001-7"
    assert not any(re.search(p, "Isa. xix. 12", re.I) for p in pats_b001_7), "Isa. xix. 12 falsely matched B001-7"
    assert not any(re.search(p, "Isa. xix", re.I) for p in pats_b001_7), "Isa. xix falsely matched B001-7"
    assert not any(re.search(p, "Isa 11 10", re.I) for p in pats_b001_7), "Missing delimiter Isa 11 10 matched B001-7"
    assert any(re.search(p, "Isa. xi. 10", re.I) for p in pats_b001_7), "Legitimate Isa. xi. 10 did not match"
    assert any(re.search(p, "Isaiah 11:10", re.I) for p in pats_b001_7), "Legitimate Isaiah 11:10 did not match"

    # 3. B001-5 (Romans 10:13 / Joel 2:32) MUST reject standalone Romans 10:12 and mismatched Joel 2:5 / 3:32,
    # and distinguish direct Rom 10:13 pattern from compound Rom 10:12, 13 cross-reference pattern
    pats_b001_5 = queries_by_id["B001-5"]["patterns"]
    direct_rom_10_13_pat, compound_rom_10_12_13_pat, joel_pat = pats_b001_5

    assert not any(re.search(p, "Rom. x. 12", re.I) for p in pats_b001_5), "Standalone Rom. x. 12 falsely matched B001-5"
    assert not any(re.search(p, "Rom. x. 12; Eph. ii. 14", re.I) for p in pats_b001_5), "Rom. x. 12; Eph. ii. 14 falsely matched B001-5"
    assert not any(re.search(p, "Rom 10 13", re.I) for p in pats_b001_5), "Missing delimiter Rom 10 13 matched B001-5"
    assert not any(re.search(p, "Joel ii. 5", re.I) for p in pats_b001_5), "Mismatched Joel ii. 5 falsely matched B001-5"
    assert not any(re.search(p, "Joel 3:32", re.I) for p in pats_b001_5), "Mismatched Joel 3:32 falsely matched B001-5"

    # Direct Rom 10:13 pattern matches only direct 10:13, not 10:12, 13
    assert re.search(direct_rom_10_13_pat, "Rom. x. 13", re.I)
    assert not re.search(direct_rom_10_13_pat, "Rom. x. 12, 13", re.I)

    # Compound Rom 10:12, 13 pattern matches only the 12, 13 cross-reference variant, not standalone 12 or direct 13
    assert re.search(compound_rom_10_12_13_pat, "Rom. x. 12, 13", re.I)
    assert re.search(compound_rom_10_12_13_pat, "Rom. x. 12,132.", re.I)
    assert not re.search(compound_rom_10_12_13_pat, "Rom. x. 12", re.I)
    assert not re.search(compound_rom_10_12_13_pat, "Rom. x. 13", re.I)

    # Joel pattern matches MT 2:32 and LXX 3:5
    assert re.search(joel_pat, "Joel ii. 32", re.I)
    assert re.search(joel_pat, "Joel 3:5", re.I)

    # 4. Positive controls also enforce mandatory delimiters and numeral boundaries
    assert not re.search(POSITIVE_CONTROLS[0]["pattern"], "Isa 29 14", re.I)
    assert re.search(POSITIVE_CONTROLS[0]["pattern"], "Isa. xxix. 14", re.I)


def test_verify_s03f_adjudication_rejects_generic_lxx_proximity():
    """
    Step 6 Hardening Gate (Finding S03F-R3-F3):
    Verify that out-of-catalog or unexpected matches do NOT automatically get classified
    as SUBSTANTIVE_DISCUSSION simply because the word 'LXX' or 'Hebrew' appears nearby.
    Must fail closed to CONTEXT_REVIEW_REQUIRED with substantive=False.
    """
    from scripts.verify_s03f_negative_search import (
        EXPECTED_TEXT_SHA256,
        TARGET_QUERIES,
        adjudicate_target
    )

    queries_by_id = {q["id"]: q for q in TARGET_QUERIES}

    # Context with an injected match near isolated generic words 'LXX' and 'Hebrew'
    injected_context = (
        "In our discussion of the LXX rendering of an unrelated passage, we note Hebrew usage. "
        "Meanwhile, Rom. iv. 3 is cited elsewhere in the literature without commentary."
    )
    hit = {
        "match": "Rom. iv. 3",
        "start": injected_context.index("Rom. iv. 3"),
        "snippet": injected_context
    }

    res = adjudicate_target(queries_by_id["B001-1"], [hit], injected_context, text_sha256=EXPECTED_TEXT_SHA256)
    assert res["classification"] == "CONTEXT_REVIEW_REQUIRED"
    assert res["substantive"] is False
    assert "require manual context review" in res["rationale"]


def test_verify_s03f_report_sections_dynamically_conditioned(tmp_path, monkeypatch):
    """
    Step 6 Hardening Gate (Findings S03F-R3-F3 & S03F-R4-F1):
    Verify that run_verification makes all report sections (Sections 1 through 7)
    strictly conditional on authenticated observed evidence, with zero contradictions:
      - Case A (Unauthenticated override, 0 target matches): marks all 8 targets as
        UNVERIFIED_ZERO_MATCHES and rejects any claim of 'NOT_DISCUSSED', 'Verified absent ... in the volume',
        or 'across all 504 pages under authenticated search patterns'.
      - Case B (Unauthenticated override, B001-5/B001-6 hits + injected unrelated 'LXX' near B001-1):
        marks matched targets CONTEXT_REVIEW_REQUIRED and zero-hit targets UNVERIFIED_ZERO_MATCHES.
      - Case C (Authenticated expected-hash run, 0 target matches): when EXPECTED_TEXT_SHA256 matches
        the text digest, zero-hit targets are certified as NOT_DISCUSSED while Sections 6 and 7
        report 0 matches without falsely claiming B001-5 or B001-6 are substantively present.
      - Case D (Canonical report path protection): refuses to overwrite DEFAULT_OUT_PATH on unauthenticated override.
    """
    from scripts.verify_s03f_negative_search import DEFAULT_OUT_PATH, run_verification

    dummy_pdf = tmp_path / "dummy.pdf"
    dummy_pdf.write_bytes(b"%PDF-1.4 synthetic")
    dummy_sha = hashlib.sha256(b"%PDF-1.4 synthetic").hexdigest()

    monkeypatch.setattr("scripts.verify_s03f_negative_search.EXPECTED_RAW_PDF_SHA256", dummy_sha)
    monkeypatch.setattr("scripts.verify_s03f_negative_search.EXPECTED_RAW_PDF_BYTES", len(b"%PDF-1.4 synthetic"))

    # Synthetic text passing positive controls and index checks, but with 0 matches for target queries
    synthetic_clean_text = (
        "POSITIVE CONTROLS:\n"
        "Isa. xxix. 14\n"
        "Gen. ii. 24\n"
        "Deut. xxv. 4\n"
        "Exod. xxxii. 6\n"
        "Isa. xxv. 8\n"
        "Sanday and Headlam\n\n"
        "MAIN COMMENTARY TEXT:\n"
        "General discussion of Corinthians without target citations.\n\n"
        "INDEXES\n"
        "I. GENERAL\n"
        "Allegorical interpretation Assimilation Aquila\n"
        "II. GREEK WORDS\n"
        "ἀδάπανος ἀλοάω\n"
        "III. LATIN AND ENGLISH WORDS\n"
        "Caritas underling\n"
        "Printed by Morrison & Gibb Limited, Edinburgh\n"
    )

    clean_text_file = tmp_path / "clean_text.txt"
    clean_text_file.write_text(synthetic_clean_text, encoding="utf-8")
    report_file = tmp_path / "report.md"

    # Case D: Canonical report replacement must fail closed under unauthenticated override
    with pytest.raises(RuntimeError, match="Refusing to overwrite canonical report path"):
        run_verification(
            dummy_pdf,
            clean_text_file,
            DEFAULT_OUT_PATH,
            allow_text_digest_mismatch=True
        )

    # Case A: Unauthenticated override with 0 target matches
    code = run_verification(
        dummy_pdf,
        clean_text_file,
        report_file,
        allow_text_digest_mismatch=True
    )
    assert code == 0
    report_content = report_file.read_text(encoding="utf-8")

    # Under mismatch override, MUST NOT claim NOT_DISCUSSED, Verified absent in volume, or 504-page certainty!
    assert "| **B001-1** | Romans 4:3 / Genesis 15:6 | 0 | **UNVERIFIED_ZERO_MATCHES** |" in report_content
    assert "| **B001-5** | Romans 10:13 / Joel 2:32 | 0 | **UNVERIFIED_ZERO_MATCHES** |" in report_content
    assert "| **B001-6** | Romans 11:34 / Isaiah 40:13 | 0 | **UNVERIFIED_ZERO_MATCHES** |" in report_content
    assert "NOT_DISCUSSED" not in report_content
    assert "Verified absent. No Fourth Section, Scripture Index, or Passage Index heading exists in the volume" not in report_content
    assert "0 matches found under verified search patterns across all 504 pages" not in report_content
    assert "across all 504 pages under authenticated search patterns" not in report_content
    assert "Authentication Status:** **UNAUTHENTICATED OVERRIDE**" in report_content
    assert "No Fourth Section or Scripture Index heading detected in supplied unauthenticated text (does not certify absence across the 504-page volume)" in report_content
    assert "No substantive comparative or secondary interpretive loci can be certified because the supplied text layer is unauthenticated." in report_content
    assert "For targets (**B001-1**, **B001-2**, **B001-3**, **B001-4**, **B001-5**, **B001-6**, **B001-7**, **B001-12**), **0 matches** were found in the supplied unauthenticated text (**UNVERIFIED_ZERO_MATCHES**); genuine absence across the 504-page volume is **not certified**." in report_content
    assert "NOTICE:** Verification executed under text digest mismatch override" in report_content

    # Case B: Source-hash mismatch with B001-5/B001-6 hits present AND injected unrelated 'LXX' near B001-1
    synthetic_unauth_hits_text = (
        "POSITIVE CONTROLS:\n"
        "Isa. xxix. 14\n"
        "Gen. ii. 24\n"
        "Deut. xxv. 4\n"
        "Exod. xxxii. 6\n"
        "Isa. xxv. 8\n"
        "Sanday and Headlam\n\n"
        "MAIN COMMENTARY TEXT:\n"
        "Unrelated discussion of LXX rendering and Hebrew clause near Rom. iv. 3 in passing.\n"
        "Also mentioning Joel ii. 32 and Rom. x. 12, 13 and Isa. xl. 13 and Rom. xi. 34 in unverified text.\n\n"
        "INDEXES\n"
        "I. GENERAL\n"
        "Allegorical interpretation Assimilation Aquila\n"
        "II. GREEK WORDS\n"
        "ἀδάπανος ἀλοάω\n"
        "III. LATIN AND ENGLISH WORDS\n"
        "Caritas underling\n"
        "Printed by Morrison & Gibb Limited, Edinburgh\n"
    )
    unauth_text_file = tmp_path / "unauth_hits.txt"
    unauth_text_file.write_text(synthetic_unauth_hits_text, encoding="utf-8")
    report_unauth_file = tmp_path / "report_unauth.md"

    code_unauth = run_verification(
        dummy_pdf,
        unauth_text_file,
        report_unauth_file,
        allow_text_digest_mismatch=True
    )
    assert code_unauth == 0
    unauth_report = report_unauth_file.read_text(encoding="utf-8")

    # Across Sections 1–7: hits under hash mismatch fail closed to CONTEXT_REVIEW_REQUIRED,
    # and zero-hit loci fail closed to UNVERIFIED_ZERO_MATCHES (never NOT_DISCUSSED)
    assert "| **B001-1** | Romans 4:3 / Genesis 15:6 | 1 | **CONTEXT_REVIEW_REQUIRED** |" in unauth_report
    assert "| **B001-5** | Romans 10:13 / Joel 2:32 | 2 | **CONTEXT_REVIEW_REQUIRED** |" in unauth_report
    assert "| **B001-6** | Romans 11:34 / Isaiah 40:13 | 2 | **CONTEXT_REVIEW_REQUIRED** |" in unauth_report
    assert "| **B001-2** | Romans 9:25 / Hosea 2:23 | 0 | **UNVERIFIED_ZERO_MATCHES** |" in unauth_report
    assert "NOT_DISCUSSED" not in unauth_report
    assert "SUBSTANTIVE_DISCUSSION" not in unauth_report
    assert "SUBSTANTIVE_CROSS_EPISTLE_COMPARISON" not in unauth_report
    assert "RELEVANT_INTERPRETIVE_CROSS_REFERENCE" not in unauth_report
    assert "No substantive comparative or secondary interpretive loci can be certified because the supplied text layer is unauthenticated." in unauth_report
    assert "Targets (**B001-1**, **B001-5**, **B001-6**) contain unverified matches requiring manual context review." in unauth_report
    assert "For targets (**B001-2**, **B001-3**, **B001-4**, **B001-7**, **B001-12**), **0 matches** were found in the supplied unauthenticated text (**UNVERIFIED_ZERO_MATCHES**); genuine absence across the 504-page volume is **not certified**." in unauth_report

    # Case C: Authenticated expected-hash run with 0 target matches retains NOT_DISCUSSED
    # while dynamically omitting B001-5/B001-6 substantive claims
    clean_sha = hashlib.sha256(synthetic_clean_text.encode("utf-8")).hexdigest()
    monkeypatch.setattr("scripts.verify_s03f_negative_search.EXPECTED_TEXT_SHA256", clean_sha)
    report_auth_zero_file = tmp_path / "report_auth_zero.md"

    code_auth_zero = run_verification(
        dummy_pdf,
        clean_text_file,
        report_auth_zero_file,
        allow_text_digest_mismatch=False
    )
    assert code_auth_zero == 0
    auth_zero_report = report_auth_zero_file.read_text(encoding="utf-8")

    assert "Authentication Status:** **AUTHENTICATED**" in auth_zero_report
    assert "| **B001-5** | Romans 10:13 / Joel 2:32 | 0 | **NOT_DISCUSSED** |" in auth_zero_report
    assert "| **B001-6** | Romans 11:34 / Isaiah 40:13 | 0 | **NOT_DISCUSSED** |" in auth_zero_report
    assert "UNVERIFIED_ZERO_MATCHES" not in auth_zero_report
    assert "No substantive comparative or secondary interpretive loci were detected in this volume under authenticated search patterns." in auth_zero_report
    assert "Admitted as substantive comparative evidence row" not in auth_zero_report
    assert "Admitted as secondary interpretive cross-reference evidence row" not in auth_zero_report
    assert "For targets (**B001-1**, **B001-2**, **B001-3**, **B001-4**, **B001-5**, **B001-6**, **B001-7**, **B001-12**), **0 matches** were detected across all 504 pages under authenticated search patterns." in auth_zero_report


def test_verify_s03f_negative_search_enforces_index_boundaries():
    """
    Step 6 Hardening Gate (Finding S03F-R2-F2):
    Verify verify_index_structure enforces section-localized positive controls,
    and fails closed on synthetic index fixtures containing a Fourth section
    or Scripture passage index heading.
    """
    from scripts.verify_s03f_negative_search import verify_index_structure

    # 1. Text without INDEXES heading fails
    res1 = verify_index_structure("No index heading here")
    assert res1["passed"] is False
    assert "INDEXES heading not found" in res1["error"]

    # 2. Text with INDEXES heading but without end delimiter fails
    res2 = verify_index_structure("INDEXES\nI. GENERAL\nAbbott\nII. GREEK WORDS\nIII. LATIN\nNo end colophon")
    assert res2["passed"] is False
    assert "Authentic index end delimiter not found" in res2["error"]

    # 3. Synthetic text with out-of-order sections fails
    synthetic_out_of_order = (
        "INDEXES\n"
        "III. LATIN\n"
        "II. GREEK WORDS\n"
        "I. GENERAL\n"
        "Printed by Morrison & Gibb Limited\n"
    )
    res3 = verify_index_structure(synthetic_out_of_order)
    assert res3["passed"] is False
    assert res3["ordered"] is False

    # 4. Adversarial fixture with IV. BIBLICAL REFERENCES fails closed
    synthetic_with_fourth_section = (
        "INDEXES\n"
        "I. GENERAL\n"
        "Allegorical interpretation Assimilation Aquila\n"
        "II. GREEK WORDS\n"
        "ἀδάπανος ἀλοάω\n"
        "III. LATIN\n"
        "Caritas underling\n"
        "IV. BIBLICAL REFERENCES\n"
        "Genesis, Exodus, Romans\n"
        "Printed by Morrison & Gibb Limited\n"
    )
    res4 = verify_index_structure(synthetic_with_fourth_section)
    assert res4["has_scripture_index"] is True
    assert res4["passed"] is False

    # 5. Adversarial fixture with INDEX OF SCRIPTURE fails closed
    synthetic_with_scripture_index = (
        "INDEXES\n"
        "I. GENERAL\n"
        "Allegorical interpretation Assimilation Aquila\n"
        "II. GREEK WORDS\n"
        "ἀδάπανος ἀλοάω\n"
        "III. LATIN\n"
        "Caritas underling\n"
        "INDEX OF SCRIPTURE\n"
        "Romans 4:3\n"
        "Printed by Morrison & Gibb Limited\n"
    )
    res5 = verify_index_structure(synthetic_with_scripture_index)
    assert res5["has_scripture_index"] is True
    assert res5["passed"] is False

    # 6. Non-localized positive controls fail closed
    # (e.g. ἀδάπανος placed in Section I instead of Section II)
    synthetic_mislocalized = (
        "INDEXES\n"
        "I. GENERAL\n"
        "Allegorical interpretation Assimilation Aquila ἀδάπανος\n"
        "II. GREEK WORDS\n"
        "ἀλοάω\n"
        "III. LATIN\n"
        "Caritas underling\n"
        "Printed by Morrison & Gibb Limited\n"
    )
    res6 = verify_index_structure(synthetic_mislocalized)
    assert res6["passed"] is False
    assert res6["positive_controls"]["Section II: ἀδάπανος"] is False
