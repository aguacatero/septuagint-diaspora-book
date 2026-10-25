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

    # Review request file must also reflect this standard
    req_path = repo_root / "research-queue/B001_CHATGPT_REVIEW_REQUEST.md"
    with open(req_path, encoding="utf-8") as f:
        req_text = f.read()
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

    # Index structure validation tests
    # Missing index fails
    bad_index = vns.verify_index_structure("A text with no index at all.")
    assert bad_index["passed"] is False
    assert bad_index["index_present"] is False

    # Valid index succeeds
    good_index_text = (
        "Main text...\nINDEX              TO THE                NOTES\n"
        "I. SUBJECTS\nAbraham, Righteousness of, p. 100 ff.\nAdam, p. 130 ff.\n"
        "Old Testament, Use of the, pp. 77; 302-307.\n"
        "II. LATIN WORDS\nIII. GREEK WORDS\n"
    )
    good_index = vns.verify_index_structure(good_index_text)
    assert good_index["passed"] is True
    assert good_index["has_subjects_section"] is True
    assert good_index["has_latin_section"] is True
    assert good_index["has_greek_section"] is True
    assert good_index["ordered"] is True
    assert good_index["has_scripture_index"] is False

    # Adversarial index test 1: Unexpected Scripture index detected
    scrip_index_text = (
        "Main text...\nINDEX              TO THE                NOTES\n"
        "I. SUBJECTS\nAbraham, Righteousness of, p. 100 ff.\nAdam, p. 130 ff.\n"
        "Old Testament, Use of the, pp. 77; 302-307.\n"
        "II. LATIN WORDS\nIII. GREEK WORDS\nIV. PASSAGES OF SCRIPTURE\n"
    )
    scrip_index = vns.verify_index_structure(scrip_index_text)
    assert scrip_index["has_scripture_index"] is True
    assert scrip_index["passed"] is False
    scrip_report = vns.build_markdown_report(res_zero, dummy_positive_results, scrip_index, dummy_pdf, 1000, "sha", dummy_text, "sha_txt", 50, 100, raw_text=scrip_index_text)
    # MUST NOT print None when scripture index exists
    assert "Dedicated Scripture Passage Index (Index Locorum): None" not in scrip_report
    assert "PRESENT (detected pattern" in scrip_report

    # Adversarial index test 2: Out-of-order sections fail
    out_of_order_text = (
        "Main text...\nINDEX              TO THE                NOTES\n"
        "III. GREEK WORDS\nI. SUBJECTS\nAbraham, Righteousness of, p. 100 ff.\n"
        "II. LATIN WORDS\n"
    )
    ooo_index = vns.verify_index_structure(out_of_order_text)
    assert ooo_index["passed"] is False
    assert ooo_index["ordered"] is False

    # Adversarial index test 3: Positive control out-of-bounds (e.g. Abraham after Latin section) fails
    oob_text = (
        "Main text...\nINDEX              TO THE                NOTES\n"
        "I. SUBJECTS\nAdam, p. 130 ff.\nOld Testament, Use of the, pp. 77; 302-307.\n"
        "II. LATIN WORDS\nAbraham, Righteousness of, p. 100 ff.\nIII. GREEK WORDS\n"
    )
    oob_index = vns.verify_index_structure(oob_text)
    assert oob_index["passed"] is False
    assert oob_index["positive_controls"]["Abraham"] is False

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
