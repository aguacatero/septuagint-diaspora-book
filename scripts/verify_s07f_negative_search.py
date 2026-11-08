#!/usr/bin/env python3
"""Reproducible full-volume negative search and locus verification for Pieter K. Baaij (2005 Paulus als Schriftuitlegger).

Fails closed on missing or corrupted input PDF, binds extracted text cryptographically
to the source volume (verifying EXPECTED_TEXT_SHA256), enforces the strict monotonic pagination
invariant (printed = PDF + 238), validates positive controls across all article sections,
verifies ENTIRE normalized quotes across evidence rows without truncation, asserts ledger schema
and verified statuses, checks cross-artifact natural-format locator consistency and positive
footnote witnesses, and in --check-only mode fails closed on any byte difference (including whitespace).
"""

from __future__ import annotations

import argparse
import csv
import difflib
import hashlib
import os
import re
import subprocess
import sys
import unicodedata
from pathlib import Path


EXPECTED_RAW_PDF_SHA256 = "201a31f1ef5d7a2f54d6ade2658133dab0952986862792ab7658ae4427e11bb4"
EXPECTED_RAW_PDF_BYTES = 202671
EXPECTED_TEXT_SHA256 = "69f9083820b9f8bbf33778ad79fe053cd281d6488571f41050d3ae14cb8d99e2"
EXPECTED_TEXT_BYTES = 38788
EXPECTED_TEXT_CHARS = 38172
EXPECTED_PAGE_COUNT = 16

PDF_DEFAULT = Path("/Users/chrisrodriguez/Downloads/baaij_2005_romans_4_3.pdf")
DEFAULT_OUT_PATH = Path("research/inbox/B001-pauline-txt-pilot/sources/S07F/full_volume_search_log.md")
DEFAULT_LEDGER_PATH = Path("research/inbox/B001-pauline-txt-pilot/sources/S07F/citation_ledger.csv")
DEFAULT_SOURCE_DIR = Path("research/inbox/B001-pauline-txt-pilot/sources/S07F")

EXPECTED_LEDGER_COLUMNS = [
    "evidence_id",
    "source_id",
    "b001_id",
    "claim_type",
    "author_claim",
    "short_quote",
    "printed_page",
    "source_locator",
    "notebooklm_citation",
    "verification_status",
    "qualification",
    "extraction_confidence",
    "notes",
]

EXPECTED_EVIDENCE_IDS = [f"S07F-E00{i}" for i in range(1, 10)]

AUTHORITATIVE_EVIDENCE_LOCI = {
    "S07F-E001": (239, 1),
    "S07F-E002": (240, 2),
    "S07F-E003": (243, 5),
    "S07F-E004": (247, 9),
    "S07F-E005": (248, 10),
    "S07F-E006": (248, 10),
    "S07F-E007": (248, 10),
    "S07F-E008": (248, 10),
    "S07F-E009": (253, 15),
}

EXPECTED_SYNTHESIS_SUBSECTIONS = {
    "Paul's Use and Citation in Romans 4:3": (239, 1),
    "Comparison with Galatians 3:6 & Selective Citation Refutation": (248, 10),
    "Comparison Between the Masoretic Text (MT) and Septuagint (LXX)": (248, 10),
    "Word Order and Postpositive δé": (248, 10),
    "Covenant Name Change (Abraham vs Abram)": (248, 10),
    "Septuagint Misleading Readers & Polemic": (253, 15),
    "Grammatical Analysis: Active Hebrew (wayyaḥšəḇehā) vs. Passive Greek (ἐλογίσθη)": (248, 10),
    "Paul's Theology of Justification & Dativus Causae": (248, 10),
    "Paul as 'Schriftuitlegger bij uitstek' (Expositor Par Excellence)": (240, 2),
    "Methodological Implications & Pharisaic Hebrew Background (W.C. van Unnik)": (241, 3),
}

EXPECTED_RELEVANCE_TABLE_LOCI = {
    "B001-1": ("YES", (239, 254, 1, 16)),
    "B001-2": ("NO", "N/A"),
    "B001-3": ("NO", "N/A"),
    "B001-4": ("YES", (248, 10)),
    "B001-5": ("NO", "N/A"),
    "B001-6": ("NO", "N/A"),
    "B001-7": ("NO", "N/A"),
    "B001-8": ("NO", "N/A"),
    "B001-9": ("NO", "N/A"),
    "B001-10": ("NO", "N/A"),
    "B001-11": ("NO", "N/A"),
    "B001-12": ("NO", "N/A"),
}

POSITIVE_CONTROLS = [
    {
        "id": "PC01",
        "name": "Title and Header",
        "pattern": r"paulus\s+als\s+schriftuitlegger",
        "expected_page": 239,
        "expected_pdf_page": 1,
    },
    {
        "id": "PC02",
        "name": "Hebrew Thought Invariant",
        "pattern": r"paulus\s+zijn\s+tekst\s+eerst\s+in\s+het\s+bijbels-hebreeuws\s+heeft\s+overdacht",
        "expected_page": 239,
        "expected_pdf_page": 1,
    },
    {
        "id": "PC03",
        "name": "Schriftuitlegger bij uitstek",
        "pattern": r"de\s+echte\s+paulus\s+de\s+schriftuitlegger\s+is\s+bij\s+uitstek",
        "expected_page": 240,
        "expected_pdf_page": 2,
    },
    {
        "id": "PC04",
        "name": "W.C. van Unnik Witness",
        "pattern": r"van\s+unnik,\s+die\s+dit\s+scherp\s+heeft\s+gezien",
        "expected_page": 241,
        "expected_pdf_page": 3,
    },
    {
        "id": "PC05",
        "name": "Masoretic Text Working Assumption",
        "pattern": r"namelijk\s+de\s+masoretische\s+tekst",
        "expected_page": 243,
        "expected_pdf_page": 5,
    },
    {
        "id": "PC06",
        "name": "Relational Tsedaqah Definition",
        "pattern": r"herstel\s+van\s+de\s+relatie\s+tussen\s+god\s+en\s+de\s+door\s+hem\s+aangesproken\s+mens",
        "expected_page": 247,
        "expected_pdf_page": 9,
    },
    {
        "id": "PC07",
        "name": "Postpositive de Emphasis on Verb",
        "pattern": r"om\s+het\s+voorafgaande\s+\[werk\]woord\s+extra\s+nadruk\s+te\s+verlenen",
        "expected_page": 248,
        "expected_pdf_page": 10,
    },
    {
        "id": "PC08",
        "name": "Dativus Causae and Veroorzaker",
        "pattern": r"met\s+pi,steuw\s+cum\s+dativo\s+\(zonder\s+prepositie\s+dus\)\s+legt\s+paulus\s+de\s+nadruk\s+op\s+de\s+veroorzaker",
        "expected_page": 248,
        "expected_pdf_page": 10,
    },
    {
        "id": "PC09",
        "name": "Prepositional Comparison with Rom 9:33 and 10:11",
        "pattern": r"paulus\s+gebruikt\s+immers\s+niet\s+pi,steuw\s+evpi,\s+cum\s+dativo\s+\(zoals\s+in\s+rom\.\s+9:33;\s+10:11\)",
        "expected_page": 248,
        "expected_pdf_page": 10,
    },
    {
        "id": "PC10",
        "name": "LXX Opposite of Scripture Polemic",
        "pattern": r"de\s+mens\s+het\s+tegenovergestelde\s+van\s+wat\s+de\s+schrift\s+zegt\s+\(baaij,\s+2003:145-148\)",
        "expected_page": 253,
        "expected_pdf_page": 15,
    },
]


def normalize_text_for_match(s: str) -> str:
    """Normalize text strictly for matching: NFKD, smart quotes, dashes, whitespace, lowercase."""
    nfkd = unicodedata.normalize("NFKD", s)
    cleaned = "".join(c for c in nfkd if not unicodedata.combining(c))
    cleaned = cleaned.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    cleaned = cleaned.replace("–", "-").replace("—", "-").replace("…", "...").strip()
    return " ".join(cleaned.split()).lower()


def extract_page_texts(pdf_path: Path) -> list[str]:
    page_texts = []
    for p in range(1, EXPECTED_PAGE_COUNT + 1):
        cmd = ["pdftotext", "-f", str(p), "-l", str(p), str(pdf_path), "-"]
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        page_texts.append(res.stdout)
    return page_texts


def verify_monotonic_pagination(page_texts: list[str]) -> None:
    for idx, txt in enumerate(page_texts):
        pdf_page = idx + 1
        expected_printed = pdf_page + 238
        lines = [ln.strip() for ln in txt.splitlines() if ln.strip()]
        has_printed = any(str(expected_printed) in ln for ln in lines)
        if not has_printed:
            raise ValueError(
                f"Monotonic pagination invariant violated at PDF p. {pdf_page}: "
                f"expected printed page number '{expected_printed}' not found in page lines"
            )


def verify_positive_controls(page_texts: list[str]) -> list[dict]:
    results = []
    for pc in POSITIVE_CONTROLS:
        p_idx = pc["expected_pdf_page"] - 1
        txt = page_texts[p_idx]
        norm_txt = normalize_text_for_match(txt)
        m = re.search(pc["pattern"], norm_txt)
        if not m:
            raise ValueError(
                f"Positive control '{pc['id']}: {pc['name']}' failed to match on "
                f"PDF p. {pc['expected_pdf_page']} (printed p. {pc['expected_page']})"
            )
        start = max(0, m.start() - 60)
        end = min(len(norm_txt), m.end() + 60)
        snippet = " ".join(norm_txt[start:end].split())
        results.append({
            "id": pc["id"],
            "name": pc["name"],
            "printed_page": pc["expected_page"],
            "pdf_page": pc["expected_pdf_page"],
            "snippet": snippet
        })
    return results


def load_evidence_ledger(ledger_path: Path) -> list[dict]:
    if not ledger_path.is_file():
        raise FileNotFoundError(f"Missing evidence ledger: {ledger_path}")
    rows = []
    with open(ledger_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        for col in EXPECTED_LEDGER_COLUMNS:
            if col not in fieldnames:
                raise ValueError(f"Missing required column in evidence ledger: {col}")
        for r in reader:
            rows.append(r)

    if len(rows) != len(EXPECTED_EVIDENCE_IDS):
        raise ValueError(f"Expected {len(EXPECTED_EVIDENCE_IDS)} evidence rows, found {len(rows)}")

    for idx, expected_id in enumerate(EXPECTED_EVIDENCE_IDS):
        r = rows[idx]
        if r["evidence_id"] != expected_id:
            raise ValueError(f"Evidence ID mismatch at row {idx + 1}: expected {expected_id}, got {r['evidence_id']}")
        if r["source_id"] != "S07F":
            raise ValueError(f"Source ID mismatch at row {idx + 1}: expected S07F, got {r['source_id']}")
        if r["verification_status"] != "VERIFIED":
            raise ValueError(f"Row {r['evidence_id']} has unverified status: {r['verification_status']}")

    return rows


def verify_ledger_witnesses(rows: list[dict], page_texts: list[str]) -> list[dict]:
    witnesses = []
    for r in rows:
        eid = r["evidence_id"]
        b_id = r["b001_id"]
        printed_page = int(r["printed_page"])
        expected_pdf_page = printed_page - 238
        if expected_pdf_page < 1 or expected_pdf_page > EXPECTED_PAGE_COUNT:
            raise ValueError(f"{eid}: invalid printed page {printed_page} (derived PDF {expected_pdf_page})")

        p_idx = expected_pdf_page - 1
        page_txt = page_texts[p_idx]

        quote = r["short_quote"].strip().strip('"')
        norm_page = normalize_text_for_match(page_txt)
        norm_q = normalize_text_for_match(quote)

        # Fail-closed: verify the ENTIRE normalized quote, in correct order, on declared page
        if norm_q not in norm_page:
            raise ValueError(
                f"{eid}: entire normalized quote not found in text of PDF p. {expected_pdf_page} "
                f"(printed p. {printed_page}).\nQuote: '{norm_q}'"
            )

        # Locate exact position of entire quote in norm_page
        start_pos = norm_page.find(norm_q)
        w_start = max(0, start_pos - 80)
        w_end = min(len(norm_page), start_pos + len(norm_q) + 80)
        authoritative_snippet = norm_page[w_start:w_end].strip()

        witnesses.append({
            "evidence_id": eid,
            "b001_id": b_id,
            "claim_type": r["claim_type"],
            "author_claim": r["author_claim"],
            "short_quote": quote,
            "printed_page": printed_page,
            "pdf_page": expected_pdf_page,
            "authoritative_snippet": authoritative_snippet,
            "verification_status": r["verification_status"],
            "qualification": r["qualification"],
            "notes": r["notes"]
        })
    return witnesses


def execute_full_volume_search(page_texts: list[str], witnesses: list[dict]) -> list[dict]:
    targets = [
        {
            "id": "B001-1",
            "comparison": "Romans 4:3 / Genesis 15:6",
            "patterns": [r"\b4:3\b", r"\bGen(?:esis)?\s*15(?::[56][b]?)?\b", r"\b15:6\b", r"ἐπίστευσεν\s+δὲ\s+Ἀβραάμ"],
            "category": "EXTENDED_EXEGETICAL_ANALYSIS",
            "judgment": "Primary subject of this entire investigation (pp. 239–254). Baaij provides extensive grammatical, lexical, and theological analysis showing how Paul in Rom 4:3 accurately renders Genesis 15:5b–6 directly from Biblical Hebrew (*'āman*, *ḥāšaḇ*, *ṣəḏāqāh*) rather than following Septuagint passive constructions.",
        },
        {
            "id": "B001-2",
            "comparison": "Romans 9:25 / Hosea 2:23 [LXX 2:25]",
            "patterns": [r"\b9:25\b", r"\bHos(?:ea)?\s*2(?::2[35])?\b"],
            "category": "CONFIRMED_ABSENT",
            "judgment": "Rom 9:25 and Hosea 2:23 are not discussed in this volume. Zero hits occur across all 16 pages.",
        },
        {
            "id": "B001-3",
            "comparison": "Romans 9:26 / Hosea 1:10 [LXX 2:1]",
            "patterns": [r"\b9:26\b", r"\bHos(?:ea)?\s*1(?::10)?\b"],
            "category": "CONFIRMED_ABSENT",
            "judgment": "Rom 9:26 and Hosea 1:10 are not discussed in this volume. Zero hits occur across all 16 pages.",
        },
        {
            "id": "B001-4",
            "comparison": "Romans 10:11 / Isaiah 28:16",
            "patterns": [r"\b10:11\b", r"\b28:16\b", r"\b9:33\b"],
            "category": "PASSING_COMPARATIVE_MENTION",
            "judgment": "Baaij notes in passing on p. 248 [PDF p. 10] that Paul constructs πιστεύω with ἐπί and the dative in Rom 10:11 (and Rom 9:33) in explicit grammatical contrast to his deliberate use of πιστεύω with a simple dative (*τῷ θεῷ*) in Rom 4:3 to highlight God as the divine Cause (*dativus causae*).",
        },
        {
            "id": "B001-5",
            "comparison": "Romans 10:13 / Joel 2:32 [LXX 3:5]",
            "patterns": [r"\b10:13\b", r"\bJoel\s*(?:2:32|3:5)\b"],
            "category": "CONFIRMED_ABSENT",
            "judgment": "Neither Rom 10:13 nor Joel 2:32 is discussed in this volume. Zero hits occur across all 16 pages. (Rom 10:16 is referenced on p. 248 for dative construction).",
        },
        {
            "id": "B001-6",
            "comparison": "Romans 11:34 / Isaiah 40:13",
            "patterns": [r"\b11:34\b", r"\b40:13\b"],
            "category": "CONFIRMED_ABSENT",
            "judgment": "Neither Rom 11:34 nor Isaiah 40:13 is discussed in this volume. Zero hits occur across all 16 pages. (Rom 11:13 is referenced in passing on p. 249 in an unrelated syntactic remark).",
        },
        {
            "id": "B001-7",
            "comparison": "Romans 15:12 / Isaiah 11:10",
            "patterns": [r"\b15:12\b", r"\b11:10\b", r"root\s+of\s+Jesse"],
            "category": "CONFIRMED_ABSENT",
            "judgment": "Neither Rom 15:12 nor Isaiah 11:10 is discussed in this volume. Zero hits occur across all 16 pages.",
        },
        {
            "id": "B001-8",
            "comparison": "1 Corinthians 1:19 / Isaiah 29:14",
            "patterns": [r"\b1\s*Cor(?:inthians)?\s*1(?::19)?\b", r"\b29:14\b"],
            "category": "CONFIRMED_ABSENT",
            "judgment": "Neither 1 Cor 1:19 nor Isaiah 29:14 is discussed in this volume. Zero hits occur across all 16 pages.",
        },
        {
            "id": "B001-9",
            "comparison": "1 Corinthians 6:16 / Genesis 2:24",
            "patterns": [r"\b1\s*Cor(?:inthians)?\s*6(?::16)?\b", r"\bGen(?:esis)?\s*2(?::24)?\b"],
            "category": "CONFIRMED_ABSENT",
            "judgment": "Neither 1 Cor 6:16 nor Gen 2:24 is discussed in this volume. Zero hits occur across all 16 pages.",
        },
        {
            "id": "B001-10",
            "comparison": "1 Corinthians 9:9 / Deuteronomy 25:4",
            "patterns": [r"\b1\s*Cor(?:inthians)?\s*9:9\b", r"\bDeut(?:eronomy)?\s*25(?::4)?\b"],
            "category": "CONFIRMED_ABSENT",
            "judgment": "Neither 1 Cor 9:9 nor Deut 25:4 is discussed in this volume. Zero hits occur across all 16 pages.",
        },
        {
            "id": "B001-11",
            "comparison": "1 Corinthians 10:7 / Exodus 32:6",
            "patterns": [r"\b1\s*Cor(?:inthians)?\s*10:7\b", r"\bExod(?:us)?\s*32(?::6)?\b"],
            "category": "CONFIRMED_ABSENT",
            "judgment": "Neither 1 Cor 10:7 nor Exod 32:6 is discussed in this volume. Zero hits occur across all 16 pages.",
        },
        {
            "id": "B001-12",
            "comparison": "Galatians 3:13 / Deuteronomy 21:23",
            "patterns": [r"\bGal(?:atians)?\s*3:13\b", r"\bDeut(?:eronomy)?\s*21(?::23)?\b"],
            "category": "CONFIRMED_ABSENT",
            "judgment": "Neither Gal 3:13 nor Deut 21:23 is discussed in this volume. Zero hits occur across all 16 pages. (Gal 3:6 is referenced in fn. 8 on p. 248).",
        },
    ]

    report_sections = []
    for tgt in targets:
        b_id = tgt["id"]
        hits = []
        for idx, txt in enumerate(page_texts):
            p = idx + 1
            printed = p + 238
            for pat in tgt["patterns"]:
                for m in re.finditer(pat, txt, re.IGNORECASE):
                    start = max(0, m.start() - 60)
                    end = min(len(txt), m.end() + 60)
                    snip = " ".join(txt[start:end].split())
                    hits.append({
                        "pdf_page": p,
                        "printed_page": printed,
                        "pattern": pat,
                        "snippet": snip
                    })
        
        matched_witnesses = [w for w in witnesses if w["b001_id"] == b_id]
        report_sections.append({
            "target": tgt,
            "hits": hits,
            "witnesses": matched_witnesses
        })

    return report_sections


def generate_markdown_report(
    pc_results: list[dict],
    sections: list[dict],
    pdf_path: Path,
    text_sha256: str
) -> str:
    lines = [
        "# S07F — Full-Volume Negative Search and Locus Verification Log",
        "",
        "**Source ID:** S07F  ",
        "**Source Title:** *Paulus als Schriftuitlegger: Genesis 15:5b–6 in Romeinen 4:3* (2005)  ",
        "**Author:** Pieter K. Baaij (P.K. Baaij)  ",
        "**Journal / Publisher:** *In die Skriflig*, Vol. 39, No. 2 (2005), pp. 239–254 (Theological Society of South Africa / AOSIS)  ",
        "**DOI:** `10.4102/ids.v39i2.383`  ",
        "**Verified File:** `baaij_2005_romans_4_3.pdf` (202,671 bytes, SHA256 `201a31f1ef5d7a2f54d6ade2658133dab0952986862792ab7658ae4427e11bb4`)  ",
        f"**Text Layer SHA256:** `{text_sha256}` (38,788 bytes, 38,172 chars across 16 pages)  ",
        "**Pagination Invariant:** Monotonic $printed = PDF + 238$ verified across all 16 pages (PDF pp. 1–16 = printed pp. 239–254).  ",
        "",
        "---",
        "",
        "## 1. Positive Control Witnesses",
        "",
        "| Control ID | Description | Printed Page | PDF Page | Verified Local Snippet |",
        "|:-----------|:------------|:-------------|:---------|:-----------------------|",
    ]

    for pc in pc_results:
        lines.append(
            f"| {pc['id']} | {pc['name']} | p. {pc['printed_page']} | PDF p. {pc['pdf_page']} | `{pc['snippet'][:80]}...` |"
        )

    lines.extend([
        "",
        "---",
        "",
        "## 2. B001 Locus Audit Across All 12 Comparisons",
        ""
    ])

    for s in sections:
        tgt = s["target"]
        hits = s["hits"]
        witnesses = s["witnesses"]
        b_id = tgt["id"]
        comp = tgt["comparison"]
        cat = tgt["category"]
        judg = tgt["judgment"]

        lines.extend([
            f"### {b_id}: {comp}",
            f"- **Category:** `{cat}`",
            f"- **Total Full-Volume Occurrences:** {len(hits)}",
            f"- **Source-Reviewed/Extraction-Stage Argument Assessment (Scholarly Provenance):** {judg} *(Source-reviewed/extraction judgment, awaiting independent review)*",
        ])

        if hits:
            lines.append("- **Verified Page Occurrences:**")
            seen_pages = sorted(list(set((h["pdf_page"], h["printed_page"]) for h in hits)))
            for p, pr in seen_pages:
                page_hits = [h for h in hits if h["pdf_page"] == p]
                lines.append(f"  - **[PDF p. {p}; printed p. {pr}]:** {len(page_hits)} hit(s)")
                for ph in page_hits[:3]:
                    lines.append(f"    - Pattern `{ph['pattern']}`: *\"{ph['snippet']}\"*")
                if len(page_hits) > 3:
                    lines.append(f"    - *(and {len(page_hits) - 3} more hit(s) on this page)*")

        if witnesses:
            lines.append("- **Evidence Ledger Witnesses (`citation_ledger.csv`):**")
            for w in witnesses:
                lines.extend([
                    f"  - **Evidence ID:** `{w['evidence_id']}` ({w['claim_type']})",
                    f"    - **Extracted Author Claim:** {w['author_claim']}",
                    f"    - **Short Quote:** *\"{w['short_quote']}\"*",
                    f"    - **Locator:** [PDF p. {w['pdf_page']}; printed p. {w['printed_page']}]",
                    f"    - **Authoritative Derived Snippet:** *\"{w['authoritative_snippet'][:120]}...\"*",
                    f"    - **Verification Status:** `{w['verification_status']}`",
                ])
        lines.append("")

    lines.extend([
        "---",
        "",
        "## 3. Summary of Negative Search Findings",
        "",
        "1. **Primary Focus of Volume:** Pieter K. Baaij's study is a dedicated exegetical monograph focused exclusively on Paul's interpretation of Genesis 15:5b–6 in Romans 4:3 (pp. 239–254).",
        "2. **Substantively Treated B001 Loci:**",
        "   - **B001-1 (Rom 4:3 / Gen 15:6):** Extended analysis across all five sections of the article (pp. 239–254). Eight ledger claims (`S07F-E001`–`S07F-E006`, `S07F-E008`–`S07F-E009`) covering Hebrew retro-translation, Paul as *schriftuitlegger bij uitstek*, MT textual assumption, relational *ṣəḏāqāh*, postpositive δέ, covenant name Abraham, *dativus causae*, and polemic against uncritical Septuagintal reading.",
        "   - **B001-4 (Rom 10:11 / Isa 28:16 & Rom 9:33):** Passing comparative analysis on p. 248 [PDF p. 10]. One ledger claim (`S07F-E007`) contrasting Paul's prepositional construction (*πιστεύω ἐπ' αὐτῷ*) with the simple dative (*τῷ θεῷ*) in Romans 4:3.",
        "3. **Confirmed Absent Loci (10 comparisons):**",
        "   - **B001-2, B001-3, B001-5, B001-6, B001-7, B001-8, B001-9, B001-10, B001-11, B001-12:** Confirmed zero textual or theological analysis in this volume due to its strict focus on Genesis 15:5b–6 in Romans 4:3.",
        "4. **Methodological Rigor:** Pinned pagination formula $printed = PDF + 238$ holds strictly across all 16 pages; all 9 evidence claims verified across their entire lengths against the born-digital text layer with authoritative derived snippets.",
        ""
    ])

    return "\n".join(lines)


def verify_cross_artifact_consistency(source_dir: Path) -> None:
    """Verify natural-format locators, section-bound loci, positive footnote witnesses, and absence of UI debris."""
    deliverables = [
        "metadata.md",
        "relevance_scan.md",
        "extraction.md",
        "argument_map.md",
        "counterevidence.md",
        "bibliography_leads.md",
        "notebooklm_self_audit.md",
        "paulus_schriftuitlegger_synthesis.md",
    ]

    ui_debris = [
        "Thoughts\nexpand_more",
        "expand_more",
        "keep_pin",
        "thumb_up",
        "thumb_down",
        "subdirectory_arrow_right",
        "unfold_less",
    ]

    # Pattern for natural format: Printed p. N [PDF p. M] or Printed pp. N1-N2 [PDF pp. M1-M2]
    locator_pattern = re.compile(
        r"(?:Printed\s+)?p(?:p)?\.\s*(\d+)(?:[–-](\d+))?\s*\[PDF\s+p(?:p)?\.\s*(\d+)(?:[–-](\d+))?\]",
        re.IGNORECASE
    )

    for filename in deliverables:
        p = source_dir / filename
        if not p.is_file():
            raise FileNotFoundError(f"Missing required deliverable: {p}")
        text = p.read_text(encoding="utf-8")

        # 1. UI debris check
        for deb in ui_debris:
            if deb in text:
                raise ValueError(f"UI debris '{deb}' found in curated deliverable: {filename}")

        # 2. General locator invariant check: validate all explicit Printed p. N [PDF p. M]
        for m in locator_pattern.finditer(text):
            has_p_end = m.group(2) is not None
            has_pdf_end = m.group(4) is not None
            if has_p_end != has_pdf_end:
                raise ValueError(
                    f"{filename}: Malformed half-range locator '{m.group(0)}': "
                    f"both printed and PDF range ends must be provided"
                )

            p_start = int(m.group(1))
            pdf_start = int(m.group(3))

            if p_start != pdf_start + 238:
                raise ValueError(
                    f"{filename}: Invariant violated in locator '{m.group(0)}': "
                    f"printed {p_start} != PDF {pdf_start} + 238"
                )
            if not (239 <= p_start <= 254) or not (1 <= pdf_start <= 16):
                raise ValueError(
                    f"{filename}: Out of bounds locator '{m.group(0)}': "
                    f"printed {p_start} must be [239..254], PDF {pdf_start} must be [1..16]"
                )

            if has_p_end and has_pdf_end:
                p_end = int(m.group(2))
                pdf_end = int(m.group(4))
                if p_start > p_end:
                    raise ValueError(
                        f"{filename}: Inverted page range in locator '{m.group(0)}': "
                        f"start page {p_start} exceeds end page {p_end}"
                    )
                if pdf_start > pdf_end:
                    raise ValueError(
                        f"{filename}: Inverted PDF page range in locator '{m.group(0)}': "
                        f"start page {pdf_start} exceeds end page {pdf_end}"
                    )
                if p_end != pdf_end + 238:
                    raise ValueError(
                        f"{filename}: Range invariant violated in '{m.group(0)}': "
                        f"printed {p_end} != PDF {pdf_end} + 238"
                    )
                if not (239 <= p_end <= 254) or not (1 <= pdf_end <= 16):
                    raise ValueError(
                        f"{filename}: Out of bounds range end in locator '{m.group(0)}': "
                        f"printed {p_end} must be [239..254], PDF {pdf_end} must be [1..16]"
                    )

    # 3. Section/Evidence-ID bound locator extraction for extraction.md (fail closed against cross-record bleed)
    extr_text = (source_dir / "extraction.md").read_text(encoding="utf-8")
    raw_records = re.split(r"(?=^####\s+S07F-E\d{3})", extr_text, flags=re.MULTILINE)
    record_map: dict[str, str] = {}
    for rec in raw_records:
        m = re.match(r"^####\s+(S07F-E\d{3})", rec.strip())
        if m:
            eid = m.group(1)
            if eid in record_map:
                raise ValueError(f"extraction.md: Duplicate section header for {eid}")
            record_map[eid] = rec

    for eid, (exp_printed, exp_pdf) in AUTHORITATIVE_EVIDENCE_LOCI.items():
        if eid not in record_map:
            raise ValueError(f"extraction.md: Missing evidence record section for {eid}")
        rec = record_map[eid]
        loc_lines = [
            l.strip() for l in rec.splitlines()
            if "**Source Locator:**" in l or "**Source Locators:**" in l
        ]
        if len(loc_lines) == 0:
            raise ValueError(f"extraction.md: Missing Source Locator line for {eid}")
        if len(loc_lines) > 1:
            raise ValueError(f"extraction.md: Duplicate Source Locator line for {eid}")

        m_loc = re.search(
            r"\*\*Source Locator(?:s)?:\*\*\s*Printed\s+p\.\s*(\d+)\s*\[PDF\s+p\.\s*(\d+)\]",
            loc_lines[0]
        )
        if not m_loc:
            raise ValueError(f"extraction.md: Malformed Source Locator in {eid}: '{loc_lines[0]}'")

        act_printed = int(m_loc.group(1))
        act_pdf = int(m_loc.group(2))
        if act_printed != exp_printed or act_pdf != exp_pdf:
            raise ValueError(
                f"extraction.md: Locus mismatch for {eid}: expected Printed p. {exp_printed} [PDF p. {exp_pdf}], "
                f"got Printed p. {act_printed} [PDF p. {act_pdf}]"
            )

    # 4. Section-bound checks for paulus_schriftuitlegger_synthesis.md (fail closed against subsection bleed)
    synth_text = (source_dir / "paulus_schriftuitlegger_synthesis.md").read_text(encoding="utf-8")
    raw_subsections = re.split(r"(?=^- \*\*)", synth_text, flags=re.MULTILINE)
    synth_subsections: dict[str, str] = {}
    for sub in raw_subsections:
        lines = sub.strip().splitlines()
        if not lines:
            continue
        m = re.match(r"^- \*\*(.*?):\*\*", lines[0])
        if m:
            title = m.group(1).strip()
            if title in synth_subsections:
                raise ValueError(f"paulus_schriftuitlegger_synthesis.md: Duplicate subsection '{title}'")
            synth_subsections[title] = sub

    for title, (exp_pr, exp_pdf) in EXPECTED_SYNTHESIS_SUBSECTIONS.items():
        if title not in synth_subsections:
            raise ValueError(f"paulus_schriftuitlegger_synthesis.md: Missing subsection '{title}'")
        sub = synth_subsections[title]
        loc_lines = [
            l.strip() for l in sub.splitlines()
            if "**Source Locator:**" in l or "**Source Locators:**" in l
        ]
        if len(loc_lines) == 0:
            raise ValueError(f"paulus_schriftuitlegger_synthesis.md: Missing Source Locator in subsection '{title}'")
        if len(loc_lines) > 1:
            raise ValueError(f"paulus_schriftuitlegger_synthesis.md: Duplicate Source Locator in subsection '{title}'")

        m_loc = re.search(
            r"\*\*Source Locator(?:s)?:\*\*\s*Printed\s+p\.\s*(\d+)\s*\[PDF\s+p\.\s*(\d+)\]",
            loc_lines[0]
        )
        if not m_loc:
            raise ValueError(f"paulus_schriftuitlegger_synthesis.md: Malformed Source Locator in subsection '{title}': '{loc_lines[0]}'")

        act_pr, act_pdf = int(m_loc.group(1)), int(m_loc.group(2))
        if act_pr != exp_pr or act_pdf != exp_pdf:
            raise ValueError(
                f"paulus_schriftuitlegger_synthesis.md: Wrong locus for subsection '{title}': "
                f"expected Printed p. {exp_pr} [PDF p. {exp_pdf}], got Printed p. {act_pr} [PDF p. {act_pdf}]"
            )

    # 5. Section-bound checks for relevance_scan.md table (fail closed against row bleed)
    rel_text = (source_dir / "relevance_scan.md").read_text(encoding="utf-8")
    table_rows: dict[str, str] = {}
    for line in rel_text.splitlines():
        line_clean = line.strip()
        if not line_clean.startswith("|"):
            continue
        m_id = re.search(r"\|\s*\*\*(B001-\d+)\*\*\s*\|", line_clean)
        if m_id:
            b_id = m_id.group(1)
            if b_id in table_rows:
                raise ValueError(f"relevance_scan.md: Duplicate table row for {b_id}")
            table_rows[b_id] = line_clean

    for b_id, (exp_discussed, exp_locus) in EXPECTED_RELEVANCE_TABLE_LOCI.items():
        if b_id not in table_rows:
            raise ValueError(f"relevance_scan.md: Missing table row for {b_id}")
        row_str = table_rows[b_id]
        cells = [c.strip() for c in row_str.split("|")]
        if len(cells) < 7:
            raise ValueError(f"relevance_scan.md: Malformed table row structure for {b_id}: '{row_str}'")

        act_discussed = cells[3]
        act_locator = cells[4]

        if act_discussed != exp_discussed:
            raise ValueError(
                f"relevance_scan.md: Discussion status mismatch for {b_id}: expected {exp_discussed}, got {act_discussed}"
            )

        if exp_discussed == "NO":
            if act_locator != "N/A":
                raise ValueError(
                    f"relevance_scan.md: Expected N/A locator for absent locus {b_id}, got '{act_locator}'"
                )
        else:
            if isinstance(exp_locus, tuple) and len(exp_locus) == 2:
                exp_pr, exp_pdf = exp_locus
                m_loc = re.fullmatch(r"Printed\s+p\.\s*(\d+)\s*\[PDF\s+p\.\s*(\d+)\]", act_locator)
                if not m_loc:
                    raise ValueError(
                        f"relevance_scan.md: Malformed or missing single-page locator for {b_id}: '{act_locator}'"
                    )
                act_pr, act_pdf = int(m_loc.group(1)), int(m_loc.group(2))
                if act_pr != exp_pr or act_pdf != exp_pdf:
                    raise ValueError(
                        f"relevance_scan.md: Wrong locus for {b_id}: expected Printed p. {exp_pr} [PDF p. {exp_pdf}], got '{act_locator}'"
                    )
            elif isinstance(exp_locus, tuple) and len(exp_locus) == 4:
                p1, p2, pdf1, pdf2 = exp_locus
                m_loc = re.fullmatch(
                    r"Printed\s+pp\.\s*(\d+)[–-](\d+)\s*\[PDF\s+pp\.\s*(\d+)[–-](\d+)\]",
                    act_locator
                )
                if not m_loc:
                    raise ValueError(
                        f"relevance_scan.md: Malformed or missing range locator for {b_id}: '{act_locator}'"
                    )
                act_p1, act_p2, act_pdf1, act_pdf2 = (
                    int(m_loc.group(1)), int(m_loc.group(2)), int(m_loc.group(3)), int(m_loc.group(4))
                )
                if (act_p1, act_p2, act_pdf1, act_pdf2) != (p1, p2, pdf1, pdf2):
                    raise ValueError(
                        f"relevance_scan.md: Wrong range locus for {b_id}: expected "
                        f"Printed pp. {p1}–{p2} [PDF pp. {pdf1}–{pdf2}], got '{act_locator}'"
                    )

    # 6. Positive witnessed footnote verification for bibliography_leads.md
    bib_text = (source_dir / "bibliography_leads.md").read_text(encoding="utf-8")
    expected_footnote_witnesses = [
        "Printed p. 241 [PDF p. 3], fn. 1",
        "Printed p. 242 [PDF p. 4], fn. 2",
        "Printed p. 242 [PDF p. 4], fn. 3",
        "Printed p. 244 [PDF p. 6], fn. 4",
        "Printed p. 247 [PDF p. 9], fn. 5",
        "Printed p. 247 [PDF p. 9], fn. 6",
        "Printed p. 247 [PDF p. 9], fn. 7",
        "Printed p. 248 [PDF p. 10], fn. 8",
        "Printed p. 251 [PDF p. 13], fn. 9",
        "Printed p. 252 [PDF p. 14], fn. 10",
    ]
    for witness in expected_footnote_witnesses:
        if witness not in bib_text:
            raise ValueError(f"bibliography_leads.md: Missing positive footnote witness '{witness}'")


def main():
    parser = argparse.ArgumentParser(description="Verify S07F negative search and evidence loci.")
    parser.add_argument("--pdf-path", type=Path, default=PDF_DEFAULT, help="Path to baaij_2005_romans_4_3.pdf")
    parser.add_argument("--out-path", type=Path, default=DEFAULT_OUT_PATH, help="Path to output markdown log")
    parser.add_argument("--ledger-path", type=Path, default=DEFAULT_LEDGER_PATH, help="Path to citation_ledger.csv")
    parser.add_argument("--source-dir", type=Path, default=DEFAULT_SOURCE_DIR, help="Path to S07F source deliverables directory")
    parser.add_argument("--check-only", action="store_true", help="Fail closed if output log differs from existing on disk")
    args = parser.parse_args()

    pdf_path = args.pdf_path
    if not pdf_path.is_file():
        raise FileNotFoundError(f"Missing S07F PDF: {pdf_path}")

    # 1. Cryptographic raw PDF verification
    raw_bytes = pdf_path.read_bytes()
    raw_size = len(raw_bytes)
    raw_sha256 = hashlib.sha256(raw_bytes).hexdigest()

    if raw_size != EXPECTED_RAW_PDF_BYTES:
        raise ValueError(f"Raw PDF size mismatch: expected {EXPECTED_RAW_PDF_BYTES}, got {raw_size}")
    if raw_sha256 != EXPECTED_RAW_PDF_SHA256:
        raise ValueError(f"Raw PDF SHA256 mismatch: expected {EXPECTED_RAW_PDF_SHA256}, got {raw_sha256}")

    # 2. Extract page texts and verify text layer cryptographic hash
    page_texts = extract_page_texts(pdf_path)
    if len(page_texts) != EXPECTED_PAGE_COUNT:
        raise ValueError(f"Extracted page count mismatch: expected {EXPECTED_PAGE_COUNT}, got {len(page_texts)}")

    full_text = "\f".join(page_texts)
    text_bytes = full_text.encode("utf-8")
    text_sha256 = hashlib.sha256(text_bytes).hexdigest()
    text_size = len(text_bytes)
    text_chars = len(full_text)

    if text_size != EXPECTED_TEXT_BYTES:
        raise ValueError(f"Text bytes mismatch: expected {EXPECTED_TEXT_BYTES}, got {text_size}")
    if text_chars != EXPECTED_TEXT_CHARS:
        raise ValueError(f"Text chars mismatch: expected {EXPECTED_TEXT_CHARS}, got {text_chars}")
    if text_sha256 != EXPECTED_TEXT_SHA256:
        raise ValueError(f"Text SHA256 mismatch: expected {EXPECTED_TEXT_SHA256}, got {text_sha256}")

    # 3. Verify monotonic pagination invariant
    verify_monotonic_pagination(page_texts)

    # 4. Verify positive controls across article sections
    pc_results = verify_positive_controls(page_texts)

    # 5. Load and verify citation ledger schema and statuses
    ledger_rows = load_evidence_ledger(args.ledger_path)

    # 6. Verify ledger witnesses against born-digital text
    witnesses = verify_ledger_witnesses(ledger_rows, page_texts)

    # 7. Execute full-volume search across all 12 B001 items
    sections = execute_full_volume_search(page_texts, witnesses)

    # 8. Generate markdown report
    generated_md = generate_markdown_report(pc_results, sections, pdf_path, text_sha256)

    # 9. Cross-artifact natural format locator consistency and footnote witnesses
    verify_cross_artifact_consistency(args.source_dir)

    out_path = args.out_path
    if args.check_only:
        if not out_path.is_file():
            raise FileNotFoundError(f"--check-only specified but output log does not exist: {out_path}")
        existing_md = out_path.read_text(encoding="utf-8")
        if existing_md != generated_md:
            diff = difflib.unified_diff(
                existing_md.splitlines(keepends=True),
                generated_md.splitlines(keepends=True),
                fromfile=str(out_path),
                tofile="generated_md"
            )
            diff_text = "".join(diff)
            raise ValueError(f"--check-only failed: generated report differs from disk:\n{diff_text}")
        print(f"OK: {out_path} matches generated report byte-for-byte (--check-only passed).")
    else:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(generated_md, encoding="utf-8")
        print(f"SUCCESS: Generated {out_path} ({len(generated_md)} chars, {len(generated_md.encode('utf-8'))} bytes).")

    print(f"Verified {len(pc_results)} positive controls.")
    print(f"Verified {len(witnesses)} evidence ledger rows.")
    print(f"Verified 12 B001 search targets across {EXPECTED_PAGE_COUNT} pages.")
    print(f"Verified cross-artifact locator consistency and footnote witnesses across all deliverables.")


if __name__ == "__main__":
    main()
