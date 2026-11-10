import csv
import json
import re
from pathlib import Path

def test_citation_ledger_crosswalk_integrity():
    repo_root = Path(__file__).resolve().parent.parent
    s01f_dir = repo_root / "research/inbox/B001-pauline-txt-pilot/sources/S01F"
    csv_path = s01f_dir / "citation_ledger.csv"

    prompts = {}
    for p in [2, 3, 4]:
        with open(s01f_dir / f"prompt_{p}_raw.json", encoding="utf-8") as f:
            prompts[p] = json.load(f)["citations"]

    with open(csv_path, encoding="utf-8") as f:
        reader = list(csv.DictReader(f))

    assert len(reader) == 18, f"Expected 18 ledger rows, found {len(reader)}"

    for row in reader:
        eid = row["evidence_id"]
        raw_ptr = row["notebooklm_citation"]
        m = re.search(r"Prompt (\d+) / citations\[index=(\d+)\], label=(\d+)", raw_ptr)
        assert m is not None, f"Could not parse pointer '{raw_ptr}' for {eid}"

        p_num = int(m.group(1))
        c_idx = int(m.group(2))
        c_lbl = m.group(3)

        assert p_num in prompts, f"Prompt {p_num} not loaded"
        assert c_idx < len(prompts[p_num]), f"Citation index {c_idx} out of range for Prompt {p_num}"

        citation = prompts[p_num][c_idx]
        assert citation["label"] == c_lbl, f"Label mismatch for {eid}: expected {c_lbl}, found {citation['label']}"
        assert citation["snippet"], f"Empty snippet for {eid}"

        # Verify measured audit metadata
        audit = citation.get("audit", {})
        assert audit.get("pre_hover_cleared") is True, f"Audit pre_hover_cleared failed for {eid}"
        assert audit.get("overlay_pane_id"), f"Missing overlay_pane_id for {eid}"
        assert audit.get("is_fresh_pane") is True, f"Audit is_fresh_pane failed for {eid}"
        assert audit.get("trigger_bound") is True, f"Audit trigger_bound failed for {eid}"
        assert audit.get("handshake_verified") is True, f"Audit handshake_verified failed for {eid}"

def test_s02f_citation_ledger_crosswalk_integrity():
    repo_root = Path(__file__).resolve().parent.parent
    s02f_dir = repo_root / "research/inbox/B001-pauline-txt-pilot/sources/S02F"
    csv_path = s02f_dir / "citation_ledger.csv"

    prompts = {}
    for p in [2, 3, 4, 7]:
        raw_file = s02f_dir / f"prompt_{p}_raw.json"
        if raw_file.is_file():
            with open(raw_file, encoding="utf-8") as f:
                prompts[p] = json.load(f)["citations"]

    with open(csv_path, encoding="utf-8") as f:
        reader = list(csv.DictReader(f))

    assert len(reader) == 14, f"Expected 14 ledger rows for S02F, found {len(reader)}"

    for row in reader:
        eid = row["evidence_id"]
        assert row["source_id"] == "S02F"
        raw_ptr = row["notebooklm_citation"]
        m = re.search(r"Prompt (\d+) / citations\[index=(\d+)\], label=(\d+)", raw_ptr)
        assert m is not None, f"Could not parse pointer '{raw_ptr}' for {eid}"

        p_num = int(m.group(1))
        c_idx = int(m.group(2))
        c_lbl = m.group(3)

        assert p_num in prompts, f"Prompt {p_num} not loaded"
        assert c_idx < len(prompts[p_num]), f"Citation index {c_idx} out of range for Prompt {p_num}"

        citation = prompts[p_num][c_idx]
        assert citation["label"] == c_lbl, f"Label mismatch for {eid}: expected {c_lbl}, found {citation['label']}"
        assert citation["snippet"], f"Empty snippet for {eid}"

        # Verify measured audit metadata
        audit = citation.get("audit", {})
        assert audit.get("pre_hover_cleared") is True, f"Audit pre_hover_cleared failed for {eid}"
        assert audit.get("overlay_pane_id"), f"Missing overlay_pane_id for {eid}"
        assert audit.get("is_fresh_pane") is True, f"Audit is_fresh_pane failed for {eid}"
        assert audit.get("trigger_bound") is True, f"Audit trigger_bound failed for {eid}"
        assert audit.get("handshake_verified") is True, f"Audit handshake_verified failed for {eid}"
        assert row["verification_status"] == "VERIFIED", f"Verification status not VERIFIED for {eid}"

def test_s02f_self_audit_corrections_incorporated():
    repo_root = Path(__file__).resolve().parent.parent
    s02f_dir = repo_root / "research/inbox/B001-pauline-txt-pilot/sources/S02F"
    csv_path = s02f_dir / "citation_ledger.csv"

    with open(csv_path, encoding="utf-8") as f:
        rows = {r["evidence_id"]: r for r in csv.DictReader(f)}

    # Check 1: E003 authorial hedging (F2)
    e003 = rows["S02F-E003"]
    assert "seems to have used" in e003["author_claim"]
    assert "seems to have used" in e003["short_quote"]
    assert "hedging" in e003["notes"].lower()

    # Check 2: E004 assimilation mechanism (F2)
    e004 = rows["S02F-E004"]
    assert "naturally crept in" in e004["author_claim"]
    assert "naturally crept in" in e004["short_quote"]
    assert "mechanism" in e004["notes"].lower()

    # Check 3: E007 non-verbatim cross-language agreement (F5)
    e007 = rows["S02F-E007"]
    assert "verbatim" not in e007["author_claim"].lower()
    assert "agrees with both" in e007["short_quote"]

    # Check 4: Excursus items present spanning pp. 302-306 (F1)
    for eid in ["S02F-E010", "S02F-E011", "S02F-E012", "S02F-E013", "S02F-E014"]:
        assert eid in rows, f"Missing excursus evidence item {eid}"
        assert int(rows[eid]["printed_page"]) in range(302, 308)

def test_s02f_provenance_and_hash_integrity():
    repo_root = Path(__file__).resolve().parent.parent
    req_path = repo_root / "research-queue/B001_CHATGPT_REVIEW_REQUEST.md"

    with open(req_path, encoding="utf-8") as f:
        req_text = f.read()

    # If S02F is currently under review, verify review request details
    if "Source ID: `S02F`" in req_text or "SOURCE_ID: S02F" in req_text:
        # Verified Internet Archive link to 1895 Scribner's first edition
        assert "https://archive.org/details/epistlecommentar00sanduoft" in req_text
        assert "1895" in req_text
        assert "acriticalandexe00headgoog" not in req_text

        # Target PDF hash and reconciled byte size
        assert "4be4cad08705963505f13a38a12b8737040e531a6146b1fa4400c936cc37cf4c" in req_text
        assert "4,187,334 bytes" in req_text
        assert "4,183,892 bytes" not in req_text

    # Diagnostic byte match
    diag_path = repo_root / "research/inbox/B001-pauline-txt-pilot/sources/S02F/ingestion_diagnostic.md"
    with open(diag_path, encoding="utf-8") as f:
        diag_text = f.read()
    assert "4,187,334 bytes" in diag_text

    # Provenance manifest match
    prov_path = repo_root / "research/inbox/B001-pauline-txt-pilot/sources/S02F/provenance_manifest.json"
    assert prov_path.is_file(), "Missing provenance_manifest.json"
    with open(prov_path, encoding="utf-8") as f:
        prov = json.load(f)
    assert prov["raw_volume_scan"]["size_bytes"] == 47318528
    assert prov["raw_volume_scan"]["sha256"] == "4a6369a0595550c8c1b92b71613a73182fe4a82aa02cfc989633e6c4dc0b80af"
    assert prov["ingested_derivative_section"]["size_bytes"] == 4187334
    assert prov["ingested_derivative_section"]["sha256"] == "4be4cad08705963505f13a38a12b8737040e531a6146b1fa4400c936cc37cf4c"

    # If physical files exist in local environment, verify actual file stats directly
    local_deriv = Path("/Users/chrisrodriguez/Downloads/sanday_headlam_1895_romans_icc.pdf")
    if local_deriv.is_file():
        import os
        import hashlib
        assert os.path.getsize(local_deriv) == 4187334
        h = hashlib.sha256(local_deriv.read_bytes()).hexdigest()
        assert h == "4be4cad08705963505f13a38a12b8737040e531a6146b1fa4400c936cc37cf4c"

def test_s02f_negative_search_evidence_discipline():
    repo_root = Path(__file__).resolve().parent.parent
    s02f_dir = repo_root / "research/inbox/B001-pauline-txt-pilot/sources/S02F"

    # Search script and reproducible log existence
    script_path = repo_root / "scripts/verify_s02f_negative_search.py"
    log_path = s02f_dir / "full_volume_search_log.md"
    assert script_path.is_file(), "Missing verify_s02f_negative_search.py"
    assert log_path.is_file(), "Missing full_volume_search_log.md"

    with open(log_path, encoding="utf-8") as f:
        log_text = f.read()

    # Log must cover all 5 non-Romans loci
    for locus in ["B001-8", "B001-9", "B001-10", "B001-11", "B001-12"]:
        assert locus in log_text

    # Positive control section verified
    assert "## Positive-Control Validation (19th-Century Citation Typography)" in log_text
    assert "**PASS (Detected)**" in log_text

    # B001-8 to B001-11 must be NO MATCH FOUND
    for locus in ["B001-8", "B001-9", "B001-10", "B001-11"]:
        assert f"| `{locus}` |" in log_text
    assert "NO MATCH FOUND BY DOCUMENTED FULL-VOLUME TEXT SEARCH" in log_text

    # B001-12 documents the parenthetical citation on p. 118 with Deut 21:23 absent
    assert "Gal. iii, 13" in log_text
    assert "118" in log_text

    # Discipline in narrative files: must use standard negative-search phrasing
    for fname in ["relevance_scan.md", "extraction.md", "counterevidence.md"]:
        fpath = s02f_dir / fname
        with open(fpath, encoding="utf-8") as f:
            content = f.read()
        assert "NO MATCH FOUND BY DOCUMENTED FULL-VOLUME TEXT SEARCH" in content, (
            f"{fname} lacks standard documented negative search phrasing"
        )
        assert "full_volume_search_log.md" in content

    # Review request file must reflect S02F if S02F is currently under review
    req_path = repo_root / "research-queue/B001_CHATGPT_REVIEW_REQUEST.md"
    with open(req_path, encoding="utf-8") as f:
        req_text = f.read()
    if "Source ID: `S02F`" in req_text or "SOURCE_ID: S02F" in req_text:
        assert "NO MATCH FOUND BY DOCUMENTED FULL-VOLUME TEXT SEARCH" in req_text
        assert "Gal. iii, 13" in req_text

def test_s02f_negative_search_script_fail_closed_and_controls(tmp_path):
    repo_root = Path(__file__).resolve().parent.parent
    import subprocess
    import sys

    script = repo_root / "scripts/verify_s02f_negative_search.py"

    # Test 1: Nonexistent PDF fails closed (exit code 1)
    fake_pdf = tmp_path / "nonexistent.pdf"
    res = subprocess.run([sys.executable, str(script), "--pdf", str(fake_pdf)], capture_output=True, text=True)
    assert res.returncode == 1, f"Expected exit code 1 for missing PDF, got {res.returncode}: {res.stderr}"
    assert "Fail closed" in res.stderr

    # Test 2: Dummy PDF with wrong byte size fails closed (exit code 2)
    dummy_pdf = tmp_path / "corrupt.pdf"
    dummy_pdf.write_bytes(b"not a valid 47mb pdf")
    res = subprocess.run([sys.executable, str(script), "--pdf", str(dummy_pdf)], capture_output=True, text=True)
    assert res.returncode == 2, f"Expected exit code 2 for size mismatch, got {res.returncode}: {res.stderr}"
    assert "size mismatch" in res.stderr

    # Test 3: Positive and negative regex control strings in 19th-century typography
    sys.path.insert(0, str(repo_root / "scripts"))
    import verify_s02f_negative_search as vns

    # Authentic 19th-century typography variants with period-plus-space, commas, and Roman numerals
    typography_samples = [
        ("1 Cor. iii. 19", True),
        ("I Cor. vi. 16", True),
        ("Gen. ii. 24", True),
        ("Deut. xxv. 4", True),
        ("Ex. xxxii. 6", True),
        ("Gal. iii, 13", True),
    ]
    # Check that our target pattern definitions detect these formats
    # 1 Cor 6:16 pattern
    pat_cor_6_16 = [p[1] for p in vns.TARGET_QUERIES[1]["patterns"] if "NT citation" in p[0]][0]
    import re
    assert re.search(pat_cor_6_16, "cited in I Cor. vi. 16 by Paul", re.IGNORECASE) is not None
    assert re.search(pat_cor_6_16, "1 Cor. 6:16", re.IGNORECASE) is not None

    # Gal 3:13 pattern
    pat_gal_3_13 = [p[1] for p in vns.TARGET_QUERIES[4]["patterns"] if "NT citation" in p[0]][0]
    assert re.search(pat_gal_3_13, "stead (Gal. iii, 13; 2 Cor. v. 21)", re.IGNORECASE) is not None
    assert re.search(pat_gal_3_13, "Gal. 3:13", re.IGNORECASE) is not None

    # Negative controls (must not match)
    assert re.search(pat_cor_6_16, "Rom. vi. 16", re.IGNORECASE) is None
    assert re.search(pat_gal_3_13, "Gal. iv. 22", re.IGNORECASE) is None

def test_s02f_synthetic_report_generation_and_index_validation():
    repo_root = Path(__file__).resolve().parent.parent
    import sys
    sys.path.insert(0, str(repo_root / "scripts"))
    import verify_s02f_negative_search as vns

    dummy_pdf = Path("test_volume.pdf")
    dummy_text = Path("test_volume.txt")

    dummy_positive_results = [
        {"name": "1 Cor 3:19", "pattern": "pat1", "count": 1, "expected_min": 1, "passed": True},
    ]
    dummy_index_results = {
        "index_present": True,
        "index_offset": 100,
        "has_subjects_section": True,
        "has_latin_section": True,
        "has_greek_section": True,
        "positive_controls": {"Abraham": True, "Adam": True, "Old Testament, Use of the": True},
        "has_scripture_index": False,
        "passed": True,
    }

    # Scenario A: Synthetic NT-only hit for B001-12 (arbitrary text, unverified context)
    text_nt = "Incidental cross-reference to Gal. iii, 13 in dogmatic note."
    res_nt = vns.run_search(text_nt)
    b12_nt = [r for r in res_nt if r["id"] == "B001-12"][0]
    assert b12_nt["nt_matches"] == 1
    assert b12_nt["ot_matches"] == 0
    assert b12_nt["lemma_matches"] == 0
    report_nt = vns.build_markdown_report(res_nt, dummy_positive_results, dummy_index_results, dummy_pdf, 1000, "sha_arbitrary", dummy_text, "sha_txt_arbitrary", 50, 100, raw_text=text_nt)
    assert "MATCH DETECTED (1 hit(s): 1 NT, 0 OT, 0 lemma)" in report_nt
    # CRITICAL INVARIANT: For arbitrary synthetic text, specific p. 118 / Schäder context is NEVER emitted!
    assert "Schäder" not in report_nt
    assert "Printed p. 118" not in report_nt
    assert "Contextual interpretation unverified" in report_nt

    # Scenario B: Synthetic OT-positive hit for B001-12 (Deut 21:23)
    text_ot = "Paul's citation of Deut. xxi. 23 examined critically."
    res_ot = vns.run_search(text_ot)
    b12_ot = [r for r in res_ot if r["id"] == "B001-12"][0]
    assert b12_ot["nt_matches"] == 0
    assert b12_ot["ot_matches"] == 1
    assert b12_ot["lemma_matches"] == 0
    report_ot = vns.build_markdown_report(res_ot, dummy_positive_results, dummy_index_results, dummy_pdf, 1000, "sha_ot", dummy_text, "sha_txt_ot", 50, 100, raw_text=text_ot)
    assert "MATCH DETECTED (1 hit(s): 0 NT, 1 OT, 0 lemma)" in report_ot
    # CRITICAL INVARIANT: When OT matches, no statement asserting Deut is absent may exist anywhere in report!
    assert "Deut 21:23 is not cited" not in report_ot
    assert "Deut 21:23 is nowhere cited" not in report_ot
    assert "Schäder" not in report_ot

    # Scenario C: Synthetic lemma-positive hit for B001-12
    text_lemma = "Quoting ἐπικατάρατος πᾶς as Greek text."
    res_lemma = vns.run_search(text_lemma)
    b12_lemma = [r for r in res_lemma if r["id"] == "B001-12"][0]
    assert b12_lemma["nt_matches"] == 0
    assert b12_lemma["ot_matches"] == 0
    # Matches both accented and unaccented lemma patterns
    assert b12_lemma["lemma_matches"] == 2
    report_lemma = vns.build_markdown_report(res_lemma, dummy_positive_results, dummy_index_results, dummy_pdf, 1000, "sha_lemma", dummy_text, "sha_txt_lemma", 50, 100, raw_text=text_lemma)
    assert "MATCH DETECTED (2 hit(s): 0 NT, 0 OT, 2 lemma)" in report_lemma
    assert "Schäder" not in report_lemma

    # Scenario D: Synthetic combined hit
    text_combined = "Gal. iii, 13 citing Deut. xxi. 23 with ἐπικατάρατος πᾶς."
    res_combined = vns.run_search(text_combined)
    b12_combined = [r for r in res_combined if r["id"] == "B001-12"][0]
    assert b12_combined["nt_matches"] == 1
    assert b12_combined["ot_matches"] == 1
    assert b12_combined["lemma_matches"] == 2
    assert b12_combined["total_matches"] == 4
    report_combined = vns.build_markdown_report(res_combined, dummy_positive_results, dummy_index_results, dummy_pdf, 1000, "sha_comb", dummy_text, "sha_txt_comb", 50, 100, raw_text=text_combined)
    assert "MATCH DETECTED (4 hit(s): 1 NT, 1 OT, 2 lemma)" in report_combined
    assert "Deut 21:23 is not cited" not in report_combined

    # Scenario E: Synthetic zero-match text
    text_zero = "General discourse mentioning no targets."
    res_zero = vns.run_search(text_zero)
    for r in res_zero:
        assert r["total_matches"] == 0
    report_zero = vns.build_markdown_report(res_zero, dummy_positive_results, dummy_index_results, dummy_pdf, 1000, "sha_zero", dummy_text, "sha_txt_zero", 50, 100, raw_text=text_zero)
    assert report_zero.count("NO MATCH FOUND BY DOCUMENTED FULL-VOLUME TEXT SEARCH") >= 5
    assert "No discussion of any of the five non-Romans B001 passage comparisons was found" in report_zero

    # Scenario F: R6-F1 Boolean Precedence Regression Tests (Wrong hash + keywords)
    # Even if raw text contains Gal 3:13 AND keywords, a wrong text hash MUST NEVER emit p. 118 historical interpretation
    text_fake_schader = "Appendix note: Gal. iii, 13." + " " * 100 + "Unrelated note mentioning Herr Schäder."
    res_fake_schader = vns.run_search(text_fake_schader)
    b12_fs = [r for r in res_fake_schader if r["id"] == "B001-12"][0]
    assert b12_fs["nt_matches"] == 1
    report_fake_schader = vns.build_markdown_report(
        res_fake_schader, dummy_positive_results, dummy_index_results, dummy_pdf, 1000,
        "dummy_pdf_sha", dummy_text, "WRONG_TEXT_HASH_12345", 50, 100, raw_text=text_fake_schader
    )
    assert "Verified Source Context (Printed p. 118)" not in report_fake_schader
    assert "E. Schäder's 1893 monograph" not in report_fake_schader
    assert "theological note on Rom 4:25" not in report_fake_schader
    assert "Die Bedeutung des lebendigen Christus" not in report_fake_schader
    assert "Contextual interpretation unverified" in report_fake_schader

    text_fake_lebendigen = "Incidental Gal. iii, 13." + " " * 100 + "Unrelated line mentioning lebendigen Christus elsewhere."
    res_fake_lebendigen = vns.run_search(text_fake_lebendigen)
    report_fake_lebendigen = vns.build_markdown_report(
        res_fake_lebendigen, dummy_positive_results, dummy_index_results, dummy_pdf, 1000,
        "dummy_pdf_sha", dummy_text, "WRONG_TEXT_HASH_67890", 50, 100, raw_text=text_fake_lebendigen
    )
    assert "Verified Source Context (Printed p. 118)" not in report_fake_lebendigen
    assert "E. Schäder's 1893 monograph" not in report_fake_lebendigen
    assert "theological note on Rom 4:25" not in report_fake_lebendigen
    assert "Die Bedeutung des lebendigen Christus" not in report_fake_lebendigen
    assert "Contextual interpretation unverified" in report_fake_lebendigen

    text_fake_both = "Gal. iii, 13." + " " * 100 + "Schäder monograph on lebendigen Christus."
    res_fake_both = vns.run_search(text_fake_both)
    report_fake_both = vns.build_markdown_report(
        res_fake_both, dummy_positive_results, dummy_index_results, dummy_pdf, 1000,
        "dummy_pdf_sha", dummy_text, "WRONG_TEXT_HASH_ABCDEF", 50, 100, raw_text=text_fake_both
    )
    assert "Verified Source Context (Printed p. 118)" not in report_fake_both
    assert "E. Schäder's 1893 monograph" not in report_fake_both
    assert "theological note on Rom 4:25" not in report_fake_both
    assert "Die Bedeutung des lebendigen Christus" not in report_fake_both
    assert "Contextual interpretation unverified" in report_fake_both

    # Direct validation helper test (verifies that validate_p118_context fails closed on wrong hash)
    assert vns.validate_p118_context(text_fake_both, "WRONG_HASH", 0) is False
    assert vns.validate_p118_context(text_fake_schader, "WRONG_HASH", 0) is False
    assert vns.validate_p118_context(text_fake_lebendigen, "WRONG_HASH", 0) is False

    # Index structure validation tests
    # Missing index fails
    bad_index = vns.verify_index_structure("A text with no index at all.")
    assert bad_index["passed"] is False
    assert bad_index["index_present"] is False

    # Valid index with authentic end delimiter succeeds
    good_index_text = (
        "Main text...\nINDEX              TO THE                NOTES\n"
        "I. SUBJECTS\nAbraham, Righteousness of, p. 100 ff.\nAdam, p. 130 ff.\n"
        "Old Testament, Use of the, pp. 77; 302-307.\n"
        "II. LATIN WORDS\nIII. GREEK WORDS\n"
        "The International Theological Library\n"
    )
    good_index = vns.verify_index_structure(good_index_text)
    assert good_index["passed"] is True
    assert good_index["has_end_marker"] is True
    assert good_index["has_subjects_section"] is True
    assert good_index["has_latin_section"] is True
    assert good_index["has_greek_section"] is True
    assert good_index["ordered"] is True
    assert good_index["has_scripture_index"] is False

    # Adversarial index test 1: Missing end marker fails closed
    no_end_text = (
        "Main text...\nINDEX              TO THE                NOTES\n"
        "I. SUBJECTS\nAbraham, Righteousness of, p. 100 ff.\nAdam, p. 130 ff.\n"
        "Old Testament, Use of the, pp. 77; 302-307.\n"
        "II. LATIN WORDS\nIII. GREEK WORDS\n"
    )
    no_end_index = vns.verify_index_structure(no_end_text)
    assert no_end_index["passed"] is False
    assert no_end_index["has_end_marker"] is False
    assert "end delimiter not found" in no_end_index["error"]

    # Adversarial index test 2: Unrelated trailing Scripture index heading AFTER end delimiter
    # (Must NOT fail the bounded index because it occurs outside index boundaries in publisher ads)
    trailing_scrip_text = (
        "Main text...\nINDEX              TO THE                NOTES\n"
        "I. SUBJECTS\nAbraham, Righteousness of, p. 100 ff.\nAdam, p. 130 ff.\n"
        "Old Testament, Use of the, pp. 77; 302-307.\n"
        "II. LATIN WORDS\nIII. GREEK WORDS\n"
        "The International Theological Library\n"
        "Publisher ad mentioning IV. PASSAGES OF SCRIPTURE in Driver's volume.\n"
    )
    trailing_index = vns.verify_index_structure(trailing_scrip_text)
    assert trailing_index["passed"] is True
    assert trailing_index["has_scripture_index"] is False

    # Adversarial index test 3: Scripture index heading INSIDE the index (before end delimiter)
    inside_scrip_text = (
        "Main text...\nINDEX              TO THE                NOTES\n"
        "I. SUBJECTS\nAbraham, Righteousness of, p. 100 ff.\nAdam, p. 130 ff.\n"
        "Old Testament, Use of the, pp. 77; 302-307.\n"
        "II. LATIN WORDS\nIII. GREEK WORDS\nIV. PASSAGES OF SCRIPTURE\n"
        "The International Theological Library\n"
    )
    scrip_index = vns.verify_index_structure(inside_scrip_text)
    assert scrip_index["has_scripture_index"] is True
    assert scrip_index["passed"] is False
    scrip_report = vns.build_markdown_report(res_zero, dummy_positive_results, scrip_index, dummy_pdf, 1000, "sha", dummy_text, "sha_txt", 50, 100, raw_text=inside_scrip_text)
    assert "Dedicated Scripture Passage Index (Index Locorum): None" not in scrip_report
    assert "PRESENT (detected pattern" in scrip_report

    # Adversarial index test 4: Out-of-order sections fail
    out_of_order_text = (
        "Main text...\nINDEX              TO THE                NOTES\n"
        "III. GREEK WORDS\nI. SUBJECTS\nAbraham, Righteousness of, p. 100 ff.\n"
        "II. LATIN WORDS\nThe International Theological Library\n"
    )
    ooo_index = vns.verify_index_structure(out_of_order_text)
    assert ooo_index["passed"] is False
    assert ooo_index["ordered"] is False

    # Adversarial index test 5: Positive control out-of-bounds (e.g. Abraham after Latin section) fails
    oob_text = (
        "Main text...\nINDEX              TO THE                NOTES\n"
        "I. SUBJECTS\nAdam, p. 130 ff.\nOld Testament, Use of the, pp. 77; 302-307.\n"
        "II. LATIN WORDS\nAbraham, Righteousness of, p. 100 ff.\nIII. GREEK WORDS\n"
        "The International Theological Library\n"
    )
    oob_index = vns.verify_index_structure(oob_text)
    assert oob_index["passed"] is False
    assert oob_index["positive_controls"]["Abraham"] is False

    # Adversarial index test 6: Cross-entry borrowing of page numbers
    # Abraham lacks 100, but subsequent unrelated entry Absalom has 100 -> MUST FAIL
    cross_entry_abraham_text = (
        "Main text...\nINDEX              TO THE                NOTES\n"
        "I. SUBJECTS\n"
        "Abraham, Faith of, p. 97 ff.\n"
        "Absalom, rebellion of, p. 100 ff.\n"
        "Adam, p. 130 ff.\n"
        "Old Testament, Use of the, pp. 77; 302-307.\n"
        "II. LATIN WORDS\nIII. GREEK WORDS\n"
        "The International Theological Library\n"
    )
    cross_abraham_idx = vns.verify_index_structure(cross_entry_abraham_text)
    assert cross_abraham_idx["passed"] is False
    assert cross_abraham_idx["positive_controls"]["Abraham"] is False

    # Adam lacks 130, but subsequent unrelated entry Adrian has 130 -> MUST FAIL
    cross_entry_adam_text = (
        "Main text...\nINDEX              TO THE                NOTES\n"
        "I. SUBJECTS\n"
        "Abraham, Righteousness of, p. 100 ff.\n"
        "Adam, Fall of, p. 136 ff.\n"
        "Adrian, Emperor, p. 130.\n"
        "Old Testament, Use of the, pp. 77; 302-307.\n"
        "II. LATIN WORDS\nIII. GREEK WORDS\n"
        "The International Theological Library\n"
    )
    cross_adam_idx = vns.verify_index_structure(cross_entry_adam_text)
    assert cross_adam_idx["passed"] is False
    assert cross_adam_idx["positive_controls"]["Adam"] is False

    # Old Testament lacks 302, but subsequent unrelated entry Oltramare has 302 -> MUST FAIL
    cross_entry_ot_text = (
        "Main text...\nINDEX              TO THE                NOTES\n"
        "I. SUBJECTS\n"
        "Abraham, Righteousness of, p. 100 ff.\n"
        "Adam, p. 130 ff.\n"
        "Old Testament, Use of the, pp. 77; 264.\n"
        "Oltramare, Hugues, p. 302.\n"
        "II. LATIN WORDS\nIII. GREEK WORDS\n"
        "The International Theological Library\n"
    )
    cross_ot_idx = vns.verify_index_structure(cross_entry_ot_text)
    assert cross_ot_idx["passed"] is False
    assert cross_ot_idx["positive_controls"]["Old Testament, Use of the"] is False

def test_s02f_self_audit_consistency_with_search_log():
    repo_root = Path(__file__).resolve().parent.parent
    s02f_dir = repo_root / "research/inbox/B001-pauline-txt-pilot/sources/S02F"
    audit_path = s02f_dir / "notebooklm_self_audit.md"

    with open(audit_path, encoding="utf-8") as f:
        audit_text = f.read()

    # Must accurately distinguish 4 no-match loci from the 1 parenthetical Gal 3:13 hit
    assert "B001-8" in audit_text
    assert "B001-9" in audit_text
    assert "B001-10" in audit_text
    assert "B001-11" in audit_text
    assert "B001-12" in audit_text
    assert "Gal. iii, 13" in audit_text
    assert "0 occurrences across all 5 loci" not in audit_text


def test_s02f_text_digest_mismatch_exit_code_8_and_override(tmp_path, monkeypatch):
    """Test that main() fails closed with exit code 8 on text digest mismatch,

    and that --allow-text-digest-mismatch explicitly permits continued execution.
    """
    repo_root = Path(__file__).resolve().parent.parent
    import sys
    sys.path.insert(0, str(repo_root / "scripts"))
    import verify_s02f_negative_search as vns

    fake_pdf = tmp_path / "fake_romans.pdf"
    fake_pdf.write_bytes(b"0" * vns.EXPECTED_RAW_PDF_BYTES)
    fake_text = tmp_path / "fake_extracted.txt"
    fake_out = tmp_path / "out_log.md"

    # Mock get_sha256 for the fake PDF to match EXPECTED_RAW_PDF_SHA256
    orig_get_sha256 = vns.get_sha256
    def mock_get_sha256(p):
        if Path(p) == fake_pdf:
            return vns.EXPECTED_RAW_PDF_SHA256
        return orig_get_sha256(p)

    monkeypatch.setattr(vns, "get_sha256", mock_get_sha256)

    # Mock subprocess.run for pdftotext to write text with a non-matching digest
    def mock_subprocess_run(cmd, check=False):
        out_txt = Path(cmd[3])
        out_txt.write_text("Dummy extracted text line\n" * 2000, encoding="utf-8")
        class SubprocessResult:
            returncode = 0
        return SubprocessResult()

    monkeypatch.setattr("subprocess.run", mock_subprocess_run)

    # 1. Without --allow-text-digest-mismatch -> MUST exit 8
    test_args_strict = [
        "verify_s02f_negative_search.py",
        "--pdf", str(fake_pdf),
        "--text", str(fake_text),
        "--out", str(fake_out),
    ]
    monkeypatch.setattr(sys, "argv", test_args_strict)
    ret_strict = vns.main()
    assert ret_strict == 8, f"Expected exit code 8 on digest mismatch, got {ret_strict}"

    # 2. With --allow-text-digest-mismatch -> MUST bypass exit 8
    test_args_override = [
        "verify_s02f_negative_search.py",
        "--pdf", str(fake_pdf),
        "--text", str(fake_text),
        "--out", str(fake_out),
        "--allow-text-digest-mismatch",
    ]
    monkeypatch.setattr(sys, "argv", test_args_override)
    ret_override = vns.main()
    assert ret_override != 8, f"Expected override to bypass exit code 8, got {ret_override}"


def test_s03f_citation_ledger_crosswalk_integrity():
    repo_root = Path(__file__).resolve().parent.parent
    s03f_dir = repo_root / "research/inbox/B001-pauline-txt-pilot/sources/S03F"
    csv_path = s03f_dir / "citation_ledger.csv"

    prompts = {}
    for p in [2, 3]:
        raw_file = s03f_dir / f"prompt_{p}_raw.json"
        if raw_file.is_file():
            with open(raw_file, encoding="utf-8") as f:
                prompts[p] = json.load(f)["citations"]

    with open(csv_path, encoding="utf-8") as f:
        reader = list(csv.DictReader(f))

    assert len(reader) == 14, f"Expected 14 ledger rows for S03F, found {len(reader)}"

    for row in reader:
        eid = row["evidence_id"]
        assert row["source_id"] == "S03F"
        raw_ptr = row["notebooklm_citation"]
        m = re.search(r"Prompt (\d+) / citations\[index=(\d+)\], label=(\d+)", raw_ptr)
        assert m is not None, f"Could not parse pointer '{raw_ptr}' for {eid}"

        p_num = int(m.group(1))
        c_idx = int(m.group(2))
        c_lbl = m.group(3)

        assert p_num in prompts, f"Prompt {p_num} not loaded"
        assert c_idx < len(prompts[p_num]), f"Citation index {c_idx} out of range for Prompt {p_num}"

        citation = prompts[p_num][c_idx]
        assert citation["label"] == c_lbl, f"Label mismatch for {eid}: expected {c_lbl}, found {citation['label']}"
        assert citation["snippet"], f"Empty snippet for {eid}"

        # Verify measured audit metadata
        audit = citation.get("audit", {})
        assert audit.get("pre_hover_cleared") is True, f"Audit pre_hover_cleared failed for {eid}"
        assert audit.get("overlay_pane_id"), f"Missing overlay_pane_id for {eid}"
        assert audit.get("is_fresh_pane") is True, f"Audit is_fresh_pane failed for {eid}"
        assert audit.get("trigger_bound") is True, f"Audit trigger_bound failed for {eid}"
        assert audit.get("handshake_verified") is True, f"Audit handshake_verified failed for {eid}"
        assert row["verification_status"] == "VERIFIED", f"Verification status not VERIFIED for {eid}"


def test_s03f_self_audit_corrections_incorporated():
    repo_root = Path(__file__).resolve().parent.parent
    s03f_dir = repo_root / "research/inbox/B001-pauline-txt-pilot/sources/S03F"
    csv_path = s03f_dir / "citation_ledger.csv"

    with open(csv_path, encoding="utf-8") as f:
        rows = {r["evidence_id"]: r for r in csv.DictReader(f)}

    # Check 1: S03F-E001 preserves possibility framing from Ps 33:10
    e001 = rows["S03F-E001"]
    assert "possibly" in e001["author_claim"].lower() or "possibly" in e001["qualification"].lower()
    assert "33:10" in e001["author_claim"] or "33:10" in e001["qualification"]

    # Check 2: S03F-E006 includes explicit qualification regarding pantos
    e006 = rows["S03F-E006"]
    assert "πάντως" in e006["qualification"]
    assert "oxen" in e006["qualification"]

    # Check 3: S03F-E005 preserves explicit uncertainty "not easy to decide"
    e005 = rows["S03F-E005"]
    assert "not easy to decide" in e005["author_claim"].lower() or "not easy to decide" in e005["qualification"].lower()
    assert "κημώσεις" in e005["author_claim"]

    # Check 4: S03F-E011 preserves authors' exact qualification "seems to make changes"
    e011 = rows["S03F-E011"]
    assert "seems to make changes" in e011["author_claim"]

    # Check 5: S03F-E004 retains Sirach 19:2 as alternate/contributing verbal source
    e004 = rows["S03F-E004"]
    assert "Sirach 19:2" in e004["author_claim"] or "Sirach 19:2" in e004["qualification"]

    # Check 6: S03F-E003 clarifies Robertson & Plummer attribution and Hebrew context
    e003 = rows["S03F-E003"]
    assert "not in the original" in e003["author_claim"].lower()
    assert "Hebrew" in e003["qualification"]

    # Check 7: S03F-E013 is admitted for B001-6 comparative evidence
    e013 = rows["S03F-E013"]
    assert e013["b001_id"] == "B001-6"
    assert "Rom. xi. 34" in e013["short_quote"] or "Rom 11:34" in e013["author_claim"]
    assert "50" in e013["printed_page"]

    # Check 8: S03F-E014 is admitted for B001-5 secondary interpretive evidence
    e014 = rows["S03F-E014"]
    assert e014["b001_id"] == "B001-5"
    assert "Joel" in e014["author_claim"] and "Rom" in e014["author_claim"]
    assert "3" in e014["printed_page"]


def test_s04f_citation_ledger_crosswalk_integrity():
    repo_root = Path(__file__).resolve().parent.parent
    s04f_dir = repo_root / "research/inbox/B001-pauline-txt-pilot/sources/S04F"
    csv_path = s04f_dir / "citation_ledger.csv"

    prompts = {}
    for p in [2, 3, 7]:
        raw_file = s04f_dir / f"prompt_{p}_raw.json"
        if raw_file.is_file():
            with open(raw_file, encoding="utf-8") as f:
                prompts[p] = json.load(f)["citations"]

    with open(csv_path, encoding="utf-8") as f:
        reader = list(csv.DictReader(f))

    assert len(reader) == 14, f"Expected 14 ledger rows for S04F, found {len(reader)}"

    for row in reader:
        eid = row["evidence_id"]
        assert row["source_id"] == "S04F"
        raw_ptr = row["notebooklm_citation"]
        m = re.search(r"Prompt (\d+) / citations\[index=(\d+)\], label=(\d+)", raw_ptr)
        assert m is not None, f"Could not parse pointer '{raw_ptr}' for {eid}"

        p_num = int(m.group(1))
        c_idx = int(m.group(2))
        c_lbl = m.group(3)

        assert p_num in prompts, f"Prompt {p_num} not loaded"
        assert c_idx < len(prompts[p_num]), f"Citation index {c_idx} out of range for Prompt {p_num}"

        citation = prompts[p_num][c_idx]
        assert citation["label"] == c_lbl, f"Label mismatch for {eid}: expected {c_lbl}, found {citation['label']}"
        assert citation["snippet"], f"Empty snippet for {eid}"

        # Verify measured audit metadata
        audit = citation.get("audit", {})
        assert audit.get("pre_hover_cleared") is True, f"Audit pre_hover_cleared failed for {eid}"
        assert audit.get("overlay_pane_id"), f"Missing overlay_pane_id for {eid}"
        assert audit.get("is_fresh_pane") is True, f"Audit is_fresh_pane failed for {eid}"
        assert audit.get("trigger_bound") is True, f"Audit trigger_bound failed for {eid}"
        assert audit.get("handshake_verified") is True, f"Audit handshake_verified failed for {eid}"
        assert row["verification_status"] == "VERIFIED", f"Verification status not VERIFIED for {eid}"


def test_s04f_self_audit_corrections_incorporated():
    repo_root = Path(__file__).resolve().parent.parent
    s04f_dir = repo_root / "research/inbox/B001-pauline-txt-pilot/sources/S04F"
    csv_path = s04f_dir / "citation_ledger.csv"

    with open(csv_path, encoding="utf-8") as f:
        rows = {r["evidence_id"]: r for r in csv.DictReader(f)}

    # Check 1: S04F-E009 preserves qualification on James and Paul
    e009 = rows["S04F-E009"]
    assert "destroy the force" in e009["short_quote"]
    assert "coincidence" in e009["short_quote"]
    assert "James" in e009["author_claim"]

    # Check 2: S04F-E002 includes theological qualification on omission of hypo Theou
    e002 = rows["S04F-E002"]
    assert "instinctively omits" in e002["short_quote"]
    assert "sinner" in e002["qualification"].lower() or "vicarious" in e002["author_claim"].lower()

    # Check 3: S04F-E001 preserves construct phrase grammatical ambiguity
    e001 = rows["S04F-E001"]
    assert "ambiguity" in e001["short_quote"].lower()
    assert "subjective" in e001["author_claim"].lower() or "objective" in e001["author_claim"].lower()

    # Check 4: S04F-E004 preserves legitimacy of applying post-mortem impalement to crucifixion
    e004 = rows["S04F-E004"]
    assert "crucifixion" in e004["short_quote"]
    assert "legitimate" in e004["short_quote"]

    # Check 5: S04F-E005 preserves verbatim agreement between Gal 3:6, Rom 4:3, and Gen 15:6
    e005 = rows["S04F-E005"]
    assert "Rom. iv. 3" in e005["short_quote"]
    assert "Lxx" in e005["short_quote"]

    # Check 6: S04F-E010 documents passing lexical citation of 1 Cor 1:19
    e010 = rows["S04F-E010"]
    assert "1 Cor. i. 19" in e010["short_quote"]
    assert e010["b001_id"] == "B001-8"

    # Check 7: S04F-E013 documents Justin Martyr's Dial. 96 citation
    e013 = rows["S04F-E013"]
    assert "Justin" in e013["author_claim"]
    assert "Gal. iii. 10, 13" in e013["short_quote"]


def test_s04f_provenance_and_hash_integrity():
    import os
    import hashlib
    repo_root = Path(__file__).resolve().parent.parent
    prov_path = repo_root / "research/inbox/B001-pauline-txt-pilot/sources/S04F/provenance_manifest.json"
    assert prov_path.is_file(), "Missing provenance_manifest.json for S04F"

    with open(prov_path, encoding="utf-8") as f:
        prov = json.load(f)

    assert prov["raw_volume_scan"]["size_bytes"] == 27846788
    assert prov["raw_volume_scan"]["sha256"] == "0131c0916a037f058cd9607d60ce1bf1c93fdabff621ca31767ec03b3d5788f4"
    assert prov["ingested_derivative_section"]["size_bytes"] == 20643909
    assert prov["ingested_derivative_section"]["sha256"] == "4d6176f9b487dc291ef0d1ac828c695bb5485fd1898404177d28c0b28e5591b4"

    # If physical files exist in local environment, verify stats
    local_deriv = Path("/Users/chrisrodriguez/Downloads/lightfoot_1914_galatians.pdf")
    if local_deriv.is_file():
        assert os.path.getsize(local_deriv) == 20643909
        h = hashlib.sha256(local_deriv.read_bytes()).hexdigest()
        assert h == "4d6176f9b487dc291ef0d1ac828c695bb5485fd1898404177d28c0b28e5591b4"


def test_s04f_negative_search_evidence_discipline():
    repo_root = Path(__file__).resolve().parent.parent
    s04f_dir = repo_root / "research/inbox/B001-pauline-txt-pilot/sources/S04F"

    script_path = repo_root / "scripts/verify_s04f_negative_search.py"
    log_path = s04f_dir / "full_volume_search_log.md"
    assert script_path.is_file(), "Missing verify_s04f_negative_search.py"
    assert log_path.is_file(), "Missing full_volume_search_log.md"

    with open(log_path, encoding="utf-8") as f:
        log_text = f.read()

    # Log covers all non-Galatians 3:13 loci
    for locus in ["B001-1", "B001-2", "B001-3", "B001-4", "B001-5", "B001-6", "B001-7", "B001-8", "B001-9", "B001-10", "B001-11"]:
        assert locus in log_text

    # Positive controls validated
    assert "Positive-Control Validation" in log_text
    assert "**PASS**" in log_text

    # B001-2 through B001-7, B001-9, B001-10 must be NO MATCH / NO OCCURRENCES
    for locus in ["B001-2", "B001-3", "B001-4", "B001-5", "B001-6", "B001-7", "B001-9", "B001-10"]:
        assert f"| `{locus}` |" in log_text
    assert (
        "NO MATCH FOUND BY DOCUMENTED FULL-VOLUME TEXT SEARCH" in log_text
        or "NO OCCURRENCES FOR ENUMERATED PATTERNS" in log_text
    )

    # B001-1 is substantive cross-epistle comparison
    assert "SUBSTANTIVE CROSS-EPISTLE COMPARISON" in log_text

    # B001-8 and B001-11 are passing citations
    assert "PASSING CITATION" in log_text


def test_s04f_negative_search_script_fail_closed_and_controls(tmp_path):
    repo_root = Path(__file__).resolve().parent.parent
    import subprocess
    import sys

    script = repo_root / "scripts/verify_s04f_negative_search.py"

    # Test 1: Nonexistent PDF fails closed (exit code 1)
    fake_pdf = tmp_path / "nonexistent.pdf"
    res = subprocess.run([sys.executable, str(script), "--pdf", str(fake_pdf)], capture_output=True, text=True)
    assert res.returncode == 1, f"Expected exit code 1 for missing PDF, got {res.returncode}: {res.stderr}"
    assert "Fail closed" in res.stderr

    # Test 2: Dummy PDF with wrong byte size fails closed (exit code 2)
    dummy_pdf = tmp_path / "corrupt.pdf"
    dummy_pdf.write_bytes(b"not a valid 27mb pdf")
    res = subprocess.run([sys.executable, str(script), "--pdf", str(dummy_pdf)], capture_output=True, text=True)
    assert res.returncode == 2, f"Expected exit code 2 for size mismatch, got {res.returncode}: {res.stderr}"
    assert "size mismatch" in res.stderr

    # Test 3: Positive and negative regex control strings
    sys.path.insert(0, str(repo_root / "scripts"))
    import verify_s04f_negative_search as vns

    typography_samples = [
        ("Gal. iii. 13", True),
        ("Deut. xxi. 23", True),
        ("Gen. xv. 6", True),
        ("Rom. iv. 3", True),
        ("1 Cor. i. 19", True),
    ]
    pat_deut_21 = vns.POSITIVE_CONTROLS[0]["pattern"]
    assert re.search(pat_deut_21, "cited in Deut. xxi. 23 by Paul", re.IGNORECASE) is not None
    assert re.search(pat_deut_21, "Deut. 21:23", re.IGNORECASE) is not None


def test_s04f_text_digest_mismatch_exit_code_8_and_override(tmp_path, monkeypatch):
    repo_root = Path(__file__).resolve().parent.parent
    import sys
    sys.path.insert(0, str(repo_root / "scripts"))
    import verify_s04f_negative_search as vns

    fake_pdf = tmp_path / "fake_galatians.pdf"
    fake_pdf.write_bytes(b"0" * vns.EXPECTED_RAW_PDF_BYTES)
    fake_text = tmp_path / "fake_extracted.txt"
    fake_out = tmp_path / "out_log.md"

    # Mock get_sha256 for fake PDF
    orig_get_sha256 = vns.get_sha256
    def mock_get_sha256(p):
        if Path(p) == fake_pdf:
            return vns.EXPECTED_RAW_PDF_SHA256
        return orig_get_sha256(p)

    monkeypatch.setattr(vns, "get_sha256", mock_get_sha256)

    # Mock subprocess.run for pdftotext
    def mock_subprocess_run(cmd, check=False):
        out_txt = Path(cmd[2])
        out_txt.write_text("Dummy extracted text line\n" * 2000, encoding="utf-8")
        class SubprocessResult:
            returncode = 0
        return SubprocessResult()

    monkeypatch.setattr("subprocess.run", mock_subprocess_run)

    # 1. Without override -> exit 8
    test_args_strict = [
        "verify_s04f_negative_search.py",
        "--pdf", str(fake_pdf),
        "--text", str(fake_text),
        "--out", str(fake_out),
    ]
    monkeypatch.setattr(sys, "argv", test_args_strict)
    ret_strict = vns.main()
    assert ret_strict == 8, f"Expected exit code 8 on digest mismatch, got {ret_strict}"

    # 2. With override -> bypass exit 8
    test_args_override = [
        "verify_s04f_negative_search.py",
        "--pdf", str(fake_pdf),
        "--text", str(fake_text),
        "--out", str(fake_out),
        "--allow-text-digest-mismatch",
    ]
    monkeypatch.setattr(sys, "argv", test_args_override)
    ret_override = vns.main()
    assert ret_override != 8, f"Expected override to bypass exit code 8, got {ret_override}"


def test_s04f_derivative_page_crosswalk_computed():
    """F3 regression guard: Programmatically verify derivative pages from manifest slices."""
    repo_root = Path(__file__).resolve().parent.parent
    s04f_dir = repo_root / "research/inbox/B001-pauline-txt-pilot/sources/S04F"
    manifest_path = s04f_dir / "provenance_manifest.json"
    csv_path = s04f_dir / "citation_ledger.csv"

    with open(manifest_path, encoding="utf-8") as f:
        manifest = json.load(f)

    sections = manifest["ingested_derivative_section"]["included_sections"]
    slices = []
    for sec_key, sec_desc in sections.items():
        m = re.search(r"Derivative pp\.\s*(\d+)-(\d+).*?Printed pp\.\s*(\d+)-(\d+)", sec_desc)
        if m:
            slices.append({
                "name": sec_key,
                "start_page_derivative": int(m.group(1)),
                "end_page_derivative": int(m.group(2)),
                "start_page_printed": int(m.group(3)),
                "end_page_printed": int(m.group(4)),
            })

    assert len(slices) >= 4, f"Expected at least 4 sliced sections in manifest, found {len(slices)}"

    with open(csv_path, encoding="utf-8") as f:
        reader = list(csv.DictReader(f))

    assert len(reader) == 14, f"Expected 14 ledger rows for S04F, found {len(reader)}"

    for row in reader:
        eid = row["evidence_id"]
        p_printed = int(row["printed_page"])
        locator = row["source_locator"]

        # Find matching slice
        matched_slice = None
        for sl in slices:
            if sl["start_page_printed"] <= p_printed <= sl["end_page_printed"]:
                matched_slice = sl
                break

        assert matched_slice is not None, f"No manifest slice found for {eid} with printed page {p_printed}"

        expected_deriv_page = matched_slice["start_page_derivative"] + (p_printed - matched_slice["start_page_printed"])

        # Extract derivative page(s) from locator string
        # Match either "PDF derivative p. X" or "PDF derivative pp. X-Y"
        m_single = re.search(r"PDF derivative p\.\s*(\d+)", locator)
        m_range = re.search(r"PDF derivative pp\.\s*(\d+)-(\d+)", locator)

        if m_single:
            deriv_page = int(m_single.group(1))
            assert deriv_page == expected_deriv_page, (
                f"Derivative page mismatch for {eid} (printed p. {p_printed}): "
                f"expected {expected_deriv_page}, found {deriv_page} in locator '{locator}'"
            )
        elif m_range:
            start_deriv = int(m_range.group(1))
            end_deriv = int(m_range.group(2))
            assert start_deriv <= expected_deriv_page <= end_deriv, (
                f"Derivative page range mismatch for {eid} (printed p. {p_printed}): "
                f"expected {expected_deriv_page} inside range {start_deriv}-{end_deriv} in locator '{locator}'"
            )
        else:
            raise AssertionError(f"Could not parse derivative page from locator '{locator}' for {eid}")


def test_s04f_failing_gates_reject_certified_verdict(tmp_path):
    """F1 regression guard: Gate failures produce fail-closed exits and no certified report."""
    repo_root = Path(__file__).resolve().parent.parent
    import sys
    sys.path.insert(0, str(repo_root / "scripts"))
    import verify_s04f_negative_search as vns

    fake_pdf = tmp_path / "fake_gal.pdf"
    fake_text = tmp_path / "fake_text.txt"

    # Test 1: Positive control failure causes build_markdown_report to mark FAIL / UNVERIFIED
    pos_results_failed = [
        {"name": "Deut. 21:23 positive control", "pattern": r"Deut\.", "expected_min": 1, "passed": False, "count": 0, "sample": "None"},
        {"name": "Gen. 15:6 positive control", "pattern": r"Gen\.", "expected_min": 1, "passed": True, "count": 5, "sample": "Gen. xv. 6"},
    ]
    index_results_ok = {"passed": True, "sample": "Deuteronomy xxi. 23"}

    report = vns.build_markdown_report(
        search_results=[],
        pos_results=pos_results_failed,
        index_results=index_results_ok,
        pdf_path=fake_pdf,
        pdf_size=vns.EXPECTED_RAW_PDF_BYTES,
        pdf_sha=vns.EXPECTED_RAW_PDF_SHA256,
        text_path=fake_text,
        text_sha=vns.EXPECTED_TEXT_SHA256,
        text_chars=10000,
        text_lines=500,
    )
    assert "**Gate Verification Overall:** **FAIL / UNVERIFIED**" in report
    assert "**Gate Verification Overall:** **PASS**" not in report
    assert "**Overall Negative Search Verdict:** **FAILED**" in report
    assert "**Overall Negative Search Verdict:** **PASSED**" not in report

    # Test 2: Index failure causes build_markdown_report to mark FAIL / UNVERIFIED
    pos_results_ok = [
        {"name": "Deut. 21:23 positive control", "pattern": r"Deut\.", "expected_min": 1, "passed": True, "count": 10, "sample": "Deut. xxi. 23"},
    ]
    index_results_failed = {"passed": False, "error": "Index structure missing"}
    report_idx_fail = vns.build_markdown_report(
        search_results=[],
        pos_results=pos_results_ok,
        index_results=index_results_failed,
        pdf_path=fake_pdf,
        pdf_size=vns.EXPECTED_RAW_PDF_BYTES,
        pdf_sha=vns.EXPECTED_RAW_PDF_SHA256,
        text_path=fake_text,
        text_sha=vns.EXPECTED_TEXT_SHA256,
        text_chars=10000,
        text_lines=500,
    )
    assert "**Gate Verification Overall:** **FAIL / UNVERIFIED**" in report_idx_fail
    assert "**Gate Verification Overall:** **PASS**" not in report_idx_fail
    assert "**Overall Negative Search Verdict:** **FAILED**" in report_idx_fail
    assert "**Overall Negative Search Verdict:** **PASSED**" not in report_idx_fail


def test_s04f_unauthenticated_override_prohibits_canonical_overwrite(tmp_path, monkeypatch):
    """F2 regression guard: Digest mismatch override refuses canonical path (exit code 9)."""
    repo_root = Path(__file__).resolve().parent.parent
    import sys
    sys.path.insert(0, str(repo_root / "scripts"))
    import verify_s04f_negative_search as vns

    fake_pdf = tmp_path / "fake_gal.pdf"
    fake_pdf.write_bytes(b"0" * vns.EXPECTED_RAW_PDF_BYTES)
    fake_text = tmp_path / "fake_text.txt"

    monkeypatch.setattr(vns, "get_sha256", lambda p: vns.EXPECTED_RAW_PDF_SHA256)

    def mock_subprocess_run(cmd, check=False):
        out_txt = Path(cmd[2])
        out_txt.write_text("Dummy extracted text\n" * 100, encoding="utf-8")
        class SubprocessResult:
            returncode = 0
        return SubprocessResult()

    monkeypatch.setattr("subprocess.run", mock_subprocess_run)

    # Calling with canonical report path under unauthenticated override must exit 9
    ret = vns.run_verification(
        pdf_path=fake_pdf,
        text_path=fake_text,
        out_path=vns.DEFAULT_OUT_PATH,
        allow_text_digest_mismatch=True,
        quiet=True,
    )
    assert ret == 9, f"Expected exit code 9 for canonical overwrite under digest mismatch, got {ret}"


def test_s04f_e013_greek_text_critical_invariants():
    """F4 regression guard: E013 must not assert Paul added πᾶς or ἐπὶ ξύλου to Deut 21:23."""
    repo_root = Path(__file__).resolve().parent.parent
    s04f_dir = repo_root / "research/inbox/B001-pauline-txt-pilot/sources/S04F"
    csv_path = s04f_dir / "citation_ledger.csv"

    with open(csv_path, encoding="utf-8") as f:
        rows = {r["evidence_id"]: r for r in csv.DictReader(f)}

    e013 = rows["S04F-E013"]
    claim_text = e013["author_claim"].lower()
    qual_text = e013["qualification"].lower()

    # Must NOT claim Paul added πᾶς or ἐπὶ ξύλου to Deut 21:23
    assert "adding πᾶς" not in claim_text
    assert "adding ἐπὶ ξύλου" not in claim_text
    assert "adding πᾶς and ἐπὶ ξύλου" not in claim_text

    # Must identify the actual Pauline modifications: ἐπικατάρατος, article ὁ, omitting ὑπὸ θεοῦ
    assert "ἐπικατάρατος" in e013["author_claim"]
    assert "ὑπὸ θεοῦ" in claim_text or "ὑπὸ Θεοῦ" in e013["author_claim"]
    assert "ὁ" in e013["author_claim"]

    # Must characterize Justin's dependence as an authorial historical inference
    assert "historical inference" in qual_text or "inference" in qual_text


def test_s04f_authorial_qualifications_and_b001_11_sync():
    """M1/M2 regression guard: Concessions preserved and B001-11 synchronized across artifacts."""
    repo_root = Path(__file__).resolve().parent.parent
    s04f_dir = repo_root / "research/inbox/B001-pauline-txt-pilot/sources/S04F"
    csv_path = s04f_dir / "citation_ledger.csv"

    with open(csv_path, encoding="utf-8") as f:
        rows = {r["evidence_id"]: r for r in csv.DictReader(f)}

    # E004 p. 154 crucifixion pre-Christian absence concession
    e004 = rows["S04F-E004"]
    assert "any evidence to show that this passage of deuteronomy had been applied" in e004["qualification"].lower()

    # E009 James awareness qualification
    e009 = rows["S04F-E009"]
    assert "whether james knew paul's epistles" in e009["author_claim"].lower() or "leaves open" in e009["author_claim"].lower()

    # B001-11 synchronized in relevance_scan.md
    rel_scan = (s04f_dir / "relevance_scan.md").read_text(encoding="utf-8")
    assert "11. 1 Corinthians 10:7 / Exodus 32:6\n\t\nYES\n\t\nPage 311\n\t\nPassing" in rel_scan

    # B001-11 synchronized in counterevidence.md
    counter_ev = (s04f_dir / "counterevidence.md").read_text(encoding="utf-8")
    assert "Page 311 (Dissertation III: \"St Paul and the Three\")" in counter_ev
    assert "PASSING CROSS-REFERENCE ONLY" in counter_ev


def test_s04f_index_per_locus_scripture_inventory():
    """S04F-R2-F1 & S04F-R3-M1: Verify per-locus Scripture Index evaluation on clean-clone versioned fixture."""
    repo_root = Path(__file__).resolve().parent.parent
    import sys
    sys.path.insert(0, str(repo_root / "scripts"))
    import verify_s04f_negative_search as vns

    fixture_path = repo_root / "tests/fixtures/s04f_authorial_index_fixture.txt"
    assert fixture_path.exists(), f"Tracked index fixture missing at {fixture_path}"
    text = fixture_path.read_text(encoding="utf-8")

    index_res = vns.verify_index_structure(text)
    assert index_res["index_present"] is True
    assert index_res["has_end_marker"] is True
    assert index_res["structural_passed"] is True
    assert index_res["targets_passed"] is True
    assert index_res["passed"] is True

    target_res = index_res["target_results"]
    assert len(target_res) == 12, f"Expected 12 B001 target results in index inventory, got {len(target_res)}"

    # Positive index controls: B001-1 and B001-12
    assert target_res["B001-1"]["passed"] is True
    assert target_res["B001-1"]["expected_in_index"] is True
    assert target_res["B001-1"]["hit_count"] >= 1
    assert target_res["B001-1"]["index_status"] == "VERIFIED INDEX ENTRY"
    assert any("Genesis" in h["match"] and "15" in h["match"] or "xv" in h["match"].lower() for h in target_res["B001-1"]["hits"])

    assert target_res["B001-12"]["passed"] is True
    assert target_res["B001-12"]["expected_in_index"] is True
    assert target_res["B001-12"]["hit_count"] >= 1
    assert target_res["B001-12"]["index_status"] == "VERIFIED INDEX ENTRY"
    assert any("Deuteronomy" in h["match"] and "21" in h["match"] or "xxi" in h["match"].lower() for h in target_res["B001-12"]["hits"])

    # Negative index targets: B001-2 through B001-11 must have zero hits
    # B001-2 through B001-7: Unindexed books without authorial headings (Hosea, Joel, Isaiah)
    for locus in ["B001-2", "B001-3", "B001-4", "B001-5", "B001-6", "B001-7"]:
        assert target_res[locus]["passed"] is True, f"Target {locus} failed index verification"
        assert target_res[locus]["expected_in_index"] is False
        assert target_res[locus]["hit_count"] == 0, f"Expected 0 hits for {locus} in authentic index, got {target_res[locus]['hit_count']}: {target_res[locus]['hits']}"
        assert target_res[locus]["index_status"] == "UNINDEXED BOOK (NO AUTHORIAL HEADING)"

    # B001-8 through B001-11: Indexed books where specific target is absent (1 Cor, Gen, Deut, Exod)
    for locus in ["B001-8", "B001-9", "B001-10", "B001-11"]:
        assert target_res[locus]["passed"] is True, f"Target {locus} failed index verification"
        assert target_res[locus]["expected_in_index"] is False
        assert target_res[locus]["hit_count"] == 0, f"Expected 0 hits for {locus} in authentic index, got {target_res[locus]['hit_count']}: {target_res[locus]['hits']}"
        assert target_res[locus]["index_status"] == "VERIFIED ABSENT (BOOK INDEXED; TARGET ABSENT)"


def test_s04f_index_counterexample_fails_closed():
    """
    S04F-R2-F1 & S04F-R3-F1 adversarial regression suite:
    1. Reviewer R2 counterexample (Isa. xl. 13 inserted) fails closed under B001-6.
    2. Reviewer R3-F1 counterexample (Joel iii. 5 inserted) fails closed under B001-5.
    3. Multi-entry book-section entry beyond 100 characters (Deut xxv. 4 inserted) fails closed under B001-10.
    """
    repo_root = Path(__file__).resolve().parent.parent
    import sys
    sys.path.insert(0, str(repo_root / "scripts"))
    import verify_s04f_negative_search as vns

    fixture_path = repo_root / "tests/fixtures/s04f_authorial_index_fixture.txt"
    assert fixture_path.exists(), f"Tracked index fixture missing at {fixture_path}"
    text = fixture_path.read_text(encoding="utf-8")

    m_start = re.search(r"\n\x0cINDEX\.\n|INDEX\.\nApranaM", text)
    idx_start = m_start.start() if m_start else 0
    m_end = re.search(vns.INDEX_END_PATTERNS[0], text[idx_start:])
    assert m_end is not None
    insert_pos = idx_start + m_end.start()

    # Adversarial Case 1: Reviewer R2 counterexample (Isa. xl. 13, p. 44)
    adv_isa = text[:insert_pos] + "\nIII. PASSAGES OF SCRIPTURE\nIsa. xl. 13, p. 44\n" + text[insert_pos:]
    res_isa = vns.verify_index_structure(adv_isa)
    assert res_isa["targets_passed"] is False, "Expected targets verification to fail on inserted Isa. xl. 13"
    assert res_isa["passed"] is False, "Expected index verification to fail on inserted Isa. xl. 13"
    assert res_isa["target_results"]["B001-6"]["passed"] is False
    assert any("Isa. xl. 13" in h["match"] for h in res_isa["target_results"]["B001-6"]["hits"])

    # Adversarial Case 2: Reviewer R3-F1 counterexample (Joel iii. 5, p. 44)
    adv_joel = text[:insert_pos] + "\nJoel iii. 5, p. 44\n" + text[insert_pos:]
    res_joel = vns.verify_index_structure(adv_joel)
    assert res_joel["targets_passed"] is False, "Expected targets verification to fail on inserted Joel iii. 5"
    assert res_joel["passed"] is False, "Expected index verification to fail on inserted Joel iii. 5"
    assert res_joel["target_results"]["B001-5"]["passed"] is False
    assert any("iii. 5" in h["match"] or "3:5" in h["match"] for h in res_joel["target_results"]["B001-5"]["hits"])

    # Adversarial Case 3: Book-section entry beyond 100 characters from heading (Deut xxv. 4 inserted)
    adv_deut = text.replace(
        "Deuteronomy, passages commented on;",
        "Deuteronomy, passages commented on; (iv. 1) p. 10; (v. 2) p. 20; (vi. 3) p. 30; (vii. 4) p. 40; (viii. 5) p. 50; (ix. 6) p. 60; (x. 7) p. 70; (xxv. 4) p. 80;"
    )
    res_deut = vns.verify_index_structure(adv_deut)
    assert res_deut["targets_passed"] is False, "Expected targets verification to fail on inserted Deut xxv. 4"
    assert res_deut["passed"] is False, "Expected index verification to fail on inserted Deut xxv. 4"
    assert res_deut["target_results"]["B001-10"]["passed"] is False
    assert any("xxv. 4" in h["match"] or "25:4" in h["match"] for h in res_deut["target_results"]["B001-10"]["hits"])


def test_s04f_index_fixture_provenance_and_clean_clone_reproducibility():
    """S04F-R3-M1 regression guard: Verify index fixture existence, provenance SHA, and clean-clone portability."""
    import hashlib
    repo_root = Path(__file__).resolve().parent.parent
    import sys
    sys.path.insert(0, str(repo_root / "scripts"))
    import verify_s04f_negative_search as vns

    fixture_path = repo_root / "tests/fixtures/s04f_authorial_index_fixture.txt"
    assert fixture_path.exists(), f"Fixture missing at {fixture_path}"

    # Verify SHA-256 of the versioned fixture matches the authentic index layer
    fixture_bytes = fixture_path.read_bytes()
    fixture_sha = hashlib.sha256(fixture_bytes).hexdigest()
    assert fixture_sha == "8e89b1b9ecf61c9350aea2e1ff32f60135d834ebf9ff26cf6c1c68c848968d88", (
        f"Fixture SHA mismatch: expected 8e89b1b9..., got {fixture_sha}"
    )

    # Verify that full index verification passes cleanly on the fixture alone
    fixture_text = fixture_bytes.decode("utf-8")
    res = vns.verify_index_structure(fixture_text)
    assert res["passed"] is True
    assert res["structural_passed"] is True
    assert res["targets_passed"] is True


def test_s04f_index_reordered_continuation_counterexample_fails_closed():
    """
    S04F-R4-F1 adversarial regression test:
    Reviewer R4 counterexample: In the two-column OCR layout of Lightfoot's index,
    'Corinthians, 1st Epistle to the, ... passages com-' (p. 376 col. 2) continues
    at 'mented on, (i. 12) p. 372, (ii. g) p. 334...' (p. 377 col. 1).
    If an adversary or OCR displacement inserts a target like '(ix. 9) p. 80;' into
    this continuation fragment, verify_index_structure must detect it under B001-10
    and fail closed.
    """
    repo_root = Path(__file__).resolve().parent.parent
    import sys
    sys.path.insert(0, str(repo_root / "scripts"))
    import verify_s04f_negative_search as vns

    fixture_path = repo_root / "tests/fixtures/s04f_authorial_index_fixture.txt"
    assert fixture_path.exists(), f"Tracked index fixture missing at {fixture_path}"
    text = fixture_path.read_text(encoding="utf-8")

    # Baseline: fixture passes cleanly
    res_base = vns.verify_index_structure(text)
    assert res_base["passed"] is True
    assert res_base["target_results"]["B001-10"]["passed"] is True
    assert res_base["target_results"]["B001-10"]["index_status"] == "VERIFIED ABSENT (BOOK INDEXED; TARGET ABSENT)"

    # Adversarial injection into reordered continuation: (ix. 9) p. 80; (i. 12) p. 372
    adv_text = text.replace(
        "mented on, (i. 12) p. 372",
        "mented on, (ix. 9) p. 80; (i. 12) p. 372",
    )
    assert adv_text != text, "Substitution target not found in fixture"

    res_adv = vns.verify_index_structure(adv_text)
    assert res_adv["targets_passed"] is False, "Expected targets verification to fail on inserted 1 Cor 9:9 in continuation"
    assert res_adv["passed"] is False, "Expected index verification to fail closed"

    b10_res = res_adv["target_results"]["B001-10"]
    assert b10_res["passed"] is False
    assert b10_res["index_status"] == "UNEXPECTED INDEX HIT"
    assert b10_res["hit_count"] >= 1
    assert any("ix. 9" in h["match"] or "9. 9" in h["match"] for h in b10_res["hits"])


def test_s04f_index_unqualified_verse_after_intervening_headword_boundary():
    """
    S04F-R4-F1 boundary characterization test:
    Verify that extract_book_sections strictly respects headword boundaries.
    If an unqualified verse citation like '(ix. 9) p. 80' appears after an intervening
    major headword (e.g. under 'Damascenus (Johannes)'), it must NOT be mistakenly
    attributed to Corinthians.
    """
    repo_root = Path(__file__).resolve().parent.parent
    import sys
    sys.path.insert(0, str(repo_root / "scripts"))
    import verify_s04f_negative_search as vns

    fixture_path = repo_root / "tests/fixtures/s04f_authorial_index_fixture.txt"
    text = fixture_path.read_text(encoding="utf-8")

    # Inject unqualified (ix. 9) under Damascenus headword
    adv_dam = text.replace(
        "Damascenus (Johannes), his commentary on St Paul",
        "Damascenus (Johannes), (ix. 9) p. 80; his commentary on St Paul",
    )
    assert adv_dam != text

    # Extract book sections for Corinthians
    sections = vns.extract_book_sections(adv_dam, r"\bCorinthians\b")
    # Verify that the injected verse does NOT appear in any Corinthians section
    for start_off, sec_chunk in sections:
        assert "(ix. 9)" not in sec_chunk, "Unqualified verse under intervening headword leaked into Corinthians section"


def test_s04f_authorial_index_scripture_ledger_complete():
    """
    S04F-R4-F1 & S04F-R4 ledger verification:
    Verify that tests/fixtures/s04f_authorial_index_scripture_ledger.json provides
    an exhaustive census of all 13 scriptural book entries from printed pages 375-384,
    confirming positive presence of B001-1 (Gen 15:6) and B001-12 (Deut 21:23),
    unindexed status for B001-2..B001-7 (Hosea, Joel, Isaiah), and target absence
    for B001-8..B001-11 in the indexed books.
    """
    import json
    repo_root = Path(__file__).resolve().parent.parent
    ledger_path = repo_root / "tests/fixtures/s04f_authorial_index_scripture_ledger.json"
    assert ledger_path.exists(), f"Authorial Scripture index ledger missing at {ledger_path}"

    with open(ledger_path, encoding="utf-8") as f:
        ledger = json.load(f)

    assert ledger["source_id"] == "S04F"
    assert ledger["total_scriptural_book_entries"] == 13
    entries = ledger["entries"]
    assert len(entries) == 13

    book_names = [e["book"] for e in entries]
    expected_books = [
        "Acts", "1 Corinthians", "2 Corinthians", "Deuteronomy", "Exodus",
        "Ephesians", "Genesis", "Habakkuk", "John", "1 Maccabees",
        "Revelation", "Romans", "2 Timothy"
    ]
    assert book_names == expected_books

    # Positive controls
    gen_entry = next(e for e in entries if e["book"] == "Genesis")
    assert any("xv. 6" in c or "15" in c for c in gen_entry["citations"])

    deut_entry = next(e for e in entries if e["book"] == "Deuteronomy")
    assert any("xxi. 23" in c or "21" in c for c in deut_entry["citations"])

    # Unindexed books: Hosea, Joel, Isaiah must NOT appear in the authorial book headings
    assert "Hosea" not in book_names
    assert "Joel" not in book_names
    assert "Isaiah" not in book_names

    # Target absence in indexed books:
    cor1_entry = next(e for e in entries if e["book"] == "1 Corinthians")
    # 1 Cor 1:19, 6:16, 9:9, 10:7 must not be in 1 Cor citations
    for target_verse in ["i. 19", "vi. 16", "ix. 9", "x. 7"]:
        assert not any(target_verse in c for c in cor1_entry["citations"]), f"Unexpected hit {target_verse} in 1 Cor citations"

    exod_entry = next(e for e in entries if e["book"] == "Exodus")
    assert not any("xxxii. 6" in c or "32:6" in c for c in exod_entry["citations"])

    # Deuteronomy 25:4 absent
    assert not any("xxv. 4" in c or "25:4" in c for c in deut_entry["citations"])


def test_s05_citation_ledger_crosswalk_integrity():
    repo_root = Path(__file__).resolve().parent.parent
    s05_dir = repo_root / "research/inbox/B001-pauline-txt-pilot/sources/S05"
    csv_path = s05_dir / "citation_ledger.csv"

    assert csv_path.is_file(), f"Missing citation_ledger.csv for S05 at {csv_path}"

    with open(csv_path, encoding="utf-8") as f:
        reader = list(csv.DictReader(f))

    assert len(reader) == 12, f"Expected exactly 12 ledger rows for S05, found {len(reader)}"

    expected_locus_map = {
        "S05-E001": "B001-2",
        "S05-E002": "B001-3",
        "S05-E003": "B001-4",
        "S05-E004": "B001-4",
        "S05-E005": "B001-5",
        "S05-E006": "B001-6",
        "S05-E007": "B001-6",
        "S05-E008": "B001-7",
        "S05-E009": "B001-7",
        "S05-E010": "B001-8",
        "S05-E011": "B001-8",
        "S05-E012": "B001-12",
    }

    for idx, row in enumerate(reader, 1):
        expected_eid = f"S05-E{idx:03d}"
        assert row["evidence_id"] == expected_eid, f"Expected {expected_eid}, got {row['evidence_id']}"
        assert row["source_id"] == "S05"
        assert row["b001_id"] == expected_locus_map[expected_eid], (
            f"Referential integrity failure: {expected_eid} claimed locus {row['b001_id']} != expected {expected_locus_map[expected_eid]}"
        )
        assert row["verification_status"] == "VERIFIED", f"Row {expected_eid} status not VERIFIED: {row['verification_status']}"
        assert len(row["short_quote"]) > 5, f"Short quote too short for {expected_eid}"
        assert len(row["author_claim"]) > 10, f"Author claim too short for {expected_eid}"
        assert row["printed_page"].isdigit(), f"Invalid printed_page for {expected_eid}: {row['printed_page']}"
        assert "S." in row["source_locator"], f"Invalid source_locator for {expected_eid}: {row['source_locator']}"

    # Specific check for S05-E012
    e012 = reader[11]
    assert e012["evidence_id"] == "S05-E012"
    assert e012["b001_id"] == "B001-12"
    assert e012["printed_page"] == "47"
    assert "Gal 313" in e012["short_quote"]
    assert "epikataratos" in e012["author_claim"].lower() or "ἐπικατάρατος" in e012["author_claim"]
    assert e012["claim_type"] == "TEXTUAL_CRITICAL"


def test_s05_self_audit_corrections_incorporated():
    repo_root = Path(__file__).resolve().parent.parent
    s05_dir = repo_root / "research/inbox/B001-pauline-txt-pilot/sources/S05"
    csv_path = s05_dir / "citation_ledger.csv"

    with open(csv_path, encoding="utf-8") as f:
        rows = {r["evidence_id"]: r for r in csv.DictReader(f)}

    # Check 1: S05-E008 preserves Wilk's explicit text-critical reservation on page 238 note 28
    e008 = rows["S05-E008"]
    assert "238" in e008["source_locator"]
    assert "238" in e008["qualification"] and "28" in e008["qualification"]
    assert "hebraizing" in e008["qualification"].lower() or "hebraisierend" in e008["qualification"].lower()

    # Check 2: S05-E004 preserves distinction between dual-aspect stumbling stone in Rom 9:33 and unmixed positive promise in Rom 10:11
    e004 = rows["S05-E004"]
    claim_004 = e004["author_claim"].lower()
    assert "9:33" in claim_004
    assert "10:11" in claim_004
    assert "dual" in claim_004 or "stumbling" in claim_004


def test_s05_provenance_and_hash_integrity():
    import hashlib
    import os
    repo_root = Path(__file__).resolve().parent.parent
    prov_path = repo_root / "research/inbox/B001-pauline-txt-pilot/sources/S05/provenance_manifest.json"
    assert prov_path.is_file(), "Missing provenance_manifest.json for S05"

    with open(prov_path, encoding="utf-8") as f:
        prov = json.load(f)

    assert prov["source_id"] == "S05"
    assert prov["raw_volume_scan"]["size_bytes"] == 96225856
    assert prov["raw_volume_scan"]["sha256"] == "700323565f6687163dc92f410779b054b763ee10bf3f745f5c2370b5455aa1b3"
    assert prov["ingested_volume"]["size_bytes"] == 96225856
    assert prov["ingested_volume"]["sha256"] == "700323565f6687163dc92f410779b054b763ee10bf3f745f5c2370b5455aa1b3"

    # If physical files exist in local environment, verify stats
    local_raw = Path("/Users/chrisrodriguez/Downloads/wilk_1998_jesaja_paulus_mdz_raw.pdf")
    if local_raw.is_file():
        assert os.path.getsize(local_raw) == 96225856
        h = hashlib.sha256(local_raw.read_bytes()).hexdigest()
        assert h == "700323565f6687163dc92f410779b054b763ee10bf3f745f5c2370b5455aa1b3"


def test_s05_negative_search_evidence_discipline():
    repo_root = Path(__file__).resolve().parent.parent
    s05_dir = repo_root / "research/inbox/B001-pauline-txt-pilot/sources/S05"

    script_path = repo_root / "scripts/verify_s05_negative_search.py"
    log_path = s05_dir / "full_volume_search_log.md"
    assert script_path.is_file(), "Missing verify_s05_negative_search.py"
    assert log_path.is_file(), "Missing full_volume_search_log.md"

    with open(log_path, encoding="utf-8") as f:
        log_text = f.read()

    # Log covers all 12 B001 loci
    for i in range(1, 13):
        locus = f"B001-{i}"
        assert locus in log_text

    # Positive controls validated
    assert "Positive Control Verification" in log_text
    assert "PASSED" in log_text

    # Stellenregister sections verified
    assert "8/8 passed" in log_text
    assert "13/13 required book/testament sections pattern-bounded with verified start and end delimiters" in log_text

    # Accurate text byte and character accounting (Fixes L1)
    assert "`1470319` bytes" in log_text
    assert "`1439712` characters" in log_text

    # Exact evidence ID referential integrity crosswalk (Fixes F3)
    assert "crosswalked to S05-E001 (" in log_text
    assert "crosswalked to S05-E002 (" in log_text
    assert "crosswalked to S05-E003, S05-E004 (" in log_text
    assert "crosswalked to S05-E005 (" in log_text
    assert "crosswalked to S05-E006, S05-E007 (" in log_text
    assert "crosswalked to S05-E008, S05-E009 (" in log_text
    assert "crosswalked to S05-E010, S05-E011 (" in log_text
    assert "Crosswalked to S05-E012 (" in log_text or "crosswalked to S05-E012 (" in log_text

    # Negative non-prophetic loci B001-1 and B001-9 must be NOT DISCUSSED
    assert "| B001-1 | Romans 4:3 / Genesis 15:6 | 1 | 0 | 0 | NOT DISCUSSED |" in log_text
    assert "| B001-9 | 1 Corinthians 6:16 / Genesis 2:24 | 0 | 0 | 0 | NOT DISCUSSED |" in log_text

    # Substantive loci
    for sub_id in ["B001-2", "B001-3", "B001-4", "B001-5", "B001-6", "B001-7", "B001-8"]:
        assert f"| {sub_id} |" in log_text
        assert "SUBSTANTIVE_DISCUSSION" in log_text

    # Passing loci
    assert "| B001-10 |" in log_text
    assert "PASSING_REFERENCE" in log_text
    assert "| B001-11 |" in log_text
    assert "| B001-12 |" in log_text
    assert "PASSING_TEXT_CRITICAL_NOTE" in log_text


def test_s05_negative_search_script_fail_closed_and_controls(tmp_path):
    repo_root = Path(__file__).resolve().parent.parent
    import subprocess
    import sys

    script = repo_root / "scripts/verify_s05_negative_search.py"

    # Test 1: Nonexistent PDF fails closed (exit code 1)
    fake_pdf = tmp_path / "nonexistent.pdf"
    res = subprocess.run([sys.executable, str(script), "--pdf", str(fake_pdf)], capture_output=True, text=True)
    assert res.returncode == 1, f"Expected exit code 1 for missing PDF, got {res.returncode}: {res.stderr}"
    assert "Fail closed" in res.stderr

    # Test 2: Dummy PDF with wrong byte size fails closed (exit code 2)
    dummy_pdf = tmp_path / "corrupt.pdf"
    dummy_pdf.write_bytes(b"not a valid 96mb pdf")
    res = subprocess.run([sys.executable, str(script), "--pdf", str(dummy_pdf)], capture_output=True, text=True)
    assert res.returncode == 2, f"Expected exit code 2 for size mismatch, got {res.returncode}: {res.stderr}"
    assert "size mismatch" in res.stderr


def test_s05_authorial_index_fixture_provenance_and_clean_clone_reproducibility():
    import hashlib
    repo_root = Path(__file__).resolve().parent.parent
    fixture_path = repo_root / "tests/fixtures/s05_authorial_index_fixture.txt"
    assert fixture_path.is_file(), f"Missing index fixture at {fixture_path}"

    content = fixture_path.read_text(encoding="utf-8")
    h = hashlib.sha256(content.encode("utf-8")).hexdigest()
    assert h == "16f301c5be9320c07637ebf54025674a6a40e0911ebe6f9fee2e7a74d4f8ae24", f"SHA mismatch: {h}"
    assert "Stellenregister" in content
    assert "VERZEICHNIS DER UNTERSUCHTEN" in content or "V E R Z E I C H N I S" in content


def test_s05_authorial_index_scripture_ledger_complete():
    repo_root = Path(__file__).resolve().parent.parent
    ledger_path = repo_root / "tests/fixtures/s05_authorial_index_scripture_ledger.json"
    assert ledger_path.is_file(), f"Missing scripture ledger fixture at {ledger_path}"

    with open(ledger_path, encoding="utf-8") as f:
        ledger = json.load(f)

    assert ledger["source_id"] == "S05"
    assert ledger["year"] == 1998
    census = ledger["b001_targets_census"]
    assert len(census) == 12

    # Verify classifications in ledger census
    assert census["B001-1"]["status"] == "VERIFIED_ABSENT"
    assert census["B001-9"]["status"] == "VERIFIED_ABSENT"
    for tid in ["B001-2", "B001-3", "B001-4", "B001-5", "B001-6", "B001-7", "B001-8"]:
        assert census[tid]["status"] == "VERIFIED_PRESENT"
    for tid in ["B001-10", "B001-11", "B001-12"]:
        assert census[tid]["status"] == "VERIFIED_PRESENT_PARTIAL"


def test_s05_adversarial_index_failure_modes():
    """
    S05-R1-F2 & S05-R2-F2 adversarial regression test:
    (a) Inject 4,3 into Römerbrief section fixture -> fail B001-1
    (b) Inject 15,6 into Genesis section fixture -> fail B001-1
    (c) Remove genuine B001-10 entry ('9 112') from 1. Korintherbrief -> fail B001-10
    (d) Remove genuine B001-11 entry ('7 319') from 1. Korintherbrief -> fail B001-11
    (e) Remove genuine B001-12 entry ('47') from Galaterbrief -> fail B001-12
    (f) Inject 1 Cor 10:7 entry into Exodus section -> does NOT satisfy 1. Korintherbrief
    (g) Missing/corrupted book section (e.g. Genesis) -> fails coverage, marks negative targets INDETERMINATE
    (h) Inject Isaiah 28:16 into Genesis -> does NOT satisfy Section 1.1 scoped Isaiah check
    """
    import sys
    repo_root = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(repo_root / "scripts"))
    import verify_s05_negative_search as vns

    fixture_path = repo_root / "tests/fixtures/s05_authorial_index_fixture.txt"
    assert fixture_path.exists(), f"Tracked index fixture missing at {fixture_path}"
    text = fixture_path.read_text(encoding="utf-8")

    # 0. Clean baseline fixture must pass
    res_base = vns.verify_index_structure(text)
    assert res_base["passed"] is True, f"Baseline fixture failed index verification: {res_base.get('error')}"
    assert res_base["targets_passed"] is True

    # 1. Adversarial Injection (a): Inject '4,3' into Römerbrief section fixture -> fail B001-1
    adv_rom = text.replace("Römerbrief\n1-16\n1 1-7", "Römerbrief\n4,3\n1-16\n1 1-7")
    assert adv_rom != text
    res_adv_rom = vns.verify_index_structure(adv_rom)
    assert res_adv_rom["targets_passed"] is False, "Expected targets verification to fail on inserted Rom 4,3"
    assert res_adv_rom["target_results"]["B001-1"]["passed"] is False
    assert res_adv_rom["target_results"]["B001-1"]["index_status"] == "UNEXPECTED INDEX HIT"

    # 2. Adversarial Injection (b): Inject '15,6' into Genesis section fixture -> fail B001-1
    adv_gen = text.replace("Genesis\n\n1 it.", "Genesis\n15,6\n1 it.")
    assert adv_gen != text
    res_adv_gen = vns.verify_index_structure(adv_gen)
    assert res_adv_gen["targets_passed"] is False, "Expected targets verification to fail on inserted Gen 15,6"
    assert res_adv_gen["target_results"]["B001-1"]["passed"] is False
    assert res_adv_gen["target_results"]["B001-1"]["index_status"] == "UNEXPECTED INDEX HIT"

    # 3. Adversarial Deletion (c): Remove genuine B001-10 entry ('9 112') from 1. Korintherbrief -> fail B001-10
    adv_del_10 = text.replace("9\n112", "9\n999")
    assert adv_del_10 != text
    res_del_10 = vns.verify_index_structure(adv_del_10)
    assert res_del_10["targets_passed"] is False, "Expected targets verification to fail when 1 Cor 9:9 entry is removed"
    assert res_del_10["target_results"]["B001-10"]["passed"] is False
    assert res_del_10["target_results"]["B001-10"]["index_status"] == "MISSING EXPECTED ENTRY"

    # 4. Adversarial Deletion (d): Remove genuine B001-11 entry ('7\n319') from 1. Korintherbrief -> fail B001-11
    adv_del_11 = text.replace("7\n319", "7\n999")
    assert adv_del_11 != text
    res_del_11 = vns.verify_index_structure(adv_del_11)
    assert res_del_11["targets_passed"] is False, "Expected targets verification to fail when 1 Cor 10:7 entry is removed"
    assert res_del_11["target_results"]["B001-11"]["passed"] is False
    assert res_del_11["target_results"]["B001-11"]["index_status"] == "MISSING EXPECTED ENTRY"

    # 5. Adversarial Deletion (e): Remove genuine B001-12 entry ('47') from Galaterbrief -> fail B001-12
    adv_del_12 = text.replace("130, 191\n216, 247\n47\n94, 152", "130, 191\n216, 247\n999\n94, 152")
    assert adv_del_12 != text
    res_del_12 = vns.verify_index_structure(adv_del_12)
    assert res_del_12["targets_passed"] is False, "Expected targets verification to fail when Gal 3:13 p. 47 is removed"
    assert res_del_12["target_results"]["B001-12"]["passed"] is False
    assert res_del_12["target_results"]["B001-12"]["index_status"] == "MISSING EXPECTED ENTRY"

    # 6. Cross-Section Misplacement (f): Inject 1 Cor 10:7 entry into Exodus section -> does NOT satisfy 1. Korintherbrief
    adv_cross = text.replace("7\n319", "7\n999").replace("Exodus\n3f.", "Exodus\n10 7 319\n3f.")
    res_cross = vns.verify_index_structure(adv_cross)
    assert res_cross["target_results"]["B001-11"]["passed"] is False, "Matches outside target book section must not satisfy verification"

    # 7. S05-R2-F2: Fail-closed book coverage when a required heading is missing or corrupted
    adv_missing_gen = text.replace("Genesis\n", "UNKNOWN_BOOK\n")
    assert adv_missing_gen != text
    res_missing_gen = vns.verify_index_structure(adv_missing_gen)
    assert res_missing_gen["passed"] is False, "Expected index verification to fail when Genesis heading is missing"
    assert res_missing_gen["coverage_passed"] is False
    assert "Genesis" in res_missing_gen["missing_sections"]
    assert res_missing_gen["target_results"]["B001-1"]["passed"] is False
    assert "INDETERMINATE" in res_missing_gen["target_results"]["B001-1"]["index_status"]
    assert res_missing_gen["target_results"]["B001-9"]["passed"] is False
    assert "INDETERMINATE" in res_missing_gen["target_results"]["B001-9"]["index_status"]

    # 8. S05-R2-F2: Section 1.1 scoping discipline - matches outside sec_1_1 do not satisfy Isaiah checks
    target_isa = "2816\n\n(Rom\n\n933\n\n(Rom\n\nlOll"
    assert target_isa in text
    adv_isa_cross = text.replace(target_isa, "9999\n\n(Rom\n\n999").replace("Genesis\n", f"Genesis\n{target_isa}\n")
    res_isa_cross = vns.verify_index_structure(adv_isa_cross)
    assert res_isa_cross["target_results"]["B001-4"]["passed"] is False, "Section 1.1 matches placed in Genesis must not satisfy B001-4"

    # 9. S05-R3-F2: Fail-closed boundary failure when end delimiter '2.3. Jüdische' is mutated
    adv_del_boundary = text.replace("2.3. Jüdische", "2.3. UNKNOWN_SECTION")
    assert adv_del_boundary != text
    res_del_boundary = vns.verify_index_structure(adv_del_boundary)
    assert res_del_boundary["passed"] is False, "Expected index verification to fail when 2.3 end delimiter is mutated"
    assert res_del_boundary["coverage_passed"] is False
    assert len(res_del_boundary["boundary_failures"]) > 0
    assert any("2.3." in f or "sec_nt" in f for f in res_del_boundary["boundary_failures"])
    assert res_del_boundary["target_results"]["B001-1"]["passed"] is False
    assert "BOUNDARY VERIFICATION FAILED" in res_del_boundary["target_results"]["B001-1"]["index_status"]

    # 10. S05-R3-F2: Fail-closed boundary failure when next-book delimiter in OT is mutated
    adv_book_boundary = text.replace("Exodus\n", "UNKNOWN_BOOK\n")
    assert adv_book_boundary != text
    res_book_boundary = vns.verify_index_structure(adv_book_boundary)
    assert res_book_boundary["passed"] is False, "Expected index verification to fail when Exodus boundary is mutated"
    assert res_book_boundary["coverage_passed"] is False
    assert any("Genesis" in f for f in res_book_boundary["boundary_failures"])
    assert res_book_boundary["target_results"]["B001-1"]["passed"] is False
    assert "BOUNDARY VERIFICATION FAILED" in res_book_boundary["target_results"]["B001-1"]["index_status"]


def test_s05_dynamic_adjudication_rejects_synthetic_substantive_or_uncataloged_hits():
    """
    S05-R1-F1 regression test:
    Proves that zero-hit substantive queries cannot inherit substantive verdicts,
    and uncataloged hits for NOT DISCUSSED targets cannot pass.
    """
    import sys
    repo_root = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(repo_root / "scripts"))
    import verify_s05_negative_search as vns

    # Case 1: Synthetic 0-hit substantive target definition
    target_def_sub = {
        "id": "B001-4",
        "name": "Romans 10:11 / Isaiah 28:16",
        "nt_target": "Rom 10:11",
        "ot_target": "Isa 28:16",
        "expected_classification": "SUBSTANTIVE_DISCUSSION",
        "evidence_ids": ["S05-E003", "S05-E004"],
        "min_substantive_hits": 5,
    }
    adj_zero = vns.adjudicate_target(target_def_sub, [], {"passed": True})
    assert adj_zero["passed"] is False
    assert adj_zero["classification"] == "UNEXPECTED_ZERO_HITS"
    assert "FAIL" in adj_zero["summary"]

    # Case 2: Insufficient hits for substantive target
    adj_insuf = vns.adjudicate_target(target_def_sub, [{"start": 100}], {"passed": True})
    assert adj_insuf["passed"] is False
    assert adj_insuf["classification"] == "INSUFFICIENT_HITS"
    assert "below required substantive threshold" in adj_insuf["summary"]

    # Case 3: Synthetic uncataloged hit for NOT DISCUSSED target
    target_def_neg = {
        "id": "B001-9",
        "name": "1 Corinthians 6:16 / Genesis 2:24",
        "nt_target": "1 Cor 6:16",
        "ot_target": "Gen 2:24",
        "expected_classification": "NOT DISCUSSED",
        "evidence_ids": [],
        "allowed_incidental_max": 0,
    }
    adj_neg = vns.adjudicate_target(target_def_neg, [{"start": 500, "match": "1Kor 6:16"}], {"passed": True})
    assert adj_neg["passed"] is False
    assert adj_neg["classification"] == "UNEXPECTED_HITS"
    assert "FAIL" in adj_neg["summary"]

    # Case 4 (S05-R2-F1 & S05-R3-F1): 5 threshold-satisfying synthetic incidental-only hits without substantive scholarly phrases fail
    incidental_hits = [
        {"start": i * 100, "match": "Rom 10:11", "snippet": "incidental mention of Rom 10:11 in Hosea and Paulus context"}
        for i in range(5)
    ]
    adj_inc = vns.adjudicate_target(target_def_sub, incidental_hits, {"passed": True})
    assert adj_inc["passed"] is False
    assert adj_inc["classification"] == "INCIDENTAL_ONLY_HITS"
    assert "FAIL" in adj_inc["summary"]
    assert "contain substantive scholarly context" in adj_inc["summary"]

    # Case 4b (S05-R3-F1): Incidental Hosea hits containing book name keywords but without scholarly analytical phrases fail
    target_def_hos = {
        "id": "B001-2",
        "name": "Romans 9:25 / Hosea 2:23",
        "nt_target": "Rom 9:25",
        "ot_target": "Hos 2:23",
        "expected_classification": "SUBSTANTIVE_DISCUSSION",
        "evidence_ids": ["S05-E001"],
        "min_substantive_hits": 3,
        "substantive_analytical_phrases": ["Auszeichnungen", "Erbarmensgefäße", "Befund", "Vorlage", "Wortlaut"],
    }
    incidental_book_hits = [
        {"start": i * 100, "match": "Hosea 2:25", "snippet": "incidental mention of Hosea 2:25 in book of Hosea and Paulus context"}
        for i in range(5)
    ]
    adj_inc_book = vns.adjudicate_target(target_def_hos, incidental_book_hits, {"passed": True})
    assert adj_inc_book["passed"] is False
    assert adj_inc_book["classification"] == "INCIDENTAL_ONLY_HITS"
    assert "FAIL" in adj_inc_book["summary"]
    assert "contain substantive scholarly context" in adj_inc_book["summary"]

    # Case 5 (S05-R2-F1): Substantive target with missing evidence record in ledger fails fail-closed
    substantive_hits = [
        {"start": i * 100, "match": "Rom 10:11", "snippet": "Untersuchung des Zitats Rom 10:11 Textform Vorlage Septuaginta"}
        for i in range(5)
    ]
    incomplete_ledger = {
        "S05-E003": {
            "evidence_id": "S05-E003",
            "b001_id": "B001-4",
            "verification_status": "VERIFIED",
            "printed_page": "45",
            "notebooklm_citation": "wilk [PDF p. 57; printed p. 45]",
            "source_locator": "Teil II.1.2.1.3a, S. 45",
        }
    }
    adj_miss = vns.adjudicate_target(target_def_sub, substantive_hits, {"passed": True}, ledger=incomplete_ledger)
    assert adj_miss["passed"] is False
    assert adj_miss["classification"] == "EVIDENCE_LEDGER_MISMATCH"
    assert "FAIL" in adj_miss["summary"]
    assert "Required evidence ID S05-E004 not found" in adj_miss["summary"]

    # Case 6 (S05-R2-F1): Substantive target with mismatched target_id in ledger fails fail-closed
    mismatched_ledger = {
        "S05-E003": {
            "evidence_id": "S05-E003",
            "b001_id": "B001-4",
            "verification_status": "VERIFIED",
            "printed_page": "45",
            "notebooklm_citation": "wilk [PDF p. 57; printed p. 45]",
            "source_locator": "Teil II.1.2.1.3a, S. 45",
        },
        "S05-E004": {
            "evidence_id": "S05-E004",
            "b001_id": "B001-99",
            "verification_status": "VERIFIED",
            "printed_page": "164",
            "notebooklm_citation": "wilk [PDF p. 176; printed p. 164]",
            "source_locator": "Teil II.3.1b, S. 164",
        },
    }
    adj_mism = vns.adjudicate_target(target_def_sub, substantive_hits, {"passed": True}, ledger=mismatched_ledger)
    assert adj_mism["passed"] is False
    assert adj_mism["classification"] == "EVIDENCE_LEDGER_MISMATCH"
    assert "FAIL" in adj_mism["summary"]
    assert "mapped to B001-99, expected B001-4" in adj_mism["summary"]

    # Case 7 (S05-R3-F1): Evidence row with short quote not found in authenticated text layer fails fail-closed
    unfound_quote_ledger = {
        "S05-E003": {
            "evidence_id": "S05-E003",
            "b001_id": "B001-4",
            "verification_status": "VERIFIED",
            "printed_page": "45",
            "notebooklm_citation": "wilk [PDF p. 57; printed p. 45]",
            "source_locator": "Teil II.1.2.1.3a, S. 45",
            "short_quote": "FABRICATED_QUOTE_NOT_IN_SOURCE_TEXT_12345",
            "author_claim": "Fabricated claim",
        },
        "S05-E004": {
            "evidence_id": "S05-E004",
            "b001_id": "B001-4",
            "verification_status": "VERIFIED",
            "printed_page": "164",
            "notebooklm_citation": "wilk [PDF p. 176; printed p. 164]",
            "source_locator": "Teil II.3.1b, S. 164",
            "short_quote": "ANOTHER_FABRICATED_QUOTE_67890",
            "author_claim": "Fabricated claim 2",
        },
    }
    adj_unfound = vns.adjudicate_target(
        target_def_sub, substantive_hits, {"passed": True}, ledger=unfound_quote_ledger, full_text="Authentic source text here."
    )
    assert adj_unfound["passed"] is False
    assert adj_unfound["classification"] == "EVIDENCE_LEDGER_MISMATCH"
    assert "quote not found in source text" in adj_unfound["summary"] or "quotation verification failed" in adj_unfound["summary"]

    # Case 4c (S05-R4-F1): >= threshold incidental citations WITH generic scholarly phrase on unrelated pages (pp. 10, 20, 30) fail hit-witness correlation
    target_def_b2 = {
        "id": "B001-2",
        "name": "Romans 9:25 / Hosea 2:23",
        "nt_target": "Rom 9:25",
        "ot_target": "Hos 2:23",
        "expected_classification": "SUBSTANTIVE_DISCUSSION",
        "evidence_ids": ["S05-E001"],
        "min_substantive_hits": 3,
        "expected_printed_pages": [130],
        "substantive_analytical_phrases": ["Auszeichnungen verheißend zuspricht", "Erbarmensgefäße"],
    }
    valid_b2_ledger = {
        "S05-E001": {
            "evidence_id": "S05-E001",
            "b001_id": "B001-2",
            "verification_status": "VERIFIED",
            "printed_page": "130",
            "notebooklm_citation": "wilk [PDF p. 142; printed p. 130]",
            "source_locator": "Teil II.2.2a, S. 130",
            "short_quote": "Indem es Heiden diejenigen „Auszeichnungen“ verheißend zuspricht...",
            "author_claim": "Valid claim",
        }
    }
    # Mock text with 142 pages for page-bounded quote verification
    mock_pages = ["Dummy page text\n"] * 200
    mock_pages[141] = "Indem es Heiden diejenigen 'Auszeichnungen' verheißend zuspricht, die Israel besaß..."
    mock_full_text = "\x0c".join(mock_pages)

    unrelated_hits_4c = [
        {"start": 100, "printed_page": 10, "match": "Hos 225", "snippet": "Hier ist ein Mischzitat aus Jesaja zu finden."},
        {"start": 200, "printed_page": 20, "match": "Hos 225", "snippet": "Hier ist ein Mischzitat aus Jesaja zu finden."},
        {"start": 300, "printed_page": 30, "match": "Hos 225", "snippet": "Hier ist ein Mischzitat aus Jesaja zu finden."},
    ]
    adj_4c = vns.adjudicate_target(
        target_def_b2, unrelated_hits_4c, {"passed": True}, ledger=valid_b2_ledger, pages=mock_pages, full_text=mock_full_text
    )
    assert adj_4c["passed"] is False
    assert adj_4c["classification"] == "HIT_WITNESS_PAGE_MISMATCH"
    assert "none intersect argument witness discussion loci" in adj_4c["summary"]

    # Case 4d (S05-R4-F1): Hits with contrary context ('wird von Paulus nicht diskutiert') fail adjudication
    contrary_hits_4d = [
        {"start": 100, "printed_page": 130, "match": "Hos 225", "snippet": "Hos 225 wird von Paulus nicht diskutiert."},
        {"start": 200, "printed_page": 130, "match": "Hos 225", "snippet": "Auszeichnungen verheißend zuspricht"},
        {"start": 300, "printed_page": 130, "match": "Hos 225", "snippet": "Erbarmensgefäße"},
    ]
    adj_4d = vns.adjudicate_target(
        target_def_b2, contrary_hits_4d, {"passed": True}, ledger=valid_b2_ledger, pages=mock_pages, full_text=mock_full_text
    )
    assert adj_4d["passed"] is False
    assert adj_4d["classification"] == "CONTRARY_CONTEXT_FOUND"
    assert "contrary context" in adj_4d["summary"]

    # Case 4e (S05-R4-F1): Single unrelated context hit among incidental hits (below min threshold) fails
    single_ctx_hits_4e = [
        {"start": 100, "printed_page": 10, "match": "Hos 225", "snippet": "Auszeichnungen verheißend zuspricht"},
        {"start": 200, "printed_page": 20, "match": "Hos 225", "snippet": "nur ein beiläufiger Verweis"},
        {"start": 300, "printed_page": 30, "match": "Hos 225", "snippet": "ein weiterer Verweis"},
    ]
    adj_4e = vns.adjudicate_target(
        target_def_b2, single_ctx_hits_4e, {"passed": True}, ledger=valid_b2_ledger, pages=mock_pages, full_text=mock_full_text
    )
    assert adj_4e["passed"] is False
    assert adj_4e["classification"] == "INSUFFICIENT_SUBSTANTIVE_HITS"
    assert "below required substantive threshold" in adj_4e["summary"]

    # Case 7b (S05-R4-F2): Authentic opening + fabricated suffix in short_quote fails page-bounded verification
    fab_suffix_ledger = {
        "S05-E001": {
            "evidence_id": "S05-E001",
            "b001_id": "B001-2",
            "verification_status": "VERIFIED",
            "printed_page": "130",
            "notebooklm_citation": "wilk [PDF p. 142; printed p. 130]",
            "source_locator": "Teil II.2.2a, S. 130",
            "short_quote": "Indem es Heiden diejenigen „Auszeichnungen“ verheißend zuspricht FABRICATED_SUFFIX_HERE",
            "author_claim": "Claim with fabricated suffix",
        }
    }
    adj_7b = vns.adjudicate_target(
        target_def_b2, substantive_hits, {"passed": True}, ledger=fab_suffix_ledger, pages=mock_pages, full_text=mock_full_text
    )
    assert adj_7b["passed"] is False
    assert adj_7b["classification"] == "EVIDENCE_LEDGER_MISMATCH"
    assert "fabricated suffix, altered Greek, or altered numeral" in adj_7b["summary"]

    # Case 7c (S05-R4-F2): Authentic quote attributed to wrong page fails
    wrong_page_ledger = {
        "S05-E001": {
            "evidence_id": "S05-E001",
            "b001_id": "B001-2",
            "verification_status": "VERIFIED",
            "printed_page": "131",
            "notebooklm_citation": "wilk [PDF p. 143; printed p. 131]",
            "source_locator": "Teil II.2.2a, S. 131",
            "short_quote": "Indem es Heiden diejenigen „Auszeichnungen“ verheißend zuspricht...",
            "author_claim": "Claim on wrong page",
        }
    }
    target_def_b2_p131 = dict(target_def_b2, expected_printed_pages=[131])
    adj_7c = vns.adjudicate_target(
        target_def_b2_p131, substantive_hits, {"passed": True}, ledger=wrong_page_ledger, pages=mock_pages, full_text=mock_full_text
    )
    assert adj_7c["passed"] is False
    assert adj_7c["classification"] == "EVIDENCE_LEDGER_MISMATCH"
    assert "not found on printed page 131" in adj_7c["summary"]

    # Case 7d (S05-R4-F2): Missing quotation or all-short-token quotation fails fail-closed
    short_token_ledger = {
        "S05-E001": {
            "evidence_id": "S05-E001",
            "b001_id": "B001-2",
            "verification_status": "VERIFIED",
            "printed_page": "130",
            "notebooklm_citation": "wilk [PDF p. 142; printed p. 130]",
            "source_locator": "Teil II.2.2a, S. 130",
            "short_quote": "a b c d",
            "author_claim": "Short token claim",
        }
    }
    adj_7d = vns.adjudicate_target(
        target_def_b2, substantive_hits, {"passed": True}, ledger=short_token_ledger, pages=mock_pages, full_text=mock_full_text
    )
    assert adj_7d["passed"] is False
    assert adj_7d["classification"] == "EVIDENCE_LEDGER_MISMATCH"
    assert "no qualifying tokens" in adj_7d["summary"]

    # Case 7e (S05-R5-F1): Authentic German with altered Greek tokens in quote fails page-bounded verification
    target_def_b4 = {
        "id": "B001-4",
        "name": "Romans 10:11 / Isaiah 28:16",
        "nt_target": "Rom 10:11",
        "ot_target": "Isa 28:16",
        "expected_classification": "SUBSTANTIVE_DISCUSSION",
        "evidence_ids": ["S05-E003"],
        "min_substantive_hits": 2,
        "expected_printed_pages": [45],
        "substantive_analytical_phrases": ["rein stilistische Modifikation", "von Futura durchzogene Umfeld"],
    }
    mock_b4_pages = ["Dummy\n"] * 100
    mock_b4_pages[57 - 1] = (
        "Die rein stilistische Modifikation — Paulus schreibt 'οὐ καταισχυνθήσεται' "
        "statt 'οὐ μὴ καταισχυνθῇ' — dürfte in dem Bestreben begründet sein, das Zitat "
        "in das von Futura durchzogene Umfeld einzupassen."
    )
    mock_b4_text = "\x0c".join(mock_b4_pages)
    altered_greek_ledger = {
        "S05-E003": {
            "evidence_id": "S05-E003",
            "b001_id": "B001-4",
            "verification_status": "VERIFIED",
            "printed_page": "45",
            "notebooklm_citation": "wilk [PDF p. 57; printed p. 45]",
            "source_locator": "Teil II.1.2.1.3a, S. 45",
            "short_quote": "Die rein stilistische Modifikation — Paulus schreibt 'λόγος' statt 'πνεῦμα' — dürfte in dem Bestreben begründet sein, das Zitat in das von Futura durchzogene Umfeld einzupassen.",
            "author_claim": "Altered Greek claim",
        }
    }
    b4_hits = [
        {"start": 100, "printed_page": 45, "match": "Rom 10:11", "snippet": "rein stilistische Modifikation im Umfeld"},
        {"start": 200, "printed_page": 45, "match": "Rom 10:11", "snippet": "von Futura durchzogene Umfeld"},
    ]
    adj_7e = vns.adjudicate_target(
        target_def_b4, b4_hits, {"passed": True}, ledger=altered_greek_ledger, pages=mock_b4_pages, full_text=mock_b4_text
    )
    assert adj_7e["passed"] is False
    assert adj_7e["classification"] == "EVIDENCE_LEDGER_MISMATCH"
    assert "fabricated suffix, altered Greek, or altered numeral" in adj_7e["summary"]

    # Case 7f (S05-R5-F1): Altered verse numeral in quote fails page-bounded verification
    mock_b6_pages = ["Dummy\n"] * 350
    mock_b6_pages[319 - 1] = (
        "Angesichts der schwachen Bezeugung von ἤ in der Tradition steht zu vermuten, "
        "daß Paulus es in Rom 1134, zur Angleichung an 1135, selbst eingefügt hat."
    )
    mock_b6_text = "\x0c".join(mock_b6_pages)
    target_def_b6 = {
        "id": "B001-6",
        "name": "Romans 11:34 / Isaiah 40:13",
        "nt_target": "Rom 11:34",
        "ot_target": "Isa 40:13",
        "expected_classification": "SUBSTANTIVE_DISCUSSION",
        "evidence_ids": ["S05-E006"],
        "min_substantive_hits": 2,
        "expected_printed_pages": [307],
        "substantive_analytical_phrases": ["schwachen Bezeugung", "steht zu vermuten"],
    }
    altered_num_ledger = {
        "S05-E006": {
            "evidence_id": "S05-E006",
            "b001_id": "B001-6",
            "verification_status": "VERIFIED",
            "printed_page": "307",
            "notebooklm_citation": "wilk [PDF p. 319; printed p. 307]",
            "source_locator": "Teil III.2.3.1b, S. 307 Anm. 23",
            "short_quote": "Angesichts der schwachen Bezeugung von ἤ in der Tradition steht zu vermuten, daß Paulus es in Rom 9999, zur Angleichung an 1135, selbst eingefügt hat.",
            "author_claim": "Altered numeral claim",
        }
    }
    b6_hits = [
        {"start": 100, "printed_page": 307, "match": "Rom 11:34", "snippet": "schwachen Bezeugung von in der Tradition"},
        {"start": 200, "printed_page": 307, "match": "Rom 11:34", "snippet": "steht zu vermuten daß Paulus"},
    ]
    adj_7f = vns.adjudicate_target(
        target_def_b6, b6_hits, {"passed": True}, ledger=altered_num_ledger, pages=mock_b6_pages, full_text=mock_b6_text
    )
    assert adj_7f["passed"] is False
    assert adj_7f["classification"] == "EVIDENCE_LEDGER_MISMATCH"
    assert "fabricated suffix, altered Greek, or altered numeral" in adj_7f["summary"]

    # Case 4f (S05-R5-F2): Same-page incidental citations with generic terms fail as INCIDENTAL_ONLY_HITS
    incidental_same_page_hits = [
        {"start": 100, "printed_page": 130, "match": "Hos 225", "snippet": "Hier wird Hos 225 zitiert ohne Analyse."},
        {"start": 200, "printed_page": 130, "match": "Hos 225", "snippet": "Ein weiterer beiläufiger Beleg für Hos 225."},
        {"start": 300, "printed_page": 130, "match": "Hos 225", "snippet": "Dritter beiläufiger Verweis auf Hos 225."},
    ]
    adj_4f = vns.adjudicate_target(
        target_def_b2, incidental_same_page_hits, {"passed": True}, ledger=valid_b2_ledger, pages=mock_pages, full_text=mock_full_text
    )
    assert adj_4f["passed"] is False
    assert adj_4f["classification"] == "INCIDENTAL_ONLY_HITS"
    assert "contain substantive scholarly context" in adj_4f["summary"]

    # Case 4g (S05-R5-F2): One local hit + two distant hits fails INSUFFICIENT_LOCAL_SUBSTANTIVE_HITS
    one_local_two_distant_hits = [
        {"start": 100, "printed_page": 130, "match": "Hos 225", "snippet": "Auszeichnungen verheißend zuspricht"},
        {"start": 200, "printed_page": 10, "match": "Hos 225", "snippet": "Auszeichnungen verheißend zuspricht"},
        {"start": 300, "printed_page": 20, "match": "Hos 225", "snippet": "Auszeichnungen verheißend zuspricht"},
    ]
    adj_4g = vns.adjudicate_target(
        target_def_b2, one_local_two_distant_hits, {"passed": True}, ledger=valid_b2_ledger, pages=mock_pages, full_text=mock_full_text
    )
    assert adj_4g["passed"] is False
    assert adj_4g["classification"] == "INSUFFICIENT_LOCAL_SUBSTANTIVE_HITS"
    assert "local substantive hits in discussion loci" in adj_4g["summary"]

    # Case 8a (S05-R5-F3): Inconsistent notebooklm_citation ([PDF p. 999; printed p. 130]) fails ledger integrity
    inconsistent_nlm_ledger = {
        "S05-E001": {
            "evidence_id": "S05-E001",
            "b001_id": "B001-2",
            "verification_status": "VERIFIED",
            "printed_page": "130",
            "notebooklm_citation": "wilk [PDF p. 999; printed p. 130]",
            "source_locator": "Teil II.2.2a, S. 130",
            "short_quote": "Indem es Heiden diejenigen „Auszeichnungen“ verheißend zuspricht...",
            "author_claim": "Claim with bad PDF locator",
        }
    }
    adj_8a = vns.adjudicate_target(
        target_def_b2, substantive_hits, {"passed": True}, ledger=inconsistent_nlm_ledger, pages=mock_pages, full_text=mock_full_text
    )
    assert adj_8a["passed"] is False
    assert adj_8a["classification"] == "EVIDENCE_LEDGER_MISMATCH"
    assert "offset formula +12" in adj_8a["summary"]

    # Case 8b (S05-R5-F3): Inconsistent source_locator (pointing to wrong page) fails ledger integrity
    inconsistent_loc_ledger = {
        "S05-E001": {
            "evidence_id": "S05-E001",
            "b001_id": "B001-2",
            "verification_status": "VERIFIED",
            "printed_page": "130",
            "notebooklm_citation": "wilk [PDF p. 142; printed p. 130]",
            "source_locator": "Teil II.2.2a, S. 999",
            "short_quote": "Indem es Heiden diejenigen „Auszeichnungen“ verheißend zuspricht...",
            "author_claim": "Claim with bad locator page",
        }
    }
    adj_8b = vns.adjudicate_target(
        target_def_b2, substantive_hits, {"passed": True}, ledger=inconsistent_loc_ledger, pages=mock_pages, full_text=mock_full_text
    )
    assert adj_8b["passed"] is False
    assert adj_8b["classification"] == "EVIDENCE_LEDGER_MISMATCH"
    assert "does not contain expected printed page 130" in adj_8b["summary"]

    # Case 8c (S05-R6-F3): Primary wrong page with secondary vgl. ('S. 999 (vgl. S. 130)') fails primary locator verification
    secondary_vgl_loc_ledger = {
        "S05-E001": {
            "evidence_id": "S05-E001",
            "b001_id": "B001-2",
            "verification_status": "VERIFIED",
            "printed_page": "130",
            "notebooklm_citation": "wilk [PDF p. 142; printed p. 130]",
            "source_locator": "Teil II.2.2a, S. 999 (vgl. S. 130)",
            "short_quote": "Indem es Heiden diejenigen „Auszeichnungen“ verheißend zuspricht...",
            "author_claim": "Claim with wrong primary page masked by secondary vgl.",
        }
    }
    adj_8c = vns.adjudicate_target(
        target_def_b2, substantive_hits, {"passed": True}, ledger=secondary_vgl_loc_ledger, pages=mock_pages, full_text=mock_full_text
    )
    assert adj_8c["passed"] is False
    assert adj_8c["classification"] == "EVIDENCE_LEDGER_MISMATCH"
    assert "primary source_locator" in adj_8c["summary"]

    # Case 7g (S05-R6-F1): Altered single-digit numbers fail page-bounded verbatim verification
    ok_7g, msg_7g, _ = vns.verify_page_bounded_quote(
        "Wilk treats chapter 1 and verse 2.", "Wilk treats chapter 9 and verse 8.", 1
    )
    assert ok_7g is False
    assert "complete verbatim sequence failed" in msg_7g

    # Case 7h (S05-R6-F1): Adjacent numeral insertion ('11134' vs '1134') fails page-bounded verbatim verification
    ok_7h, msg_7h, _ = vns.verify_page_bounded_quote(
        "Rom 1134 steht zu vermuten", "Rom 11134 steht zu vermuten", 1
    )
    assert ok_7h is False
    assert "complete verbatim sequence failed" in msg_7h

    # Case 7i (S05-R6-F1): Swapped critical Greek forms fail page-bounded verbatim verification
    ok_7i, msg_7i, _ = vns.verify_page_bounded_quote(
        "Paulus schreibt οὐ καταισχυνθήσεται statt οὐ μὴ καταισχυνθῇ.",
        "Paulus schreibt οὐ καταισχυνθῇ statt οὐ μὴ καταισχυνθήσεται.",
        45,
    )
    assert ok_7i is False
    assert "complete verbatim sequence failed" in msg_7i

    # Case 7j (S05-R6-F1): Swapped Greek OCR signatures fail page-bounded verbatim verification
    ok_7j, msg_7j, _ = vns.verify_page_bounded_quote(
        "Paulus schreibt οὐ καταισχυνθήσεται statt οὐ μὴ καταισχυνθῇ.",
        "Paulus schreibt οὐ xaTaiGvuVTTrj statt οὐ μὴ xaTaiov_uvv-f|GETat.",
        45,
    )
    assert ok_7j is False
    assert "complete verbatim sequence failed" in msg_7j

    # Case 7k (S05-R6-F1): Arbitrary OCR prefix ('xaTaiWRONG' / 'xaTaiOTHER') fails page-bounded verbatim verification
    ok_7k, msg_7k, _ = vns.verify_page_bounded_quote(
        "Paulus schreibt οὐ καταισχυνθήσεται statt οὐ μὴ καταισχυνθῇ.",
        "Paulus schreibt οὐ xaTaiWRONG statt οὐ μὴ xaTaiOTHER.",
        45,
    )
    assert ok_7k is False
    assert "complete verbatim sequence failed" in msg_7k

    # Case 4h (S05-R6-F2): Same-page hits containing multi-word phrase only in incidental bibliographic context fail
    incidental_bib_hits = [
        {"start": 100, "printed_page": 130, "match": "Rom 9,25", "snippet": "Vgl. Rom 9,25; siehe Miller (1990) S. 42: Auszeichnungen verheißend zuspricht."},
        {"start": 200, "printed_page": 130, "match": "Rom 9,25", "snippet": "Siehe Rom 9,25; vgl. Schmidt (1985) S. 12: Auszeichnungen verheißend zuspricht."},
        {"start": 300, "printed_page": 130, "match": "Rom 9,25", "snippet": "Literatur: Rom 9,25; vgl. Weber (1992) S. 88: Auszeichnungen verheißend zuspricht."},
    ]
    adj_4h = vns.adjudicate_target(
        target_def_b2, incidental_bib_hits, {"passed": True}, ledger=valid_b2_ledger, pages=mock_pages, full_text=mock_full_text
    )
    assert adj_4h["passed"] is False
    assert adj_4h["classification"] == "INCIDENTAL_ONLY_HITS"

    # Case 4i (S05-R7-F1): Reviewer exact counterexamples — author-year with parentheses BEFORE matched citation,
    # multi-line bibliographic lists, and incidental quotations containing configured analytical phrases MUST be detected
    # as incidental and rejected as INCIDENTAL_ONLY_HITS.
    ex1 = "Literatur: Müller (1990), Rom 9,25; Auszeichnungen verheißend zuspricht."
    ex2 = "Vgl. Weber (1992), Rom 9,25; Auszeichnungen verheißend zuspricht."
    ex3 = "Siehe dazu:\n  1. Schmidt [1988] S. 14;\n  2. Bauer (1994), Rom 9,25: „Auszeichnungen verheißend zuspricht“."
    assert vns.is_incidental_context(ex1, "Rom 9,25") is True
    assert vns.is_incidental_context(ex2, "Rom 9,25") is True
    assert vns.is_incidental_context(ex3, "Rom 9,25") is True

    author_year_before_citation_hits = [
        {"start": 100, "printed_page": 130, "match": "Rom 9,25", "snippet": ex1},
        {"start": 200, "printed_page": 130, "match": "Rom 9,25", "snippet": ex2},
        {"start": 300, "printed_page": 130, "match": "Rom 9,25", "snippet": ex3},
    ]
    adj_4i = vns.adjudicate_target(
        target_def_b2, author_year_before_citation_hits, {"passed": True}, ledger=valid_b2_ledger, pages=mock_pages, full_text=mock_full_text
    )
    assert adj_4i["passed"] is False
    assert adj_4i["classification"] == "INCIDENTAL_ONLY_HITS"

    # Case 4j (S05-R7-F2): Unauthenticated caller-provided hit offset/snippet on p. 130 fails authentication & binding
    spoofed_offset_hits = [
        {"start": 10, "printed_page": 130, "page_offset_start": 0, "page_offset_end": 8, "match": "Hos 225", "snippet": "Indem es Heiden diejenigen Auszeichnungen verheißend zuspricht, die Israel besaß"},
        {"start": 20, "printed_page": 130, "page_offset_start": 10, "page_offset_end": 18, "match": "Hos 225", "snippet": "Indem es Heiden diejenigen Auszeichnungen verheißend zuspricht, die Israel besaß"},
        {"start": 30, "printed_page": 130, "page_offset_start": 20, "page_offset_end": 28, "match": "Hos 225", "snippet": "Indem es Heiden diejenigen Auszeichnungen verheißend zuspricht, die Israel besaß"},
    ]
    adj_4j = vns.adjudicate_target(
        target_def_b2, spoofed_offset_hits, {"passed": True}, ledger=valid_b2_ledger, pages=mock_pages, full_text=mock_full_text
    )
    assert adj_4j["passed"] is False
    assert adj_4j["classification"] == "MANUAL_REVIEW_REQUIRED"

    # Case 4k (S05-R7-F2): Hit on same page p. 130 but far outside witness passage (distance > 500 chars) fails binding
    far_page_text = (
        "Indem es Heiden diejenigen 'Auszeichnungen' verheißend zuspricht, die Israel besaß und besitzt..."
        + (" XxxUnrelatedFillerText" * 40)
        + " Späterer Verweis auf Hos 225 mit Erbarmensgefäße am Seitenende."
    )
    mock_pages_far = list(mock_pages)
    mock_pages_far[141] = far_page_text
    far_pos = far_page_text.find("Hos 225")
    assert far_pos > 700
    distant_same_page_hits = [
        {"start": far_pos, "printed_page": 130, "page_offset_start": far_pos, "page_offset_end": far_pos + 7, "match": "Hos 225", "snippet": "Späterer Verweis auf Hos 225 mit Erbarmensgefäße am Seitenende."},
        {"start": far_pos, "printed_page": 130, "page_offset_start": far_pos, "page_offset_end": far_pos + 7, "match": "Hos 225", "snippet": "Späterer Verweis auf Hos 225 mit Erbarmensgefäße am Seitenende."},
        {"start": far_pos, "printed_page": 130, "page_offset_start": far_pos, "page_offset_end": far_pos + 7, "match": "Hos 225", "snippet": "Späterer Verweis auf Hos 225 mit Erbarmensgefäße am Seitenende."},
    ]
    adj_4k = vns.adjudicate_target(
        target_def_b2, distant_same_page_hits, {"passed": True}, ledger=valid_b2_ledger, pages=mock_pages_far, full_text="\x0c".join(mock_pages_far)
    )
    assert adj_4k["passed"] is False
    assert adj_4k["classification"] == "MANUAL_REVIEW_REQUIRED"

    # Case 4l (S05-R7-F2): Hit within 500 chars on same page but with zero semantic token overlap with witness quote fails binding
    wit_passage = "Indem es Heiden diejenigen 'Auszeichnungen' verheißend zuspricht, die Israel besaß. "
    filler_4l = " NeutralerKontext" * 25  # ~400 chars, distance <= 500 chars from witness
    no_overlap_page_text = (
        wit_passage
        + filler_4l
        + " Hos 225 nennt Erbarmensgefäße im Kontext."
    )
    mock_pages_no_ov = list(mock_pages)
    mock_pages_no_ov[141] = no_overlap_page_text
    pos_h = no_overlap_page_text.find("Hos 225")
    no_overlap_hits = [
        {"start": pos_h, "printed_page": 130, "page_offset_start": pos_h, "page_offset_end": pos_h + 7, "match": "Hos 225", "snippet": "Hos 225 nennt Erbarmensgefäße im Kontext."},
        {"start": pos_h, "printed_page": 130, "page_offset_start": pos_h, "page_offset_end": pos_h + 7, "match": "Hos 225", "snippet": "Hos 225 nennt Erbarmensgefäße im Kontext."},
        {"start": pos_h, "printed_page": 130, "page_offset_start": pos_h, "page_offset_end": pos_h + 7, "match": "Hos 225", "snippet": "Hos 225 nennt Erbarmensgefäße im Kontext."},
    ]
    adj_4l = vns.adjudicate_target(
        target_def_b2, no_overlap_hits, {"passed": True}, ledger=valid_b2_ledger, pages=mock_pages_no_ov, full_text="\x0c".join(mock_pages_no_ov)
    )
    assert adj_4l["passed"] is False
    assert adj_4l["classification"] == "MANUAL_REVIEW_REQUIRED"

    # Case 4m (S05-R7-F2): Report builder emits MANUAL_REVIEW_REQUIRED instead of VERIFIED_COMPLETE when any target fails
    failed_report = vns.build_markdown_report(
        search_results=[adj_4l],
        pos_results=[{"name": "pc", "pattern": "p", "expected_min": 1, "count": 1, "passed": True}],
        index_results={"passed": True, "positive_controls": {}, "missing_sections": [], "target_results": {}},
        pdf_path=Path("dummy.pdf"),
        pdf_bytes=vns.EXPECTED_RAW_PDF_BYTES,
        pdf_sha=vns.EXPECTED_RAW_PDF_SHA256,
        text_path=Path("dummy.txt"),
        text_sha=vns.EXPECTED_TEXT_SHA256,
        text_bytes=100,
        text_chars=100,
        text_lines=10,
        is_authenticated=True,
    )
    assert "Verification Status:** `MANUAL_REVIEW_REQUIRED`" in failed_report
    assert "Verification Status:** `VERIFIED_COMPLETE`" not in failed_report

    # Case 4n (S05-R8-F1): Valid citation offsets on p. 130 + fabricated snippet containing >50% real page words fails authentication
    fab_snip_4n = "Indem es Heiden diejenigen Auszeichnungen verheißend zuspricht Paulus und Erbarmensgefäße hier erfunden"
    p_pos_4n = mock_pages[141].find("Indem")
    fab_snippet_hits = [
        {"start": p_pos_4n, "printed_page": 130, "page_offset_start": p_pos_4n, "page_offset_end": p_pos_4n + 5, "match": "Indem", "snippet": fab_snip_4n},
        {"start": p_pos_4n, "printed_page": 130, "page_offset_start": p_pos_4n, "page_offset_end": p_pos_4n + 5, "match": "Indem", "snippet": fab_snip_4n},
        {"start": p_pos_4n, "printed_page": 130, "page_offset_start": p_pos_4n, "page_offset_end": p_pos_4n + 5, "match": "Indem", "snippet": fab_snip_4n},
    ]
    adj_4n = vns.adjudicate_target(
        target_def_b2, fab_snippet_hits, {"passed": True}, ledger=valid_b2_ledger, pages=mock_pages, full_text=mock_full_text
    )
    assert adj_4n["passed"] is False
    assert adj_4n["classification"] == "MANUAL_REVIEW_REQUIRED"
    assert "could not be authenticated and semantically bound" in adj_4n["summary"]

    # Case 4o (S05-R8-F1): Fail-closed behavior when pages is None or empty list
    ok_none, h_none, msg_none = vns.authenticate_hit({"printed_page": 130, "match": "Indem"}, pages=None)
    assert ok_none is False and h_none is None
    assert "unavailable" in msg_none.lower()

    ok_bind_none, b_none = vns.authenticate_and_bind_hit(
        {"printed_page": 130, "match": "Indem"}, pages=None, verified_witnesses=[]
    )
    assert ok_bind_none is False and b_none is None

    ok_empty, h_empty, msg_empty = vns.authenticate_hit({"printed_page": 130, "match": "Indem"}, pages=[])
    assert ok_empty is False and h_empty is None
    assert "unavailable" in msg_empty.lower()

    ok_bind_empty, b_empty = vns.authenticate_and_bind_hit(
        {"printed_page": 130, "match": "Indem"}, pages=[], verified_witnesses=[]
    )
    assert ok_bind_empty is False and b_empty is None

    # Case 4p (S05-R8-F2): Token integrity, bounded token equality, and threshold requirements
    # 1. Stopwords-only overlap fails binding
    wit_stopwords = {
        "evidence_id": "S05-E001",
        "printed_page": 130,
        "quote": "Paulus zitiert Heiden und Juden an dieser Stelle.",
        "author_claim": "Claim",
        "witnesses": [{"segment_index": 1, "page_offset_start": 10, "page_offset_end": 55, "matched_text": "Paulus zitiert Heiden und Juden"}]
    }
    p130_stopwords = "A" * 10 + "Paulus zitiert Heiden und Juden" + " " * 5 + "An dieser Stelle spricht der Apostel über Heiden und Juden." + "B" * 50
    pages_p = ["Dummy\n"] * 200
    pages_p[141] = p130_stopwords
    spricht_pos = p130_stopwords.find("spricht")
    hit_stopwords = {
        "printed_page": 130,
        "match": "spricht",
        "page_offset_start": spricht_pos,
        "page_offset_end": spricht_pos + len("spricht"),
    }
    ok_stop, b_stop = vns.authenticate_and_bind_hit(hit_stopwords, pages=pages_p, verified_witnesses=[wit_stopwords])
    assert ok_stop is False and b_stop is None

    # 2. Substring non-containment: witness has "mitteilen", hit page text has "Urteil" (shared substring "teil")
    wit_sub = {
        "evidence_id": "S05-E001",
        "printed_page": 130,
        "quote": "Wir müssen mitteilen",
        "author_claim": "Claim",
        "witnesses": [{"segment_index": 1, "page_offset_start": 10, "page_offset_end": 30, "matched_text": "Wir müssen mitteilen"}]
    }
    p130_sub = "A" * 10 + "Ein hartes Urteil folgt hier ganz deutlich." + "B" * 50
    pages_sub = ["Dummy\n"] * 200
    pages_sub[141] = p130_sub
    urteil_pos = p130_sub.find("Urteil")
    hit_sub = {
        "printed_page": 130,
        "match": "Urteil",
        "page_offset_start": urteil_pos,
        "page_offset_end": urteil_pos + len("Urteil"),
    }
    ok_sub, b_sub = vns.authenticate_and_bind_hit(hit_sub, pages=pages_sub, verified_witnesses=[wit_sub])
    assert ok_sub is False and b_sub is None

    # 3. Exactly 1 shared token of length 6 fails (< 2 tokens, length < 8)
    wit_single6 = {
        "evidence_id": "S05-E001",
        "printed_page": 130,
        "quote": "Hier fremde.",
        "author_claim": "Claim",
        "witnesses": [{"segment_index": 1, "page_offset_start": 10, "page_offset_end": 22, "matched_text": "Hier fremde."}]
    }
    p130_single6 = "A" * 10 + "Hier fremde." + " " * 5 + "Nur fremde Belege folgen." + "B" * 50
    pages_s6 = ["Dummy\n"] * 200
    pages_s6[141] = p130_single6
    fremde_pos = p130_single6.rfind("fremde")
    hit_s6 = {
        "printed_page": 130,
        "match": "fremde",
        "page_offset_start": fremde_pos,
        "page_offset_end": fremde_pos + len("fremde"),
    }
    ok_s6, b_s6 = vns.authenticate_and_bind_hit(hit_s6, pages=pages_s6, verified_witnesses=[wit_single6])
    assert ok_s6 is False and b_s6 is None

    # 4. Exactly 2 shared tokens of length 6 pass
    wit_two6 = {
        "evidence_id": "S05-E001",
        "printed_page": 130,
        "quote": "fremde stimme",
        "author_claim": "Claim",
        "witnesses": [{"segment_index": 1, "page_offset_start": 10, "page_offset_end": 23, "matched_text": "fremde stimme"}]
    }
    p130_two6 = "A" * 10 + "fremde stimme" + " " * 5 + "Eine fremde stimme folgt." + "B" * 50
    pages_t6 = ["Dummy\n"] * 200
    pages_t6[141] = p130_two6
    stimme_pos = p130_two6.rfind("stimme")
    hit_t6 = {
        "printed_page": 130,
        "match": "stimme",
        "page_offset_start": stimme_pos,
        "page_offset_end": stimme_pos + len("stimme"),
    }
    ok_t6, b_t6 = vns.authenticate_and_bind_hit(hit_t6, pages=pages_t6, verified_witnesses=[wit_two6])
    assert ok_t6 is True and b_t6 is not None

    # 5. Exactly 1 distinctive token of length >= 8 passes
    wit_one8 = {
        "evidence_id": "S05-E001",
        "printed_page": 130,
        "quote": "Auszeichnungen",
        "author_claim": "Claim",
        "witnesses": [{"segment_index": 1, "page_offset_start": 10, "page_offset_end": 24, "matched_text": "Auszeichnungen"}]
    }
    p130_one8 = "A" * 10 + "Auszeichnungen" + " " * 5 + "Neue Auszeichnungen folgen." + "B" * 50
    pages_o8 = ["Dummy\n"] * 200
    pages_o8[141] = p130_one8
    ausz_pos = p130_one8.rfind("Auszeichnungen")
    hit_o8 = {
        "printed_page": 130,
        "match": "Auszeichnungen",
        "page_offset_start": ausz_pos,
        "page_offset_end": ausz_pos + len("Auszeichnungen"),
    }
    ok_o8, b_o8 = vns.authenticate_and_bind_hit(hit_o8, pages=pages_o8, verified_witnesses=[wit_one8])
    assert ok_o8 is True and b_o8 is not None

    # Case 4q (S05-R9-F1): Correct citation offset paired with authentic but distant snippet (>1,000 chars away)
    # containing configured analytical terms fails local window alignment [-300..+450] and cannot open substantive gate.
    distant_filler = " UnrelatedFillerWord" * 70  # >1400 chars
    distant_phrase_4q = "Erbarmensgefäße und Auszeichnungen verheißend zuspricht."
    p130_distant_text = (
        "Hos 225                 "  # 0..24
        "Indem es Heiden diejenigen Auszeichnungen verheißend zuspricht."
        + distant_filler
        + " " + distant_phrase_4q
    )
    mock_pages_4q = list(mock_pages)
    mock_pages_4q[141] = p130_distant_text
    mock_text_4q = "\x0c".join(mock_pages_4q)

    # 1. Attacker supplies correct Hos 225 offset (0..7) on p. 130, but supplies the distant phrase as snippet
    hit_distant_snip = {
        "start": 0,
        "printed_page": 130,
        "page_offset_start": 0,
        "page_offset_end": 7,
        "match": "Hos 225",
        "snippet": distant_phrase_4q,
    }
    ok_dist, h_dist, msg_dist = vns.authenticate_hit(hit_distant_snip, mock_pages_4q)
    assert ok_dist is False
    assert h_dist is None
    assert "does not align with local text window" in msg_dist

    # 2. When passed to adjudicate_target, hits with distant snippets cannot open substantive gate
    distant_snippet_hits = [dict(hit_distant_snip) for _ in range(3)]
    adj_4q = vns.adjudicate_target(
        target_def_b2, distant_snippet_hits, {"passed": True}, ledger=valid_b2_ledger, pages=mock_pages_4q, full_text=mock_text_4q
    )
    assert adj_4q["passed"] is False
    assert adj_4q["classification"] == "MANUAL_REVIEW_REQUIRED"
    assert "could not be authenticated and semantically bound" in adj_4q["summary"]

    # 3. When caller provides NO snippet, derived_snippet is bounded to local window [0..457]
    # and does NOT contain analytical terms located only in the distant phrase (>1,400 chars away)
    hit_no_snip = {
        "start": 0,
        "printed_page": 130,
        "page_offset_start": 0,
        "page_offset_end": 7,
        "match": "Hos 225",
    }
    ok_derived, h_derived, _ = vns.authenticate_hit(hit_no_snip, mock_pages_4q)
    assert ok_derived is True
    assert "Erbarmensgefäße" not in h_derived["snippet"]

    # Case 4r (S05-R9-F2): Conflicting printed_page and caller-supplied pdf_page fails invariant enforcement
    hit_conflict_pdf = {
        "printed_page": 130,
        "pdf_page": 20,
        "page_offset_start": 0,
        "page_offset_end": 7,
        "match": "Hos 225",
    }
    ok_conf, h_conf, msg_conf = vns.authenticate_hit(hit_conflict_pdf, mock_pages)
    assert ok_conf is False
    assert h_conf is None
    assert "Contradictory pdf_page 20" in msg_conf

    ok_bind_conf, b_conf = vns.authenticate_and_bind_hit(
        hit_conflict_pdf, mock_pages, [{"evidence_id": "S05-E001", "printed_page": 130, "witnesses": []}]
    )
    assert ok_bind_conf is False
    assert b_conf is None

    adj_4r = vns.adjudicate_target(
        target_def_b2, [dict(hit_conflict_pdf) for _ in range(3)], {"passed": True}, ledger=valid_b2_ledger, pages=mock_pages, full_text=mock_full_text
    )
    assert adj_4r["passed"] is False


def test_s05_qualifications_and_locators_discipline():
    """
    S05-R2-M1 & S05-R2-L1 regression test:
    - Verifies S05-E006 preserves Wilk's qualified probabilistic judgment ('dürfte das Wort auf Paulus zurückgehen', p. 308)
      and labels it as secondary-author hypothesis.
    - Verifies S05-E008 preserves Wilk's explicit textual reservation (p. 238 n. 28) regarding a possible pre-Pauline Hebraizing Vorlage.
    - Verifies all 12 rows of citation_ledger.csv contain dual locators [PDF p. X; printed p. Y].
    - Verifies relevance_scan.md bounds Part V to pp. 381–408.
    """
    repo_root = Path(__file__).resolve().parent.parent
    s05_dir = repo_root / "research/inbox/B001-pauline-txt-pilot/sources/S05"

    # 1. Dual locators in citation_ledger.csv
    csv_path = s05_dir / "citation_ledger.csv"
    with open(csv_path, encoding="utf-8") as f:
        reader = list(csv.DictReader(f))
    assert len(reader) == 12

    locator_pattern = re.compile(r"\[PDF p\.\s*(\d+);\s*printed p\.\s*([^\]]+)\]")
    for row in reader:
        eid = row["evidence_id"]
        cit = row["notebooklm_citation"]
        m = locator_pattern.search(cit)
        assert m, f"Row {eid} missing dual locator format '[PDF p. X; printed p. Y]': {cit}"
        pdf_p = int(m.group(1))
        # Validate PDF = printed + 12 formula for integer printed pages
        first_printed = re.search(r"\d+", m.group(2))
        if first_printed:
            printed_num = int(first_printed.group(0))
            assert pdf_p == printed_num + 12, f"Row {eid} locator offset mismatch: PDF {pdf_p} != printed {printed_num} + 12"

    # 2. S05-E006 secondary-author hypothesis and probabilistic qualification (S05-R2-M1, S05-R3-M1 & S05-R4-F2)
    e006 = next(r for r in reader if r["evidence_id"] == "S05-E006")
    assert "secondary-author" in e006["qualification"].lower() or "secondary-author" in e006["author_claim"].lower()
    assert "steht zu vermuten" in e006["qualification"] or "steht zu vermuten" in e006["short_quote"]
    assert e006["printed_page"] == "307"
    assert "PDF p. 319" in e006["notebooklm_citation"]

    # 2b. S05-E007 page-bounded locator (S05-R4-F2)
    e007 = next(r for r in reader if r["evidence_id"] == "S05-E007")
    assert e007["printed_page"] == "397"
    assert "PDF p. 409" in e007["notebooklm_citation"]

    # 3. S05-E008 secondary-author hypothesis and textual reservation (S05-R2-M1)
    e008 = next(r for r in reader if r["evidence_id"] == "S05-E008")
    assert "secondary-author" in e008["qualification"].lower() or "secondary-author" in e008["author_claim"].lower()
    assert "238 n. 28" in e008["qualification"]
    assert "hebraizing" in e008["qualification"].lower() or "vorlage" in e008["qualification"].lower()

    # 4. relevance_scan.md bounds Part V to pp. 381–408 (S05-R2-L1)
    rel_path = s05_dir / "relevance_scan.md"
    rel_text = rel_path.read_text(encoding="utf-8")
    assert "381–408" in rel_text or "381-408" in rel_text
    assert "409–442" in rel_text or "409-442" in rel_text


def test_s05_digest_override_suppresses_certification(tmp_path, monkeypatch):
    """
    S05-R1-F4 regression test:
    Verifies that when text digest mismatches, canonical overwrite is refused (exit code 9),
    and report generation explicitly marks status as UNAUTHENTICATED_OVERRIDE and suppresses VERIFIED_COMPLETE.
    """
    import sys
    repo_root = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(repo_root / "scripts"))
    import verify_s05_negative_search as vns

    fake_pdf = tmp_path / "fake_wilk.pdf"
    fake_pdf.write_bytes(b"0" * vns.EXPECTED_RAW_PDF_BYTES)
    fake_text = tmp_path / "fake_wilk_text.txt"
    fake_text.write_text("Dummy extracted text\n" * 100, encoding="utf-8")
    noncanonical_out = tmp_path / "override_log.md"

    monkeypatch.setattr(vns, "get_sha256", lambda p: vns.EXPECTED_RAW_PDF_SHA256)

    def mock_subprocess_run(cmd, check=False):
        class SubprocessResult:
            returncode = 0
        return SubprocessResult()

    monkeypatch.setattr("subprocess.run", mock_subprocess_run)

    # Check 1: Refuses canonical path under unauthenticated override (exit code 9)
    ret_canon = vns.run_verification(
        pdf_path=fake_pdf,
        text_path=fake_text,
        out_path=vns.DEFAULT_OUT_PATH,
        allow_text_digest_mismatch=True,
        quiet=True,
    )
    assert ret_canon == 9, f"Expected exit code 9 for canonical overwrite under digest mismatch, got {ret_canon}"

    # Check 2: build_markdown_report with is_authenticated=False suppresses VERIFIED_COMPLETE
    report = vns.build_markdown_report(
        search_results=[],
        pos_results=[],
        index_results={},
        pdf_path=fake_pdf,
        pdf_bytes=vns.EXPECTED_RAW_PDF_BYTES,
        pdf_sha=vns.EXPECTED_RAW_PDF_SHA256,
        text_path=fake_text,
        text_sha="mismatched_sha",
        text_bytes=1000,
        text_chars=1000,
        text_lines=50,
        is_authenticated=False,
    )
    assert "Verification Status:** `UNAUTHENTICATED_OVERRIDE (Digest mismatch)`" in report
    assert "Verification Status:** `VERIFIED_COMPLETE`" not in report
    assert "Confirmed against authentic MDZ Digi20 scan" not in report
    assert "suppressed" in report.lower()


def test_s05_greek_script_integrity_and_confusables():
    """
    S05-R3-M1 regression test:
    Verifies that Greek transcriptions across narrative and ledger files are pure Greek
    (no Latin confusables like 'καταισchυνθῇ' or 'ἀθεteῖν').
    """
    repo_root = Path(__file__).resolve().parent.parent
    s05_dir = repo_root / "research/inbox/B001-pauline-txt-pilot/sources/S05"

    # 1. Check citation_ledger.csv
    ledger_path = s05_dir / "citation_ledger.csv"
    with open(ledger_path, encoding="utf-8") as f:
        reader = list(csv.DictReader(f))
    e003 = next(r for r in reader if r["evidence_id"] == "S05-E003")
    e010 = next(r for r in reader if r["evidence_id"] == "S05-E010")

    # Pure Greek assertions
    assert "καταισχυνθῇ" in e003["author_claim"]
    assert "καταισchυνθῇ" not in e003["author_claim"]
    assert "ἀθετεῖν" in e010["short_quote"]
    assert "ἀθεteῖν" not in e010["short_quote"]
    assert "läßt" in e010["short_quote"]

    # 2. Check extraction.md
    ext_path = s05_dir / "extraction.md"
    ext_text = ext_path.read_text(encoding="utf-8")
    assert "ἀθετεῖν" in ext_text
    assert "ἀθεteῖν" not in ext_text
    assert "καταισχυνθῇ" in ext_text
    assert "καταισchυνθῇ" not in ext_text
    assert "steht zu vermuten" in ext_text

    # 3. Confusable detector: check that no Latin letters are embedded inside Greek words
    confusable_pat = re.compile(r"[\u0370-\u03ff\u1f00-\u1fff]+[a-zA-Z]+[\u0370-\u03ff\u1f00-\u1fff]+")
    matches = confusable_pat.findall(ext_text)
    assert not matches, f"Corrupted mixed-script confusable found: {matches}"


def test_s06f_citation_ledger_crosswalk_integrity():
    """Verify S06F citation ledger schema, pagination mapping, and quote integrity."""
    repo_root = Path(__file__).resolve().parent.parent
    s06f_dir = repo_root / "research/inbox/B001-pauline-txt-pilot/sources/S06F"
    csv_path = s06f_dir / "citation_ledger.csv"

    assert csv_path.is_file(), f"Missing citation_ledger.csv at {csv_path}"
    with open(csv_path, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    assert len(rows) == 9, f"Expected 9 ledger rows for S06F, found {len(rows)}"

    for r in rows:
        eid = r["evidence_id"]
        assert r["source_id"] == "S06F"
        assert r["verification_status"] == "VERIFIED"
        assert r["extraction_confidence"] == "HIGH"
        assert len(r["short_quote"].strip()) > 10

        printed = int(r["printed_page"])
        expected_pdf = printed - 94
        assert expected_pdf >= 1 and expected_pdf <= 22, f"Invalid printed page {printed} for {eid}"
        assert f"PDF p. {expected_pdf}; printed p. {printed}" in r["notebooklm_citation"]


def test_s06f_provenance_manifest_and_pagination_invariant():
    """Verify S06F provenance manifest and pagination invariant."""
    repo_root = Path(__file__).resolve().parent.parent
    manifest_path = repo_root / "research/inbox/B001-pauline-txt-pilot/sources/S06F/provenance_manifest.json"
    assert manifest_path.is_file(), f"Missing manifest at {manifest_path}"

    with open(manifest_path, encoding="utf-8") as f:
        manifest = json.load(f)

    assert manifest["source_id"] == "S06F"
    assert manifest["work"]["authors"] == ["Mireia Ryšková"]
    assert manifest["work"]["doi"] == "10.14712/23363398.2020.8"
    assert manifest["ingested_volume"]["size_bytes"] == 201323
    assert manifest["ingested_volume"]["pages"] == 22
    assert manifest["ingested_volume"]["sha256"] == "ae823536b0ac41a9b24bce0671cb083f350b4384ed97803bbe089d4564a8f0c7"


def test_s06f_negative_search_verification():
    """Verify S06F negative search verification script passes with clean exit code."""
    import subprocess
    import sys
    repo_root = Path(__file__).resolve().parent.parent
    script_path = repo_root / "scripts/verify_s06f_negative_search.py"
    res = subprocess.run(
        [sys.executable, str(script_path), "--check-only"],
        cwd=str(repo_root),
        capture_output=True,
        text=True
    )
    assert res.returncode == 0, f"verify_s06f_negative_search failed:\n{res.stderr}\n{res.stdout}"


def test_s06f_adversarial_quote_witness_tail_mutation_fails_closed():
    """Verify that quote witness verification authenticates the ENTIRE quote, failing closed on tail mutations after char 60."""
    import sys
    import pytest
    repo_root = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(repo_root))
    from scripts.verify_s06f_negative_search import (
        extract_page_texts,
        load_evidence_ledger,
        verify_ledger_witnesses,
        PDF_DEFAULT,
        DEFAULT_LEDGER_PATH
    )

    page_texts = extract_page_texts(PDF_DEFAULT)
    rows = load_evidence_ledger(DEFAULT_LEDGER_PATH)

    # Pick S06F-E001 (quote length 134 chars)
    e001_quote = rows[0]["short_quote"]
    assert len(e001_quote) > 80

    mutations = [
        # Negation after char 60
        e001_quote[:60] + " but not in Christ or God.",
        # Greek tokens after char 60
        e001_quote[:60] + " (πᾶς οὐ μὴ καταισχυνθῇ).",
        # Numerical reference after char 60
        e001_quote[:60] + " in chapter 99 verse 100.",
        # Arbitrary fabricated tail
        e001_quote[:60] + " fabricated ending that does not occur on the page.",
    ]

    for mutated_quote in mutations:
        test_rows = [dict(r) for r in rows]
        test_rows[0]["short_quote"] = mutated_quote
        with pytest.raises(ValueError) as excinfo:
            verify_ledger_witnesses(test_rows, page_texts)
        assert "entire normalized quote not found" in str(excinfo.value)


def test_s06f_check_only_detects_tampered_search_log(tmp_path):
    """Verify that --check-only compares exact bytes and fails closed on semantic or whitespace tampering."""
    import subprocess
    import sys
    repo_root = Path(__file__).resolve().parent.parent
    script_path = repo_root / "scripts/verify_s06f_negative_search.py"
    committed_log = repo_root / "research/inbox/B001-pauline-txt-pilot/sources/S06F/full_volume_search_log.md"
    assert committed_log.is_file()

    # Tampering test cases
    tampering_cases = [
        # Alter category
        ("`SUBSTANTIVE_DISCUSSION`", "`PASSING_MENTION`"),
        # Alter locator
        ("[PDF p. 12; printed p. 106]", "[PDF p. 99; printed p. 199]"),
        # Alter claim
        ("universal availability of salvation", "restricted salvation only for few"),
        # Terminal whitespace tampering (S06F-R2-F3: byte-for-byte exactness)
        (None, "trailing_newline"),
        (None, "trailing_space"),
    ]

    for original, tampered in tampering_cases:
        content = committed_log.read_text(encoding="utf-8")
        if original is not None:
            assert original in content, f"Target string '{original}' not found in committed log"
            tampered_content = content.replace(original, tampered, 1)
        elif tampered == "trailing_newline":
            tampered_content = content + "\n"
        elif tampered == "trailing_space":
            tampered_content = content + " "

        tampered_file = tmp_path / "tampered_log.md"
        tampered_file.write_text(tampered_content, encoding="utf-8")

        res = subprocess.run(
            [sys.executable, str(script_path), "--check-only", "--out", str(tampered_file)],
            cwd=str(repo_root),
            capture_output=True,
            text=True
        )
        assert res.returncode != 0, f"Expected non-zero exit for tampering '{original}' -> '{tampered}'"
        assert "does not match computed output" in res.stdout or "does not match computed output" in res.stderr


def test_s06f_ledger_schema_and_verification_assertions_fail_closed(tmp_path):
    """Verify that verifier asserts ledger schema, expected IDs, and VERIFIED statuses."""
    import pytest
    import sys
    repo_root = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(repo_root))
    from scripts.verify_s06f_negative_search import load_evidence_ledger, DEFAULT_LEDGER_PATH

    # Valid load
    valid_rows = load_evidence_ledger(DEFAULT_LEDGER_PATH)
    assert len(valid_rows) == 9

    # 1. Missing column
    bad_csv = tmp_path / "bad_col.csv"
    bad_csv.write_text("evidence_id,source_id,author_claim\nS06F-E001,S06F,claim\n", encoding="utf-8")
    with pytest.raises(ValueError) as exc:
        load_evidence_ledger(bad_csv)
    assert "Missing required column" in str(exc.value)

    # 2. Missing ID / wrong count
    bad_id_csv = tmp_path / "bad_id.csv"
    with open(DEFAULT_LEDGER_PATH, encoding="utf-8") as f:
        lines = f.readlines()
    bad_id_csv.write_text("".join(lines[:5]), encoding="utf-8")  # only 4 rows
    with pytest.raises(ValueError) as exc:
        load_evidence_ledger(bad_id_csv)
    assert "Expected 9 evidence rows" in str(exc.value)

    # 3. Unverified status
    unverified_csv = tmp_path / "unverified.csv"
    unverified_lines = [l.replace("VERIFIED", "PENDING_REVIEW") if "S06F-E001" in l else l for l in lines]
    unverified_csv.write_text("".join(unverified_lines), encoding="utf-8")
    with pytest.raises(ValueError) as exc:
        load_evidence_ledger(unverified_csv)
    assert "unverified status" in str(exc.value)


def test_s06f_cross_artifact_consistency_fails_on_debris_or_bad_loci(tmp_path):
    """Verify that cross-artifact check catches UI debris, natural-format wrong locators, and missing footnote witnesses."""
    import pytest
    import shutil
    import sys
    repo_root = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(repo_root))
    from scripts.verify_s06f_negative_search import verify_cross_artifact_consistency, DEFAULT_SOURCE_DIR

    # Valid check passes
    verify_cross_artifact_consistency(DEFAULT_SOURCE_DIR)

    # Copy files to temp dir
    temp_sources = tmp_path / "sources_test"
    shutil.copytree(DEFAULT_SOURCE_DIR, temp_sources)

    # 1. Test UI debris detection
    target_md = temp_sources / "metadata.md"
    orig_text = target_md.read_text(encoding="utf-8")
    target_md.write_text(orig_text + "\nexpand_more\n", encoding="utf-8")
    with pytest.raises(ValueError) as exc:
        verify_cross_artifact_consistency(temp_sources)
    assert "UI debris 'expand_more' found" in str(exc.value)
    target_md.write_text(orig_text, encoding="utf-8")

    # 2. Test natural-format wrong printed page in extraction.md for S06F-E001 (Printed p. 104 [PDF p. 10])
    extr_md = temp_sources / "extraction.md"
    orig_extr = extr_md.read_text(encoding="utf-8")
    extr_md.write_text(orig_extr.replace("Printed p. 106 [PDF p. 12]", "Printed p. 104 [PDF p. 10]", 1), encoding="utf-8")
    with pytest.raises(ValueError) as exc:
        verify_cross_artifact_consistency(temp_sources)
    assert "Locus mismatch for S06F-E001" in str(exc.value)
    extr_md.write_text(orig_extr, encoding="utf-8")

    # 3. Test natural-format wrong PDF page in extraction.md for S06F-E001 (Printed p. 106 [PDF p. 99])
    extr_md.write_text(orig_extr.replace("Printed p. 106 [PDF p. 12]", "Printed p. 106 [PDF p. 99]", 1), encoding="utf-8")
    with pytest.raises(ValueError) as exc:
        verify_cross_artifact_consistency(temp_sources)
    assert "Invariant violated in locator" in str(exc.value) or "Locus mismatch for S06F-E001" in str(exc.value)
    extr_md.write_text(orig_extr, encoding="utf-8")

    # 4. Test natural-format wrong locator for Rom 11:34 (S06F-E006)
    extr_md.write_text(orig_extr.replace("Printed p. 112 [PDF p. 18]", "Printed p. 108 [PDF p. 14]", 1), encoding="utf-8")
    with pytest.raises(ValueError) as exc:
        verify_cross_artifact_consistency(temp_sources)
    assert "Locus mismatch for S06F-E006" in str(exc.value)
    extr_md.write_text(orig_extr, encoding="utf-8")

    # 5. Test natural-format wrong locator in isaiah_in_romans_synthesis.md for Addition of πᾶς
    synth_md = temp_sources / "isaiah_in_romans_synthesis.md"
    orig_synth = synth_md.read_text(encoding="utf-8")
    synth_md.write_text(orig_synth.replace("Printed p. 106 [PDF p. 12]", "Printed p. 104 [PDF p. 10]", 1), encoding="utf-8")
    with pytest.raises(ValueError) as exc:
        verify_cross_artifact_consistency(temp_sources)
    assert "Wrong locus for subsection 'Addition of πᾶς'" in str(exc.value)
    synth_md.write_text(orig_synth, encoding="utf-8")

    # 6. Test natural-format wrong locator in relevance_scan.md for B001-2
    rel_md = temp_sources / "relevance_scan.md"
    orig_rel = rel_md.read_text(encoding="utf-8")
    rel_md.write_text(orig_rel.replace("Printed p. 104 [PDF p. 10]", "Printed p. 101 [PDF p. 7]", 1), encoding="utf-8")
    with pytest.raises(ValueError) as exc:
        verify_cross_artifact_consistency(temp_sources)
    assert "Wrong locus for B001-2" in str(exc.value)
    rel_md.write_text(orig_rel, encoding="utf-8")

    # 7. Test missing positive footnote witness in bibliography_leads.md
    bib_md = temp_sources / "bibliography_leads.md"
    orig_bib = bib_md.read_text(encoding="utf-8")
    bib_md.write_text(orig_bib.replace("Printed p. 99 [PDF p. 5], fn. 14", "Printed p. 97 [PDF p. 3], fn. 14"), encoding="utf-8")
    with pytest.raises(ValueError) as exc:
        verify_cross_artifact_consistency(temp_sources)
    assert "Missing positive footnote witness" in str(exc.value)
    bib_md.write_text(orig_bib, encoding="utf-8")


def test_s06f_section_boundary_escape_and_range_bounds_fail_closed(tmp_path):
    """Adversarial regression tests for S06F-R2-F2 (section boundary escape) and S06F-R3-F1 (locator range bounds)."""
    import pytest
    import shutil
    import sys
    repo_root = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(repo_root))
    from scripts.verify_s06f_negative_search import verify_cross_artifact_consistency, DEFAULT_SOURCE_DIR

    # Valid check passes
    verify_cross_artifact_consistency(DEFAULT_SOURCE_DIR)

    temp_sources = tmp_path / "sources_boundary_test"
    shutil.copytree(DEFAULT_SOURCE_DIR, temp_sources)

    # Counterexample A: Delete locator from S06F-E001 in extraction.md
    # Must fail closed on E001 and NOT silently match E002 sharing page 106/12
    extr_path = temp_sources / "extraction.md"
    orig_extr = extr_path.read_text(encoding="utf-8")
    mutated_extr = orig_extr.replace("- **Source Locator:** Printed p. 106 [PDF p. 12]; Section 6 (Rom 10:11)\n", "", 1)
    extr_path.write_text(mutated_extr, encoding="utf-8")
    with pytest.raises(ValueError) as exc:
        verify_cross_artifact_consistency(temp_sources)
    assert "extraction.md: Missing Source Locator line for S06F-E001" in str(exc.value)
    extr_path.write_text(orig_extr, encoding="utf-8")

    # Duplicate locator in extraction.md section S06F-E001 fails closed
    dup_extr = orig_extr.replace(
        "- **Source Locator:** Printed p. 106 [PDF p. 12]; Section 6 (Rom 10:11)",
        "- **Source Locator:** Printed p. 106 [PDF p. 12]; Section 6 (Rom 10:11)\n- **Source Locator:** Printed p. 106 [PDF p. 12]; Section 6 (Rom 10:11)",
        1
    )
    extr_path.write_text(dup_extr, encoding="utf-8")
    with pytest.raises(ValueError) as exc:
        verify_cross_artifact_consistency(temp_sources)
    assert "extraction.md: Duplicate Source Locator line for S06F-E001" in str(exc.value)
    extr_path.write_text(orig_extr, encoding="utf-8")

    # Counterexample B: Delete locator from 'Addition of πᾶς' in isaiah_in_romans_synthesis.md
    # Must fail closed on subsection and NOT silently match following subsection sharing page 106/12
    synth_path = temp_sources / "isaiah_in_romans_synthesis.md"
    orig_synth = synth_path.read_text(encoding="utf-8")
    mutated_synth = orig_synth.replace("  - **Source Locator:** Printed p. 106 [PDF p. 12]; Section 6 (Rom 10:11)\n", "", 1)
    synth_path.write_text(mutated_synth, encoding="utf-8")
    with pytest.raises(ValueError) as exc:
        verify_cross_artifact_consistency(temp_sources)
    assert "isaiah_in_romans_synthesis.md: Missing Source Locator in subsection 'Addition of πᾶς'" in str(exc.value)
    synth_path.write_text(orig_synth, encoding="utf-8")

    # Duplicate locator in synthesis subsection fails closed
    dup_synth = orig_synth.replace(
        "  - **Source Locator:** Printed p. 106 [PDF p. 12]; Section 6 (Rom 10:11)",
        "  - **Source Locator:** Printed p. 106 [PDF p. 12]; Section 6 (Rom 10:11)\n  - **Source Locator:** Printed p. 106 [PDF p. 12]; Section 6 (Rom 10:11)",
        1
    )
    synth_path.write_text(dup_synth, encoding="utf-8")
    with pytest.raises(ValueError) as exc:
        verify_cross_artifact_consistency(temp_sources)
    assert "isaiah_in_romans_synthesis.md: Duplicate Source Locator in subsection 'Addition of πᾶς'" in str(exc.value)
    synth_path.write_text(orig_synth, encoding="utf-8")

    # Counterexample C: Replace B001-2 locator with N/A in relevance_scan.md table
    # Must fail closed on B001-2 and NOT silently match B001-3 sharing page 104/10
    rel_path = temp_sources / "relevance_scan.md"
    orig_rel = rel_path.read_text(encoding="utf-8")
    mutated_rel = orig_rel.replace("| Printed p. 104 [PDF p. 10] |", "| N/A |", 1)
    rel_path.write_text(mutated_rel, encoding="utf-8")
    with pytest.raises(ValueError) as exc:
        verify_cross_artifact_consistency(temp_sources)
    assert "relevance_scan.md: Malformed or missing single-page locator for B001-2: 'N/A'" in str(exc.value)
    rel_path.write_text(orig_rel, encoding="utf-8")

    # Counterexample D (S06F-R3-F1 Range Bounds): Append out-of-bounds end page range to argument_map.md
    arg_path = temp_sources / "argument_map.md"
    orig_arg = arg_path.read_text(encoding="utf-8")
    arg_path.write_text(orig_arg + "\nPrinted pp. 105–200 [PDF pp. 11–106]\n", encoding="utf-8")
    with pytest.raises(ValueError) as exc:
        verify_cross_artifact_consistency(temp_sources)
    assert "Out of bounds range end in locator 'Printed pp. 105–200 [PDF pp. 11–106]'" in str(exc.value)
    arg_path.write_text(orig_arg, encoding="utf-8")

    # Counterexample E (S06F-R3-F1 Inverted Range): Inverted page range in argument_map.md fails closed
    arg_path.write_text(orig_arg + "\nPrinted pp. 114–105 [PDF pp. 20–11]\n", encoding="utf-8")
    with pytest.raises(ValueError) as exc:
        verify_cross_artifact_consistency(temp_sources)
    assert "Inverted page range in locator 'Printed pp. 114–105 [PDF pp. 20–11]'" in str(exc.value)
    arg_path.write_text(orig_arg, encoding="utf-8")

    # Counterexample F (S06F-R3-F1 Half-range): Half-range locator in argument_map.md fails closed
    arg_path.write_text(orig_arg + "\nPrinted pp. 105–106 [PDF p. 11]\n", encoding="utf-8")
    with pytest.raises(ValueError) as exc:
        verify_cross_artifact_consistency(temp_sources)
    assert "Malformed half-range locator 'Printed pp. 105–106 [PDF p. 11]'" in str(exc.value)
    arg_path.write_text(orig_arg, encoding="utf-8")


def test_s07f_citation_ledger_crosswalk_integrity():
    """Verify S07F citation ledger schema, evidence IDs, and locators."""
    repo_root = Path(__file__).resolve().parent.parent
    s07f_dir = repo_root / "research/inbox/B001-pauline-txt-pilot/sources/S07F"
    csv_path = s07f_dir / "citation_ledger.csv"

    assert csv_path.is_file(), f"Missing S07F citation ledger: {csv_path}"

    with open(csv_path, encoding="utf-8") as f:
        reader = list(csv.DictReader(f))

    assert len(reader) == 9, f"Expected 9 ledger rows for S07F, found {len(reader)}"

    expected_ids = [f"S07F-E00{i}" for i in range(1, 10)]
    for idx, row in enumerate(reader):
        eid = row["evidence_id"]
        assert eid == expected_ids[idx], f"Expected {expected_ids[idx]}, got {eid}"
        assert row["source_id"] == "S07F"
        assert row["verification_status"] == "VERIFIED"
        assert row["short_quote"], f"Missing short quote for {eid}"
        assert row["author_claim"], f"Missing author claim for {eid}"
        assert row["source_locator"], f"Missing source locator for {eid}"
        if "-" in row["printed_page"]:
            p_start, p_end = [int(x) for x in row["printed_page"].split("-")]
            m = re.search(r"Printed pp\.\s*(\d+)[–-](\d+)", row["source_locator"])
            assert m, f"Locator format mismatch for range in {row['source_locator']}"
            assert p_start == int(m.group(1))
            assert p_end == int(m.group(2))
        else:
            assert int(row["printed_page"]) == int(re.search(r"Printed p\.\s*(\d+)", row["source_locator"]).group(1))


def test_s07f_verifier_negative_search_passes():
    """Verify scripts/verify_s07f_negative_search.py passes in --check-only mode."""
    import subprocess
    repo_root = Path(__file__).resolve().parent.parent
    verifier_script = repo_root / "scripts/verify_s07f_negative_search.py"
    assert verifier_script.is_file(), f"Missing verifier script: {verifier_script}"

    cmd = ["python3", str(verifier_script), "--check-only"]
    res = subprocess.run(cmd, cwd=str(repo_root), capture_output=True, text=True)
    assert res.returncode == 0, f"Verifier failed with return code {res.returncode}:\nStdout:\n{res.stdout}\nStderr:\n{res.stderr}"
    assert "matches generated report byte-for-byte (--check-only passed)" in res.stdout


def test_s07f_section_boundary_escape_and_range_bounds_fail_closed(tmp_path):
    """Verify S07F fails closed on section-boundary escape, duplicate locators, and range bound violations."""
    import shutil
    import sys
    import pytest
    repo_root = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(repo_root))
    from scripts.verify_s07f_negative_search import verify_cross_artifact_consistency
    s07f_dir = repo_root / "research/inbox/B001-pauline-txt-pilot/sources/S07F"

    temp_sources = tmp_path / "S07F"
    shutil.copytree(s07f_dir, temp_sources)

    # Base state must pass
    verify_cross_artifact_consistency(temp_sources)

    # Counterexample A: Delete locator from S07F-E001 in extraction.md
    extr_path = temp_sources / "extraction.md"
    orig_extr = extr_path.read_text(encoding="utf-8")
    mutated_extr = orig_extr.replace("- **Source Locator:** Printed p. 239 [PDF p. 1]; Section 1\n", "", 1)
    extr_path.write_text(mutated_extr, encoding="utf-8")
    with pytest.raises(ValueError) as exc:
        verify_cross_artifact_consistency(temp_sources)
    assert "extraction.md: Missing Source Locator line for S07F-E001" in str(exc.value)
    extr_path.write_text(orig_extr, encoding="utf-8")

    # Duplicate locator in extraction.md section S07F-E001 fails closed
    dup_extr = orig_extr.replace(
        "- **Source Locator:** Printed p. 239 [PDF p. 1]; Section 1",
        "- **Source Locator:** Printed p. 239 [PDF p. 1]; Section 1\n- **Source Locator:** Printed p. 239 [PDF p. 1]; Section 1",
        1
    )
    extr_path.write_text(dup_extr, encoding="utf-8")
    with pytest.raises(ValueError) as exc:
        verify_cross_artifact_consistency(temp_sources)
    assert "extraction.md: Duplicate Source Locator line for S07F-E001" in str(exc.value)
    extr_path.write_text(orig_extr, encoding="utf-8")

    # Counterexample B: Delete locator from synthesis subsection
    synth_path = temp_sources / "paulus_schriftuitlegger_synthesis.md"
    orig_synth = synth_path.read_text(encoding="utf-8")
    mutated_synth = orig_synth.replace("  - **Source Locator:** Printed p. 239 [PDF p. 1]; Section 1\n", "", 1)
    synth_path.write_text(mutated_synth, encoding="utf-8")
    with pytest.raises(ValueError) as exc:
        verify_cross_artifact_consistency(temp_sources)
    assert "paulus_schriftuitlegger_synthesis.md: Missing Source Locator in subsection 'Paul's Use and Citation in Romans 4:3'" in str(exc.value)
    synth_path.write_text(orig_synth, encoding="utf-8")

    # Duplicate locator in synthesis subsection fails closed
    dup_synth = orig_synth.replace(
        "  - **Source Locator:** Printed p. 239 [PDF p. 1]; Section 1",
        "  - **Source Locator:** Printed p. 239 [PDF p. 1]; Section 1\n  - **Source Locator:** Printed p. 239 [PDF p. 1]; Section 1",
        1
    )
    synth_path.write_text(dup_synth, encoding="utf-8")
    with pytest.raises(ValueError) as exc:
        verify_cross_artifact_consistency(temp_sources)
    assert "paulus_schriftuitlegger_synthesis.md: Duplicate Source Locator in subsection 'Paul's Use and Citation in Romans 4:3'" in str(exc.value)
    synth_path.write_text(orig_synth, encoding="utf-8")

    # Counterexample C: Mutate table row in relevance_scan.md
    rel_path = temp_sources / "relevance_scan.md"
    orig_rel = rel_path.read_text(encoding="utf-8")
    mutated_rel = orig_rel.replace("| Printed p. 248 [PDF p. 10] |", "| N/A |", 1)
    rel_path.write_text(mutated_rel, encoding="utf-8")
    with pytest.raises(ValueError) as exc:
        verify_cross_artifact_consistency(temp_sources)
    assert "relevance_scan.md: Malformed or missing single-page locator for B001-4: 'N/A'" in str(exc.value)
    rel_path.write_text(orig_rel, encoding="utf-8")

    # Counterexample D: Out of bounds end page range in argument_map.md fails closed
    arg_path = temp_sources / "argument_map.md"
    orig_arg = arg_path.read_text(encoding="utf-8")
    arg_path.write_text(orig_arg + "\nPrinted pp. 240–300 [PDF pp. 2–62]\n", encoding="utf-8")
    with pytest.raises(ValueError) as exc:
        verify_cross_artifact_consistency(temp_sources)
    assert "Out of bounds range end in locator 'Printed pp. 240–300 [PDF pp. 2–62]'" in str(exc.value)
    arg_path.write_text(orig_arg, encoding="utf-8")

    # Counterexample E: Inverted range in argument_map.md fails closed
    arg_path.write_text(orig_arg + "\nPrinted pp. 250–240 [PDF pp. 12–2]\n", encoding="utf-8")
    with pytest.raises(ValueError) as exc:
        verify_cross_artifact_consistency(temp_sources)
    assert "Inverted page range in locator 'Printed pp. 250–240 [PDF pp. 12–2]'" in str(exc.value)
    arg_path.write_text(orig_arg, encoding="utf-8")

    # Counterexample F: Half-range in argument_map.md fails closed
    arg_path.write_text(orig_arg + "\nPrinted pp. 240–245 [PDF p. 2]\n", encoding="utf-8")
    with pytest.raises(ValueError) as exc:
        verify_cross_artifact_consistency(temp_sources)
    assert "Malformed half-range locator 'Printed pp. 240–245 [PDF p. 2]'" in str(exc.value)
    arg_path.write_text(orig_arg, encoding="utf-8")

    # Counterexample G: Single page when range expected for S07F-E009 in extraction.md fails closed
    mutated_e009 = orig_extr.replace(
        "- **Source Locator:** Printed pp. 252–253 [PDF pp. 14–15]; Section 5",
        "- **Source Locator:** Printed p. 253 [PDF p. 15]; Section 5",
        1
    )
    extr_path.write_text(mutated_e009, encoding="utf-8")
    with pytest.raises(ValueError) as exc:
        verify_cross_artifact_consistency(temp_sources)
    assert "extraction.md: Expected range for S07F-E009, got single page in '- **Source Locator:** Printed p. 253 [PDF p. 15]; Section 5'" in str(exc.value)
    extr_path.write_text(orig_extr, encoding="utf-8")


def test_s07f_adversarial_pagination_and_negative_search_assertions():
    """Verify S07F verifier assertions fail closed against adversarial mutations (S07F-R1-F4)."""
    import pytest
    from scripts.verify_s07f_negative_search import (
        verify_monotonic_pagination,
        execute_full_volume_search,
        verify_ledger_witnesses,
    )

    # 1. Body-only numeral counterexample: '239' embedded in prose, NO standalone page numeral line
    mock_body_only_pages = [
        "Paulus als Schriftuitlegger\nThis line mentions 239 inside a prose sentence.\nIn die Skriflig 39(2) 2005:239-254\n"
    ]
    with pytest.raises(ValueError) as exc1:
        verify_monotonic_pagination(mock_body_only_pages)
    assert "expected standalone printed page number '239' not found as an isolated line" in str(exc1.value)

    # 1b. Reviewer deterministic counterexample (S07F-R2-F2): isolated mid-body numeral with header marker
    reviewer_counterexample = [
        "\n".join(["In die Skriflig 39(2) 2005:239-254"] + ["body text"] * 50 + ["239"] + ["body text"] * 50)
    ]
    with pytest.raises(ValueError) as exc1b:
        verify_monotonic_pagination(reviewer_counterexample)
    assert "is not located in a valid header/footer margin region proximate to running journal markers" in str(exc1b.value)

    # 1c. Mid-body isolated numeral with both header and footer markers far away
    mock_midbody_with_both_markers = [
        "\n".join(["Paulus als Schriftuitlegger"] + ["body text"] * 50 + ["239"] + ["body text"] * 50 + ["In die Skriflig 39(2) 2005:239-254"])
    ]
    with pytest.raises(ValueError) as exc1c:
        verify_monotonic_pagination(mock_midbody_with_both_markers)
    assert "is not located in a valid header/footer margin region proximate to running journal markers" in str(exc1c.value)

    # 2. Missing running header/footer marker counterexample
    mock_missing_marker_pages = [
        "239\nProse without any journal header or footer marker.\n"
    ]
    with pytest.raises(ValueError) as exc2:
        verify_monotonic_pagination(mock_missing_marker_pages)
    assert "is not located in a valid header/footer margin region proximate to running journal markers" in str(exc2.value)

    # 3. Injected match for CONFIRMED_ABSENT target (B001-11: 1 Cor 10:7 / Exodus 32:6)
    mock_16_pages = ["In die Skriflig 39(2) 2005:239-254\n" + str(p + 238) for p in range(1, 17)]
    # Provide expected positive hits for B001-1 (on p. 1) and B001-4 (on p. 10)
    mock_16_pages[0] += "\nRom 4:3 citing Gen 15:6 with ἐπίστευσεν δὲ Ἀβραάμ\n"
    mock_16_pages[9] += "\nRom 10:11 and 9:33\n"
    # Inject 1 Cor 10:7 on PDF p. 5 (printed 243)
    mock_16_pages[4] += "\nHere is an injected mention of 1 Cor 10:7 in text.\n"
    with pytest.raises(ValueError) as exc3:
        execute_full_volume_search(mock_16_pages, [])
    assert "Target B001-11 is categorized as CONFIRMED_ABSENT, but search pattern matched 1 hit(s)" in str(exc3.value)
    assert "on page(s) [243]" in str(exc3.value)

    # 4. Zero matches for positive target B001-1
    mock_empty_pages = ["In die Skriflig 39(2) 2005:239-254\n" + str(p + 238) + "\nGeneric text with no citations." for p in range(1, 17)]
    with pytest.raises(ValueError) as exc4:
        execute_full_volume_search(mock_empty_pages, [])
    assert "Target B001-1 is categorized as EXTENDED_EXEGETICAL_ANALYSIS, but search patterns returned zero hits!" in str(exc4.value)

    # 5. Ledger witness quote mismatch fails closed
    fake_ledger_row = [{
        "evidence_id": "S07F-E001",
        "source_id": "S07F",
        "b001_id": "B001-1",
        "claim_type": "Historical / Methodological",
        "author_claim": "Claim text",
        "short_quote": "nonexistent quote string",
        "printed_page": "239",
        "source_locator": "Printed p. 239 [PDF p. 1]",
        "notebooklm_citation": "[1]",
        "verification_status": "VERIFIED",
        "qualification": "qual",
        "extraction_confidence": "HIGH",
        "notes": "note",
    }]
    with pytest.raises(ValueError) as exc5:
        verify_ledger_witnesses(fake_ledger_row, mock_16_pages)
    assert "entire normalized quote not found in text of PDF p(p). 1 (printed p(p). 239)" in str(exc5.value)


def test_s08f_citation_ledger_crosswalk_integrity():
    """Verify S08F citation ledger schema, pagination mapping, quote integrity, and multi-locus scope."""
    repo_root = Path(__file__).resolve().parent.parent
    s08f_dir = repo_root / "research/inbox/B001-pauline-txt-pilot/sources/S08F"
    csv_path = s08f_dir / "citation_ledger.csv"
    ext_path = s08f_dir / "extraction.md"

    assert csv_path.is_file(), f"Missing citation_ledger.csv at {csv_path}"
    with open(csv_path, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    assert len(rows) == 8, f"Expected 8 ledger rows for S08F, found {len(rows)}"

    expected_b001_map = {
        "S08F-E001": "B001-2",
        "S08F-E002": "B001-2",
        "S08F-E003": "B001-3",
        "S08F-E004": "B001-2, B001-3",
        "S08F-E005": "B001-2, B001-3",
        "S08F-E006": "B001-2, B001-3",
        "S08F-E007": "B001-2, B001-3",
        "S08F-E008": "B001-2",
    }

    expected_ids = [f"S08F-E00{i}" for i in range(1, 9)]
    for idx, r in enumerate(rows):
        eid = r["evidence_id"]
        assert eid == expected_ids[idx], f"Expected {expected_ids[idx]}, got {eid}"
        assert r["source_id"] == "S08F"
        assert r["verification_status"] == "VERIFIED"
        assert r["extraction_confidence"] == "HIGH"
        assert len(r["short_quote"].strip()) > 15
        assert r["author_claim"].strip()

        # Verify B001 locus alignment
        assert r["b001_id"] == expected_b001_map[eid], f"Expected {expected_b001_map[eid]} for {eid}, got {r['b001_id']}"

        printed = int(r["printed_page"])
        expected_pdf = printed - 94
        assert 1 <= expected_pdf <= 16, f"Invalid printed page {printed} for {eid}"
        assert f"Printed p. {printed} [PDF p. {expected_pdf}" in r["source_locator"]

    # Check extraction.md cross-alignment
    ext_text = ext_path.read_text(encoding="utf-8")
    for eid, exp_b001 in expected_b001_map.items():
        assert f"`{eid}`" in ext_text
        assert re.search(
            rf"####\s+{eid}[\s\S]*?-\s+\*\*B001 Passage ID:\*\*\s*`{re.escape(exp_b001)}`",
            ext_text
        )


def test_s08f_provenance_manifest_and_pagination_invariant():
    """Verify S08F provenance manifest and pagination invariant."""
    repo_root = Path(__file__).resolve().parent.parent
    manifest_path = repo_root / "research/inbox/B001-pauline-txt-pilot/sources/S08F/provenance_manifest.json"
    assert manifest_path.is_file(), f"Missing manifest at {manifest_path}"

    with open(manifest_path, encoding="utf-8") as f:
        manifest = json.load(f)

    assert manifest["source_id"] == "S08F"
    assert manifest["work"]["authors"] == ["J. Paul Tanner"]
    assert manifest["work"]["journal"] == "Bibliotheca Sacra"
    assert manifest["ingested_volume"]["size_bytes"] == 1440727
    assert manifest["ingested_volume"]["pages"] == 17
    assert manifest["ingested_volume"]["article_pages"] == 16
    assert manifest["ingested_volume"]["sha256"] == "88263a92f5edf99217238123198ff580a91203ecca68111aaed614a1a932a64a"


def test_s08f_verifier_negative_search_passes():
    """Verify scripts/verify_s08f_negative_search.py passes in --check-only mode."""
    import subprocess
    repo_root = Path(__file__).resolve().parent.parent
    verifier_script = repo_root / "scripts/verify_s08f_negative_search.py"
    assert verifier_script.is_file(), f"Missing verifier script: {verifier_script}"

    cmd = ["python3", str(verifier_script), "--check-only"]
    res = subprocess.run(cmd, cwd=str(repo_root), capture_output=True, text=True)
    assert res.returncode == 0, f"Verifier failed with return code {res.returncode}:\nStdout:\n{res.stdout}\nStderr:\n{res.stderr}"
    assert "matches generated report byte-for-byte (--check-only passed)" in res.stdout


def test_s08f_adversarial_pagination_and_negative_search_assertions():
    """Verify S08F verifier assertions fail closed against adversarial mutations."""
    import sys
    import pytest
    repo_root = Path(__file__).resolve().parent.parent
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))
    from scripts.verify_s08f_negative_search import (
        verify_monotonic_pagination,
        execute_full_volume_search,
        verify_ledger_witnesses,
    )

    # 1. Missing header numeral in top 3 lines fails closed
    mock_body_only_pages = [
        "BiBLiOTHECA SACRA / January-March 2005\nThis line mentions 95 in mid-prose.\nThird line without numeral.\n"
    ]
    with pytest.raises(ValueError) as exc1:
        verify_monotonic_pagination(mock_body_only_pages)
    assert "expected printed page number '95' not found in header margin" in str(exc1.value)

    # 2. Missing running journal marker in header lines fails closed
    mock_missing_marker_pages = [
        "95 An Unrelated Header / January-March 2005\nSecond line.\nThird line.\n"
    ]
    with pytest.raises(ValueError) as exc2:
        verify_monotonic_pagination(mock_missing_marker_pages)
    assert "missing running journal marker in header lines" in str(exc2.value)

    # 3. Injected match for CONFIRMED_ABSENT target (B001-1: Romans 4:3) fails closed
    mock_16_pages = ["95 BiBLiOTHECA SACRA / January-March 2005\nHeader 2\nHeader 3\n"]
    for p in range(2, 17):
        prn = p + 94
        mock_16_pages.append(f"{prn} BiBLiOTHECA SACRA / January-March 2005\nLine 2\nLine 3\n")
    # Provide expected positive hits for B001-2 (Rom 9:25) and B001-3 (Rom 9:26)
    mock_16_pages[0] += "\nRom 9:25 and Hos 2:23\n"
    mock_16_pages[4] += "\nRom 9:26 and Hos 1:10\n"
    # Inject Rom 4:3 into page 3
    mock_16_pages[2] += "\nHere is an injected mention of Rom 4:3 in text.\n"
    with pytest.raises(ValueError) as exc3:
        execute_full_volume_search(mock_16_pages, [])
    assert "Target B001-1 expected absent but found 1 hits" in str(exc3.value)

    # 4. Zero matches for positive target B001-2 fails closed
    mock_no_positive_pages = [f"{p+94} BiBLiOTHECA SACRA / January-March 2005\nLine 2\nLine 3\nGeneric text without citations." for p in range(1, 17)]
    with pytest.raises(ValueError) as exc4:
        execute_full_volume_search(mock_no_positive_pages, [])
    assert "Target B001-2 expected extended discussion but found 0 hits" in str(exc4.value)

    # 5. Ledger witness quote mismatch fails closed
    fake_ledger_row = [{
        "evidence_id": "S08F-E001",
        "source_id": "S08F",
        "b001_id": "B001-2",
        "claim_type": "Exegetical / Theological",
        "author_claim": "Claim text",
        "short_quote": "nonexistent quote string that should never appear",
        "printed_page": "98",
        "source_locator": "Printed p. 98 [PDF p. 4]",
        "notebooklm_citation": "[1, 2]",
        "verification_status": "VERIFIED",
        "qualification": "qual",
        "extraction_confidence": "HIGH",
        "notes": "note",
    }]
    with pytest.raises(ValueError) as exc5:
        verify_ledger_witnesses(fake_ledger_row, mock_16_pages)
    assert "Quote text not found on declared printed p. 98 [PDF p. 4]" in str(exc5.value)

    # 6. Ledger witness b001_id mismatch fails closed
    fake_ledger_b001_mismatch = [{
        "evidence_id": "S08F-E004",
        "source_id": "S08F",
        "b001_id": "B001-2",  # Should be "B001-2, B001-3"
        "claim_type": "Hermeneutical / Theological",
        "author_claim": "Claim text",
        "short_quote": "verses 25-26 affirm that the conversion of Gentiles is a direct fulfillment of Hosea's prophecy (though not the complete fulfillment).",
        "printed_page": "102",
        "source_locator": "Printed p. 102 [PDF p. 8]",
        "notebooklm_citation": "[9, 10]",
        "verification_status": "VERIFIED",
        "qualification": "qual",
        "extraction_confidence": "HIGH",
        "notes": "note",
    }]
    with pytest.raises(ValueError) as exc6:
        verify_ledger_witnesses(fake_ledger_b001_mismatch, mock_16_pages)
    assert "S08F-E004: b001_id mismatch: expected 'B001-2, B001-3', got 'B001-2'" in str(exc6.value)

    # 7. Coordinated false PDF page locator in ledger fails closed
    fake_ledger_pdf40 = [{
        "evidence_id": "S08F-E001",
        "source_id": "S08F",
        "b001_id": "B001-2",
        "claim_type": "Exegetical / Theological",
        "author_claim": "Claim text",
        "short_quote": "it seems clear that Paul was citing these verses to establish the point that God's \"vessels of mercy\" include Gentiles.",
        "printed_page": "98",
        "source_locator": "Printed p. 98 [PDF p. 40]",
        "notebooklm_citation": "[1, 2]",
        "verification_status": "VERIFIED",
        "qualification": "qual",
        "extraction_confidence": "HIGH",
        "notes": "note",
    }]
    with pytest.raises(ValueError) as exc7:
        verify_ledger_witnesses(fake_ledger_pdf40, mock_16_pages)
    assert "source_locator PDF pages (40,) != expected (4,)" in str(exc7.value)


def test_s08f_cross_artifact_adversarial_mutations(tmp_path):
    """Verify section-bound extraction, subsection synthesis, and structured bibliography fail closed against mutations."""
    import shutil
    import sys
    import pytest

    repo_root = Path(__file__).resolve().parent.parent
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))
    from scripts.verify_s08f_negative_search import verify_cross_artifact_consistency
    s08f_src = repo_root / "research/inbox/B001-pauline-txt-pilot/sources/S08F"

    # Baseline: copy all files to tmp_path and verify it passes
    shutil.copytree(s08f_src, tmp_path / "S08F")
    test_dir = tmp_path / "S08F"
    verify_cross_artifact_consistency(test_dir)

    # Mutation 1: Missing Source Locator in extraction block fails closed
    ext_file = test_dir / "extraction.md"
    orig_ext = ext_file.read_text(encoding="utf-8")
    mutated_ext_missing_loc = orig_ext.replace("- **Source Locator:** Printed p. 99 [PDF p. 5]\n", "", 1)
    ext_file.write_text(mutated_ext_missing_loc, encoding="utf-8")
    with pytest.raises(ValueError) as exc1:
        verify_cross_artifact_consistency(test_dir)
    assert "Expected exactly one Source Locator, found 0" in str(exc1.value)
    ext_file.write_text(orig_ext, encoding="utf-8")

    # Mutation 2: Duplicate Source Locator in extraction block fails closed
    mutated_ext_dup_loc = orig_ext.replace(
        "- **Source Locator:** Printed p. 98 [PDF p. 4]\n",
        "- **Source Locator:** Printed p. 98 [PDF p. 4]\n- **Source Locator:** Printed p. 98 [PDF p. 4]\n",
        1
    )
    ext_file.write_text(mutated_ext_dup_loc, encoding="utf-8")
    with pytest.raises(ValueError) as exc2:
        verify_cross_artifact_consistency(test_dir)
    assert "Expected exactly one Source Locator, found 2" in str(exc2.value)
    ext_file.write_text(orig_ext, encoding="utf-8")

    # Mutation 3: Borrowed/swapped Source Locator across blocks fails closed
    mutated_ext_swap_loc = orig_ext.replace(
        "#### S08F-E008\n- **Proposed Evidence ID:** `S08F-E008`\n- **B001 Passage ID:** `B001-2` (Romans 9:25 / Hosea 2:23)\n- **Claim Type:** `Textual-critical / Exegetical`\n- **Author's Claim:** Paul reversed the order of the clauses in Hosea 2:23 to stress the \"My people\" aspect of the promise and God's sovereign call to them, aligning the quotation with Romans 9:24.\n- **Short Exact Quotation:** \"reversed the order of the clauses (perhaps to stress the \\\"My people\\\" aspect of the promise and God's \\\"call\\\" to them).\"\n- **Printed Page Number:** 99\n- **Source Locator:** Printed p. 99 [PDF p. 5]",
        "#### S08F-E008\n- **Proposed Evidence ID:** `S08F-E008`\n- **B001 Passage ID:** `B001-2` (Romans 9:25 / Hosea 2:23)\n- **Claim Type:** `Textual-critical / Exegetical`\n- **Author's Claim:** Paul reversed the order of the clauses in Hosea 2:23 to stress the \"My people\" aspect of the promise and God's sovereign call to them, aligning the quotation with Romans 9:24.\n- **Short Exact Quotation:** \"reversed the order of the clauses (perhaps to stress the \\\"My people\\\" aspect of the promise and God's \\\"call\\\" to them).\"\n- **Printed Page Number:** 99\n- **Source Locator:** Printed p. 98 [PDF p. 4]"
    )
    ext_file.write_text(mutated_ext_swap_loc, encoding="utf-8")
    with pytest.raises(ValueError) as exc3:
        verify_cross_artifact_consistency(test_dir)
    assert "Printed page mismatch: expected (99,), got (98,)" in str(exc3.value)
    ext_file.write_text(orig_ext, encoding="utf-8")

    # Mutation 4: Extraction B001 passage ID drift fails closed
    mutated_ext_b001_drift = orig_ext.replace(
        "#### S08F-E004\n- **Proposed Evidence ID:** `S08F-E004`\n- **B001 Passage ID:** `B001-2, B001-3`",
        "#### S08F-E004\n- **Proposed Evidence ID:** `S08F-E004`\n- **B001 Passage ID:** `B001-2`"
    )
    ext_file.write_text(mutated_ext_b001_drift, encoding="utf-8")
    with pytest.raises(ValueError) as exc4:
        verify_cross_artifact_consistency(test_dir)
    assert "B001 ID mismatch: expected 'B001-2, B001-3'" in str(exc4.value)
    ext_file.write_text(orig_ext, encoding="utf-8")

    # Mutation 5: Synthesis subsection locus swap/missing fails closed
    synth_file = test_dir / "tanner_hosea_new_covenant_synthesis.md"
    orig_synth = synth_file.read_text(encoding="utf-8")
    mutated_synth = orig_synth.replace(
        "### Composite Quotation Structure\n- **Printed Page Number:** Printed p. 98 [PDF p. 4]",
        "### Composite Quotation Structure\n- **Printed Page Number:** Printed p. 101 [PDF p. 7]"
    )
    synth_file.write_text(mutated_synth, encoding="utf-8")
    with pytest.raises(ValueError) as exc5:
        verify_cross_artifact_consistency(test_dir)
    assert "missing expected locus 'Printed p. 98 [PDF p. 4]' within its subsection block" in str(exc5.value)
    synth_file.write_text(orig_synth, encoding="utf-8")

    # Mutation 6: Bibliographic container misattribution (Daniels -> JETS) fails closed
    bib_file = test_dir / "bibliography_leads.md"
    orig_bib = bib_file.read_text(encoding="utf-8")
    mutated_bib_container = orig_bib.replace("Faith and Mission", "Journal for the Evangelical Theological Society")
    bib_file.write_text(mutated_bib_container, encoding="utf-8")
    with pytest.raises(ValueError) as exc6:
        verify_cross_artifact_consistency(test_dir)
    assert "Container mismatch: expected 'Faith and Mission'" in str(exc6.value)
    bib_file.write_text(orig_bib, encoding="utf-8")

    # Mutation 7: Bibliographic footnote number misattribution (McClain -> fn. 1) fails closed
    mutated_bib_footnote = orig_bib.replace(
        "### Alva J. McClain (1973)\n- **Author:** Alva J. McClain\n- **Title:** *The Gospel of God’s Grace*\n- **Publication Year:** 1973 (Chicago: Moody Press, p. 183)\n- **Source Locator:** Printed p. 98 [PDF p. 4], fn. 2",
        "### Alva J. McClain (1973)\n- **Author:** Alva J. McClain\n- **Title:** *The Gospel of God’s Grace*\n- **Publication Year:** 1973 (Chicago: Moody Press, p. 183)\n- **Source Locator:** Printed p. 98 [PDF p. 4], fn. 1"
    )
    bib_file.write_text(mutated_bib_footnote, encoding="utf-8")
    with pytest.raises(ValueError) as exc7:
        verify_cross_artifact_consistency(test_dir)
    assert "Footnote mismatch: expected 2, got 1" in str(exc7.value)
    bib_file.write_text(orig_bib, encoding="utf-8")

    # Mutation 8: Bibliographic footnote number misattribution (Wolff -> fn. 17) fails closed
    mutated_bib_wolff = orig_bib.replace(
        "### Hans Walter Wolff (1974)\n- **Author:** Hans Walter Wolff\n- **Title:** *Hosea* (Hermeneia Commentary, trans. Gary Stensell)\n- **Publication Year:** 1974 (Philadelphia: Fortress Press, pp. 51, 55)\n- **Source Locator:** Printed p. 107 [PDF p. 13], fn. 18",
        "### Hans Walter Wolff (1974)\n- **Author:** Hans Walter Wolff\n- **Title:** *Hosea* (Hermeneia Commentary, trans. Gary Stensell)\n- **Publication Year:** 1974 (Philadelphia: Fortress Press, pp. 51, 55)\n- **Source Locator:** Printed p. 107 [PDF p. 13], fn. 17"
    )
    bib_file.write_text(mutated_bib_wolff, encoding="utf-8")
    with pytest.raises(ValueError) as exc8:
        verify_cross_artifact_consistency(test_dir)
    assert "Footnote mismatch: expected 18, got 17" in str(exc8.value)
    bib_file.write_text(orig_bib, encoding="utf-8")

    # Mutation 9 (R2-F1): Bibliographic footnote prefix collision (McClain fn. 2 -> fn. 20) fails closed
    mutated_bib_prefix = orig_bib.replace(
        "Printed p. 98 [PDF p. 4], fn. 2; Section 2",
        "Printed p. 98 [PDF p. 4], fn. 20; Section 2"
    )
    bib_file.write_text(mutated_bib_prefix, encoding="utf-8")
    with pytest.raises(ValueError) as exc9:
        verify_cross_artifact_consistency(test_dir)
    assert "Footnote mismatch: expected 2, got 20" in str(exc9.value)
    bib_file.write_text(orig_bib, encoding="utf-8")

    # Mutation 10 (R2-F1): Invented work title in bibliography (Daniels -> *Unrelated Work*) fails closed
    mutated_bib_title = orig_bib.replace(
        '- **Title:** *"How Does the Church Relate to the New Covenant? or, Whose New Covenant Is It, Anyway?"*',
        "- **Title:** *Unrelated Work*"
    )
    bib_file.write_text(mutated_bib_title, encoding="utf-8")
    with pytest.raises(ValueError) as exc10:
        verify_cross_artifact_consistency(test_dir)
    assert "Title mismatch: expected" in str(exc10.value)
    bib_file.write_text(orig_bib, encoding="utf-8")

    # Mutation 11 (R2-F1): Invented author in bibliography (Daniels -> Another Scholar) fails closed
    mutated_bib_auth = orig_bib.replace(
        "- **Author:** Richard Daniels",
        "- **Author:** Another Scholar"
    )
    bib_file.write_text(mutated_bib_auth, encoding="utf-8")
    with pytest.raises(ValueError) as exc11:
        verify_cross_artifact_consistency(test_dir)
    assert "Author mismatch: expected 'Richard Daniels'" in str(exc11.value)
    bib_file.write_text(orig_bib, encoding="utf-8")

    # Mutation 12 (R2-F2): Coordinated false PDF-page locator (E001 PDF p. 4 -> PDF p. 40 in both ledger and extraction) fails closed
    csv_file = test_dir / "citation_ledger.csv"
    orig_csv = csv_file.read_text(encoding="utf-8")
    mutated_csv_pdf40 = orig_csv.replace("Printed p. 98 [PDF p. 4]", "Printed p. 98 [PDF p. 40]")
    mutated_ext_pdf40 = orig_ext.replace("Printed p. 98 [PDF p. 4]", "Printed p. 98 [PDF p. 40]")
    csv_file.write_text(mutated_csv_pdf40, encoding="utf-8")
    ext_file.write_text(mutated_ext_pdf40, encoding="utf-8")
    with pytest.raises(ValueError) as exc12:
        verify_cross_artifact_consistency(test_dir)
    assert "PDF page mismatch: expected (4,), got (40,)" in str(exc12.value)
    csv_file.write_text(orig_csv, encoding="utf-8")
    ext_file.write_text(orig_ext, encoding="utf-8")

    # Mutation 13 (R2-F3): Corrupted quotation field masked by notes copies fails closed
    mutated_ext_quote_notes = orig_ext.replace(
        '- **Short Exact Quotation:** "it seems clear that Paul was citing these verses to establish the point that God\'s \\"vessels of mercy\\" include Gentiles."',
        '- **Short Exact Quotation:** "A completely corrupted and invented quotation field that must fail closed."'
    ).replace(
        "- **Notes:** Tanner 2005:98. Supporting Gentile inclusion as vessels of mercy.",
        "- **Notes:** Tanner 2005:98. Supporting Gentile inclusion as vessels of mercy. Original quote: \\\"it seems clear that Paul was citing these verses to establish the point that God's vessels of mercy include Gentiles.\\\""
    )
    ext_file.write_text(mutated_ext_quote_notes, encoding="utf-8")
    with pytest.raises(ValueError) as exc13:
        verify_cross_artifact_consistency(test_dir)
    assert "Short Exact Quotation field mismatch" in str(exc13.value)
    ext_file.write_text(orig_ext, encoding="utf-8")

    # Mutation 14 (R2-F2): Missing closing delimiter in extraction locator fails closed
    mutated_ext_bad_delim = orig_ext.replace("Printed p. 98 [PDF p. 4]", "Printed p. 98 [PDF p. 4")
    ext_file.write_text(mutated_ext_bad_delim, encoding="utf-8")
    with pytest.raises(ValueError) as exc14:
        verify_cross_artifact_consistency(test_dir)
    assert "Cannot parse PDF page in locator" in str(exc14.value)
    ext_file.write_text(orig_ext, encoding="utf-8")













