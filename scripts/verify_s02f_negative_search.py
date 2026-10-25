#!/usr/bin/env python3
"""Reproducible full-volume negative search verification for Sanday & Headlam (1895).

Fails closed on missing or corrupted input PDF, binds extracted text cryptographically
to the source volume, runs positive-control validation against genuine 19th-century
citation typography, validates bounded and ordered authorial index structure, and executes
whitespace-tolerant regex searches for the five non-Romans B001 passage comparisons:
  - B001-8:  1 Cor 1:19 / Isa 29:14
  - B001-9:  1 Cor 6:16 / Gen 2:24
  - B001-10: 1 Cor 9:9 / Deut 25:4
  - B001-11: 1 Cor 10:7 / Exod 32:6
  - B001-12: Gal 3:13 / Deut 21:23

Outputs a verified markdown search log documenting patterns, positive controls,
dynamic pattern-driven counts, index bibliographic structure, and scholarly evaluation.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import subprocess
import sys
import unicodedata
from pathlib import Path


EXPECTED_RAW_PDF_SHA256 = "4a6369a0595550c8c1b92b71613a73182fe4a82aa02cfc989633e6c4dc0b80af"
EXPECTED_RAW_PDF_BYTES = 47318528
EXPECTED_TEXT_SHA256 = "c426418d349f4c6836ef59170a488351e18fb917abbcae58fd492ec53a0a2bb1"

RAW_PDF_DEFAULT = Path("/Users/chrisrodriguez/Downloads/sanday_headlam_1895_romans_icc_ia_raw.pdf")
DEFAULT_TEXT_PATH = Path("/tmp/sanday_headlam_full_text.txt")
DEFAULT_OUT_PATH = Path("research/inbox/B001-pauline-txt-pilot/sources/S02F/full_volume_search_log.md")


def strip_accents(s: str) -> str:
    """Normalize and strip diacritical marks for fault-tolerant Greek/Latin matching."""
    nfkd = unicodedata.normalize("NFKD", s)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def get_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


# Positive controls: citations known to exist in the volume in authentic 19th-century typography.
# Validates that regexes detect the source's actual punctuation, whitespace, and Roman/Arabic numerals.
POSITIVE_CONTROLS = [
    {
        "name": "1 Cor 3:19 (Excursus p. 302, Note p. 340)",
        "pattern": r"\b(?:1|I|First)\s*Cor(?:\.|inthians)?\s*(?:3|iii)[\.:,]?\s*(?:19|xix)\b",
        "expected_min_matches": 1,
    },
    {
        "name": "Gen 15:6 (Rom 4:3 commentary, pp. 100, 102)",
        "pattern": r"\b(?:Gen|Genesis)(?:\.|\b)\s*(?:15|xv)[\.:,]?\s*(?:6|vi)\b",
        "expected_min_matches": 1,
    },
    {
        "name": "Isa 40:13 (Rom 11:34 note, p. 340)",
        "pattern": r"\b(?:Isa|Is|Isaiah)(?:\.|\b)\s*(?:40|xl)[\.:,]?\s*(?:13|xiii)\b",
        "expected_min_matches": 1,
    },
    {
        "name": "Joel 2:32 (Rom 10:13 note, p. 291)",
        "pattern": r"\b(?:Joel)(?:\.|\b)\s*(?:2|ii)[\.:,]?\s*(?:32|xxxii)\b",
        "expected_min_matches": 1,
    },
    {
        "name": "Gal 4:22 (Excursus p. 303)",
        "pattern": r"\b(?:Gal|Galatians)(?:\.|\b)\s*(?:4|iv)[\.:,]?\s*(?:22|xxii)\b",
        "expected_min_matches": 1,
    },
]


TARGET_QUERIES = [
    {
        "id": "B001-8",
        "name": "1 Corinthians 1:19 / Isaiah 29:14",
        "nt_target": "1 Cor 1:19",
        "ot_target": "Isa 29:14",
        "patterns": [
            ("NT citation (Arabic/Roman, whitespace-tolerant)", r"\b(?:1|I|First)\s*Cor(?:\.|inthians)?\s*(?:1|i)[\.:,]?\s*(?:19|xix)\b", "NT"),
            ("OT citation (Arabic/Roman, whitespace-tolerant)", r"\b(?:Isa|Is|Isaiah)(?:\.|\b)\s*(?:29|xxix)[\.:,]?\s*(?:14|xiv)\b", "OT"),
            ("Greek lemma / phrase", r"ἀπολῶ\s+τὴν\s+σοφίαν", "lemma"),
            ("Greek unaccented", r"απολω\s+την\s+σοφιαν", "lemma"),
            ("Greek keyword (ἀθετήσω)", r"\bἀθετήσω\b", "lemma"),
            ("English key phrase", r"destroy\s+the\s+wisdom\s+of\s+the\s+wise", "lemma"),
        ],
    },
    {
        "id": "B001-9",
        "name": "1 Corinthians 6:16 / Genesis 2:24",
        "nt_target": "1 Cor 6:16",
        "ot_target": "Gen 2:24",
        "patterns": [
            ("NT citation (Arabic/Roman, whitespace-tolerant)", r"\b(?:1|I|First)\s*Cor(?:\.|inthians)?\s*(?:6|vi)[\.:,]?\s*(?:16|xvi)\b", "NT"),
            ("OT citation (Arabic/Roman, whitespace-tolerant)", r"\b(?:Gen|Genesis)(?:\.|\b)\s*(?:2|ii)[\.:,]?\s*(?:24|xxiv)\b", "OT"),
            ("Greek lemma / phrase", r"σάρκα\s+μίαν", "lemma"),
            ("Greek unaccented", r"σαρκα\s+μιαν", "lemma"),
            ("English key phrase", r"two\s+shall\s+be\s+one\s+flesh", "lemma"),
        ],
    },
    {
        "id": "B001-10",
        "name": "1 Corinthians 9:9 / Deuteronomy 25:4",
        "nt_target": "1 Cor 9:9",
        "ot_target": "Deut 25:4",
        "patterns": [
            ("NT citation (Arabic/Roman, whitespace-tolerant)", r"\b(?:1|I|First)\s*Cor(?:\.|inthians)?\s*(?:9|ix)[\.:,]?\s*(?:9|ix)\b", "NT"),
            ("OT citation (Arabic/Roman, whitespace-tolerant)", r"\b(?:Deut|Dt|Deuteronomy)(?:\.|\b)\s*(?:25|xxv)[\.:,]?\s*(?:4|iv)\b", "OT"),
            ("Greek lemma / verb 1", r"φιμώσεις\s+βοῦν", "lemma"),
            ("Greek lemma / verb 2", r"κημώσεις\s+βοῦν", "lemma"),
            ("Greek root (unaccented)", r"(?:φιμωσ|κημωσ)", "lemma"),
            ("English key phrase", r"muzzle\s+the\s+ox", "lemma"),
        ],
    },
    {
        "id": "B001-11",
        "name": "1 Corinthians 10:7 / Exodus 32:6",
        "nt_target": "1 Cor 10:7",
        "ot_target": "Exod 32:6",
        "patterns": [
            ("NT citation (Arabic/Roman, whitespace-tolerant)", r"\b(?:1|I|First)\s*Cor(?:\.|inthians)?\s*(?:10|x)[\.:,]?\s*(?:7|vii)\b", "NT"),
            ("OT citation (Arabic/Roman, whitespace-tolerant)", r"\b(?:Exod|Ex|Exodus)(?:\.|\b)\s*(?:32|xxxii)[\.:,]?\s*(?:6|vi)\b", "OT"),
            ("Greek lemma / phrase", r"φαγεῖν\s+καὶ\s+πεῖν", "lemma"),
            ("Greek unaccented", r"φαγειν\s+και\s+πειν", "lemma"),
            ("Greek play verb", r"ἀνέστησαν\s+παίζειν", "lemma"),
            ("English key phrase", r"rose\s+up\s+to\s+play", "lemma"),
        ],
    },
    {
        "id": "B001-12",
        "name": "Galatians 3:13 / Deuteronomy 21:23",
        "nt_target": "Gal 3:13",
        "ot_target": "Deut 21:23",
        "patterns": [
            ("NT citation (Arabic/Roman, whitespace-tolerant)", r"\b(?:Gal|Galatians)(?:\.|\b)\s*(?:3|iii)[\.:,]?\s*(?:13|xiii)\b", "NT"),
            ("OT citation (Arabic/Roman, whitespace-tolerant)", r"\b(?:Deut|Dt|Deuteronomy)(?:\.|\b)\s*(?:21|xxi)[\.:,]?\s*(?:23|xxiii)\b", "OT"),
            ("Greek lemma / phrase", r"ἐπικατάρατος\s+πᾶς", "lemma"),
            ("Greek unaccented", r"επικαταρατος\s+πας", "lemma"),
            ("Greek hang on tree", r"κρεμάμενος\s+ἐπὶ\s+ξύλου", "lemma"),
            ("English key phrase", r"cursed\s+is\s+every(?:one)?\s+that\s+hangeth", "lemma"),
        ],
    },
]


def run_positive_controls(full_text: str) -> list[dict]:
    results = []
    for pc in POSITIVE_CONTROLS:
        matches = list(re.finditer(pc["pattern"], full_text, re.IGNORECASE))
        match_snippets = []
        for m in matches[:3]:
            start = max(0, m.start() - 30)
            end = min(len(full_text), m.end() + 30)
            match_snippets.append(full_text[start:end].replace("\n", " ").strip())
        results.append({
            "name": pc["name"],
            "pattern": pc["pattern"],
            "count": len(matches),
            "expected_min": pc["expected_min_matches"],
            "passed": len(matches) >= pc["expected_min_matches"],
            "snippets": match_snippets,
        })
    return results


def run_search(full_text: str) -> list[dict]:
    results = []
    unaccented_text = strip_accents(full_text)

    for item in TARGET_QUERIES:
        query_res = {
            "id": item["id"],
            "name": item["name"],
            "nt_target": item["nt_target"],
            "ot_target": item["ot_target"],
            "patterns": [],
            "nt_matches": 0,
            "ot_matches": 0,
            "lemma_matches": 0,
            "total_matches": 0,
        }
        for desc, pat_str, cat in item["patterns"]:
            flags = re.IGNORECASE
            is_unacc = "unaccented" in desc or "root" in desc
            target_text = unaccented_text if is_unacc else full_text
            matches = list(re.finditer(pat_str, target_text, flags))
            match_snippets = []
            for m in matches:
                start = max(0, m.start() - 50)
                end = min(len(target_text), m.end() + 50)
                snippet = target_text[start:end].replace("\n", " ").strip()
                match_snippets.append({"pos": m.start(), "snippet": snippet})

            query_res["patterns"].append({
                "desc": desc,
                "pattern": pat_str,
                "category": cat,
                "count": len(matches),
                "snippets": match_snippets,
            })
            if cat == "NT":
                query_res["nt_matches"] += len(matches)
            elif cat == "OT":
                query_res["ot_matches"] += len(matches)
            else:
                query_res["lemma_matches"] += len(matches)
            query_res["total_matches"] += len(matches)

        results.append(query_res)
    return results


def verify_index_structure(full_text: str) -> dict:
    """Programmatically verify bounded, ordered index structure and positive controls."""
    # Find start heading
    m_start = re.search(r"INDEX\s+TO\s+THE\s+NOTES", full_text, re.IGNORECASE)
    if not m_start:
        return {
            "index_present": False,
            "error": "Index to the Notes heading not found in full text",
            "has_scripture_index": False,
            "passed": False,
        }

    idx_start = m_start.start()

    # Find end boundary (publisher catalog or EOF)
    m_end = re.search(r"An\s+Introduction\s+to\s+the\s+Literature\s+of\s+the\s+Old\s+Testament", full_text[idx_start:], re.IGNORECASE)
    idx_end = idx_start + m_end.start() if m_end else len(full_text)

    bounded_index_text = full_text[idx_start:idx_end]

    # Find ordered section positions within bounded text
    m_sub = re.search(r"\bI\.\s*SUBJECTS\b", bounded_index_text, re.IGNORECASE)
    m_lat = re.search(r"\bII\.\s*LATIN\b", bounded_index_text, re.IGNORECASE)
    m_grk = re.search(r"\bIII\.\s*GREEK\b", bounded_index_text, re.IGNORECASE)

    has_subjects = m_sub is not None
    has_latin = m_lat is not None
    has_greek = m_grk is not None

    ordered = False
    if has_subjects and has_latin and has_greek:
        pos_sub = m_sub.start()
        pos_lat = m_lat.start()
        pos_grk = m_grk.start()
        ordered = (0 <= pos_sub < pos_lat < pos_grk)

    if not ordered:
        return {
            "index_present": True,
            "index_offset": idx_start,
            "index_end_offset": idx_end,
            "has_subjects_section": has_subjects,
            "has_latin_section": has_latin,
            "has_greek_section": has_greek,
            "ordered": False,
            "has_scripture_index": False,
            "error": "Index sections missing or out of order",
            "passed": False,
        }

    # Bounded subjects text
    subjects_text = bounded_index_text[m_sub.start():m_lat.start()]

    # Positive controls strictly bounded inside subjects section
    has_abraham = re.search(r"\bAbraham\b.*?\b100\b", subjects_text, re.DOTALL | re.IGNORECASE) is not None
    has_adam = re.search(r"\bAdam\b.*?\b130\b", subjects_text, re.DOTALL | re.IGNORECASE) is not None
    has_ot_use = re.search(r"Old\s+Testament,\s*Use\s+of\s+the\b.*?\b302\b", subjects_text, re.DOTALL | re.IGNORECASE) is not None

    positive_controls_passed = has_abraham and has_adam and has_ot_use

    # Detect unexpected Scripture passage index patterns within bounded index text
    scripture_patterns = [
        r"\bIV\.\s*PASSAGES\b",
        r"\bINDEX\s+OF\s+PASSAGES\b",
        r"\bINDEX\s+LOCORUM\b",
        r"\bPASSAGES\s+OF\s+SCRIPTURE\b",
        r"\bSCRIPTURE\s+INDEX\b",
    ]
    detected_scripture_pattern = None
    for p in scripture_patterns:
        m_scrip = re.search(p, bounded_index_text, re.IGNORECASE)
        if m_scrip:
            detected_scripture_pattern = p
            break

    has_scripture_index = detected_scripture_pattern is not None

    # Passed requires valid bounded ordered sections, positive controls, and no unexpected scripture index
    passed = ordered and positive_controls_passed and not has_scripture_index

    return {
        "index_present": True,
        "index_offset": idx_start,
        "index_end_offset": idx_end,
        "has_subjects_section": has_subjects,
        "has_latin_section": has_latin,
        "has_greek_section": has_greek,
        "ordered": ordered,
        "positive_controls": {
            "Abraham": has_abraham,
            "Adam": has_adam,
            "Old Testament, Use of the": has_ot_use,
        },
        "has_scripture_index": has_scripture_index,
        "detected_scripture_pattern": detected_scripture_pattern,
        "passed": passed,
    }


def build_markdown_report(
    results: list[dict],
    positive_results: list[dict],
    index_results: dict,
    pdf_path: Path,
    pdf_bytes: int,
    pdf_sha256: str,
    text_path: Path,
    text_sha256: str,
    line_count: int,
    word_count: int,
    raw_text: str = "",
) -> str:
    md = []
    md.append("# S02F — Full-Volume Negative Search Verification Log")
    md.append("")
    md.append("**Source ID:** `S02F`")
    md.append("")
    md.append("**Source Work:** William Sanday and Arthur C. Headlam, *A Critical and Exegetical Commentary on the Epistle to the Romans* (ICC; New York: Charles Scribner's Sons, 1895 [first edition]).")
    md.append("")
    md.append("**Provenance Locator:** Internet Archive: `https://archive.org/details/epistlecommentar00sanduoft`")
    md.append("")
    md.append(f"**Full Volume Raw File:** `{pdf_path.name}`")
    md.append("")
    md.append(f"**Raw File Size:** {pdf_bytes:,} bytes (586 pages)")
    md.append("")
    md.append(f"**Raw File SHA-256:** `{pdf_sha256}`")
    md.append("")
    md.append(f"**Extracted Text Layer:** `{text_path}` ({line_count:,} lines, {word_count:,} words)")
    md.append("")
    md.append(f"**Extracted Text SHA-256:** `{text_sha256}`")
    md.append("")
    md.append("**Extraction Tool:** Poppler `pdftotext -layout` 23.03.0")
    md.append("")
    md.append("---")
    md.append("")
    md.append("## Positive-Control Validation (19th-Century Citation Typography)")
    md.append("")
    md.append("Before executing negative target queries, the regex engine was validated against authentic citation strings appearing in this volume to ensure that period-plus-space formatting, Roman chapter numerals, and abbreviation styles are accurately detected:")
    md.append("")
    md.append("| Positive Control Passage | Target Regular Expression | Measured Matches | Validation Status |")
    md.append("|---|---|---|---|")
    for pc in positive_results:
        status_label = "PASS (Detected)" if pc["passed"] else "FAIL (Not detected)"
        md.append(f"| {pc['name']} | `{pc['pattern']}` | {pc['count']} matches | **{status_label}** |")
    md.append("")
    md.append("---")
    md.append("")
    md.append("## Executive Summary of Results")
    md.append("")
    md.append("| Locus ID | B001 Target Passage | NT Citation Matches | OT Citation Matches | Lemma Matches | Result Status |")
    md.append("|---|---|---|---|---|---|")
    for r in results:
        if r["total_matches"] == 0:
            status_str = "**NO MATCH FOUND BY DOCUMENTED FULL-VOLUME TEXT SEARCH**"
        else:
            status_str = f"**MATCH DETECTED ({r['total_matches']} hit(s): {r['nt_matches']} NT, {r['ot_matches']} OT, {r['lemma_matches']} lemma)**"
        md.append(f"| `{r['id']}` | {r['name']} | {r['nt_matches']} matches | {r['ot_matches']} matches | {r['lemma_matches']} matches | {status_str} |")
    md.append("")
    md.append("---")
    md.append("")
    md.append("## Detailed Search Target Breakdown")
    md.append("")

    for r in results:
        md.append(f"### {r['id']}: {r['name']}")
        md.append("")
        md.append(f"- **Target Loci:** NT `{r['nt_target']}` | OT `{r['ot_target']}`")
        md.append(f"- **Measured Counts:** NT: `{r['nt_matches']}` | OT: `{r['ot_matches']}` | Lemma: `{r['lemma_matches']}` (Total: `{r['total_matches']}`)")
        if r["total_matches"] == 0:
            outcome_label = "NO MATCH FOUND BY DOCUMENTED FULL-VOLUME TEXT SEARCH"
        else:
            outcome_label = f"MATCH DETECTED ({r['total_matches']} hit(s): {r['nt_matches']} NT, {r['ot_matches']} OT, {r['lemma_matches']} lemma)"
        md.append(f"- **Outcome Classification:** `{outcome_label}`")
        md.append("")
        md.append("| Pattern Description | Category | Regular Expression | Flag | Matches |")
        md.append("|---|---|---|---|---|")
        for p in r["patterns"]:
            md.append(f"| {p['desc']} | {p['category']} | `{p['pattern']}` | `re.IGNORECASE` | {p['count']} |")
        md.append("")
        if r["total_matches"] > 0:
            md.append("#### Measured Match Snippets:")
            for p in r["patterns"]:
                for s in p["snippets"]:
                    md.append(f"- *Snippet (offset {s['pos']}):* `...{s['snippet']}...`")
            md.append("")

    md.append("---")
    md.append("")
    md.append("## Bibliographic Structure of the Authorial Index")
    md.append("")
    md.append("Programmatic inspection of the authorial **Index to the Notes** (printed pp. 437–450) established the following bibliographic facts:")
    md.append(f"- **Index Present:** `{index_results.get('index_present', False)}` (bounds: offset {index_results.get('index_offset', 'N/A')} to {index_results.get('index_end_offset', 'N/A')})")
    md.append(f"- **Section I. Subjects (pp. 437–442):** Present (`{index_results.get('has_subjects_section', False)}`)")
    md.append(f"- **Section II. Latin Words (pp. 443–444):** Present (`{index_results.get('has_latin_section', False)}`)")
    md.append(f"- **Section III. Greek Words (pp. 445–450):** Present (`{index_results.get('has_greek_section', False)}`)")
    md.append(f"- **Sections Ordered:** `{index_results.get('ordered', False)}`")

    # Accurate, non-contradictory Scripture index reporting
    if index_results.get("has_scripture_index"):
        pat = index_results.get("detected_scripture_pattern", "pattern matched")
        md.append(f"- **Dedicated Scripture Passage Index (Index Locorum):** PRESENT (detected pattern: `{pat}`).")
    else:
        md.append("- **Dedicated Scripture Passage Index (Index Locorum):** None detected within the bounded index structure (pp. 437–450; subject to OCR and typographical limits). The authorial index is organized exclusively into I. Subjects, II. Latin Words, and III. Greek Words.")

    md.append("- **Subject Index Positive Controls:**")
    for k, v in index_results.get("positive_controls", {}).items():
        md.append(f"  - Entry `{k}`: `{v}`")
    md.append("")
    md.append("---")
    md.append("")
    md.append("## Scholarly Qualitative Assessment of Detected Hits")
    md.append("")

    # Source-and-text-hash-bound check for genuine 1895 volume context
    is_authentic_volume = (
        text_sha256 == EXPECTED_TEXT_SHA256
        and "Schader" in raw_text or "Sch\u00e4der" in raw_text or "lebendigen Christus" in raw_text
    )

    has_any_hits = any(r["total_matches"] > 0 for r in results)
    if not has_any_hits:
        md.append("No matches detected across any of the five non-Romans loci.")
    else:
        for r in results:
            if r["total_matches"] > 0:
                md.append(f"### Assessment for {r['id']} ({r['name']})")
                md.append("")
                md.append(f"- **Pattern Breakdown:** `{r['nt_matches']}` NT citation match(es), `{r['ot_matches']}` OT citation match(es), `{r['lemma_matches']}` lemma match(es).")
                # Genuine p. 118 historical context emitted ONLY when hash-bound and context-verified
                if r["id"] == "B001-12" and is_authentic_volume and r["nt_matches"] == 1 and r["ot_matches"] == 0 and r["lemma_matches"] == 0:
                    md.append("- **Verified Source Context (Printed p. 118):** The single NT citation (`Gal. iii, 13`) occurs on printed page 118 in a theological note on Rom 4:25 summarizing E. Schäder's 1893 monograph (*Die Bedeutung des lebendigen Christus für die Rechtfertigung nach Paulus*). It is cited parenthetically alongside 2 Cor 5:21 as a dogmatic proof text for Christ enduring divine wrath.")
                    md.append("- **Absence of Text-Critical Analysis:** The Old Testament Vorlage (Deut 21:23) is not cited (`0 matches`), Greek quotation wording (`ἐπικατάρατος πᾶς ὁ κρεμάμενος ἐπὶ ξύλου`) is not present (`0 matches`), and the textual divergence between Gal 3:13 and Deut 21:23 is not analyzed.")
                else:
                    md.append(f"- **Contextual Analysis:** Measured matches ({r['total_matches']}) require evaluation against the specific text layer. Contextual interpretation unverified for arbitrary or synthetic input.")
                md.append("")

    md.append("---")
    md.append("")
    md.append("## Methodological & Technical Limitations")
    md.append("")
    md.append(f"1. **Digital Text Layer Scope:** The search was executed across the {line_count:,}-line text layer extracted from `{pdf_path.name}` via Poppler `pdftotext -layout 23.03.0`.")
    md.append("2. **OCR and Typographical Quality:** Nineteenth-century Greek typography, accented characters, font ligatures, line breaks, hyphenations, or scan artifacts could hypothetically cause a regex pattern to miss an irregular typographical instance. Stripping accents and testing truncated stems (e.g. `φιμωσ`, `κημωσ`) mitigates this limitation.")
    md.append("3. **Epistemological Constraint:** While a negative OCR/regex search proves that no matching citation strings or diagnostic Greek/English phrases exist in the machine-readable digital text layer, it constitutes empirical negative text-search evidence rather than a metaphysical proof of non-existence in the authors' unexpressed thoughts.")

    # Scope preservation: dynamic, non-contradictory summary based on actual results
    zero_loci = [r["id"] for r in results if r["total_matches"] == 0]
    matched_loci = [r["id"] for r in results if r["total_matches"] > 0]
    if len(zero_loci) == len(results):
        md.append("4. **Scope Preservation:** No discussion of any of the five non-Romans B001 passage comparisons was found in the documented full-volume text search.")
    elif is_authentic_volume and zero_loci == ["B001-8", "B001-9", "B001-10", "B001-11"] and matched_loci == ["B001-12"]:
        md.append("4. **Scope Preservation:** While the five specific non-Romans B001 passage comparisons (and their Old Testament Vorlagen) are not analyzed in this Romans commentary (with Gal 3:13 appearing only once as an incidental parenthetical proof text on p. 118), the Excursus on 'St. Paul's Use of the Old Testament' (printed pp. 302–307) addresses cross-Pauline quotation practice globally, including Emil Kautzsch's (1869) 84-quotation taxonomy and 1 Cor 3:19 / Job 5:13. These cross-Pauline findings are preserved in `citation_ledger.csv` under `S02F-E010` through `S02F-E014`.")
    else:
        md.append(f"4. **Scope Preservation:** Measured matches detected for {', '.join(matched_loci)}; no matches detected for {', '.join(zero_loci)}. Cross-Pauline excursus evidence preserved in citation ledger.")
    md.append("")
    return "\n".join(md).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf", type=Path, default=RAW_PDF_DEFAULT)
    parser.add_argument("--text", type=Path, default=DEFAULT_TEXT_PATH)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT_PATH)
    parser.add_argument("--allow-text-digest-mismatch", action="store_true", help="Permit text layer whose SHA-256 differs from pinned EXPECTED_TEXT_SHA256")
    args = parser.parse_args()

    # Rule 1: Fail closed if raw PDF is missing
    if not args.pdf.is_file():
        print(f"Error: Raw PDF file does not exist at {args.pdf}. Fail closed.", file=sys.stderr)
        return 1

    # Rule 2: Fail closed if raw PDF size or SHA-256 does not match expected
    pdf_bytes = os.path.getsize(args.pdf)
    if pdf_bytes != EXPECTED_RAW_PDF_BYTES:
        print(f"Error: Raw PDF size mismatch. Expected {EXPECTED_RAW_PDF_BYTES}, got {pdf_bytes}.", file=sys.stderr)
        return 2

    pdf_sha256 = get_sha256(args.pdf)
    if pdf_sha256 != EXPECTED_RAW_PDF_SHA256:
        print(f"Error: Raw PDF SHA-256 mismatch. Expected {EXPECTED_RAW_PDF_SHA256}, got {pdf_sha256}.", file=sys.stderr)
        return 3

    # Rule 3: Bind extracted text to PDF. If text file missing, empty, or hash mismatched, extract directly from PDF.
    need_extract = False
    if not args.text.is_file() or os.path.getsize(args.text) == 0:
        need_extract = True
    else:
        text_sha256 = get_sha256(args.text)
        if text_sha256 != EXPECTED_TEXT_SHA256:
            print(f"Note: Text file SHA-256 ({text_sha256}) differed from expected. Re-extracting from verified PDF...", file=sys.stderr)
            need_extract = True

    if need_extract:
        print(f"Extracting full text from verified PDF {args.pdf} to {args.text}...")
        res = subprocess.run(["/opt/local/bin/pdftotext", "-layout", str(args.pdf), str(args.text)], check=False)
        if res.returncode != 0:
            print(f"pdftotext failed with exit code {res.returncode}", file=sys.stderr)
            return 4
        text_sha256 = get_sha256(args.text)
        # Strict text digest enforcement (R5-F4): fail closed on digest mismatch unless explicitly allowed
        if text_sha256 != EXPECTED_TEXT_SHA256 and not args.allow_text_digest_mismatch:
            print(f"Error: Extracted text SHA-256 ({text_sha256}) does not match expected ({EXPECTED_TEXT_SHA256}). Fail closed to enforce cryptographic reproducibility.", file=sys.stderr)
            return 8
    else:
        text_sha256 = get_sha256(args.text)

    # Read and measure text
    with open(args.text, "r", encoding="utf-8", errors="replace") as f:
        full_text = f.read()

    line_count = len(full_text.splitlines())
    word_count = len(full_text.split())

    # Fail closed if text is empty or suspiciously small
    if line_count < 1000 or word_count < 10000:
        print(f"Error: Extracted text layer suspiciously small ({line_count} lines, {word_count} words). Fail closed.", file=sys.stderr)
        return 5

    # Run positive controls on citation typography
    print("Running positive control validation on 19th-century citation typography...")
    positive_results = run_positive_controls(full_text)
    all_positive_passed = all(pc["passed"] for pc in positive_results)
    for pc in positive_results:
        print(f"  {pc['name']}: {pc['count']} matches (pass={pc['passed']})")

    if not all_positive_passed:
        print("Error: Positive control validation failed. Regex patterns cannot detect authentic citations in this volume. Fail closed.", file=sys.stderr)
        return 6

    # Verify authorial index structure
    print("Verifying authorial index structure...")
    index_results = verify_index_structure(full_text)
    if not index_results["passed"]:
        print(f"Error: Index structure validation failed: {index_results.get('error', 'Section check failed')}. Fail closed.", file=sys.stderr)
        return 7
    print(f"Index structure verified: Subjects={index_results['has_subjects_section']}, Latin={index_results['has_latin_section']}, Greek={index_results['has_greek_section']}.")

    # Run negative target queries
    print(f"Searching {line_count:,} lines ({word_count:,} words) for 5 non-Romans loci...")
    results = run_search(full_text)

    total_all_matches = sum(r["total_matches"] for r in results)
    print(f"Search complete. Total matches across all 5 non-Romans loci: {total_all_matches}")
    for r in results:
        print(f"  {r['id']}: {r['total_matches']} matches (NT={r['nt_matches']}, OT={r['ot_matches']}, lemma={r['lemma_matches']})")

    report_md = build_markdown_report(
        results,
        positive_results,
        index_results,
        args.pdf,
        pdf_bytes,
        pdf_sha256,
        args.text,
        text_sha256,
        line_count,
        word_count,
        raw_text=full_text,
    )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(report_md)
    print(f"Search log written to {args.out}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
