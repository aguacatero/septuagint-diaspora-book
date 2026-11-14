#!/usr/bin/env python3
"""Reproducible full-volume negative search and locus verification for Willem Oliver (2015 Romans 10:5–13).

Fails closed on missing or corrupted input PDF, binds extracted text cryptographically
to the source volume (verifying EXPECTED_TEXT_SHA256), enforces the strict monotonic pagination
invariant (printed = PDF, offset = 0), validates positive controls across all article pages,
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


EXPECTED_RAW_PDF_SHA256 = "8148a72d1e0a3138df70a19156b8adbcd4482311bce4b3254fb2746175e31789"
EXPECTED_RAW_PDF_BYTES = 602923
EXPECTED_TEXT_SHA256 = "462c388b7004f8de5f7d117596ac3878eed8a2b3605a939fd12bee8a5e911cfc"
EXPECTED_TEXT_BYTES = 74465
EXPECTED_TEXT_CHARS = 68862
EXPECTED_PAGE_COUNT = 12
EXPECTED_TOTAL_PAGES = 12

REPO_ROOT = Path(__file__).resolve().parents[1]
PDF_DEFAULT = Path("/Users/chrisrodriguez/Downloads/oliver_2015_romans_10.pdf")
DEFAULT_OUT_PATH = Path("research/inbox/B001-pauline-txt-pilot/sources/S09F/full_volume_search_log.md")
DEFAULT_LEDGER_PATH = Path("research/inbox/B001-pauline-txt-pilot/sources/S09F/citation_ledger.csv")
DEFAULT_SOURCE_DIR = Path("research/inbox/B001-pauline-txt-pilot/sources/S09F")

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

EXPECTED_EVIDENCE_IDS = [f"S09F-E{i:03d}" for i in range(1, 11)]

AUTHORITATIVE_EVIDENCE_LOCI = {
    "S09F-E001": {"printed": (5,), "pdf": (5,), "fn": None, "locator": "Printed p. 5 [PDF p. 5]"},
    "S09F-E002": {"printed": (4,), "pdf": (4,), "fn": None, "locator": "Printed p. 4 [PDF p. 4]"},
    "S09F-E003": {"printed": (4,), "pdf": (4,), "fn": None, "locator": "Printed p. 4 [PDF p. 4]"},
    "S09F-E004": {"printed": (9,), "pdf": (9,), "fn": None, "locator": "Printed p. 9 [PDF p. 9]"},
    "S09F-E005": {"printed": (7,), "pdf": (7,), "fn": None, "locator": "Printed p. 7 [PDF p. 7]"},
    "S09F-E006": {"printed": (10,), "pdf": (10,), "fn": None, "locator": "Printed p. 10 [PDF p. 10]"},
    "S09F-E007": {"printed": (5,), "pdf": (5,), "fn": None, "locator": "Printed p. 5 [PDF p. 5]"},
    "S09F-E008": {"printed": (3,), "pdf": (3,), "fn": None, "locator": "Printed p. 3 [PDF p. 3]"},
    "S09F-E009": {"printed": (3,), "pdf": (3,), "fn": None, "locator": "Printed p. 3 [PDF p. 3]"},
    "S09F-E010": {"printed": (3,), "pdf": (3,), "fn": 5, "locator": "Printed p. 3 [PDF p. 3], fn. 5"},
}

EXPECTED_EVIDENCE_B001_MAP = {
    "S09F-E001": "B001-CONTEXT",
    "S09F-E002": "B001-CONTEXT",
    "S09F-E003": "B001-CONTEXT",
    "S09F-E004": "B001-CONTEXT",
    "S09F-E005": "B001-4, B001-5",
    "S09F-E006": "B001-5",
    "S09F-E007": "B001-5",
    "S09F-E008": "B001-CONTEXT",
    "S09F-E009": "B001-4",
    "S09F-E010": "B001-4",
}

VALID_B001_PASSAGE_ID_RE = re.compile(
    r"^(?:B001-(?:[1-9]|1[0-2]|CONTEXT))(?:\s*,\s*B001-(?:[1-9]|1[0-2]|CONTEXT))*$"
)

CANONICAL_B001_COMPARISONS = {
    "B001-1": "Romans 4:3 / Genesis 15:6",
    "B001-2": "Romans 9:25 / Hosea 2:23",
    "B001-3": "Romans 9:26 / Hosea 1:10",
    "B001-4": "Romans 10:11 / Isaiah 28:16",
    "B001-5": "Romans 10:13 / Joel 2:32",
    "B001-6": "Romans 11:34 / Isaiah 40:13",
    "B001-7": "Romans 15:12 / Isaiah 11:10",
    "B001-8": "1 Corinthians 1:19 / Isaiah 29:14",
    "B001-9": "1 Corinthians 6:16 / Genesis 2:24",
    "B001-10": "1 Corinthians 9:9 / Deuteronomy 25:4",
    "B001-11": "1 Corinthians 10:7 / Exodus 32:6",
    "B001-12": "Galatians 3:13 / Deuteronomy 21:23",
}

EXPECTED_SYNTHESIS_SUBSECTIONS = {
    "1. B001-4: Romans 10:11 / Isaiah 28:16 (`Substantive`)": "Printed pp. 3, 4, 5, 7, 10, and 11 [PDF pp. 3, 4, 5, 7, 10, 11]",
    "2. B001-5: Romans 10:13 / Joel 2:32 [LXX 3:5] (`Substantive`)": "Printed pp. 4, 5, 7, 8, 9, 10, and 11 [PDF pp. 4, 5, 7, 8, 9, 10, 11]",
    "3. B001-CONTEXT: Romans 10:5–10 & Pericope Encasement (`Contextual Only`)": "Printed p. 9",
}

EXPECTED_RELEVANCE_TABLE_LOCI = {
    "B001-1": {"comparison": "Romans 4:3 / Genesis 15:6", "status": "NO", "pages": (), "depth": "N/A"},
    "B001-2": {"comparison": "Romans 9:25 / Hosea 2:23", "status": "NO", "pages": (), "depth": "N/A"},
    "B001-3": {"comparison": "Romans 9:26 / Hosea 1:10", "status": "NO", "pages": (), "depth": "N/A"},
    "B001-4": {"comparison": "Romans 10:11 / Isaiah 28:16", "status": "YES", "pages": (3, 4, 5, 7, 10, 11), "depth": "Substantive"},
    "B001-5": {"comparison": "Romans 10:13 / Joel 2:32", "status": "YES", "pages": (4, 5, 7, 8, 9, 10, 11), "depth": "Substantive"},
    "B001-6": {"comparison": "Romans 11:34 / Isaiah 40:13", "status": "NO", "pages": (), "depth": "N/A"},
    "B001-7": {"comparison": "Romans 15:12 / Isaiah 11:10", "status": "NO", "pages": (), "depth": "N/A"},
    "B001-8": {"comparison": "1 Corinthians 1:19 / Isaiah 29:14", "status": "NO", "pages": (), "depth": "N/A"},
    "B001-9": {"comparison": "1 Corinthians 6:16 / Genesis 2:24", "status": "NO", "pages": (), "depth": "N/A"},
    "B001-10": {"comparison": "1 Corinthians 9:9 / Deuteronomy 25:4", "status": "NO", "pages": (), "depth": "N/A"},
    "B001-11": {"comparison": "1 Corinthians 10:7 / Exodus 32:6", "status": "NO", "pages": (), "depth": "N/A"},
    "B001-12": {"comparison": "Galatians 3:13 / Deuteronomy 21:23", "status": "NO", "pages": (), "depth": "N/A"},
}

FORBIDDEN_BIB_CONTAINERS = (
    "online publication",
    "research monograph",
    "vol. 38b",
    "pp. 3–35",
    "pp. 268–275",
    "pp. 556–563",
    "pp. 330–342",
)

EXPECTED_BIBLIOGRAPHY_LEADS = [
    {
        "header": "Akio Ito (2006)",
        "citation": '*"The written Torah and the oral Gospel: Romans 10:5–13 in the dynamic tension between orality and literacy"*',
        "year": 2006,
        "witness_token": "Ito",
        "ref_page": 12,
        "ref_key": "Ito, A., 2006",
        "container_type": "journal",
        "container_tokens": ("Novum Testamentum", "48", "3", "234–260"),
        "forbidden_tokens": (),
        "printed_pages": (4, 5, 6, 8, 9),
        "pdf_pages": (4, 5, 6, 8, 9),
        "footnotes": (),
    },
    {
        "header": "J. F. Hart (1999)",
        "citation": '*"Why confess Christ? The use and abuse of Romans 10:9–10"*',
        "year": 1999,
        "witness_token": "Hart",
        "ref_page": 12,
        "ref_key": "Hart, J.F., 1999",
        "container_type": "journal",
        "container_tokens": ("Journal of the Grace Evangelical Society", "12", "23", "faithalone.org"),
        "forbidden_tokens": ("pp. 3–35", "3–35"),
        "printed_pages": (1, 2, 3, 4, 5, 7, 8),
        "pdf_pages": (1, 2, 3, 4, 5, 7, 8),
        "footnotes": ((5, 11),),
    },
    {
        "header": "James D. G. Dunn (1988)",
        "citation": "*Romans 1–8* (`1988a`) and *Romans 9–16* (`1988b`)",
        "year": 1988,
        "witness_token": "Dunn",
        "ref_page": 12,
        "ref_key": "Dunn, J.D.G., 1988a",
        "container_type": "book",
        "container_tokens": ("Word Biblical Commentary", "Dallas, TX", "Word Books"),
        "forbidden_tokens": ("38B",),
        "printed_pages": (2, 3, 4, 8),
        "pdf_pages": (2, 3, 4, 8),
        "footnotes": (),
    },
    {
        "header": "Colin G. Kruse (2012)",
        "citation": "*Paul’s letter to the Romans*",
        "year": 2012,
        "witness_token": "Kruse",
        "ref_page": 12,
        "ref_key": "Kruse, C.G., 2012",
        "container_type": "book",
        "container_tokens": ("The Pillar New Testament Commentary", "Cambridge", "Eerdmans"),
        "forbidden_tokens": ("Grand Rapids",),
        "printed_pages": (1, 4, 7, 8),
        "pdf_pages": (1, 4, 7, 8),
        "footnotes": ((1, 1),),
    },
    {
        "header": "H.-J. Eckstein (1988)",
        "citation": '*"“Nahe ist dir das Wort:“ Exegetische Erwägungen zu Röm 10, 8"*',
        "year": 1988,
        "witness_token": "Eckstein",
        "ref_page": 12,
        "ref_key": "Eckstein, H-J., 1988",
        "container_type": "journal",
        "container_tokens": ("Zeitschrift für Neutestamentliche Wissenschaft", "79", "204–220"),
        "forbidden_tokens": (),
        "printed_pages": (3,),
        "pdf_pages": (3,),
        "footnotes": (),
    },
    {
        "header": "Walter C. Kaiser Jr. (1971)",
        "citation": '*"Leviticus 18:5 and Paul: Do this and you shall live (eternally?)"*',
        "year": 1971,
        "witness_token": "Kaiser",
        "ref_page": 12,
        "ref_key": "Kaiser, W.C. (Jr.), 1971",
        "container_type": "journal",
        "container_tokens": ("Journal of the Evangelical Theological Society", "14", "1", "20–28"),
        "forbidden_tokens": (),
        "printed_pages": (3,),
        "pdf_pages": (3,),
        "footnotes": (),
    },
    {
        "header": "Bruce C. Dunson (2011)",
        "citation": '*"Faith in Romans: The salvation of the individual or life in community?"*',
        "year": 2011,
        "witness_token": "Dunson",
        "ref_page": 12,
        "ref_key": "Dunson, B.C., 2011",
        "container_type": "journal",
        "container_tokens": ("Journal for the Study of the New Testament", "34", "1", "19–46"),
        "forbidden_tokens": (),
        "printed_pages": (2, 3, 6, 7, 11),
        "pdf_pages": (2, 3, 6, 7, 11),
        "footnotes": ((2, 2), (6, 12)),
    },
    {
        "header": "Adolf Schlatter (1991)",
        "citation": "*Gottes Gerechtigkeit: Ein Kommentar zum Römerbrief*",
        "year": 1991,
        "witness_token": "Schlatter",
        "ref_page": 12,
        "ref_key": "Schlatter, A., 1991",
        "container_type": "book",
        "container_tokens": ("Stuttgart", "Calver Verlag"),
        "forbidden_tokens": (),
        "printed_pages": (9,),
        "pdf_pages": (9,),
        "footnotes": (),
    },
    {
        "header": "G. Aho (1981)",
        "citation": '*"3D Sunday in Lent"*',
        "year": 1981,
        "witness_token": "Aho",
        "ref_page": 11,
        "ref_key": "Aho, G., 1981",
        "container_type": "journal",
        "container_tokens": ("Concordia Theological Quarterly", "45", "4", "308–309"),
        "forbidden_tokens": (),
        "printed_pages": (3, 8),
        "pdf_pages": (3, 8),
        "footnotes": ((3, 5),),
    },
    {
        "header": "Douglas J. Moo (1996)",
        "citation": "*The epistle to the Romans*",
        "year": 1996,
        "witness_token": "Moo",
        "ref_page": 12,
        "ref_key": "Moo, D.J., 1996",
        "container_type": "book",
        "container_tokens": ("New International Commentary on the New Testament", "Grand Rapids, MI", "Eerdmans"),
        "forbidden_tokens": (),
        "printed_pages": (2, 8),
        "pdf_pages": (2, 8),
        "footnotes": ((8, 20),),
    },
    {
        "header": "Herman Ridderbos (1959)",
        "citation": "*Commentaar op het Nieuwe Testament: Aan de Romeinen*",
        "year": 1959,
        "witness_token": "Ridderbos",
        "ref_page": 12,
        "ref_key": "Ridderbos, H., 1959",
        "container_type": "book",
        "container_tokens": ("Kampen", "JH Kok"),
        "forbidden_tokens": (),
        "printed_pages": (6,),
        "pdf_pages": (6,),
        "footnotes": ((6, 13),),
    },
    {
        "header": "Zane C. Hodges (1989)",
        "citation": "*Absolutely free: A Biblical reply to lordship salvation*",
        "year": 1989,
        "witness_token": "Hodges",
        "ref_page": 12,
        "ref_key": "Hodges, Z.C., 1989",
        "container_type": "book",
        "container_tokens": ("Dallas, TX", "Redención Viva"),
        "forbidden_tokens": (),
        "printed_pages": (7, 8, 9),
        "pdf_pages": (7, 8, 9),
        "footnotes": (),
    },
    {
        "header": "J. Ross Wagner (2002)",
        "citation": "*Heralds of the Good News: Isaiah and Paul “in concert” in the letter to the Romans*",
        "year": 2002,
        "witness_token": "Wagner",
        "ref_page": 12,
        "ref_key": "Wagner, J.R., 2002",
        "container_type": "book",
        "container_tokens": ("Novum Testamentum, suppl. 101", "Leiden/Boston/Köln", "EJ Brill"),
        "forbidden_tokens": (),
        "printed_pages": (5,),
        "pdf_pages": (5,),
        "footnotes": (),
    },
    {
        "header": "Karl Olav Sandnes (1991)",
        "citation": "*Paul – One of the prophets?: A contribution to the apostle’s selfunderstanding*",
        "year": 1991,
        "witness_token": "Sandnes",
        "ref_page": 12,
        "ref_key": "Sandnes, K.O., 1991",
        "container_type": "book",
        "container_tokens": ("43/2", "Tübingen", "JCB Mohr"),
        "forbidden_tokens": (),
        "printed_pages": (5,),
        "pdf_pages": (5,),
        "footnotes": (),
    },
    {
        "header": "J. D. M. Derrett (1983)",
        "citation": '*"The reason for the cock-crowings"*',
        "year": 1983,
        "witness_token": "Derrett",
        "ref_page": 12,
        "ref_key": "Derrett, J.D.M., 1983",
        "container_type": "journal",
        "container_tokens": ("New Testament Studies", "29", "1", "142–144"),
        "forbidden_tokens": (),
        "printed_pages": (4,),
        "pdf_pages": (4,),
        "footnotes": ((4, 9),),
    },
    {
        "header": "Nils W. Lund (1942)",
        "citation": "*Chiasmus in the New Testament: A study in Formgeschichte*",
        "year": 1942,
        "witness_token": "Lund",
        "ref_page": 12,
        "ref_key": "Lund, N.W., 1942",
        "container_type": "book",
        "container_tokens": ("Chapel Hill, NC", "The University of North Carolina Press"),
        "forbidden_tokens": (),
        "printed_pages": (1, 2),
        "pdf_pages": (1, 2),
        "footnotes": (),
    },
    {
        "header": "J. M. Gibbs (2013)",
        "citation": "*Chiastic structuring: An introduction*",
        "year": 2013,
        "witness_token": "Gibbs",
        "ref_page": 12,
        "ref_key": "Gibbs, J.M., 2013",
        "container_type": "web_resource",
        "container_tokens": ("Dated web resource", "newtestamentresearch.com", "viewed 11 November 2014", "chiastic_structuring.htm", "UNKNOWN"),
        "forbidden_tokens": ("Online Publication", "Research Monograph"),
        "printed_pages": (2,),
        "pdf_pages": (2,),
        "footnotes": (),
    },
    {
        "header": "Ulrich Wilckens (1980)",
        "citation": "*Der Brief an die Römer*",
        "year": 1980,
        "witness_token": "Wilckens",
        "ref_page": 12,
        "ref_key": "Wilckens, U., 1980",
        "container_type": "book",
        "container_tokens": ("6", "Zürich", "Benziger Verlag"),
        "forbidden_tokens": (),
        "printed_pages": (6,),
        "pdf_pages": (6,),
        "footnotes": ((6, 14),),
    },
    {
        "header": "Eduard Lohse (2003)",
        "citation": "*Der Brief an die Römer*",
        "year": 2003,
        "witness_token": "Lohse",
        "ref_page": 12,
        "ref_key": "Lohse, E., 2003",
        "container_type": "book",
        "container_tokens": ("4", "Göttingen", "Vandenhoeck & Ruprecht"),
        "forbidden_tokens": (),
        "printed_pages": (6,),
        "pdf_pages": (6,),
        "footnotes": ((6, 14),),
    },
    {
        "header": "William Sanday & Arthur C. Headlam (1902)",
        "citation": "*A critical and exegetical commentary on the epistle to the Romans*",
        "year": 1902,
        "witness_token": "Sanday",
        "ref_page": 12,
        "ref_key": "Sanday, W. & Headlam, A.C., 1902",
        "container_type": "book",
        "container_tokens": ("Edinburgh", "T & T Clark"),
        "forbidden_tokens": (),
        "printed_pages": (7, 8),
        "pdf_pages": (7, 8),
        "footnotes": (),
    },
    {
        "header": "Ernst Käsemann (1973)",
        "citation": "*An die Römer*",
        "year": 1973,
        "witness_token": "Käsemann",
        "ref_page": 12,
        "ref_key": "Käsemann, E., 1973",
        "container_type": "book",
        "container_tokens": ("Handbuch zum Neuen Testament 8a", "Tübingen", "Mohr Siebeck", "UNKNOWN"),
        "forbidden_tokens": ("pp. 268–275", "268–275"),
        "printed_pages": (2,),
        "pdf_pages": (2,),
        "footnotes": ((2, 2),),
    },
    {
        "header": "Steven R. Bechtler (1994)",
        "citation": '*"Christ, the Τέλος of the law: The goal of Romans 10:4"*',
        "year": 1994,
        "witness_token": "Bechtler",
        "ref_page": 11,
        "ref_key": "Bechtler, S.R., 1994",
        "container_type": "journal",
        "container_tokens": ("Catholic Biblical Quarterly", "56", "2", "288–308"),
        "forbidden_tokens": ("Christ, the End of the Law",),
        "printed_pages": (1, 6, 7),
        "pdf_pages": (1, 6, 7),
        "footnotes": (),
    },
    {
        "header": "Thomas R. Schreiner (1998)",
        "citation": "*Romans*",
        "year": 1998,
        "witness_token": "Schreiner",
        "ref_page": 12,
        "ref_key": "Schreiner, T.R., 1998",
        "container_type": "book",
        "container_tokens": ("Baker Exegetical Commentary on the New Testament", "Grand Rapids, MI", "Baker Book House", "UNKNOWN"),
        "forbidden_tokens": ("pp. 556–563", "556–563"),
        "printed_pages": (8,),
        "pdf_pages": (8,),
        "footnotes": (),
    },
    {
        "header": "N. T. Wright (2002)",
        "citation": '*"The letter to the Romans: Introduction, commentary, and reflections"*',
        "year": 2002,
        "witness_token": "Wright",
        "ref_page": 12,
        "ref_key": "Wright, N.T., 2002",
        "container_type": "chapter",
        "container_tokens": ("L.E. Keck (ed.)", "The new interpreter’s Bible", "Vol. X", "pp. 393–770", "Nashville, TN", "Abingdon Press"),
        "forbidden_tokens": (),
        "printed_pages": (2,),
        "pdf_pages": (2,),
        "footnotes": (),
    },
    {
        "header": "Francis Watson (2004)",
        "citation": "*Paul and the hermeneutics of faith*",
        "year": 2004,
        "witness_token": "Watson",
        "ref_page": 12,
        "ref_key": "Watson, F., 2004",
        "container_type": "book",
        "container_tokens": ("London", "T & T Clark", "UNKNOWN"),
        "forbidden_tokens": ("pp. 330–342", "330–342"),
        "printed_pages": (2, 3),
        "pdf_pages": (2, 3),
        "footnotes": (),
    },
    {
        "header": "Mark A. Seifrid (2007)",
        "citation": '*"Romans"*',
        "year": 2007,
        "witness_token": "Seifrid",
        "ref_page": 12,
        "ref_key": "Seifrid, M.A., 2007",
        "container_type": "chapter",
        "container_tokens": ("G.K. Beale & D.A. Carson (eds.)", "Commentary on the New Testament use of the Old Testament", "pp. 607–694", "Grand Rapids, MI", "Baker Academic"),
        "forbidden_tokens": (),
        "printed_pages": (2,),
        "pdf_pages": (2,),
        "footnotes": (),
    },
]

POSITIVE_CONTROLS = [
    {
        "id": "PC01",
        "name": "Title and Journal Header",
        "pattern": r"romans\s+10:5-13\s+revisited",
        "expected_page": 1,
        "expected_pdf_page": 1,
    },
    {
        "id": "PC02",
        "name": "Chiasm in Ancient Rhetoric",
        "pattern": r"chiasm\s+as\s+rhetoric\s+device\s+back\s+to\s+the\s+ancient\s+greek\s+and\s+roman",
        "expected_page": 2,
        "expected_pdf_page": 2,
    },
    {
        "id": "PC03",
        "name": "Encasement Architecture",
        "pattern": r"paul\s+has\s+encased\s+these\s+words\s+with\s+scriptures\s+so\s+as\s+to\s+highlight",
        "expected_page": 3,
        "expected_pdf_page": 3,
    },
    {
        "id": "PC04",
        "name": "Deuteronomy 30 Alteration to Abyss",
        "pattern": r"the\s+'sea'\s+of\s+deuteronomy\s+30:13\s+is\s+changed\s+to\s+the\s+'deep\s+\(abyss\)'",
        "expected_page": 4,
        "expected_pdf_page": 4,
    },
    {
        "id": "PC05",
        "name": "Antithetical Chiasm in Verses 5a and 6a",
        "pattern": r"this\s+contrast\s+is\s+set\s+in\s+the\s+form\s+of\s+a\s+stark\s+a-b-b-a\s+chiasm",
        "expected_page": 5,
        "expected_pdf_page": 5,
    },
    {
        "id": "PC06",
        "name": "Righteousness of Faith vs Law",
        "pattern": r"behaviour\s+of\s+a\s+person\s+who\s+lives\s+according\s+to\s+the\s+righteousness",
        "expected_page": 6,
        "expected_pdf_page": 6,
    },
    {
        "id": "PC07",
        "name": "Universality of God's Salvation in Verses 11-13",
        "pattern": r"paul\s+asserts\s+the\s+universality\s+of\s+god's\s+salvation",
        "expected_page": 7,
        "expected_pdf_page": 7,
    },
    {
        "id": "PC08",
        "name": "Synonymous Reading Refutation",
        "pattern": r"to\s+believe\s+in\s+christ\s+is\s+to\s+confess\s+christ",
        "expected_page": 8,
        "expected_pdf_page": 8,
    },
    {
        "id": "PC09",
        "name": "Double Chiasm Number Combinations",
        "pattern": r"the\s+1-2-3-4\s+and\s+4-3-21\s+combinations\s+of\s+verses\s+9\s+and\s+10",
        "expected_page": 9,
        "expected_pdf_page": 9,
    },
    {
        "id": "PC10",
        "name": "Joel 2:32 Oral Invocation and Salvation",
        "pattern": r"it\s+is\s+the\s+'something-being-said'\s+\(in\s+this\s+case\s+a\s+repetition\s+of\s+the\s+verb",
        "expected_page": 10,
        "expected_pdf_page": 10,
    },
    {
        "id": "PC11",
        "name": "Prophetic Mission of Herald",
        "pattern": r"if\s+you\s+do\s+not\s+enact\s+your\s+prophetic\s+task\s+to\s+convey\s+the\s+word\s+of\s+god\s+to\s+others",
        "expected_page": 11,
        "expected_pdf_page": 11,
    },
    {
        "id": "PC12",
        "name": "Bibliography Verification",
        "pattern": r"journal\s+of\s+the\s+evangelical\s+theological\s+society",
        "expected_page": 12,
        "expected_pdf_page": 12,
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
      - Strictly monotonic pagination derivation (printed = PDF, offset = 0)
      - No duplicate, conflicting, or unparsed trailing fragments
    Permissible forms:
      Printed p. 5 [PDF p. 5]
      Printed pp. 3–5 [PDF pp. 3–5]
      Printed p. 4 [PDF p. 4], fn. 9
      Printed p. 6 [PDF p. 6], fn. 13; Section 2
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

    # 5. Monotonic formula check: printed = PDF (offset = 0)
    for prn, pdf in zip(prn_pages, pdf_pages):
        if prn != pdf:
            raise ValueError(f"Monotonic pagination mismatch: printed {prn} != PDF {pdf} in '{loc_str}'")

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


def parse_bib_locator(loc_str: str) -> dict:
    """Strict parser for bibliographic locators supporting per-page optional footnote tokens.

    Permissible form:
      Printed p. N [PDF p. N](, fn. M)?(, p. K [PDF p. K](, fn. L)?)*
    Enforces monotonic invariant (printed = PDF, offset = 0), strictly ordered unique pages,
    and valid footnote attachment to the immediately preceding page token.
    """
    loc = loc_str.strip().strip("`")
    if not loc.startswith("Printed "):
        raise ValueError(f"Bibliographic locator must start with 'Printed ': '{loc_str}'")

    tokens = [s.strip() for s in loc.split(",")]
    prn_list: list[int] = []
    pdf_list: list[int] = []
    footnotes: list[tuple[int, int]] = []
    last_page: int | None = None
    seen_fns_for_page: set[tuple[int, int]] = set()

    for i, tok in enumerate(tokens):
        if i == 0:
            m = re.match(r"^Printed\s+p\.\s*(\d+)\s*\[PDF\s+p\.\s*(\d+)\]$", tok)
            if not m:
                raise ValueError(f"Malformed initial bibliographic locator segment '{tok}' in '{loc_str}'")
        elif tok.startswith("fn."):
            m_fn = re.match(r"^fn\.\s*(\d+)$", tok)
            if not m_fn or last_page is None:
                raise ValueError(f"Malformed or misplaced footnote token '{tok}' in '{loc_str}'")
            fn_num = int(m_fn.group(1))
            pair = (last_page, fn_num)
            if pair in seen_fns_for_page:
                raise ValueError(f"Conflicting duplicate footnote reference '{tok}' in '{loc_str}'")
            seen_fns_for_page.add(pair)
            footnotes.append(pair)
            continue
        else:
            if tok.count("[") != 1 or tok.count("]") != 1:
                raise ValueError(f"Expected exactly one [PDF ...] pair in segment '{tok}' of '{loc_str}'")
            m = re.match(r"^p\.\s*(\d+)\s*\[PDF\s+p\.\s*(\d+)\]$", tok)
            if not m:
                raise ValueError(f"Malformed bibliographic page locator segment '{tok}' in '{loc_str}'")

        prn = int(m.group(1))
        pdf = int(m.group(2))
        if prn != pdf:
            raise ValueError(f"Monotonic pagination mismatch: printed {prn} != PDF {pdf} in '{loc_str}'")
        if prn_list and prn <= prn_list[-1]:
            raise ValueError(f"Duplicate or non-increasing page {prn} in bibliographic locator '{loc_str}'")
        prn_list.append(prn)
        pdf_list.append(pdf)
        last_page = prn

    return {
        "printed_pages": tuple(prn_list),
        "pdf_pages": tuple(pdf_list),
        "footnotes": tuple(footnotes),
    }


def extract_page_texts(pdf_path: Path) -> list[str]:
    page_texts = []
    for p in range(1, EXPECTED_PAGE_COUNT + 1):
        cmd = ["pdftotext", "-f", str(p), "-l", str(p), str(pdf_path), "-"]
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        page_texts.append(res.stdout)
    return page_texts


def verify_monotonic_pagination(page_texts: list[str]) -> None:
    """Verify strictly monotonic pagination invariant (printed = PDF, offset = 0) across all 12 article pages.

    Enforces that each page contains its expected printed numeral (PDF page) within the top 3 lines
    as 'Page X of 12' and has a verified journal header.
    """
    for idx, txt in enumerate(page_texts):
        pdf_page = idx + 1
        expected_printed = pdf_page
        expected_str = f"Page {expected_printed} of 12"
        lines = [ln.strip() for ln in txt.splitlines() if ln.strip()]

        top_lines = lines[:3]
        if not top_lines:
            raise ValueError(f"PDF p. {pdf_page} has no text lines.")

        has_numeral_in_header = any(expected_str in ln for ln in top_lines)
        if not has_numeral_in_header:
            raise ValueError(
                f"Monotonic pagination invariant violated at PDF p. {pdf_page}: "
                f"expected header '{expected_str}' not found in top 3 lines: {top_lines}"
            )

        has_journal_marker = any(
            (re.search(r"original\s+research", ln, re.IGNORECASE) or
             re.search(r"romans\s+10", ln, re.IGNORECASE) or
             re.search(r"page\s+\d+\s+of\s+12", ln, re.IGNORECASE))
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
        if r["source_id"] != "S09F":
            raise ValueError(f"Source ID mismatch at row {idx + 1}: expected S09F, got {r['source_id']}")
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
            exp_pdf = (int(parts[0]), int(parts[1]))
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
            exp_pdf = (prn_val,)
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
                f"{eid}: source_locator PDF pages {parsed_loc['pdf_pages']} != expected {exp_pdf} (offset 0)"
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
            layout_matched = False
            if eid == "S09F-E004" and "4-3-2-1" in quote and PDF_DEFAULT.is_file():
                res_layout = subprocess.run(
                    ["pdftotext", "-layout", "-f", "9", "-l", "9", str(PDF_DEFAULT), "-"],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                has_hyphen_wrap = re.search(r"4-3-2-\s*\n\s*1\s+combinations", res_layout.stdout) is not None
                layout_matched = has_hyphen_wrap and (norm_quote.replace("4-3-2-1", "4-3-21") in norm_target_text)
            if not layout_matched:
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
            "judgment": "Neither Rom 4:3 nor Gen 15:6 is discussed in this volume. Zero hits occur across all 12 article pages.",
        },
        {
            "id": "B001-2",
            "comparison": "Romans 9:25 / Hosea 2:23",
            "patterns": [r"\b9:25\b", r"\bHos(?:ea)?\s*2:23\b"],
            "category": "CONFIRMED_ABSENT",
            "judgment": "Neither Rom 9:25 nor Hos 2:23 is discussed in this volume. Zero hits occur across all 12 article pages.",
        },
        {
            "id": "B001-3",
            "comparison": "Romans 9:26 / Hosea 1:10",
            "patterns": [r"\b9:26\b", r"\bHos(?:ea)?\s*1:10\b"],
            "category": "CONFIRMED_ABSENT",
            "judgment": "Neither Rom 9:26 nor Hos 1:10 is discussed in this volume. Zero hits occur across all 12 article pages.",
        },
        {
            "id": "B001-4",
            "comparison": "Romans 10:11 / Isaiah 28:16",
            "patterns": [r"\b(?:romans|rom|rm)\s*10:(?:[^;\n]*,\s*)?11\b", r"\b(?:isaiah|isa|is)\s*28:16\b"],
            "category": "SUBSTANTIVE_DISCUSSION",
            "judgment": "Substantive discussion across pp. 3, 4, 5, 7, 10, 11 (without MT-vs-LXX text-critical collation). Oliver identifies Is 28:16 (LXX), links Rom 10:11 (καταισχύνω) to Rom 1:16 (ἐπαισχύνομαι), qualifies Aho (1981:308) on p. 3 fn. 5, and places v. 11 in the fourfold γάρ universality chain (p. 7).",
        },
        {
            "id": "B001-5",
            "comparison": "Romans 10:13 / Joel 2:32",
            "patterns": [r"\b(?:romans|rom|rm)\s*10:(?:[^;\n]*,\s*)?13\b", r"\bJoel\s*2:32\b", r"\bJoel\s*3:5\b", r"\bJl\s*2:32\b"],
            "category": "SUBSTANTIVE_DISCUSSION",
            "judgment": "Substantive discussion across pp. 4, 5, 7, 8, 9, 10, 11. Oliver analyzes the quotation of Joel 2:32 (Acts 2:17–21, p. 4 fn. 10), oral invocation resulting in salvation (σωθήσεται), and its link to apostolic preaching in verses 14–15.",
        },
        {
            "id": "B001-6",
            "comparison": "Romans 11:34 / Isaiah 40:13",
            "patterns": [r"\b11:34\b", r"\bIsa(?:iah)?\s*40:13\b"],
            "category": "CONFIRMED_ABSENT",
            "judgment": "Neither Rom 11:34 nor Isa 40:13 is discussed in this volume. Zero hits occur across all 12 article pages.",
        },
        {
            "id": "B001-7",
            "comparison": "Romans 15:12 / Isaiah 11:10",
            "patterns": [r"\b15:12\b", r"\bIsa(?:iah)?\s*11:10\b"],
            "category": "CONFIRMED_ABSENT",
            "judgment": "Neither Rom 15:12 nor Isa 11:10 is discussed in this volume. Zero hits occur across all 12 article pages.",
        },
        {
            "id": "B001-8",
            "comparison": "1 Corinthians 1:19 / Isaiah 29:14",
            "patterns": [r"\b1\s*Cor(?:inthians)?\s*1:19\b", r"\bIsa(?:iah)?\s*29:14\b"],
            "category": "CONFIRMED_ABSENT",
            "judgment": "Neither 1 Cor 1:19 nor Isa 29:14 is discussed in this volume. Zero hits occur across all 12 article pages.",
        },
        {
            "id": "B001-9",
            "comparison": "1 Corinthians 6:16 / Genesis 2:24",
            "patterns": [r"\b1\s*Cor(?:inthians)?\s*6:16\b", r"\bGen(?:esis)?\s*2:24\b"],
            "category": "CONFIRMED_ABSENT",
            "judgment": "Neither 1 Cor 6:16 nor Gen 2:24 is discussed in this volume. Zero hits occur across all 12 article pages.",
        },
        {
            "id": "B001-10",
            "comparison": "1 Corinthians 9:9 / Deuteronomy 25:4",
            "patterns": [r"\b1\s*Cor(?:inthians)?\s*9:9\b", r"\bDeut(?:eronomy)?\s*25:4\b"],
            "category": "CONFIRMED_ABSENT",
            "judgment": "Neither 1 Cor 9:9 nor Deut 25:4 is discussed in this volume. Zero hits occur across all 12 article pages.",
        },
        {
            "id": "B001-11",
            "comparison": "1 Corinthians 10:7 / Exodus 32:6",
            "patterns": [r"\b1\s*Cor(?:inthians)?\s*10:7\b", r"\bExod(?:us)?\s*32:6\b"],
            "category": "CONFIRMED_ABSENT",
            "judgment": "Neither 1 Cor 10:7 nor Exod 32:6 is discussed in this volume. Zero hits occur across all 12 article pages.",
        },
        {
            "id": "B001-12",
            "comparison": "Galatians 3:13 / Deuteronomy 21:23",
            "patterns": [r"\bGal(?:atians)?\s*3:13\b", r"\bDeut(?:eronomy)?\s*21:23\b"],
            "category": "CONFIRMED_ABSENT",
            "judgment": "Neither Gal 3:13 nor Deut 21:23 is discussed in this volume. Zero hits occur across all 12 article pages.",
        },
    ]

    full_normalized_text = " ".join(normalize_text_for_match(txt) for txt in page_texts)

    results = []
    for tgt in targets:
        hit_count = 0
        for pat in tgt["patterns"]:
            matches = list(re.finditer(pat, full_normalized_text, re.IGNORECASE))
            hit_count += len(matches)

        if tgt["category"] == "CONFIRMED_ABSENT" and hit_count != 0:
            raise ValueError(
                f"Negative search assertion failed for {tgt['id']} ({tgt['comparison']}): "
                f"expected 0 hits, found {hit_count}"
            )
        if tgt["category"] != "CONFIRMED_ABSENT" and hit_count == 0:
            raise ValueError(
                f"Positive search assertion failed for {tgt['id']} ({tgt['comparison']}): "
                f"expected hits, found 0"
            )

        results.append({
            "id": tgt["id"],
            "comparison": tgt["comparison"],
            "category": tgt["category"],
            "hit_count": hit_count,
            "judgment": tgt["judgment"],
        })
    return results


def _verify_extraction_artifact(source_dir: Path, ledger_map: dict[str, dict]) -> None:
    """Enforce exact evidence-ID coverage and line-anchored field equality for extraction.md."""
    extr_path = source_dir / "extraction.md"
    if not extr_path.is_file():
        raise FileNotFoundError(f"Missing extraction.md in {source_dir}")
    extr_txt = extr_path.read_text(encoding="utf-8")

    ext_blocks = re.split(r"(?=^###\s+)", extr_txt, flags=re.MULTILINE)
    ext_block_map: dict[str, str] = {}
    for blk in ext_blocks:
        m = re.match(r"^###\s+([^\s\n]+)", blk)
        if m:
            eid = m.group(1).strip()
            if eid in ext_block_map:
                raise ValueError(f"extraction.md: Duplicate section block for {eid}")
            ext_block_map[eid] = blk

    expected_set = set(EXPECTED_EVIDENCE_IDS)
    actual_set = set(ext_block_map.keys())
    extra_ids = sorted(actual_set - expected_set)
    missing_ids = sorted(expected_set - actual_set)
    if extra_ids:
        raise ValueError(f"extraction.md: Unexpected extra section block(s): {extra_ids}")
    if missing_ids:
        raise ValueError(f"extraction.md: Missing discrete section block(s): {missing_ids}")

    for eid in EXPECTED_EVIDENCE_IDS:
        blk = ext_block_map[eid]
        row = ledger_map[eid]
        auth_spec = AUTHORITATIVE_EVIDENCE_LOCI[eid]

        # 1. Proposed Evidence ID (line-anchored, single)
        m_prop = re.findall(r"(?m)^-\s+\*\*Proposed Evidence ID:\*\*\s*`?([^\n`]+)`?\s*$", blk)
        if len(m_prop) != 1 or m_prop[0].strip() != eid:
            raise ValueError(f"extraction.md [{eid}]: Expected exactly one Proposed Evidence ID `{eid}`, got {m_prop}")

        # 2. B001 Passage ID (line-anchored, full line, strict syntax — never truncate at '(')
        raw_b001 = re.findall(r"(?m)^-\s+\*\*B001 Passage ID:\*\*\s*([^\n]+)$", blk)
        m_b001 = [x.strip("` ").strip() for x in raw_b001]
        if len(m_b001) != 1:
            raise ValueError(f"extraction.md [{eid}]: Expected exactly one B001 Passage ID line, got {m_b001}")
        if not VALID_B001_PASSAGE_ID_RE.fullmatch(m_b001[0]):
            raise ValueError(f"extraction.md [{eid}]: Invalid B001 Passage ID syntax '{m_b001[0]}'")
        if m_b001[0] != row["b001_id"].strip():
            raise ValueError(f"extraction.md [{eid}]: B001 ID mismatch: expected '{row['b001_id']}', got '{m_b001[0]}'")
        if m_b001[0] != EXPECTED_EVIDENCE_B001_MAP[eid]:
            raise ValueError(
                f"extraction.md [{eid}]: B001 ID mismatch: expected '{EXPECTED_EVIDENCE_B001_MAP[eid]}', got '{m_b001[0]}'"
            )

        # 3. Author's Claim (line-anchored, exact 1 line, normalized equality with ledger)
        claim_lines = re.findall(r"(?m)^-\s+\*\*Author's Claim:\*\*\s*([^\n]+)$", blk)
        if len(claim_lines) != 1:
            raise ValueError(f"extraction.md [{eid}]: Expected exactly one Author's Claim line, found {len(claim_lines)}")
        norm_row_claim = normalize_text_for_match(row["author_claim"])
        norm_ext_claim = normalize_text_for_match(claim_lines[0].strip())
        if norm_row_claim != norm_ext_claim:
            raise ValueError(
                f"extraction.md [{eid}]: Author's Claim mismatch:\n  Ledger: '{norm_row_claim}'\n  Ext: '{norm_ext_claim}'"
            )

        # 4. Source Locator (line-anchored, exact 1 line, strict parser vs ledger & authoritative)
        loc_lines = re.findall(r"(?m)^-\s+\*\*Source Locator:\*\*\s*([^\n]+)$", blk)
        if len(loc_lines) != 1:
            raise ValueError(f"extraction.md [{eid}]: Expected exactly one Source Locator line, found {len(loc_lines)}")
        parsed_ext_loc = parse_source_locator(loc_lines[0].strip())
        parsed_ledger_loc = parse_source_locator(row["source_locator"])

        for field_key, spec_key in (("printed_pages", "printed"), ("pdf_pages", "pdf"), ("footnote", "fn")):
            if parsed_ext_loc[field_key] != auth_spec[spec_key]:
                raise ValueError(
                    f"extraction.md [{eid}]: {field_key} mismatch: expected {auth_spec[spec_key]}, got {parsed_ext_loc[field_key]}"
                )
            if parsed_ext_loc[field_key] != parsed_ledger_loc[field_key]:
                raise ValueError(
                    f"extraction.md [{eid}]: {field_key} does not match ledger: {parsed_ext_loc[field_key]} vs {parsed_ledger_loc[field_key]}"
                )

        # 5. Printed Page Number (line-anchored, full-field strict grammar + ledger/authoritative check)
        m_page = re.findall(r"(?m)^-\s+\*\*Printed Page Number:\*\*\s*([^\n]+)$", blk)
        if len(m_page) != 1:
            raise ValueError(f"extraction.md [{eid}]: Expected exactly one Printed Page Number line, found {len(m_page)}")
        parsed_prn_field = parse_source_locator(m_page[0].strip())
        if parsed_prn_field["footnote"] is not None or parsed_prn_field["section"] is not None:
            raise ValueError(f"extraction.md [{eid}]: Printed Page Number must not include fn/Section: '{m_page[0]}'")
        if parsed_prn_field["printed_pages"] != auth_spec["printed"] or parsed_prn_field["pdf_pages"] != auth_spec["pdf"]:
            raise ValueError(
                f"extraction.md [{eid}]: Printed Page Number tuple mismatch: expected {auth_spec['printed']}, got {parsed_prn_field['printed_pages']}"
            )
        if parsed_prn_field["printed_pages"] != (int(row["printed_page"]),):
            raise ValueError(
                f"extraction.md [{eid}]: Printed Page Number mismatch vs ledger: expected {row['printed_page']}, got {parsed_prn_field['printed_pages']}"
            )

        # 6. Short Exact Quotation (line-anchored, exact 1 line, normalized equality with ledger)
        quote_lines = re.findall(r"(?m)^-\s+\*\*Short Exact Quotation:\*\*\s*([^\n]+)$", blk)
        if len(quote_lines) != 1:
            raise ValueError(f"extraction.md [{eid}]: Expected exactly one Short Exact Quotation line, found {len(quote_lines)}")
        norm_row_quote = normalize_text_for_match(row["short_quote"].strip(' "'))
        norm_field_quote = normalize_text_for_match(quote_lines[0].strip().strip(' "'))
        if norm_row_quote != norm_field_quote:
            raise ValueError(
                f"extraction.md [{eid}]: Short Exact Quotation field mismatch:\n  Ledger: '{norm_row_quote}'\n  Ext field: '{norm_field_quote}'"
            )


def _verify_canonical_queue_alignment() -> None:
    """Verify CANONICAL_B001_COMPARISONS against research-queue/B001-pauline-txt-pilot.md when present."""
    pilot_path = REPO_ROOT / "research-queue" / "B001-pauline-txt-pilot.md"
    if not pilot_path.is_file():
        return
    pilot_txt = pilot_path.read_text(encoding="utf-8")
    if "PAU-B001-04-TXT" not in pilot_txt or "Romans 10:11" not in pilot_txt or "Isaiah 28:16" not in pilot_txt:
        raise ValueError("Canonical batch contract PAU-B001-04-TXT mismatch in research-queue/B001-pauline-txt-pilot.md")
    m04 = re.search(r"PAU-B001-04-TXT[^\n]+", pilot_txt)
    if not m04 or "Romans 10:11" not in m04.group(0) or "Isaiah 28:16" not in m04.group(0):
        raise ValueError("Canonical table row PAU-B001-04-TXT must map to Romans 10:11 and Isaiah 28:16")


def _verify_relevance_scan_and_canonical(source_dir: Path, check_search_log: bool) -> None:
    """Validate every YES and NO row of relevance_scan.md and canonical B001 comparison fidelity."""
    _verify_canonical_queue_alignment()

    rel_path = source_dir / "relevance_scan.md"
    if not rel_path.is_file():
        raise FileNotFoundError(f"Missing relevance_scan.md in {source_dir}")
    rel_txt = rel_path.read_text(encoding="utf-8")

    row_pattern = re.compile(
        r"^\|\s*\*\*(B001-\d+)\*\*\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|$",
        re.MULTILINE,
    )
    parsed_rows: dict[str, tuple[str, str, str, str, str]] = {}
    for m in row_pattern.finditer(rel_txt):
        b_id = m.group(1).strip()
        if b_id in parsed_rows:
            raise ValueError(f"relevance_scan.md: Duplicate table row for {b_id}")
        parsed_rows[b_id] = tuple(m.group(i).strip() for i in range(2, 7))  # type: ignore[assignment]

    if set(parsed_rows.keys()) != set(EXPECTED_RELEVANCE_TABLE_LOCI.keys()):
        raise ValueError(
            f"relevance_scan.md: Table rows mismatch: expected {sorted(EXPECTED_RELEVANCE_TABLE_LOCI)}, "
            f"got {sorted(parsed_rows)}"
        )

    for b_id, spec in EXPECTED_RELEVANCE_TABLE_LOCI.items():
        comparison, discussed, locator, depth, _desc = parsed_rows[b_id]
        if normalize_text_for_match(comparison) != normalize_text_for_match(spec["comparison"]):
            raise ValueError(
                f"relevance_scan.md [{b_id}]: Comparison mismatch against canonical B001 table: "
                f"expected '{spec['comparison']}', got '{comparison}'"
            )
        if discussed != spec["status"]:
            raise ValueError(
                f"relevance_scan.md [{b_id}]: Discussed status mismatch: expected '{spec['status']}', got '{discussed}'"
            )
        if depth != spec["depth"]:
            raise ValueError(
                f"relevance_scan.md [{b_id}]: Depth mismatch: expected '{spec['depth']}', got '{depth}'"
            )
        if spec["status"] == "NO":
            if locator != "N/A":
                raise ValueError(f"relevance_scan.md [{b_id}]: Expected locator 'N/A' for NO row, got '{locator}'")
        else:
            parsed_loc = parse_bib_locator(locator)
            if parsed_loc["printed_pages"] != spec["pages"] or parsed_loc["pdf_pages"] != spec["pages"]:
                raise ValueError(
                    f"relevance_scan.md [{b_id}]: Page tuple mismatch: expected {spec['pages']}, got {parsed_loc['printed_pages']}"
                )
            if parsed_loc["footnotes"] != ():
                raise ValueError(
                    f"relevance_scan.md [{b_id}]: Unexpected footnote token in table locator '{locator}'"
                )

    if "- **B001-4 (Romans 10:11 / Isaiah 28:16):** Discussed — **Substantive**" not in rel_txt:
        raise ValueError("relevance_scan.md missing canonical summary bullet for B001-4 (Romans 10:11 / Isaiah 28:16)")

    if check_search_log:
        log_path = source_dir / "full_volume_search_log.md"
        if log_path.is_file():
            log_txt = log_path.read_text(encoding="utf-8")
            log_row_re = re.compile(r"^\|\s*`(B001-\d+)`\s*\|\s*([^|]+?)\s*\|\s*`([^`]+)`\s*\|", re.MULTILINE)
            log_rows = {m.group(1): (m.group(2).strip(), m.group(3).strip()) for m in log_row_re.finditer(log_txt)}
            for b_id, spec in EXPECTED_RELEVANCE_TABLE_LOCI.items():
                if b_id not in log_rows:
                    raise ValueError(f"full_volume_search_log.md missing search row for {b_id}")
                comp_str, cat_str = log_rows[b_id]
                if normalize_text_for_match(comp_str) != normalize_text_for_match(spec["comparison"]):
                    raise ValueError(
                        f"full_volume_search_log.md [{b_id}]: Comparison mismatch '{comp_str}' != '{spec['comparison']}'"
                    )
                exp_cat = "SUBSTANTIVE_DISCUSSION" if spec["status"] == "YES" else "CONFIRMED_ABSENT"
                if cat_str != exp_cat:
                    raise ValueError(f"full_volume_search_log.md [{b_id}]: Expected category {exp_cat}, got {cat_str}")


def _verify_supporting_prose_artifacts(source_dir: Path) -> None:
    """Verify synthesis headings/loci and clean prose discipline across argument_map & counterevidence."""
    synth_path = source_dir / "oliver_romans_10_chiasm_synthesis.md"
    if not synth_path.is_file():
        raise FileNotFoundError(f"Missing oliver_romans_10_chiasm_synthesis.md in {source_dir}")
    synth_txt = synth_path.read_text(encoding="utf-8")

    for subsec_title, expected_loc in EXPECTED_SYNTHESIS_SUBSECTIONS.items():
        if subsec_title not in synth_txt:
            raise ValueError(f"synthesis missing expected subsection heading '{subsec_title}'")
        sec_idx = synth_txt.find(subsec_title)
        next_sec_idx = synth_txt.find("\n## ", sec_idx + len(subsec_title))
        sub_block = synth_txt[sec_idx:next_sec_idx] if next_sec_idx != -1 else synth_txt[sec_idx:]
        if expected_loc not in sub_block:
            raise ValueError(
                f"synthesis missing expected locus '{expected_loc}' within its subsection block '{subsec_title}'"
            )

    for fname in ("argument_map.md", "counterevidence.md"):
        fpath = source_dir / fname
        if not fpath.is_file():
            raise FileNotFoundError(f"Missing {fname} in {source_dir}")
        ftxt = fpath.read_text(encoding="utf-8")
        for ui_tok in ("expand_more", "unfold_less", "keep_pin", "thumb_up", "\nThoughts\n"):
            if ui_tok in ftxt:
                raise ValueError(f"{fname}: Raw NotebookLM UI token '{ui_tok.strip()}' must be removed")
        if "Acts 2:21" in ftxt:
            raise ValueError(f"{fname}: Erroneous 'Acts 2:21' reference must be corrected to 'Acts 2:17–21'")


def _verify_bibliography_leads(source_dir: Path, page_texts: list[str] | None = None) -> None:
    """Enforce exact 26-lead inventory, structured metadata, locators, provenance, and PDF witness fidelity."""
    bib_path = source_dir / "bibliography_leads.md"
    if not bib_path.is_file():
        raise FileNotFoundError(f"Missing bibliography_leads.md in {source_dir}")
    bib_txt = bib_path.read_text(encoding="utf-8")

    lower_bib = bib_txt.lower()
    for bad in FORBIDDEN_BIB_CONTAINERS:
        if bad in lower_bib:
            raise ValueError(f"bibliography_leads.md: Forbidden unprinted/fabricated metadata '{bad}'")

    bib_blocks = re.split(r"(?=^###\s+)", bib_txt, flags=re.MULTILINE)
    bib_block_map: dict[str, str] = {}
    for blk in bib_blocks:
        m = re.match(r"^###\s+([^\n]+)", blk)
        if m:
            entry_title = m.group(1).strip()
            if entry_title in bib_block_map:
                raise ValueError(f"bibliography_leads.md: Duplicate section block for '{entry_title}'")
            bib_block_map[entry_title] = blk

    expected_headers = {lead["header"] for lead in EXPECTED_BIBLIOGRAPHY_LEADS}
    actual_headers = set(bib_block_map.keys())
    extra_headers = sorted(actual_headers - expected_headers)
    missing_headers = sorted(expected_headers - actual_headers)
    if extra_headers:
        raise ValueError(f"bibliography_leads.md: Unexpected extra lead block(s): {extra_headers}")
    if missing_headers:
        raise ValueError(f"bibliography_leads.md: Missing expected lead block(s): {missing_headers}")

    for lead in EXPECTED_BIBLIOGRAPHY_LEADS:
        lead_header = lead["header"]
        blk = bib_block_map[lead_header]

        m_hdr_year = re.search(r"\((\d{4})\)", lead_header)
        if not m_hdr_year or int(m_hdr_year.group(1)) != lead["year"]:
            raise ValueError(f"bibliography_leads.md [{lead_header}]: Header year mismatch")

        cit_lines = re.findall(r"(?m)^-\s+\*\*Citation:\*\*\s*([^\n]+)$", blk)
        if len(cit_lines) != 1:
            raise ValueError(f"bibliography_leads.md [{lead_header}]: Expected 1 Citation line, found {len(cit_lines)}")
        if normalize_text_for_match(lead["citation"]) != normalize_text_for_match(cit_lines[0].strip()):
            raise ValueError(
                f"bibliography_leads.md [{lead_header}]: Citation mismatch: expected '{lead['citation']}', got '{cit_lines[0].strip()}'"
            )

        cont_lines = re.findall(r"(?m)^-\s+\*\*Container / Venue:\*\*\s*([^\n]+)$", blk)
        if len(cont_lines) != 1:
            raise ValueError(f"bibliography_leads.md [{lead_header}]: Expected 1 Container / Venue line, found {len(cont_lines)}")
        cont_val = cont_lines[0].strip()
        for tok in lead["container_tokens"]:
            if tok.lower() not in cont_val.lower():
                raise ValueError(
                    f"bibliography_leads.md [{lead_header}]: Container / Venue missing required token '{tok}' in '{cont_val}'"
                )
        for bad_tok in lead["forbidden_tokens"]:
            if bad_tok.lower() in blk.lower():
                raise ValueError(
                    f"bibliography_leads.md [{lead_header}]: Forbidden token '{bad_tok}' found in block"
                )

        ref_lines = re.findall(r"(?m)^-\s+\*\*Oliver References Page:\*\*\s*([^\n]+)$", blk)
        if len(ref_lines) != 1:
            raise ValueError(
                f"bibliography_leads.md [{lead_header}]: Expected 1 Oliver References Page line, found {len(ref_lines)}"
            )
        ref_val = ref_lines[0].strip()
        exp_ref_marker = f"Printed p. {lead['ref_page']} [PDF p. {lead['ref_page']}]"
        if exp_ref_marker not in ref_val or lead["ref_key"] not in ref_val:
            raise ValueError(
                f"bibliography_leads.md [{lead_header}]: Oliver References Page mismatch: expected '{exp_ref_marker}' & '{lead['ref_key']}', got '{ref_val}'"
            )

        loc_lines = re.findall(r"(?m)^-\s+\*\*Oliver Locators:\*\*\s*([^\n]+)$", blk)
        if len(loc_lines) != 1:
            raise ValueError(
                f"bibliography_leads.md [{lead_header}]: Expected 1 Oliver Locators line, found {len(loc_lines)}"
            )
        parsed_bib_loc = parse_bib_locator(loc_lines[0].strip())
        if parsed_bib_loc["printed_pages"] != lead["printed_pages"] or parsed_bib_loc["pdf_pages"] != lead["pdf_pages"]:
            raise ValueError(
                f"bibliography_leads.md [{lead_header}]: Locator page mismatch: expected {lead['printed_pages']}, got {parsed_bib_loc['printed_pages']}"
            )
        if parsed_bib_loc["footnotes"] != lead["footnotes"]:
            raise ValueError(
                f"bibliography_leads.md [{lead_header}]: Footnote mismatch: expected {lead['footnotes']}, got {parsed_bib_loc['footnotes']}"
            )

        prov_lines = re.findall(r"(?m)^-\s+\*\*Source-Witness Provenance:\*\*\s*([^\n]+)$", blk)
        if len(prov_lines) != 1:
            raise ValueError(
                f"bibliography_leads.md [{lead_header}]: Expected 1 Source-Witness Provenance line, found {len(prov_lines)}"
            )
        prov_val = prov_lines[0].strip()
        if "oliver_2015_romans_10.pdf" not in prov_val or "References" not in prov_val:
            raise ValueError(
                f"bibliography_leads.md [{lead_header}]: Source-Witness Provenance must cite oliver_2015_romans_10.pdf & References: '{prov_val}'"
            )
        if "independent external" in prov_val.lower() or "crossref" in prov_val.lower():
            raise ValueError(
                f"bibliography_leads.md [{lead_header}]: Must not misrepresent internal witness match as external verification: '{prov_val}'"
            )

        if page_texts is not None:
            ref_txt = page_texts[lead["ref_page"] - 1]
            if lead["witness_token"] not in ref_txt or str(lead["year"]) not in ref_txt:
                raise ValueError(
                    f"bibliography_leads.md [{lead_header}]: PDF Reference page {lead['ref_page']} witness check failed"
                )
            for pg in parsed_bib_loc["printed_pages"]:
                if lead["witness_token"] not in page_texts[pg - 1]:
                    raise ValueError(
                        f"bibliography_leads.md [{lead_header}]: Witness token '{lead['witness_token']}' not found on PDF p. {pg}"
                    )
            for fn_pg, fn_num in parsed_bib_loc["footnotes"]:
                pg_txt = page_texts[fn_pg - 1]
                if not re.search(rf"(?m)^{fn_num}\.", pg_txt):
                    raise ValueError(
                        f"bibliography_leads.md [{lead_header}]: Footnote {fn_num} not found on PDF p. {fn_pg}"
                    )


def verify_cross_artifact_consistency(
    source_dir: Path,
    ledger_rows: list[dict] | None = None,
    page_texts: list[str] | None = None,
    verify_search_log: bool = True,
) -> None:
    """Verify extraction.md, relevance_scan.md, synthesis, prose artifacts, bibliography_leads.md, and manifest."""
    if ledger_rows is None:
        ledger_rows = load_evidence_ledger(source_dir / "citation_ledger.csv")
    ledger_map = {r["evidence_id"]: r for r in ledger_rows}

    _verify_extraction_artifact(source_dir, ledger_map)
    _verify_relevance_scan_and_canonical(source_dir, check_search_log=verify_search_log)
    _verify_supporting_prose_artifacts(source_dir)
    _verify_bibliography_leads(source_dir, page_texts=page_texts)

    man_path = source_dir / "provenance_manifest.json"
    if not man_path.is_file():
        raise FileNotFoundError(f"Missing provenance_manifest.json in {source_dir}")
    import json
    with open(man_path, "r", encoding="utf-8") as f:
        man = json.load(f)
    if man.get("source_id") != "S09F":
        raise ValueError(f"provenance_manifest.json: expected source_id S09F, got {man.get('source_id')}")
    if man.get("ingested_volume", {}).get("sha256") != EXPECTED_RAW_PDF_SHA256:
        raise ValueError("provenance_manifest.json: raw PDF SHA-256 mismatch")


def generate_search_log_markdown(
    pdf_bytes: int,
    pdf_sha: str,
    text_chars: int,
    text_bytes: int,
    text_sha: str,
    pos_controls: list[dict],
    witnesses: list[dict],
    search_results: list[dict],
) -> str:
    lines = [
        "# S09F — Full-Volume Negative Search and Locus Verification Log",
        "",
        "**Source Volume:** Willem Oliver, *Romans 10:5–13 revisited*, *HTS Teologiese Studies / Theological Studies*, Vol. 71, No. 3 (2015), Art. #2929, 12 pages.",
        f"**Source PDF:** `oliver_2015_romans_10.pdf` ({pdf_bytes:,} bytes, SHA-256 `{pdf_sha}`)",
        f"**Text Layer Digest:** SHA-256 `{text_sha}` ({text_chars:,} chars, {text_bytes:,} bytes across 12 article pages)",
        "**Pagination Invariant:** Monotonic $printed = PDF$ (offset = 0) across all 12 article pages (PDF pp. 1–12 = printed pp. 1–12).",
        "",
        "---",
        "",
        "## 1. Positive Controls Across Article Sections",
        "",
        "| ID | Section / Concept | Printed Page | PDF Page | Normalized Text Witness | Status |",
        "| :--- | :--- | :--- | :--- | :--- | :--- |",
    ]
    for pc in pos_controls:
        snip = pc["snippet"]
        if len(snip) > 60:
            snip = snip[:57] + "..."
        lines.append(
            f"| `{pc['id']}` | {pc['name']} | p. {pc['printed_page']} | PDF p. {pc['pdf_page']} | \"{snip}\" | `VERIFIED` |"
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
        snip = w["short_quote"]
        if len(snip) > 50:
            snip = snip[:47] + "..."
        lines.append(
            f"| `{w['evidence_id']}` | `{w['b001_id']}` | {w['claim_type']} | {w['locator']} | \"{snip}\" | `VERIFIED` |"
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
    for sr in search_results:
        lines.append(
            f"| `{sr['id']}` | {sr['comparison']} | `{sr['category']}` | {sr['hit_count']} hits | {sr['judgment']} |"
        )

    lines.extend([
        "",
        "---",
        "",
        "## 4. Verification Metadata and Cryptographic Signatures",
        "",
        "- **Verification Timestamp:** `2026-11-13T16:30:00Z`",
        "- **PDF Path:** `/Users/chrisrodriguez/Downloads/oliver_2015_romans_10.pdf`",
        f"- **Raw PDF SHA-256:** `{pdf_sha}`",
        f"- **Text Layer SHA-256:** `{text_sha}`",
        "- **Evidence Ledger:** `research/inbox/B001-pauline-txt-pilot/sources/S09F/citation_ledger.csv`",
        "- **Deliverables Directory:** `research/inbox/B001-pauline-txt-pilot/sources/S09F/`",
        (
            f"- **Overall Determination:** `PASSED` — All {len(pos_controls)} positive controls verified across the "
            f"{EXPECTED_PAGE_COUNT}-page volume; all {len(witnesses)} evidence ledger rows verified (5 direct B001-4/B001-5 "
            "+ 5 B001-CONTEXT pericope-context rows) with exact physical text witnesses; 10 absent loci confirmed with zero hits; "
            "cross-artifact consistency verified."
        ),
        "",
    ])

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Deterministic full-volume verifier for S09F (Oliver 2015).")
    parser.add_argument("--check-only", action="store_true", help="Fail closed if output log differs from existing on disk.")
    parser.add_argument("--pdf", type=Path, default=PDF_DEFAULT, help="Path to source PDF.")
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER_PATH, help="Path to citation_ledger.csv.")
    parser.add_argument("--source-dir", type=Path, default=DEFAULT_SOURCE_DIR, help="Path to S09F deliverable directory.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUT_PATH, help="Path to write full_volume_search_log.md.")
    args = parser.parse_args()

    if not args.pdf.is_file():
        raise FileNotFoundError(f"Missing PDF: {args.pdf}")

    raw_bytes = args.pdf.read_bytes()
    raw_size = len(raw_bytes)
    raw_sha = hashlib.sha256(raw_bytes).hexdigest()

    if raw_size != EXPECTED_RAW_PDF_BYTES:
        raise ValueError(f"Raw PDF byte size mismatch: expected {EXPECTED_RAW_PDF_BYTES}, got {raw_size}")
    if raw_sha != EXPECTED_RAW_PDF_SHA256:
        raise ValueError(f"Raw PDF SHA-256 mismatch: expected {EXPECTED_RAW_PDF_SHA256}, got {raw_sha}")

    page_texts = extract_page_texts(args.pdf)
    if len(page_texts) != EXPECTED_PAGE_COUNT:
        raise ValueError(f"Expected {EXPECTED_PAGE_COUNT} pages, got {len(page_texts)}")

    full_text = "".join(page_texts)
    text_bytes = len(full_text.encode("utf-8"))
    text_chars = len(full_text)
    text_sha = hashlib.sha256(full_text.encode("utf-8")).hexdigest()

    if text_bytes != EXPECTED_TEXT_BYTES:
        raise ValueError(f"Text bytes mismatch: expected {EXPECTED_TEXT_BYTES}, got {text_bytes}")
    if text_chars != EXPECTED_TEXT_CHARS:
        raise ValueError(f"Text chars mismatch: expected {EXPECTED_TEXT_CHARS}, got {text_chars}")
    if text_sha != EXPECTED_TEXT_SHA256:
        raise ValueError(f"Text SHA-256 mismatch: expected {EXPECTED_TEXT_SHA256}, got {text_sha}")

    verify_monotonic_pagination(page_texts)
    pos_controls = verify_positive_controls(page_texts)
    rows = load_evidence_ledger(args.ledger)
    witnesses = verify_ledger_witnesses(rows, page_texts)
    search_results = execute_full_volume_search(page_texts, witnesses)
    verify_cross_artifact_consistency(
        args.source_dir,
        ledger_rows=rows,
        page_texts=page_texts,
        verify_search_log=args.check_only,
    )

    rendered_md = generate_search_log_markdown(
        raw_size, raw_sha, text_chars, text_bytes, text_sha,
        pos_controls, witnesses, search_results
    )

    if args.check_only:
        if not args.output.is_file():
            raise FileNotFoundError(f"--check-only failed: missing output log {args.output}")
        disk_md = args.output.read_text(encoding="utf-8")
        if disk_md != rendered_md:
            diff = "".join(difflib.unified_diff(
                disk_md.splitlines(keepends=True),
                rendered_md.splitlines(keepends=True),
                fromfile=str(args.output),
                tofile="<generated>"
            ))
            raise ValueError(f"--check-only failed: full_volume_search_log.md differs:\n{diff}")
        print(f"OK: {args.output} matches generated report byte-for-byte (--check-only passed).")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered_md, encoding="utf-8")
        print(f"SUCCESS: Generated {args.output} ({len(rendered_md)} chars, {len(rendered_md.encode('utf-8'))} bytes).")

    print(f"Verified {len(pos_controls)} positive controls.")
    print(f"Verified {len(witnesses)} evidence ledger rows.")
    print(f"Verified 12 B001 search targets across {EXPECTED_PAGE_COUNT} pages.")
    print(f"Verified cross-artifact section/field-bound consistency, subsection-bound synthesis, and structured bibliographic witnesses across all deliverables.")


if __name__ == "__main__":
    main()
