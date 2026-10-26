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


def test_verify_s03f_negative_search_dynamic_adjudication():
    """
    Step 6 Hardening Gate (Finding S03F-R2-F1):
    Verify adjudicate_target and adjudicate_hit perform real evidence-grounded
    adjudication rather than hard-coded string reflection.
    """
    from scripts.verify_s03f_negative_search import (
        TARGET_QUERIES,
        adjudicate_target,
        adjudicate_hit
    )

    queries_by_id = {q["id"]: q for q in TARGET_QUERIES}

    # 1. B001-6 hit on 1 Cor 2:16 is dynamically classified as SUBSTANTIVE_CROSS_EPISTLE_COMPARISON
    hit_b001_6 = {
        "match": "Rom. xi. 34",
        "start": 287850,
        "snippet": "This clause is retained in Rom. xi. 34, while ὃς συνβιβάσει αὐτόν is omitted..."
    }
    res_b001_6 = adjudicate_target(queries_by_id["B001-6"], [hit_b001_6], "dummy full text")
    assert res_b001_6["classification"] == "SUBSTANTIVE_CROSS_EPISTLE_COMPARISON"
    assert res_b001_6["substantive"] is True
    assert "Rom 11:34" in res_b001_6["rationale"]

    # 2. B001-5 hit on 1 Cor 1:2 is dynamically classified as RELEVANT_INTERPRETIVE_CROSS_REFERENCE
    hit_b001_5 = {
        "match": "Joel ii. 32",
        "start": 160227,
        "snippet": "This goes back to Joel ii. 32, and involves the thought of faith... See Rom. x. 12, 13."
    }
    res_b001_5 = adjudicate_target(queries_by_id["B001-5"], [hit_b001_5], "dummy full text")
    assert res_b001_5["classification"] == "RELEVANT_INTERPRETIVE_CROSS_REFERENCE"
    assert res_b001_5["substantive"] is True

    # 3. Target with 0 matches dynamically evaluates to NOT_DISCUSSED
    res_empty = adjudicate_target(queries_by_id["B001-1"], [], "dummy full text")
    assert res_empty["classification"] == "NOT_DISCUSSED"
    assert res_empty["substantive"] is False
    assert "0 matches found" in res_empty["rationale"]

    # 4. Target with only passing citation dynamically evaluates to NOT_DISCUSSED
    passing_hit = {
        "match": "Rom. ix. 25",
        "start": 690592,
        "snippet": "one each in Rom. ix. 25; Gal. iv. 8; Phil. iii. 3..."
    }
    res_passing = adjudicate_target(queries_by_id["B001-2"], [passing_hit], "dummy full text")
    assert res_passing["classification"] == "NOT_DISCUSSED"
    assert res_passing["substantive"] is False
    assert "passing citation(s) found" in res_passing["rationale"]

    # 5. ADVERSARIAL REGRESSION: Injected substantive hit for formerly negative target (B001-1)
    # Must NOT retain old NOT_DISCUSSED label; must dynamically classify as SUBSTANTIVE_DISCUSSION!
    synthetic_context = (
        "Paul's argument in Rom. iv. 3 cites the Septuagint quotation from Gen. xv. 6, "
        "translating the Hebrew text with characteristic fidelity and argumentative force."
    )
    synthetic_hit = {
        "match": "Rom. iv. 3",
        "start": 10,
        "snippet": synthetic_context
    }
    res_adversarial = adjudicate_target(queries_by_id["B001-1"], [synthetic_hit], synthetic_context)
    assert res_adversarial["classification"] == "SUBSTANTIVE_DISCUSSION"
    assert res_adversarial["substantive"] is True
    assert "substantive exegetical/textual commentary" in res_adversarial["rationale"]


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
