# S04F — Full-Volume Negative Search Verification Log

**Source ID:** S04F  
**Author:** J. B. Lightfoot  
**Title:** *Saint Paul's Epistle to the Galatians: A Revised Text with Introduction, Notes, and Dissertations*  
**Edition:** 1914 reprint of the tenth edition (1890)  
**Publisher:** Macmillan and Co., Limited; London  
**Raw Volume Scan:** `lightfoot_1914_galatians_ia_raw.pdf` (27,846,788 bytes, SHA-256: `0131c0916a037f058cd9607d60ce1bf1c93fdabff621ca31767ec03b3d5788f4`)  
**Extracted Text Layer:** `lightfoot_full_text.txt` (1,129,735 characters, 41,813 lines, SHA-256: `213da03319394f724893c31ae77bf24251020220f19e27fbf4068fc7cc34c219`)  
**Cryptographic Text Authentication:** VERIFIED  
**Gate Verification Overall:** **PASS**

---

## Executive Summary

Lightfoot's *Saint Paul's Epistle to the Galatians* (1914) provides exhaustive exegesis, text-critical analysis, and historical dissertations on the Epistle to the Galatians.
The primary B001 target in this volume is **B001-12 (Galatians 3:13 / Deuteronomy 21:23)**, which receives extensive treatment across the Introduction (§ V pp. 60–61), commentary on Gal 3:13 (pp. 139–140), and a dedicated three-page excursus (*The interpretation of Deut. xxi. 23*, pp. 152–154).

A full-volume text search across all 408 pages of the authentic volume establishes the following distribution for the remaining eleven B001 targets:
1. **B001-1 (Romans 4:3 / Genesis 15:6):** Substantive cross-epistle comparison on Galatians 3:6 (printed p. 136), analyzing the quotation of Gen 15:6 LXX, comparing passive ἐλογίσθη with Hebrew active וַיַּחְשְׁבֶהָ, cross-referencing Rom 4:3, James 2:23, Clement of Rome, and Justin Martyr, and dedicating two substantial excursuses (*The words denoting Faith*, pp. 154–158; *The Faith of Abraham*, pp. 158–164) to Philonic allegory and rabbinic interpretations.
2. **B001-8 (1 Corinthians 1:19 / Isaiah 29:14):** 1 passing lexical citation on Galatians 2:21 (printed p. 120), citing 1 Cor 1:19 for the lexical meaning of ἀθετῶ ('to nullify'); no quotation analysis of Isaiah 29:14.
3. **B001-11 (1 Corinthians 10:7 / Exodus 32:6):** 1 passing illustration citation in Dissertation III (*St Paul and the Three*, printed p. 311), citing 1 Cor 10:7–8 on the Balaam idolatry illustration; no commentary on Exodus 32:6.
4. **Remaining Eight Loci (B001-2, B001-3, B001-4, B001-5, B001-6, B001-7, B001-9, B001-10):** **0 occurrences** detected for the enumerated search patterns across all 408 pages.
   - *Measured Methodological Scope:* Regex pattern searches detect specific book/chapter/verse citation typography in authentic 19th/20th-century formats, including Septuagint/MT alternate versifications (e.g. Joel 3:5 / iii. 5, Hos 2:25, Hos 2:1). They do not constitute an exhaustive semantic proof of every unnumbered allusion or thematic discussion; however, authorial index validation confirms no dedicated entries for these scriptural loci exist in the volume's comprehensive index under either bounded multi-entry book sections or standalone citation forms.

---

## Positive-Control Validation (Authentic Citation Typography)

Total Positive Controls Evaluated: **6**

| Target / Passage | Regex Pattern | Expected Min | Detected Matches | Status |
|:---|:---|:---:|:---:|:---:|
| Gal 3:13 / Deut 21:23 (Commentary pp. 139-140, Excursus p. 152, Intro p. 60) | `\b(?:Deut|Deuteronomy)\b\.?\s*\b(?:21|xxi)\b\s*[:\.,]\s*\b(?:23|xxiii)\b` | 4 | 4 | **PASS** |
| Gal 3:6 / Gen 15:6 (Commentary p. 136, Excursuses pp. 156, 157, 164) | `\b(?:Gen|Genesis)\b\.?\s*\b(?:15|xv)\b\s*[:\.,]\s*\b(?:6|vi)\b` | 4 | 4 | **PASS** |
| Gal 3:11 / Hab 2:4 (Commentary p. 138) | `\b(?:Hab|Habakkuk)\b\.?\s*\b(?:2|ii)\b\s*[:\.,]\s*\b(?:4|iv)\b` | 1 | 3 | **PASS** |
| Justin Martyr Dialogue citation (Intro p. 60, Commentary p. 140, Excursus p. 153) | `\bJustin\b.*?\b(?:Dial|Tryph)\b` | 3 | 11 | **PASS** |
| Index positive control: Deuteronomy passages commented on | `Deuteronomy,\s*passages\s+commented\s+on` | 1 | 1 | **PASS** |
| Index positive control: Genesis passages commented on | `Genesis,\s*passages\s+commented` | 1 | 1 | **PASS** |

**Positive Controls Overall Verdict:** **PASS**

---

## Bounded Index Structure & Scripture Reference Validation

- **Index Present:** True
- **Index Start Offset:** 1101620
- **Index End Offset:** 1129038
- **Authentic End Delimiter Verified:** True
  - Positive Control `Deuteronomy commented on`: FOUND
  - Positive Control `Genesis commented on`: FOUND
  - Positive Control `Acts commented on`: FOUND
  - Positive Control `Abraham faith entry`: FOUND
  - Positive Control `Judaizers entry`: FOUND
- **Structural Controls Verdict:** **PASS**
- **Per-Locus Scripture Targets Verdict:** **PASS**
- **Index Validation Overall Verdict:** **PASS**

### Per-Locus Authorial Scripture Index Ledger

Lightfoot's *Galatians* index combines subjects, persons, Greek words, and scriptural citations into a single comprehensive index (printed pp. 375–384), indexing scripture passages commented on directly under their respective biblical book names (e.g. *Genesis, passages commented on*, *Deuteronomy, passages commented on*).
Each B001 target is evaluated against the bounded index text using dual-mode verification and authorial census cross-checking:
1. **Bounded Book-Section Parsing:** Extracts multi-entry citation lists following each book heading up to the next major headword entry (or up to 2,500 characters), detecting entries regardless of intervening citations or distance from the heading. Specifically binds reordered two-column OCR continuations (such as the column-break split between pp. 376 col. 2 and 377 col. 1 for *Corinthians, 1st Epistle to the*).
2. **Standalone Citation Typography:** Evaluates standard citation typography, abbreviations, and Septuagint/MT alternate versifications (e.g. Joel 3:5 / iii. 5, Hos 2:25, Hos 2:1) across the entire bounded index text.
3. **Authorial Scripture Census Cross-Check:** Verified against the exhaustive 13-entry scriptural book census (`tests/fixtures/s04f_authorial_index_scripture_ledger.json`). Book headings present in index: Acts, 1 Cor, 2 Cor, Deut, Exod, Eph, Gen, Hab, John, 1 Macc, Rev, Rom, 2 Tim. Unindexed books: Hosea, Joel, Isaiah.

| B001 ID | Comparison | NT / OT Target | Expected in Index | Detected Index Matches | Index Verification Status |
|:---|:---|:---|:---:|:---|:---:|
| `B001-1` | Rom 4:3 / Gen 15:6 | Romans 4:3 / Genesis 15:6 | **YES** | `xv.  6`; `(xv.  6)`; `Genesis, passages commented  on, (xv.  6)` | **VERIFIED INDEX ENTRY** |
| `B001-2` | Rom 9:25 / Hos 2:23 (LXX 2:25) | Romans 9:25 / Hosea 2:23 (LXX 2:25) | NO | *None (0 entries)* | **UNINDEXED BOOK (NO AUTHORIAL HEADING)** |
| `B001-3` | Rom 9:26 / Hos 1:10 (LXX 2:1) | Romans 9:26 / Hosea 1:10 (LXX 2:1) | NO | *None (0 entries)* | **UNINDEXED BOOK (NO AUTHORIAL HEADING)** |
| `B001-4` | Rom 10:11 / Isa 28:16 | Romans 10:11 / Isaiah 28:16 | NO | *None (0 entries)* | **UNINDEXED BOOK (NO AUTHORIAL HEADING)** |
| `B001-5` | Rom 10:13 / Joel 2:32 (LXX 3:5) | Romans 10:13 / Joel 2:32 (LXX 3:5) | NO | *None (0 entries)* | **UNINDEXED BOOK (NO AUTHORIAL HEADING)** |
| `B001-6` | Rom 11:34 / Isa 40:13 | Romans 11:34 / Isaiah 40:13 | NO | *None (0 entries)* | **UNINDEXED BOOK (NO AUTHORIAL HEADING)** |
| `B001-7` | Rom 15:12 / Isa 11:10 | Romans 15:12 / Isaiah 11:10 | NO | *None (0 entries)* | **UNINDEXED BOOK (NO AUTHORIAL HEADING)** |
| `B001-8` | 1 Cor 1:19 / Isa 29:14 | 1 Corinthians 1:19 / Isaiah 29:14 | NO | *None (0 entries)* | **VERIFIED ABSENT (BOOK INDEXED; TARGET ABSENT)** |
| `B001-9` | 1 Cor 6:16 / Gen 2:24 | 1 Corinthians 6:16 / Genesis 2:24 | NO | *None (0 entries)* | **VERIFIED ABSENT (BOOK INDEXED; TARGET ABSENT)** |
| `B001-10` | 1 Cor 9:9 / Deut 25:4 | 1 Corinthians 9:9 / Deuteronomy 25:4 | NO | *None (0 entries)* | **VERIFIED ABSENT (BOOK INDEXED; TARGET ABSENT)** |
| `B001-11` | 1 Cor 10:7 / Exod 32:6 | 1 Corinthians 10:7 / Exodus 32:6 | NO | *None (0 entries)* | **VERIFIED ABSENT (BOOK INDEXED; TARGET ABSENT)** |
| `B001-12` | Gal 3:13 / Deut 21:23 | Galatians 3:13 / Deuteronomy 21:23 | **YES** | `xxi. 23`; `(xxi. 23)`; `Deuteronomy, passages commented on;  (xxi. 23)` | **VERIFIED INDEX ENTRY** |

---

## Systematic B001 Target Query Results

| B001 ID | Comparison | NT Target | OT Target | Hits | Adjudication |
|:---|:---|:---|:---|:---:|:---|
| `B001-1` | Romans 4:3 / Genesis 15:6 | Rom 4:3 | Gen 15:6 | 5 | SUBSTANTIVE CROSS-EPISTLE COMPARISON (5 hit(s): Gal 3:6 commentary p. 136, Faith excursuses pp. 156, 157, 164) |
| `B001-2` | Romans 9:25 / Hosea 2:23 | Rom 9:25 | Hos 2:23 (LXX 2:25) | 0 | NO OCCURRENCES FOR ENUMERATED PATTERNS (0 hits in pinned text layer; verified absent from authorial index) |
| `B001-3` | Romans 9:26 / Hosea 1:10 | Rom 9:26 | Hos 1:10 (LXX 2:1) | 0 | NO OCCURRENCES FOR ENUMERATED PATTERNS (0 hits in pinned text layer; verified absent from authorial index) |
| `B001-4` | Romans 10:11 / Isaiah 28:16 | Rom 10:11 | Isa 28:16 | 0 | NO OCCURRENCES FOR ENUMERATED PATTERNS (0 hits in pinned text layer; verified absent from authorial index) |
| `B001-5` | Romans 10:13 / Joel 2:32 | Rom 10:13 | Joel 2:32 (LXX 3:5) | 0 | NO OCCURRENCES FOR ENUMERATED PATTERNS (0 hits in pinned text layer; verified absent from authorial index) |
| `B001-6` | Romans 11:34 / Isaiah 40:13 | Rom 11:34 | Isa 40:13 | 0 | NO OCCURRENCES FOR ENUMERATED PATTERNS (0 hits in pinned text layer; verified absent from authorial index) |
| `B001-7` | Romans 15:12 / Isaiah 11:10 | Rom 15:12 | Isa 11:10 | 0 | NO OCCURRENCES FOR ENUMERATED PATTERNS (0 hits in pinned text layer; verified absent from authorial index) |
| `B001-8` | 1 Corinthians 1:19 / Isaiah 29:14 | 1 Cor 1:19 | Isa 29:14 | 1 | PASSING CITATION (1 hit(s): lexical note on ἀθετῶ, Gal 2:21 p. 120) |
| `B001-9` | 1 Corinthians 6:16 / Genesis 2:24 | 1 Cor 6:16 | Gen 2:24 | 0 | NO OCCURRENCES FOR ENUMERATED PATTERNS (0 hits in pinned text layer; verified absent from authorial index) |
| `B001-10` | 1 Corinthians 9:9 / Deuteronomy 25:4 | 1 Cor 9:9 | Deut 25:4 | 0 | NO OCCURRENCES FOR ENUMERATED PATTERNS (0 hits in pinned text layer; verified absent from authorial index) |
| `B001-11` | 1 Corinthians 10:7 / Exodus 32:6 | 1 Cor 10:7 | Exod 32:6 | 1 | PASSING CITATION (1 hit(s): Balaam illustration cross-reference, Diss. III p. 311; no exegesis of Exod 32:6) |

---

## Detailed Evidence Ledger for Detected Matches

### B001-1: Romans 4:3 / Genesis 15:6 (5 detected hit(s))

#### Hit 1 (Offset: 401713)
- **Matched Text:** `Gen. xv. 6`
- **Snippet:** `...Phryn. p. 425. *"ABpaap eriotevoey x.t.A.] from the Lxx of Gen. xv. 6. The Hebrew has in the second clause ApIy % mawmy  ‘and (He...`
- **Classification:** `SUBSTANTIVE_CROSS_EPISTLE_COMPARISON`
- **Substantive:** `True`
- **Scholarly Rationale:** Commentary on Gal 3:6 (printed p. 136): explicitly analyzes quotation from Gen 15:6 LXX, compares LXX passive ἐλογίσθη with Hebrew active וַיַּחְשְׁבֶהָ, and cross-references Rom 4:3 and James 2:23.

#### Hit 2 (Offset: 401860)
- **Matched Text:** `Rom. iv. 3`
- **Snippet:** `...im (for) righteousness.’ It is quoted as in the Lxx also in Rom. iv. 3, James ii. 23, Clem. Rom.§ 10, Justin Dial. c. Tryph. § 119...`
- **Classification:** `SUBSTANTIVE_CROSS_EPISTLE_COMPARISON`
- **Substantive:** `True`
- **Scholarly Rationale:** Commentary on Gal 3:6 (printed p. 136): explicitly compares citation across Romans 4:3, James 2:23, Clement of Rome, and Justin Martyr.

#### Hit 3 (Offset: 464081)
- **Matched Text:** `Gen. xv. 6`
- **Snippet:** `...positions, 3 or 5), and is rendered morevw in the Lxx, e.g. Gen. xv. 6. But there is in biblical Hebrew no corresponding substanti...`
- **Classification:** `SUBSTANTIVE_CROSS_EPISTLE_COMPARISON`
- **Substantive:** `True`
- **Scholarly Rationale:** Excursus 'The words denoting Faith' (printed p. 156): philological analysis of Hebrew root אמן and LXX translation in Gen 15:6.

#### Hit 4 (Offset: 465991)
- **Matched Text:** `Gen. xv. 6`
- **Snippet:** `...rgum of Jonathan, the  word  denoting the faith of Abraham, Gen. xv. 6, is Xm)2D'N, and the  Syriac renders zio7s in the New Testa...`
- **Classification:** `SUBSTANTIVE_CROSS_EPISTLE_COMPARISON`
- **Substantive:** `True`
- **Scholarly Rationale:** Excursus 'The words denoting Faith' (printed p. 157): analysis of Targum Jonathan on Gen 15:6 and Syriac version.

#### Hit 5 (Offset: 489819)
- **Matched Text:** `Gen. xv. 6`
- **Snippet:** `...ast to these earlier comments is the treatment of the text, Gen. xv. 6, bysome later Jewish writers. Anxious, it would appear, to...`
- **Classification:** `SUBSTANTIVE_CROSS_EPISTLE_COMPARISON`
- **Substantive:** `True`
- **Scholarly Rationale:** Excursus 'The Faith of Abraham' (printed p. 164): analysis of later Jewish interpretations of Gen 15:6 in the Mechilta and rabbinic tradition.

### B001-8: 1 Corinthians 1:19 / Isaiah 29:14 (1 detected hit(s))

#### Hit 1 (Offset: 346524)
- **Matched Text:** `1 Cor. i. 19`
- **Snippet:** `...were superfluous,’ For déeré ‘to nullify’ see Luke vii. 30, 1 Cor. i. 19: its exact sense here is fixed by dwpeay arcOavev. ‘The gra...`
- **Classification:** `PASSING_CITATION`
- **Substantive:** `False`
- **Scholarly Rationale:** Commentary on Gal 2:21 (printed p. 120): passing lexical cross-reference on the verb ἀθετῶ ('to nullify'); no analysis of the Isaiah 29:14 quotation or its OT context.

### B001-11: 1 Corinthians 10:7 / Exodus 32:6 (1 detected hit(s))

#### Hit 1 (Offset: 926505)
- **Matched Text:** `1 Cor.

x. 7`
- **Snippet:** `...f Balaam, St Paul uses the same Old Testament illustration, 1 Cor.  x. 7, 8, ‘Neither be ye idolaters, as were some of them; as it i...`
- **Classification:** `PASSING_CITATION`
- **Substantive:** `False`
- **Scholarly Rationale:** Dissertation III 'St Paul and the Three' (printed p. 311): passing cross-reference to Paul using OT idolatry illustration from Balaam incident (1 Cor 10:7-8); no commentary on Exodus 32:6 text or version.

---

## Negative Search Verification Verdict

- **Cryptographic Text Binding:** PASSED (Pinned SHA-256 `213da03319394f724893c31ae77bf24251020220f19e27fbf4068fc7cc34c219`)
- **Citation Typography Controls:** PASSED (6 positive controls validated)
- **Bounded Index Structure & Loci Verification:** PASSED (Authentic colophon delimiter verified, positive controls confirmed, per-locus absence verified across all 8 negative targets)
- **Loci Absent (0 Hits for Enumerated Patterns):** B001-2, B001-3, B001-4, B001-5, B001-6, B001-7, B001-9, B001-10 (8 loci)
- **Loci Passing Only:** B001-8 (1 hit, lexical note on Gal 2:21), B001-11 (1 hit, Balaam illustration in Diss. III p. 311)
- **Loci Substantive / Primary:** B001-1 (Substantive cross-epistle comparison on Gal 3:6 & Faith excursuses), B001-12 (Primary volume target: commentary pp. 139-140, excursus pp. 152-154)

- **Overall Negative Search Verdict:** **PASSED**

**Search Discipline Confirmation:** Negative findings are scoped to measured pattern typography in the authenticated text layer and corroborated by comprehensive authorial index inspection.
