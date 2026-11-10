#!/usr/bin/env python3
"""Reproducible full-volume negative search and locus verification for J. Paul Tanner (2005 Hosea in Romans 9).

Fails closed on missing or corrupted input PDF, binds extracted text cryptographically
to the source volume (verifying EXPECTED_TEXT_SHA256), enforces the strict monotonic pagination
invariant (printed = PDF + 94), validates positive controls across all article sections,
verifies ENTIRE normalized quotes across evidence rows without truncation, asserts ledger schema
and verified statuses, checks cross-artifact natural-format locator consistency and positive
footnote witnesses, enforces section/evidence-ID bound extraction with field-bound quotation
and exact parsed locator matching, subsection-bound synthesis, and structured bibliographic
witness authentication with authoritative author/title/container/exact-delimited footnote checks,
and in --check-only mode fails closed on any byte difference (including whitespace).
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


EXPECTED_RAW_PDF_SHA256 = "88263a92f5edf99217238123198ff580a91203ecca68111aaed614a1a932a64a"
EXPECTED_RAW_PDF_BYTES = 1440727
EXPECTED_TEXT_SHA256 = "1950b4cfd479b85424a770453a960740ee41e1524201e9e1383865d3efa609a9"
EXPECTED_TEXT_BYTES = 46121
EXPECTED_TEXT_CHARS = 46039
EXPECTED_PAGE_COUNT = 16
EXPECTED_TOTAL_PAGES = 17

PDF_DEFAULT = Path("/Users/chrisrodriguez/Downloads/tanner_2005_hosea_romans_9.pdf")
DEFAULT_OUT_PATH = Path("research/inbox/B001-pauline-txt-pilot/sources/S08F/full_volume_search_log.md")
DEFAULT_LEDGER_PATH = Path("research/inbox/B001-pauline-txt-pilot/sources/S08F/citation_ledger.csv")
DEFAULT_SOURCE_DIR = Path("research/inbox/B001-pauline-txt-pilot/sources/S08F")

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

EXPECTED_EVIDENCE_IDS = [f"S08F-E00{i}" for i in range(1, 9)]

AUTHORITATIVE_EVIDENCE_LOCI = {
    "S08F-E001": {"printed": (98,), "pdf": (4,), "fn": None, "locator": "Printed p. 98 [PDF p. 4]"},
    "S08F-E002": {"printed": (99,), "pdf": (5,), "fn": 4, "locator": "Printed p. 99 [PDF p. 5, fn. 4]"},
    "S08F-E003": {"printed": (100,), "pdf": (6,), "fn": None, "locator": "Printed p. 100 [PDF p. 6]"},
    "S08F-E004": {"printed": (102,), "pdf": (8,), "fn": None, "locator": "Printed p. 102 [PDF p. 8]"},
    "S08F-E005": {"printed": (110,), "pdf": (16,), "fn": None, "locator": "Printed p. 110 [PDF p. 16]"},
    "S08F-E006": {"printed": (103,), "pdf": (9,), "fn": None, "locator": "Printed p. 103 [PDF p. 9]"},
    "S08F-E007": {"printed": (96,), "pdf": (2,), "fn": None, "locator": "Printed p. 96 [PDF p. 2]"},
    "S08F-E008": {"printed": (99,), "pdf": (5,), "fn": None, "locator": "Printed p. 99 [PDF p. 5]"},
}

EXPECTED_EVIDENCE_B001_MAP = {
    "S08F-E001": "B001-2",
    "S08F-E002": "B001-2",
    "S08F-E003": "B001-3",
    "S08F-E004": "B001-2, B001-3",
    "S08F-E005": "B001-2, B001-3",
    "S08F-E006": "B001-2, B001-3",
    "S08F-E007": "B001-2, B001-3",
    "S08F-E008": "B001-2",
}

EXPECTED_SYNTHESIS_SUBSECTIONS = {
    "Composite Quotation Structure": "Printed p. 98 [PDF p. 4]",
    "Relation to Isaiah 10:22–23 and 1:9 in Romans 9:27–29": "Printed pp. 97–98 [PDF pp. 3–4]",
    "Structural Sandwiching in Romans 9": "Printed p. 97 [PDF p. 3]",
    "Dependence on a Greek Vorlage": "Printed p. 99 [PDF p. 5]",
    "Reversal of Clause Order in Hosea 2:23": "Printed p. 99 [PDF p. 5]",
    "Modification of the Main Verb (*καλέσω* vs. *ἐρῶ* / *'āmar*)": "Printed p. 99 [PDF p. 5], fn. 4",
    "Selective Omission of Hosea 1:10a": "Printed p. 99 [PDF p. 5]",
    "Original Historical Setting of Hosea 1–2": "Printed pp. 99–100 [PDF pp. 5–6]",
    "The Core Hermeneutical Tension": "Printed p. 101 [PDF p. 7]",
    "Tanner’s Solution: Direct, Partial Phase of Fulfillment": "Printed pp. 101–102 [PDF pp. 7–8]",
    "The Mechanism of Status Change": "Printed pp. 106–108 [PDF pp. 12–14], p. 110 [PDF p. 16]",
    "Progressive Revelation & Historic Realization": "Printed pp. 103–105 [PDF pp. 9–11]",
    "Rejection of Replacement Theology (Supersessionism)": "Printed pp. 95–96 [PDF pp. 1–2], p. 101 [PDF p. 7], pp. 109–110 [PDF pp. 15–16]",
    "Distinction Between Shared Spiritual Blessings & National Promises": "Printed p. 106 [PDF p. 12], fn. 16; p. 110 [PDF p. 16]",
}

EXPECTED_RELEVANCE_TABLE_LOCI = {
    "B001-1": ("NO", "N/A"),
    "B001-2": ("YES", (98, 110, 4, 16)),
    "B001-3": ("YES", (98, 110, 4, 16)),
    "B001-4": ("NO", "N/A"),
    "B001-5": ("NO", "N/A"),
    "B001-6": ("NO", "N/A"),
    "B001-7": ("NO", "N/A"),
    "B001-8": ("NO", "N/A"),
    "B001-9": ("NO", "N/A"),
    "B001-10": ("NO", "N/A"),
    "B001-11": ("NO", "N/A"),
    "B001-12": ("NO", "N/A"),
}

EXPECTED_BIBLIOGRAPHY_LEADS = [
    {
        "header": "Walter C. Kaiser Jr. (1989)",
        "author": "Walter C. Kaiser Jr.",
        "title": '*"An Assessment of \'Replacement Theology\'"*',
        "year": 1989,
        "container": "Mishkan",
        "printed_pages": (95,),
        "pdf_pages": (1,),
        "footnote": 1,
    },
    {
        "header": "Alva J. McClain (1973)",
        "author": "Alva J. McClain",
        "title": "*The Gospel of God’s Grace*",
        "year": 1973,
        "container": "Moody Press",
        "printed_pages": (98,),
        "pdf_pages": (4,),
        "footnote": 2,
    },
    {
        "header": "John A. Battle, Jr. (1981)",
        "author": "John A. Battle, Jr.",
        "title": '*"Paul\'s Use of the Old Testament in Romans 9:25–26"*',
        "year": 1981,
        "container": "Grace Theological Journal",
        "printed_pages": (98,),
        "pdf_pages": (4,),
        "footnote": 2,
    },
    {
        "header": "W. Edward Glenny (1995)",
        "author": "W. Edward Glenny",
        "title": '*"The \'People of God\' in Romans 9:25–26"*',
        "year": 1995,
        "container": "Bibliotheca Sacra",
        "printed_pages": (98,),
        "pdf_pages": (4,),
        "footnote": 3,
    },
    {
        "header": "Douglas J. Moo (1996) — Romans 9:24–26 Calling of Gentiles",
        "author": "Douglas J. Moo",
        "title": "*The Epistle to the Romans* (NICNT)",
        "year": 1996,
        "container": "Eerdmans",
        "printed_pages": (98,),
        "pdf_pages": (4,),
        "footnote": 3,
    },
    {
        "header": "David L. Turner (1985)",
        "author": "David L. Turner",
        "title": '*"The Continuity of Scripture and Eschatology: Key Hermeneutical Issues"*',
        "year": 1985,
        "container": "Grace Theological Journal",
        "printed_pages": (98,),
        "pdf_pages": (4,),
        "footnote": 3,
    },
    {
        "header": "Douglas J. Moo (1996) — Textual Modification of καλέσω",
        "author": "Douglas J. Moo",
        "title": "*The Epistle to the Romans* (NICNT)",
        "year": 1996,
        "container": "Eerdmans",
        "printed_pages": (99,),
        "pdf_pages": (5,),
        "footnote": 4,
    },
    {
        "header": "Douglas J. Moo (1996) — Hermeneutical Supposition of Replacement",
        "author": "Douglas J. Moo",
        "title": "*The Epistle to the Romans* (NICNT)",
        "year": 1996,
        "container": "Eerdmans",
        "printed_pages": (101,),
        "pdf_pages": (7,),
        "footnote": 6,
    },
    {
        "header": "Robert B. Chisholm Jr. (1985)",
        "author": "Robert B. Chisholm Jr.",
        "title": '*"Hosea"*, in John F. Walvoord & Roy B. Zuck (eds.), *The Bible Knowledge Commentary, Old Testament*',
        "year": 1985,
        "container": "Victor",
        "printed_pages": (101, 102),
        "pdf_pages": (7, 8),
        "footnote": 8,
    },
    {
        "header": "John A. Witmer (1983)",
        "author": "John A. Witmer",
        "title": '*"Romans"*, in John F. Walvoord & Roy B. Zuck (eds.), *The Bible Knowledge Commentary, New Testament*',
        "year": 1983,
        "container": "Victor",
        "printed_pages": (101, 102),
        "pdf_pages": (7, 8),
        "footnote": 8,
    },
    {
        "header": "S. Lewis Johnson (1992)",
        "author": "S. Lewis Johnson",
        "title": '*"Evidence from Romans 9–11"*, in Donald K. Campbell & Jeffrey L. Townsend (eds.), *A Case for Premillennialism: A New Consensus*',
        "year": 1992,
        "container": "Moody Press",
        "printed_pages": (102,),
        "pdf_pages": (8,),
        "footnote": 8,
    },
    {
        "header": "Douglas J. Moo (1996) — Rejection of Mere Analogy",
        "author": "Douglas J. Moo",
        "title": "*The Epistle to the Romans* (NICNT)",
        "year": 1996,
        "container": "Eerdmans",
        "printed_pages": (102,),
        "pdf_pages": (8,),
        "footnote": 8,
    },
    {
        "header": "W. Edward Glenny (1992)",
        "author": "W. Edward Glenny",
        "title": '*"The Israelite Imagery of 1 Peter 2"*, in Craig A. Blaising & Darrell L. Bock (eds.), *Dispensationalism, Israel and the Church*',
        "year": 1992,
        "container": "Zondervan",
        "printed_pages": (102,),
        "pdf_pages": (8,),
        "footnote": 9,
    },
    {
        "header": "Roy B. Zuck (1991)",
        "author": "Roy B. Zuck",
        "title": "*Basic Bible Interpretation*",
        "year": 1991,
        "container": "Victor",
        "printed_pages": (103,),
        "pdf_pages": (9,),
        "footnote": 10,
    },
    {
        "header": "David K. Lowery (1983)",
        "author": "David K. Lowery",
        "title": '*"1 Corinthians"*, in John F. Walvoord & Roy B. Zuck (eds.), *The Bible Knowledge Commentary, New Testament*',
        "year": 1983,
        "container": "Victor",
        "printed_pages": (103,),
        "pdf_pages": (9,),
        "footnote": 11,
    },
    {
        "header": "Rodney J. Decker (1995)",
        "author": "Rodney J. Decker",
        "title": '*"The Church\'s Relationship to the New Covenant"*',
        "year": 1995,
        "container": "Bibliotheca Sacra",
        "printed_pages": (104,),
        "pdf_pages": (10,),
        "footnote": 12,
    },
    {
        "header": "Richard Daniels (1999)",
        "author": "Richard Daniels",
        "title": '*"How Does the Church Relate to the New Covenant? or, Whose New Covenant Is It, Anyway?"*',
        "year": 1999,
        "container": "Faith and Mission",
        "printed_pages": (104,),
        "pdf_pages": (10,),
        "footnote": 13,
    },
    {
        "header": "Larry D. Pettegrew (1993)",
        "author": "Larry D. Pettegrew",
        "title": "*The New Covenant Ministry of the Holy Spirit*",
        "year": 1993,
        "container": "University Press of America",
        "printed_pages": (104, 105),
        "pdf_pages": (10, 11),
        "footnote": 14,
    },
    {
        "header": "Paul R. Thorsell (1998)",
        "author": "Paul R. Thorsell",
        "title": '*"The Spirit in the Present Age: Preliminary Fulfillment of the Predicted New Covenant according to Paul"*',
        "year": 1998,
        "container": "Journal for the Evangelical Theological Society",
        "printed_pages": (105,),
        "pdf_pages": (11,),
        "footnote": 14,
    },
    {
        "header": "Douglas Stuart (1987)",
        "author": "Douglas Stuart",
        "title": "*Hosea–Jonah* (Word Biblical Commentary)",
        "year": 1987,
        "container": "Word Books",
        "printed_pages": (106,),
        "pdf_pages": (12,),
        "footnote": 16,
    },
    {
        "header": "Gary W. Light (1993)",
        "author": "Gary W. Light",
        "title": '*"The New Covenant in the Book of Hosea"*',
        "year": 1993,
        "container": "Review and Expositor",
        "printed_pages": (106,),
        "pdf_pages": (12,),
        "footnote": 17,
    },
    {
        "header": "Leon J. Wood (1985)",
        "author": "Leon J. Wood",
        "title": '*"Hosea"*, in Frank E. Gaebelein (ed.), *The Expositor’s Bible Commentary*, Vol. 7',
        "year": 1985,
        "container": "Zondervan",
        "printed_pages": (107,),
        "pdf_pages": (13,),
        "footnote": 18,
    },
    {
        "header": "Francis I. Andersen & David Noel Freedman (1980)",
        "author": "Francis I. Andersen & David Noel Freedman",
        "title": "*Hosea* (Anchor Bible, Vol. 24)",
        "year": 1980,
        "container": "Doubleday",
        "printed_pages": (107,),
        "pdf_pages": (13,),
        "footnote": 18,
    },
    {
        "header": "Hans Walter Wolff (1974)",
        "author": "Hans Walter Wolff",
        "title": "*Hosea* (Hermeneia Commentary, trans. Gary Stensell)",
        "year": 1974,
        "container": "Fortress Press",
        "printed_pages": (107,),
        "pdf_pages": (13,),
        "footnote": 18,
    },
    {
        "header": "Andrew G. Shead (2000)",
        "author": "Andrew G. Shead",
        "title": '*"The Covenant and Pauline Hermeneutics"*, in Peter Bolt & Mark Thompson (eds.), *The Gospel to the Nations: Perspectives on Paul’s Mission*',
        "year": 2000,
        "container": "InterVarsity Press",
        "printed_pages": (108, 109),
        "pdf_pages": (14, 15),
        "footnote": 21,
    },
    {
        "header": "George Eldon Ladd (1977)",
        "author": "George Eldon Ladd",
        "title": '*"Historic Premillennialism"*, in Robert G. Clouse (ed.), *The Meaning of the Millennium: Four Views*',
        "year": 1977,
        "container": "InterVarsity Press",
        "printed_pages": (109,),
        "pdf_pages": (15,),
        "footnote": 22,
    },
]

POSITIVE_CONTROLS = [
    {
        "id": "PC01",
        "name": "Title and Journal Header",
        "pattern": r"the\s+new\s+covenant\s+and\s+paul's\s+quotations\s+from\s+hosea\s+in\s+romans\s+9:25-26",
        "expected_page": 95,
        "expected_pdf_page": 1,
    },
    {
        "id": "PC02",
        "name": "Remnant Distinction in Romans 11",
        "pattern": r"distinction\s+between\s+ethnic\s+israel\s+in\s+unbelief\s+and\s+the\s+believing\s+israelite\s+\"remnant\.\"",
        "expected_page": 96,
        "expected_pdf_page": 2,
    },
    {
        "id": "PC03",
        "name": "Gentile Vessels of Mercy",
        "pattern": r"god's\s+\"vessels\s+of\s+mercy\"\s+include\s+gentiles",
        "expected_page": 98,
        "expected_pdf_page": 4,
    },
    {
        "id": "PC04",
        "name": "Greek Vorlage and Clause Inversion",
        "pattern": r"paul\s+quoted\s+from\s+a\s+greek\s+rendering\s+of\s+hosea\s+and\s+the\s+fact\s+that\s+he\s+reversed\s+the\s+order\s+of\s+the\s+clauses",
        "expected_page": 99,
        "expected_pdf_page": 5,
    },
    {
        "id": "PC05",
        "name": "Moo Footnote on kaleso Substitution",
        "pattern": r"paul\s+also\s+switched\s+hosea's\s+\"i\s+will\s+say\"\s+to\s+[u\"]l\s+will\s+call,\"\s+probably\s+in\s+view\s+of\s+romans\s+9:24",
        "expected_page": 99,
        "expected_pdf_page": 5,
    },
    {
        "id": "PC06",
        "name": "Original Context Excludes Gentiles",
        "pattern": r"nothing\s+in\s+the\s+context\s+of\s+these\s+passages\s+makes\s+reference\s+to\s+gentiles",
        "expected_page": 100,
        "expected_pdf_page": 6,
    },
    {
        "id": "PC07",
        "name": "Direct Partial Fulfillment Assertion",
        "pattern": r"conversion\s+of\s+gentiles\s+is\s+a\s+direct\s+fulfillment\s+of\s+hosea's\s+prophecy\s+\(though\s+not\s+the\s+complete\s+fulfillment\)",
        "expected_page": 102,
        "expected_pdf_page": 8,
    },
    {
        "id": "PC08",
        "name": "Israel Still Means Israel Invariant",
        "pattern": r"paul\s+was\s+not\s+operating\s+by\s+some\s+new\s+theological\s+dictum\s+whereby\s+israel\s+no\s+longer\s+meant\s+israel",
        "expected_page": 103,
        "expected_pdf_page": 9,
    },
    {
        "id": "PC09",
        "name": "Hosea 2:23 Context and New Covenant",
        "pattern": r"examination\s+of\s+the\s+context\s+of\s+hosea\s+2:23\s+reveals\s+that\s+the\s+new\s+covenant\s+is\s+in\s+view",
        "expected_page": 106,
        "expected_pdf_page": 12,
    },
    {
        "id": "PC10",
        "name": "New Covenant Foundation for Status Change",
        "pattern": r"it\s+was\s+the\s+new\s+covenant\s+that\s+made\s+it\s+possible\s+for\s+the\s+jewish\s+remnant\s+to\s+become\s+\"the\s+people\s+of\s+god\.\"",
        "expected_page": 110,
        "expected_pdf_page": 16,
    },
]


def normalize_text_for_match(s: str) -> str:
    """Normalize text strictly for matching: NFKD, smart quotes, dashes, whitespace, lowercase."""
    nfkd = unicodedata.normalize("NFKD", s)
    cleaned = "".join(c for c in nfkd if not unicodedata.combining(c))
    cleaned = cleaned.replace(r'\"', '"').replace(r"\'", "'")
    cleaned = cleaned.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    cleaned = cleaned.replace("–", "-").replace("—", "-").replace("…", "...").strip()
    return " ".join(cleaned.split()).lower()


def parse_source_locator(loc_str: str) -> dict:
    """Parse a strict source locator string into its component parts.

    Grammar enforces:
      - Exactly one bracketed PDF locator pair [PDF ...]
      - At most one footnote reference total (either inside or outside the bracket)
      - Strictly monotonic pagination derivation (printed = PDF + 94)
      - No duplicate, conflicting, or unparsed trailing fragments
    Permissible forms:
      Printed p. 98 [PDF p. 4]
      Printed p. 99 [PDF p. 5, fn. 4]
      Printed pp. 97–98 [PDF pp. 3–4]
      Printed p. 98 [PDF p. 4], fn. 2
      Printed p. 98 [PDF p. 4], fn. 2; Section 2
      Printed pp. 101–102 [PDF pp. 7–8], fn. 8; Section 4
    Fails closed on missing delimiters, duplicate references, or trailing fragments.
    """
    loc = loc_str.strip()

    # 1. Structural delimiter checks
    if loc.count("[") != 1 or loc.count("]") != 1:
        raise ValueError(f"Expected exactly one bracketed PDF locator pair [PDF ...], got: '{loc_str}'")

    fn_matches = re.findall(r"\bfn\.\s*(\d+)\b", loc)
    if len(fn_matches) > 1:
        raise ValueError(f"Conflicting duplicate footnote references in locator: '{loc_str}'")

    # 2. Strict grammar matching entire string from start to finish
    grammar = (
        r"^Printed\s+(?:p\.\s*(\d+)|pp\.\s*(\d+)[–-](\d+))\s+"
        r"\[PDF\s+(?:p\.\s*(\d+)|pp\.\s*(\d+)[–-](\d+))(?:,\s*fn\.\s*(\d+))?\]"
        r"(?:,\s*fn\.\s*(\d+))?"
        r"(?:;\s*Section\s*(\d+))?$"
    )
    m = re.match(grammar, loc)
    if not m:
        raise ValueError(f"Malformed source locator grammar or unparsed trailing fragments: '{loc_str}'")

    # 3. Parse printed pages
    if m.group(1):
        prn_pages = (int(m.group(1)),)
    else:
        prn_pages = (int(m.group(2)), int(m.group(3)))

    # 4. Parse PDF pages
    if m.group(4):
        pdf_pages = (int(m.group(4)),)
    else:
        pdf_pages = (int(m.group(5)), int(m.group(6)))

    if len(prn_pages) != len(pdf_pages):
        raise ValueError(f"Printed and PDF page range arity mismatch: {prn_pages} vs {pdf_pages}")

    # 5. Monotonic formula check: printed = PDF + 94
    for prn, pdf in zip(prn_pages, pdf_pages):
        if prn - 94 != pdf:
            raise ValueError(f"Monotonic pagination mismatch: printed {prn} != PDF {pdf} + 94 in '{loc_str}'")

    # 6. Footnote parsing
    fn_in = int(m.group(7)) if m.group(7) else None
    fn_out = int(m.group(8)) if m.group(8) else None
    if fn_in is not None and fn_out is not None:
        raise ValueError(f"Conflicting duplicate footnote references in locator: '{loc_str}'")
    fn = fn_in if fn_in is not None else fn_out

    section = int(m.group(9)) if m.group(9) else None

    return {
        "raw": loc,
        "printed_pages": prn_pages,
        "pdf_pages": pdf_pages,
        "footnote": fn,
        "section": section,
    }


def extract_page_texts(pdf_path: Path) -> list[str]:
    page_texts = []
    for p in range(1, EXPECTED_PAGE_COUNT + 1):
        cmd = ["pdftotext", "-f", str(p), "-l", str(p), str(pdf_path), "-"]
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        page_texts.append(res.stdout)
    return page_texts


def verify_monotonic_pagination(page_texts: list[str]) -> None:
    """Verify strictly monotonic pagination invariant (printed = PDF + 94) across all 16 article pages.

    Enforces that each page contains its expected printed numeral (PDF + 94) within the top 3
    lines (header margin region), either as an isolated numeral line, a line starting with the numeral,
    a line ending with the numeral, or in the volume header of page 95. Also verifies that a documented
    running journal marker (BiBLiOTHECA SACRA or article title) is within the top 3 lines.
    Fails closed if the numeral only appears embedded in mid-body or footer prose.
    """
    for idx, txt in enumerate(page_texts):
        pdf_page = idx + 1
        expected_printed = pdf_page + 94
        expected_str = str(expected_printed)
        lines = [ln.strip() for ln in txt.splitlines() if ln.strip()]

        top_lines = lines[:3]
        if not top_lines:
            raise ValueError(f"PDF p. {pdf_page} has no text lines.")

        has_numeral_in_header = False
        for ln in top_lines:
            if ln == expected_str:
                has_numeral_in_header = True
                break
            if ln.startswith(expected_str + " ") or ln.startswith(expected_str + "\t"):
                has_numeral_in_header = True
                break
            if ln.endswith(" " + expected_str) or ln.endswith("\t" + expected_str):
                has_numeral_in_header = True
                break
            if pdf_page == 1 and f": {expected_str}-" in ln:
                has_numeral_in_header = True
                break

        if not has_numeral_in_header:
            raise ValueError(
                f"Monotonic pagination invariant violated at PDF p. {pdf_page}: "
                f"expected printed page number '{expected_printed}' not found in header margin (top 3 lines: {top_lines})"
            )

        has_journal_marker = any(
            (re.search(r"b[il]bl[il]otheca\s+sacra", ln, re.IGNORECASE) or
             re.search(r"the\s+new\s+covenant\s+and\s+paul", ln, re.IGNORECASE))
            for ln in top_lines
        )
        if not has_journal_marker:
            raise ValueError(
                f"Monotonic pagination invariant violated at PDF p. {pdf_page}: "
                f"missing running journal marker in header lines: {top_lines}"
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
        if r["source_id"] != "S08F":
            raise ValueError(f"Source ID mismatch at row {idx + 1}: expected S08F, got {r['source_id']}")
        if r["verification_status"] != "VERIFIED":
            raise ValueError(f"Row {r['evidence_id']} has unverified status: {r['verification_status']}")

    return rows


def verify_ledger_witnesses(rows: list[dict], page_texts: list[str]) -> list[dict]:
    witnesses = []
    for r in rows:
        eid = r["evidence_id"]
        b_id = r["b001_id"].strip()
        printed_str = r["printed_page"].strip()

        # Enforce valid b001_id specification
        expected_b001 = EXPECTED_EVIDENCE_B001_MAP.get(eid)
        if b_id != expected_b001:
            raise ValueError(f"{eid}: b001_id mismatch: expected '{expected_b001}', got '{b_id}'")

        auth_spec = AUTHORITATIVE_EVIDENCE_LOCI.get(eid)
        if not auth_spec:
            raise ValueError(f"Missing authoritative locus specification for {eid}")

        # Parse and verify source_locator strictly
        parsed_loc = parse_source_locator(r["source_locator"])

        # Parse declared printed_page column
        if "-" in printed_str or "–" in printed_str:
            parts = re.split(r"[–-]", printed_str)
            exp_prn = (int(parts[0]), int(parts[1]))
            exp_pdf = (int(parts[0]) - 94, int(parts[1]) - 94)
            if exp_pdf[0] < 1 or exp_pdf[1] > EXPECTED_PAGE_COUNT or exp_pdf[0] > exp_pdf[1]:
                raise ValueError(f"{eid}: invalid printed page range {printed_str}")
            page_slice = page_texts[exp_pdf[0] - 1 : exp_pdf[1]]
            combined_txt = " ".join(page_slice)
            norm_target_text = normalize_text_for_match(combined_txt)
            display_printed = f"{parts[0]}–{parts[1]}"
            display_pdf = f"{exp_pdf[0]}–{exp_pdf[1]}"
        else:
            prn_val = int(printed_str)
            exp_prn = (prn_val,)
            exp_pdf = (prn_val - 94,)
            if exp_pdf[0] < 1 or exp_pdf[0] > EXPECTED_PAGE_COUNT:
                raise ValueError(f"{eid}: invalid printed page {prn_val}")
            txt = page_texts[exp_pdf[0] - 1]
            norm_target_text = normalize_text_for_match(txt)
            display_printed = str(prn_val)
            display_pdf = str(exp_pdf[0])

        # Enforce parsed locator values match declared printed_page and derivation
        if parsed_loc["printed_pages"] != exp_prn:
            raise ValueError(
                f"{eid}: source_locator printed pages {parsed_loc['printed_pages']} != declared printed_page '{printed_str}'"
            )
        if parsed_loc["pdf_pages"] != exp_pdf:
            raise ValueError(
                f"{eid}: source_locator PDF pages {parsed_loc['pdf_pages']} != expected {exp_pdf} (printed - 94)"
            )

        # Enforce parsed locator matches authoritative specification exactly
        if parsed_loc["printed_pages"] != auth_spec["printed"]:
            raise ValueError(
                f"{eid}: authoritative printed mismatch: expected {auth_spec['printed']}, got {parsed_loc['printed_pages']}"
            )
        if parsed_loc["pdf_pages"] != auth_spec["pdf"]:
            raise ValueError(
                f"{eid}: authoritative PDF mismatch: expected {auth_spec['pdf']}, got {parsed_loc['pdf_pages']}"
            )
        if parsed_loc["footnote"] != auth_spec["fn"]:
            raise ValueError(
                f"{eid}: authoritative footnote mismatch: expected {auth_spec['fn']}, got {parsed_loc['footnote']}"
            )

        quote = r["short_quote"].strip()
        norm_quote = normalize_text_for_match(quote)
        if len(norm_quote) < 15:
            raise ValueError(f"{eid}: Quote is too short for reliable witness matching: '{quote}'")

        if norm_quote not in norm_target_text:
            raise ValueError(
                f"{eid}: Quote text not found on declared printed p. {display_printed} [PDF p. {display_pdf}]:\n"
                f"Quote: '{quote}'\n"
                f"Normalized: '{norm_quote}'"
            )

        witnesses.append({
            "evidence_id": eid,
            "b001_id": b_id,
            "claim_type": r["claim_type"],
            "printed_page": display_printed,
            "pdf_page": display_pdf,
            "short_quote": quote,
            "author_claim": r["author_claim"],
            "locator": r["source_locator"],
        })
    return witnesses


def execute_full_volume_search(page_texts: list[str], witnesses: list[dict]) -> list[dict]:
    targets = [
        {
            "id": "B001-1",
            "comparison": "Romans 4:3 / Genesis 15:6",
            "patterns": [r"\b4:3\b", r"\bGen(?:esis)?\s*15(?::6)?\b"],
            "category": "CONFIRMED_ABSENT",
            "judgment": "Neither Rom 4:3 nor Gen 15:6 is discussed in this volume. Zero hits occur across all 16 article pages.",
        },
        {
            "id": "B001-2",
            "comparison": "Romans 9:25 / Hosea 2:23",
            "patterns": [r"\b9:25\b", r"\bHos(?:ea)?\s*2:23\b"],
            "category": "EXTENDED_DISCUSSION",
            "judgment": "Substantive extended discussion across pp. 95–110. Tanner analyzes Paul's Greek Vorlage, clause inversion, verb change to kaleso, and New Covenant framework.",
        },
        {
            "id": "B001-3",
            "comparison": "Romans 9:26 / Hosea 1:10",
            "patterns": [r"\b9:26\b", r"\bHos(?:ea)?\s*1:10\b"],
            "category": "EXTENDED_DISCUSSION",
            "judgment": "Substantive extended discussion across pp. 98–101. Tanner analyzes the selective omission of Hosea 1:10a and the New Covenant application of Hosea 1:10b to Gentiles.",
        },
        {
            "id": "B001-4",
            "comparison": "Romans 10:11 / Isaiah 28:16",
            "patterns": [r"\b10:11\b", r"\bIsa(?:iah)?\s*28:16\b"],
            "category": "CONFIRMED_ABSENT",
            "judgment": "Neither Rom 10:11 nor Isaiah 28:16 is discussed in this volume. Zero hits occur across all 16 article pages.",
        },
        {
            "id": "B001-5",
            "comparison": "Romans 10:13 / Joel 2:32",
            "patterns": [r"\b10:13\b", r"\bJoel\s*2:32\b"],
            "category": "CONFIRMED_ABSENT",
            "judgment": "Neither Rom 10:13 nor Joel 2:32 is discussed in this volume. Zero hits occur across all 16 article pages.",
        },
        {
            "id": "B001-6",
            "comparison": "Romans 11:34 / Isaiah 40:13",
            "patterns": [r"\b11:34\b", r"\bIsa(?:iah)?\s*40:13\b"],
            "category": "CONFIRMED_ABSENT",
            "judgment": "Neither Rom 11:34 nor Isaiah 40:13 is discussed in this volume. Zero hits occur across all 16 article pages.",
        },
        {
            "id": "B001-7",
            "comparison": "Romans 15:12 / Isaiah 11:10",
            "patterns": [r"\b15:12\b", r"\bIsa(?:iah)?\s*11:10\b"],
            "category": "CONFIRMED_ABSENT",
            "judgment": "Neither Rom 15:12 nor Isaiah 11:10 is discussed in this volume. Zero hits occur across all 16 article pages.",
        },
        {
            "id": "B001-8",
            "comparison": "1 Corinthians 1:19 / Isaiah 29:14",
            "patterns": [r"\b1\s*Cor(?:inthians)?\s*1:19\b", r"\bIsa(?:iah)?\s*29:14\b"],
            "category": "CONFIRMED_ABSENT",
            "judgment": "Neither 1 Cor 1:19 nor Isaiah 29:14 is discussed in this volume. Zero hits occur across all 16 article pages.",
        },
        {
            "id": "B001-9",
            "comparison": "1 Corinthians 6:16 / Genesis 2:24",
            "patterns": [r"\b1\s*Cor(?:inthians)?\s*6:16\b", r"\bGen(?:esis)?\s*2:24\b"],
            "category": "CONFIRMED_ABSENT",
            "judgment": "Neither 1 Cor 6:16 nor Gen 2:24 is discussed in this volume. Zero hits occur across all 16 article pages.",
        },
        {
            "id": "B001-10",
            "comparison": "1 Corinthians 9:9 / Deuteronomy 25:4",
            "patterns": [r"\b1\s*Cor(?:inthians)?\s*9:9\b", r"\bDeut(?:eronomy)?\s*25:4\b"],
            "category": "CONFIRMED_ABSENT",
            "judgment": "Neither 1 Cor 9:9 nor Deut 25:4 is discussed in this volume. Zero hits occur across all 16 article pages.",
        },
        {
            "id": "B001-11",
            "comparison": "1 Corinthians 10:7 / Exodus 32:6",
            "patterns": [r"\b1\s*Cor(?:inthians)?\s*10:7\b", r"\bExod(?:us)?\s*32:6\b"],
            "category": "CONFIRMED_ABSENT",
            "judgment": "Neither 1 Cor 10:7 nor Exod 32:6 is discussed in this volume. Zero hits occur across all 16 article pages.",
        },
        {
            "id": "B001-12",
            "comparison": "Galatians 3:13 / Deuteronomy 21:23",
            "patterns": [r"\bGal(?:atians)?\s*3:13\b", r"\bDeut(?:eronomy)?\s*21:23\b"],
            "category": "CONFIRMED_ABSENT",
            "judgment": "Neither Gal 3:13 nor Deut 21:23 is discussed in this volume. Zero hits occur across all 16 article pages.",
        },
    ]

    sections = []
    for tgt in targets:
        b_id = tgt["id"]
        hits = []
        for idx, txt in enumerate(page_texts):
            pdf_page = idx + 1
            printed_page = pdf_page + 94
            for pat in tgt["patterns"]:
                for m in re.finditer(pat, txt, re.IGNORECASE):
                    start = max(0, m.start() - 40)
                    end = min(len(txt), m.end() + 40)
                    snip = " ".join(txt[start:end].split())
                    hits.append({
                        "printed_page": printed_page,
                        "pdf_page": pdf_page,
                        "pattern": pat,
                        "snippet": snip
                    })

        cat = tgt["category"]
        if cat == "CONFIRMED_ABSENT" and hits:
            raise ValueError(f"Target {b_id} expected absent but found {len(hits)} hits: {hits}")
        if cat == "EXTENDED_DISCUSSION" and not hits:
            raise ValueError(f"Target {b_id} expected extended discussion but found 0 hits")

        sections.append({
            "id": b_id,
            "comparison": tgt["comparison"],
            "category": cat,
            "judgment": tgt["judgment"],
            "hits": hits,
            "witnesses": [
                w for w in witnesses
                if b_id in [x.strip() for x in w["b001_id"].split(",")]
            ]
        })

    return sections


def generate_markdown_report(
    pc_results: list[dict],
    sections: list[dict],
    witnesses: list[dict],
    pdf_path: Path,
    text_sha256: str
) -> str:
    lines = [
        "# S08F — Full-Volume Negative Search and Locus Verification Log",
        "",
        "**Source Volume:** J. Paul Tanner, *The New Covenant and Paul’s Quotations from Hosea in Romans 9:25–26*, *Bibliotheca Sacra*, Vol. 162, No. 645 (January–March 2005), pp. 95–110.",
        f"**Source PDF:** `{pdf_path.name}` ({EXPECTED_RAW_PDF_BYTES:,} bytes, SHA-256 `{EXPECTED_RAW_PDF_SHA256}`)",
        f"**Text Layer Digest:** SHA-256 `{text_sha256}` ({EXPECTED_TEXT_CHARS:,} chars, {EXPECTED_TEXT_BYTES:,} bytes across {EXPECTED_PAGE_COUNT} article pages)",
        f"**Pagination Invariant:** Monotonic $printed = PDF + 94$ across all 16 article pages (PDF pp. 1–16 = printed pp. 95–110; PDF p. 17 is ATLA user preservation notice).",
        "",
        "---",
        "",
        "## 1. Positive Controls Across Article Sections",
        "",
        "| ID | Section / Concept | Printed Page | PDF Page | Normalized Text Witness | Status |",
        "| :--- | :--- | :--- | :--- | :--- | :--- |",
    ]

    for pc in pc_results:
        lines.append(
            f"| `{pc['id']}` | {pc['name']} | p. {pc['printed_page']} | PDF p. {pc['pdf_page']} | \"{pc['snippet'][:60]}...\" | `VERIFIED` |"
        )

    lines.extend([
        "",
        "---",
        "",
        "## 2. Evidence Ledger Physical Quote Witness Verification",
        "",
        "| Evidence ID | B001 Locus | Claim Type | Locus | Short Quote Witness | Verification Status |",
        "| :--- | :--- | :--- | :--- | :--- | :--- |",
    ])

    for w in witnesses:
        lines.append(
            f"| `{w['evidence_id']}` | `{w['b001_id']}` | {w['claim_type']} | Printed p. {w['printed_page']} [PDF p. {w['pdf_page']}] | \"{w['short_quote'][:50]}...\" | `VERIFIED` |"
        )

    lines.extend([
        "",
        "---",
        "",
        "## 3. Systematic Locus Verification Across All 12 B001 Targets",
        "",
        "| B001 ID | Comparison | Category | Hit Count | Authoritative Determination |",
        "| :--- | :--- | :--- | :--- | :--- |",
    ])

    for sec in sections:
        lines.append(
            f"| `{sec['id']}` | {sec['comparison']} | `{sec['category']}` | {len(sec['hits'])} hits | {sec['judgment']} |"
        )

    lines.extend([
        "",
        "---",
        "",
        "## 4. Itemized Target Search Findings",
        "",
    ])

    for sec in sections:
        lines.extend([
            f"### {sec['id']}: {sec['comparison']}",
            f"- **Classification:** `{sec['category']}`",
            f"- **Hit Count:** {len(sec['hits'])} verified hits across {EXPECTED_PAGE_COUNT} article pages",
            f"- **Scholarly Determination:** {sec['judgment']}",
        ])
        if sec["witnesses"]:
            lines.append("- **Associated Evidence Rows:**")
            for w in sec["witnesses"]:
                lines.append(
                    f"  - `{w['evidence_id']}`: Printed p. {w['printed_page']} [PDF p. {w['pdf_page']}] — \"{w['short_quote'][:70]}...\""
                )
        if sec["hits"]:
            lines.append("- **Sample Text Hits:**")
            for h in sec["hits"][:5]:
                lines.append(
                    f"  - Printed p. {h['printed_page']} [PDF p. {h['pdf_page']}]: `{h['snippet']}`"
                )
        lines.append("")

    return "\n".join(lines)


def verify_cross_artifact_consistency(source_dir: Path, ledger_rows: list[dict] | None = None) -> None:
    """Verify strict cross-artifact consistency across all S08F deliverables.

    Enforces:
    1. metadata.md bibliographic citation details.
    2. extraction.md section/evidence-ID bound locator, quote, and B001 ID binding:
       - field-bound exact quotation verification.
       - strict parsed locator matching against authoritative loci and ledger.
    3. tanner_hosea_new_covenant_synthesis.md subsection-bound page reference assertions.
    4. relevance_scan.md table discussion categories and range locators.
    5. bibliography_leads.md structured witness authentication:
       - authoritative author and title metadata fields.
       - exact publication year container.
       - exact delimited footnote number and canonical page numbers (prefix-safe).
    """
    if ledger_rows is None:
        ledger_rows = load_evidence_ledger(source_dir / "citation_ledger.csv")
    ledger_map = {r["evidence_id"]: r for r in ledger_rows}

    # 1. Verify metadata.md
    meta_text = (source_dir / "metadata.md").read_text(encoding="utf-8")
    for phrase in ["J. Paul Tanner", "The New Covenant and Paul's Quotations", "Bibliotheca Sacra", "95-110", "16"]:
        norm_p = normalize_text_for_match(phrase)
        if norm_p not in normalize_text_for_match(meta_text):
            raise ValueError(f"metadata.md: Missing required phrase '{phrase}'")

    # 2. Section/evidence-ID-bound and field-bound verification of extraction.md
    ext_text = (source_dir / "extraction.md").read_text(encoding="utf-8")
    ext_blocks = re.split(r"(?=####\s+S08F-E\d{3})", ext_text)
    ext_block_map: dict[str, str] = {}
    for blk in ext_blocks:
        m = re.search(r"####\s+(S08F-E\d{3})", blk)
        if m:
            eid = m.group(1)
            if eid in ext_block_map:
                raise ValueError(f"extraction.md: Duplicate section block for {eid}")
            ext_block_map[eid] = blk

    for eid in EXPECTED_EVIDENCE_IDS:
        if eid not in ext_block_map:
            raise ValueError(f"extraction.md: Missing discrete section block for evidence ID {eid}")
        blk = ext_block_map[eid]
        row = ledger_map[eid]
        auth_spec = AUTHORITATIVE_EVIDENCE_LOCI[eid]

        # Enforce exactly one Proposed Evidence ID matching block ID
        m_prop = re.findall(r"-\s+\*\*Proposed Evidence ID:\*\*\s*`([^`]+)`", blk)
        if len(m_prop) != 1 or m_prop[0] != eid:
            raise ValueError(f"extraction.md [{eid}]: Expected exactly one Proposed Evidence ID `{eid}`, got {m_prop}")

        # Enforce B001 Passage ID matching ledger
        raw_b001 = re.findall(r"-\s+\*\*B001 Passage ID:\*\*\s*([^\n(]+)", blk)
        m_b001 = [x.strip("` ").strip() for x in raw_b001]
        if len(m_b001) != 1 or m_b001[0] != row["b001_id"].strip():
            raise ValueError(f"extraction.md [{eid}]: B001 ID mismatch: expected '{row['b001_id']}', got {m_b001}")

        # Enforce exactly one Source Locator line matching authoritative locator and ledger
        loc_lines = re.findall(r"-\s+\*\*Source Locator:\*\*\s*([^\n]+)", blk)
        if len(loc_lines) != 1:
            raise ValueError(f"extraction.md [{eid}]: Expected exactly one Source Locator, found {len(loc_lines)}")
        act_loc = loc_lines[0].strip()
        parsed_ext_loc = parse_source_locator(act_loc)
        parsed_ledger_loc = parse_source_locator(row["source_locator"])

        if parsed_ext_loc["printed_pages"] != auth_spec["printed"]:
            raise ValueError(
                f"extraction.md [{eid}]: Printed page mismatch: expected {auth_spec['printed']}, got {parsed_ext_loc['printed_pages']}"
            )
        if parsed_ext_loc["pdf_pages"] != auth_spec["pdf"]:
            raise ValueError(
                f"extraction.md [{eid}]: PDF page mismatch: expected {auth_spec['pdf']}, got {parsed_ext_loc['pdf_pages']}"
            )
        if parsed_ext_loc["footnote"] != auth_spec["fn"]:
            raise ValueError(
                f"extraction.md [{eid}]: Footnote mismatch: expected {auth_spec['fn']}, got {parsed_ext_loc['footnote']}"
            )

        if (
            parsed_ext_loc["printed_pages"] != parsed_ledger_loc["printed_pages"] or
            parsed_ext_loc["pdf_pages"] != parsed_ledger_loc["pdf_pages"] or
            parsed_ext_loc["footnote"] != parsed_ledger_loc["footnote"]
        ):
            raise ValueError(
                f"extraction.md [{eid}]: Parsed locator does not match ledger:\n  Ext: {parsed_ext_loc}\n  Ledger: {parsed_ledger_loc}"
            )

        # Enforce Printed Page Number matching ledger
        m_page = re.findall(r"-\s+\*\*Printed Page Number:\*\*\s*(\d+)", blk)
        if len(m_page) != 1 or int(m_page[0]) != int(row["printed_page"]):
            raise ValueError(f"extraction.md [{eid}]: Printed page mismatch: expected {row['printed_page']}, got {m_page}")

        # Enforce Short Exact Quotation strictly field-bound matching ledger
        quote_lines = re.findall(r"-\s+\*\*Short Exact Quotation:\*\*\s*([^\n]+)", blk)
        if len(quote_lines) != 1:
            raise ValueError(f"extraction.md [{eid}]: Expected exactly one Short Exact Quotation line, found {len(quote_lines)}")
        raw_field_quote = quote_lines[0].strip()
        clean_field_quote = raw_field_quote.strip(' "')
        clean_row_quote = row["short_quote"].strip(' "')
        norm_row_quote = normalize_text_for_match(clean_row_quote)
        norm_field_quote = normalize_text_for_match(clean_field_quote)
        if norm_row_quote != norm_field_quote:
            raise ValueError(
                f"extraction.md [{eid}]: Short Exact Quotation field mismatch:\n  Ledger: '{norm_row_quote}'\n  Ext field: '{norm_field_quote}'"
            )

    # 3. Subsection-bound verification of tanner_hosea_new_covenant_synthesis.md
    synth_text = (source_dir / "tanner_hosea_new_covenant_synthesis.md").read_text(encoding="utf-8")
    synth_blocks = re.split(r"(?=###\s+)", synth_text)
    synth_block_map: dict[str, str] = {}
    for blk in synth_blocks:
        m = re.match(r"###\s+([^\n]+)", blk)
        if m:
            sub_title = m.group(1).strip()
            synth_block_map[normalize_text_for_match(sub_title)] = blk

    for sub_title, expected_loc in EXPECTED_SYNTHESIS_SUBSECTIONS.items():
        norm_title = normalize_text_for_match(sub_title)
        if norm_title not in synth_block_map:
            raise ValueError(f"synthesis.md: Missing subsection '{sub_title}'")
        sub_blk = synth_block_map[norm_title]
        norm_expected_loc = normalize_text_for_match(expected_loc)
        norm_sub_blk = normalize_text_for_match(sub_blk)
        if norm_expected_loc not in norm_sub_blk:
            raise ValueError(
                f"synthesis.md: Subsection '{sub_title}' missing expected locus '{expected_loc}' within its subsection block"
            )

    # 4. Verify relevance_scan.md table loci
    rel_text = (source_dir / "relevance_scan.md").read_text(encoding="utf-8")
    for b_id, spec in EXPECTED_RELEVANCE_TABLE_LOCI.items():
        disc, loc_spec = spec
        m_row = re.search(
            rf"\|\s*\*+{b_id}\*+\s*\|\s*[^|]+\|\s*({disc})\s*\|\s*([^|]+)\|\s*([^|]+)\|",
            rel_text
        )
        if not m_row:
            raise ValueError(f"relevance_scan.md: Missing or malformed table row for {b_id}")
        act_disc = m_row.group(1).strip()
        act_locator = m_row.group(2).strip()
        if act_disc != disc:
            raise ValueError(f"relevance_scan.md: Wrong discussion status for {b_id}: expected {disc}, got {act_disc}")

        if disc == "YES":
            p1, p2, pdf1, pdf2 = loc_spec
            m_loc = re.search(
                r"Printed pp\.\s*(\d+)[–-](\d+)\s*\[PDF pp\.\s*(\d+)[–-](\d+)\]",
                act_locator
            )
            if not m_loc:
                raise ValueError(f"relevance_scan.md: Malformed range locator for {b_id}: '{act_locator}'")
            act_p1, act_p2, act_pdf1, act_pdf2 = (
                int(m_loc.group(1)), int(m_loc.group(2)), int(m_loc.group(3)), int(m_loc.group(4))
            )
            if (act_p1, act_p2, act_pdf1, act_pdf2) != (p1, p2, pdf1, pdf2):
                raise ValueError(
                    f"relevance_scan.md: Wrong range locus for {b_id}: expected "
                    f"Printed pp. {p1}–{p2} [PDF pp. {pdf1}–{pdf2}], got '{act_locator}'"
                )

    # 5. Structured bibliographic witness authentication in bibliography_leads.md
    bib_text = (source_dir / "bibliography_leads.md").read_text(encoding="utf-8")
    bib_blocks = re.split(r"(?=###\s+)", bib_text)
    bib_block_map: dict[str, str] = {}
    for blk in bib_blocks:
        m = re.match(r"###\s+([^\n]+)", blk)
        if m:
            entry_title = m.group(1).strip()
            bib_block_map[normalize_text_for_match(entry_title)] = blk

    for lead in EXPECTED_BIBLIOGRAPHY_LEADS:
        lead_header = lead["header"]
        norm_lead_header = normalize_text_for_match(lead_header)
        if norm_lead_header not in bib_block_map:
            raise ValueError(f"bibliography_leads.md: Missing structured bibliographic lead '{lead_header}'")
        blk = bib_block_map[norm_lead_header]

        # 1. Enforce Author line
        auth_lines = re.findall(r"-\s+\*\*Authors?:\*\*\s*([^\n]+)", blk)
        if len(auth_lines) != 1:
            raise ValueError(
                f"bibliography_leads.md [{lead_header}]: Expected exactly one Author line, found {len(auth_lines)}"
            )
        act_auth = auth_lines[0].strip()
        exp_auth = lead["author"]
        if normalize_text_for_match(exp_auth) != normalize_text_for_match(act_auth):
            raise ValueError(
                f"bibliography_leads.md [{lead_header}]: Author mismatch: expected '{exp_auth}', got '{act_auth}'"
            )

        # 2. Enforce Title line
        title_lines = re.findall(r"-\s+\*\*Title:\*\*\s*([^\n]+)", blk)
        if len(title_lines) != 1:
            raise ValueError(
                f"bibliography_leads.md [{lead_header}]: Expected exactly one Title line, found {len(title_lines)}"
            )
        act_title = title_lines[0].strip()
        exp_title = lead["title"]
        if normalize_text_for_match(exp_title) != normalize_text_for_match(act_title):
            raise ValueError(
                f"bibliography_leads.md [{lead_header}]: Title mismatch: expected '{exp_title}', got '{act_title}'"
            )

        # 3. Enforce Header Year, Publication Year line, and Primary Container
        m_hdr_year = re.search(r"\((\d{4})\)", lead_header)
        if not m_hdr_year:
            raise ValueError(f"bibliography_leads.md [{lead_header}]: Cannot parse 4-digit year in header")
        hdr_year = int(m_hdr_year.group(1))
        if hdr_year != lead["year"]:
            raise ValueError(
                f"bibliography_leads.md [{lead_header}]: Header year {hdr_year} does not match authoritative year {lead['year']}"
            )

        pub_lines = re.findall(r"-\s+\*\*Publication Year:\*\*\s*([^\n]+)", blk)
        if len(pub_lines) != 1:
            raise ValueError(
                f"bibliography_leads.md [{lead_header}]: Expected exactly one Publication Year line, found {len(pub_lines)}"
            )
        act_pub = pub_lines[0].strip()
        m_pub = re.match(r"^(\d{4})\s*\((.*)\)$", act_pub)
        if not m_pub:
            raise ValueError(
                f"bibliography_leads.md [{lead_header}]: Malformed Publication Year field: '{act_pub}'"
            )
        act_year = int(m_pub.group(1))
        if act_year != lead["year"]:
            raise ValueError(
                f"bibliography_leads.md [{lead_header}]: Publication year mismatch: expected {lead['year']}, got {act_year}"
            )

        details = m_pub.group(2).strip()
        if details.startswith("*"):
            mj = re.match(r"^\*([^*]+)\*", details)
            if not mj:
                raise ValueError(
                    f"bibliography_leads.md [{lead_header}]: Malformed italicized journal container in '{details}'"
                )
            act_container = mj.group(1).strip()
        else:
            mb = re.match(r"^[^:]+:\s*([^,]+)", details)
            if not mb:
                raise ValueError(
                    f"bibliography_leads.md [{lead_header}]: Malformed book publication container in '{details}'"
                )
            act_container = mb.group(1).strip()

        if normalize_text_for_match(lead["container"]) != normalize_text_for_match(act_container):
            raise ValueError(
                f"bibliography_leads.md [{lead_header}]: Primary container mismatch: expected '{lead['container']}', got '{act_container}'"
            )

        # 4. Enforce exact parsed Source Locator (printed pages, PDF pages, footnote)
        loc_lines = re.findall(r"-\s+\*\*Source Locator:\*\*\s*([^\n]+)", blk)
        if len(loc_lines) != 1:
            raise ValueError(
                f"bibliography_leads.md [{lead_header}]: Expected exactly one Source Locator, found {len(loc_lines)}"
            )
        act_loc = loc_lines[0].strip()
        parsed_bib_loc = parse_source_locator(act_loc)

        if parsed_bib_loc["printed_pages"] != lead["printed_pages"]:
            raise ValueError(
                f"bibliography_leads.md [{lead_header}]: Printed page mismatch: expected {lead['printed_pages']}, got {parsed_bib_loc['printed_pages']}"
            )
        if parsed_bib_loc["pdf_pages"] != lead["pdf_pages"]:
            raise ValueError(
                f"bibliography_leads.md [{lead_header}]: PDF page mismatch: expected {lead['pdf_pages']}, got {parsed_bib_loc['pdf_pages']}"
            )
        if parsed_bib_loc["footnote"] != lead["footnote"]:
            raise ValueError(
                f"bibliography_leads.md [{lead_header}]: Footnote mismatch: expected {lead['footnote']}, got {parsed_bib_loc['footnote']}"
            )


def main():
    parser = argparse.ArgumentParser(description="Verify S08F negative search and evidence loci.")
    parser.add_argument("--pdf-path", type=Path, default=PDF_DEFAULT, help="Path to tanner_2005_hosea_romans_9.pdf")
    parser.add_argument("--out-path", type=Path, default=DEFAULT_OUT_PATH, help="Path to output markdown log")
    parser.add_argument("--ledger-path", type=Path, default=DEFAULT_LEDGER_PATH, help="Path to citation_ledger.csv")
    parser.add_argument("--source-dir", type=Path, default=DEFAULT_SOURCE_DIR, help="Path to S08F source deliverables directory")
    parser.add_argument("--check-only", action="store_true", help="Fail closed if output log differs from existing on disk")
    args = parser.parse_args()

    pdf_path = args.pdf_path
    if not pdf_path.is_file():
        raise FileNotFoundError(f"Missing S08F PDF: {pdf_path}")

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
    generated_md = generate_markdown_report(pc_results, sections, witnesses, pdf_path, text_sha256)

    # 9. Cross-artifact natural format locator consistency, section/field-bound extraction, and structured bibliographic authentication
    verify_cross_artifact_consistency(args.source_dir, ledger_rows)

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
    print(f"Verified cross-artifact section/field-bound consistency, subsection-bound synthesis, and structured bibliographic witnesses across all deliverables.")


if __name__ == "__main__":
    main()
