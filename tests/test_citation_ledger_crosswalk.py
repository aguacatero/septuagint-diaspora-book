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

    assert len(reader) == 11, f"Expected exactly 11 ledger rows for S05, found {len(reader)}"

    for idx, row in enumerate(reader, 1):
        expected_eid = f"S05-E{idx:03d}"
        assert row["evidence_id"] == expected_eid, f"Expected {expected_eid}, got {row['evidence_id']}"
        assert row["source_id"] == "S05"
        assert row["verification_status"] == "VERIFIED", f"Row {expected_eid} status not VERIFIED: {row['verification_status']}"
        assert len(row["short_quote"]) > 5, f"Short quote too short for {expected_eid}"
        assert len(row["author_claim"]) > 10, f"Author claim too short for {expected_eid}"
        assert row["printed_page"].isdigit(), f"Invalid printed_page for {expected_eid}: {row['printed_page']}"
        assert "S." in row["source_locator"], f"Invalid source_locator for {expected_eid}: {row['source_locator']}"


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

    # Negative non-prophetic loci B001-1 and B001-9 must be NOT DISCUSSED
    assert "| B001-1 | Romans 4:3 / Genesis 15:6 | 1 | NOT DISCUSSED |" in log_text
    assert "| B001-9 | 1 Corinthians 6:16 / Genesis 2:24 | 0 | NOT DISCUSSED |" in log_text

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






