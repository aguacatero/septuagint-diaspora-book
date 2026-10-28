# Full-Volume Negative & Comparative Search Verification Log — S03F

## 1. Provenance and Cryptographic Binding

- **Source ID:** S03F
- **Authors:** Archibald Robertson and Alfred Plummer
- **Title:** *A Critical and Exegetical Commentary on the First Epistle of St Paul to the Corinthians*
- **Series:** International Critical Commentary (ICC)
- **Edition / Year:** Second Edition, 1914 (First Edition 1911)
- **Raw Scan File:** `robertson_plummer_1911_1corinthians_icc_ia_raw.pdf`
- **Raw Scan File Size:** `32,652,569` bytes
- **Raw Scan SHA-256:** `4e7d0aa655aff66d84fca857387860d25dddd4c2be1c5aa2ea0446f11df78efd`
- **Full Extracted Text Size:** `1,423,358` bytes
- **Full Extracted Text SHA-256:** `9be8ab66f4f8bd70f67b0f22bc02e9cd9be48354d6a23a304d8b1d9d69a79ade`
- **Authentication Status:** **AUTHENTICATED** (matches expected 504-page volume digest)
- **Total Volume Pages:** 504 pages (pp. i–lxx, 1–424, plus title & plates)

---

## 2. Positive Control Verification

To establish that OCR text extraction and regular expression patterns reliably match 
authentic 19th/20th-century typographical conventions, Roman numerals, and citation formatting 
in this volume, positive controls were executed for known citations:

| Positive Control Citation | Expected Min | Actual Matches | Status | Sample Context |
| :--- | :--- | :--- | :--- | :--- |
| 1 Cor 1:19 / Isa 29:14 (Commentary p. 19, Intro p. liii) | 1 | 2 | **PASSED** | `v. 11, where he substitutes σοφῶν for ἀνθρώπων, or in i. 19=Isa. xxix. 14, where he_ subst...` |
| 1 Cor 6:16 / Gen 2:24 (Commentary p. 126, Intro p. liii) | 1 | 2 | **PASSED** | `πὶ ΧΙ]. 152 ΤΠ 10 Ξ Ob ν. 12 NI 20 ΞΞ ἘΞ' xcive LE vi. 16 = Gen. ii. 24 ix. 9 = Deut. xxv....` |
| 1 Cor 9:9 / Deut 25:4 (Commentary p. 183, Intro p. liii) | 1 | 3 | **PASSED** | `Ob ν. 12 NI 20 ΞΞ ἘΞ' xcive LE vi. 16 = Gen. ii. 24 ix. 9 = Deut. xxv. 4  Hxodtexxxi 16  x...` |
| 1 Cor 10:7 / Exod 32:6 (Commentary p. 203, Intro p. liii) | 1 | 2 | **PASSED** | `are these— vi. 16 = Gen. ii. 24 1x, Ὁ = Deut. παν. 4 x. 7 = Exod. xxxii. 6 χ 20. ΞΞ Dents ...` |
| 1 Cor 15:54 / Isa 25:8 (Commentary p. 378, Intro p. liii, liv) | 1 | 4 | **PASSED** | `ded by the Hebrew in diverging from the LXX, e.g. in xv. 54=Isa. xxv. 8. Sometimes he seem...` |
| Sanday and Headlam citation (Intro p. lii) | 1 | 12 | **PASSED** | `i. 22. Quotations from the O.T. The essay on the subject in Sanday and Headlam, Romans, pp...` |

---

## 3. Bounded Index Structure & Section-Localized Positive Controls

Inspection of the volume's back matter confirms bounded, ordered, and section-localized index structure:
- **Verified Section:** `INDEX I. GENERAL (pp. 403–414)`
- **Verified Section:** `INDEX II. GREEK WORDS (pp. 415–422)`
- **Verified Section:** `INDEX III. LATIN AND ENGLISH WORDS (pp. 423–424)`
- **Independent End Delimiter:** Verified (`Printed by Morrison & Gibb Limited, Edinburgh`).
- **Ordered Sequence Check:** Verified (`Index I < Index II < Index III < End Delimiter`).
- **Section-Localized Positive Controls:**
  - `Section I: Allegorical interpretation`: **VERIFIED**
  - `Section I: Assimilation`: **VERIFIED**
  - `Section I: Aquila`: **VERIFIED**
  - `Section II: ἀδάπανος`: **VERIFIED**
  - `Section II: ἀλοάω`: **VERIFIED**
  - `Section III: Caritas`: **VERIFIED**
  - `Section III: underling`: **VERIFIED**
- **Scripture / Biblical Reference Index Absence:** Verified absent. No Fourth Section, Scripture Index, or Passage Index heading exists in the volume (consistent with Dr. Plummer's Preface p. viii stating the indexes comprise author/subject and lexical indexes compiled by himself).

---

## 4. Target Query Verification Across All 504 Pages (Dynamic Adjudication)

Robertson and Plummer's commentary is dedicated to **1 Corinthians**. The B001 research corpus 
includes twelve specific Pauline quotation comparisons. Four belong directly to 1 Corinthians 
(B001-8, B001-9, B001-10, B001-11). The remaining eight loci (B001-1 through B001-7, B001-12) 
were scanned across the entire 504-page volume to evaluate presence, cross-epistle comparison, or genuine absence:

| B001 ID | Comparison Target | Measured Matches | Scholarly Classification | Dynamic Evaluated Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **B001-1** | Romans 4:3 / Genesis 15:6 | 0 | **NOT_DISCUSSED** | 0 matches found under verified search patterns across all 504 pages. |
| **B001-2** | Romans 9:25 / Hosea 2:23 | 2 | **NOT_DISCUSSED** | 2 passing citation(s) found without substantive discussion of target quotation. |
| **B001-3** | Romans 9:26 / Hosea 1:10 | 0 | **NOT_DISCUSSED** | 0 matches found under verified search patterns across all 504 pages. |
| **B001-4** | Romans 10:11 / Isaiah 28:16 | 0 | **NOT_DISCUSSED** | 0 matches found under verified search patterns across all 504 pages. |
| **B001-5** | Romans 10:13 / Joel 2:32 | 6 | **RELEVANT_INTERPRETIVE_CROSS_REFERENCE** | Commentary on 1 Cor 1:2 (printed p. 3): explicitly connects invocation formula from Joel 2:32 to Rom 10:12-13, analyzing Pauline worship of Christ under OT divine formula. |
| **B001-6** | Romans 11:34 / Isaiah 40:13 | 2 | **SUBSTANTIVE_CROSS_EPISTLE_COMPARISON** | Commentary on 1 Cor 2:16 (printed pp. 50-51): analyzes clause retention in Rom 11:34 vs omission in 1 Cor 2:16. |
| **B001-7** | Romans 15:12 / Isaiah 11:10 | 0 | **NOT_DISCUSSED** | 0 matches found under verified search patterns across all 504 pages. |
| **B001-12** | Galatians 3:13 / Deuteronomy 21:23 | 0 | **NOT_DISCUSSED** | 0 matches found under verified search patterns across all 504 pages. |

---

## 5. Itemized Match Evidence Ledger

Every individual regex match detected across the 504-page text layer is itemized below with its exact character offset, matched string, surrounding context, hit classification, and evaluation rationale:

| Hit # | Target ID | Offset | Matched Text | Surrounding Context Excerpt | Hit Classification | Evaluation Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **B001-2** | `690592` | `Rom. ix. 25` | `.... iv. 8, 9; two in a quotation in Gal. iv. 27 ; one each in Rom. ix. 25; Gal. iv. 8; Phil. iii. 3; Col. ii. 19; 1 Thess. ii. 4. See...` | **PASSING_CITATION** | Grammatical note cataloging Pauline usage of a word; no discussion of the quotation or its OT source. |
| 2 | **B001-2** | `1093294` | `Rom. ix. 25` | `...; ‘seeing that I am not fit to be called an Apostle.’ Comp. Rom. ix. 25; Heb. iit. 11. The violent ἔκτρωσις was rendered necessary...` | **PASSING_CITATION** | Passing parenthetical cross-reference on 1 Cor 15:9; no discussion of the quotation or its OT source. |
| 3 | **B001-5** | `76476` | `Rom. x. 13` | `...was the whole of his Gospel (ii. 2); He is ‘the Lord’ (cf. Rom. x. 13), ‘through whom are all things, and we through Him’ (viii....` | **PASSING_CITATION** | Passing reference to Rom 10:13 in Introduction p. xxxvii cataloging Pauline theological concepts; no quotation analysis. |
| 4 | **B001-5** | `228383` | `Rom. x. 13` | `...stances in Paul, ii. 16, x. 22; 2 Cor. x. 17; Phil. ii. r1; Rom. x. 13. Hort’s remarks on 1 Pet. ii. 3, where 6 Κύριος in Ps. xxxi...` | **PASSING_CITATION** | Passing cross-reference on 1 Cor 1:31 citing Hort on 1 Pet 2:3; no discussion of the Joel quotation or its OT source. |
| 5 | **B001-5** | `160303` | `Rom. x. 12,132` | `...involves the thought of faith, the common bond of all. See Rom. x. 12,132. Here, as there, St Paul significantly brings in the worshi...` | **RELEVANT_INTERPRETIVE_CROSS_REFERENCE** | Commentary on 1 Cor 1:2 (printed p. 3): explicitly connects invocation formula from Joel 2:32 to Rom 10:12-13, analyzing Pauline worship of Christ under OT divine formula. |
| 6 | **B001-5** | `288281` | `Rom. x. 12, 13` | `...ix. 13;  Ecclus. 1. 6;  Job xxxvi. 22, 23, 26; and see on Rom. x. 12, 13.  νοῦν Κυρίου. The νοῦν (LXX) corresponds to the Hebrew for...` | **PASSING_CITATION** | Passing cross-reference on 1 Cor 2:16 ('and see on Rom. x. 12, 13') pointing back to the earlier 1 Cor 1:2 note; not substantive quotation commentary in this passage. |
| 7 | **B001-5** | `717693` | `Rom. x. 12,13` | `...ntification can be clearly made out in the N.T.” But see on Rom. x. 12,13. Inthe N.T. ὁ Κύριος commonly means ‘our Lord’; but this is...` | **PASSING_CITATION** | Passing cross-reference on 1 Cor 10:9 ('But see on Rom. x. 12,13') pointing back to the earlier 1 Cor 1:2 note on divine titles; not substantive quotation commentary in this passage. |
| 8 | **B001-5** | `160227` | `Joel ii. 32` | `...ot all Christendom. τοῖς ἐπικαλουμένοις. This goes back  to Joel ii. 32, and involves the thought of faith, the common bond of all....` | **RELEVANT_INTERPRETIVE_CROSS_REFERENCE** | Commentary on 1 Cor 1:2 (printed p. 3): explicitly traces invocation formula to Joel 2:32, cross-references Rom 10:12-13, and analyzes Pauline christological transfer of OT Yahweh worship formula. |
| 9 | **B001-6** | `287850` | `Rom. xi. 34` | `...καὶ τίς αὐτοῦ σύνβουλος ἐγένετο; This clause is retained in Rom. xi. 34, while és συνβιβάσει αὐτόν is omitted. The aorist (ἔγνω) be...` | **SUBSTANTIVE_CROSS_EPISTLE_COMPARISON** | Commentary on 1 Cor 2:16 (printed pp. 50-51): analyzes clause retention in Rom 11:34 vs omission in 1 Cor 2:16. |
| 10 | **B001-6** | `287731` | `Isa. xl. 13` | `...nal norm. The quotation (τίς. . . αὐτόν) is from the LXX of Isa. xl. 13, adapted by the omission of the middle clause, καὶ τίς αὐτο...` | **SUBSTANTIVE_CROSS_EPISTLE_COMPARISON** | Commentary on 1 Cor 2:16 (printed pp. 50-51): explicitly compares 1 Cor 2:16 quotation of Isa 40:13 LXX with Rom 11:34 (omission vs retention of middle clause) and analyzes LXX νοῦν translating Hebrew ruach. |

---

## 6. Detailed Case-by-Case Adjudication of Substantive Targets

### B001-5: Romans 10:13 / Joel 2:32 — RELEVANT_INTERPRETIVE_CROSS_REFERENCE
- **Total Measured Matches:** 6
- **Evaluated Scholarly Finding:** Commentary on 1 Cor 1:2 (printed p. 3): explicitly connects invocation formula from Joel 2:32 to Rom 10:12-13, analyzing Pauline worship of Christ under OT divine formula.
- **Observed Exegetical Match Evidence:**
  - Offset `160303` (`Rom. x. 12,132`): *"...involves the thought of faith, the common bond of all. See Rom. x. 12,132. Here, as there, St Paul significantly brings in the worshi..."*
    - *Rationale:* Commentary on 1 Cor 1:2 (printed p. 3): explicitly connects invocation formula from Joel 2:32 to Rom 10:12-13, analyzing Pauline worship of Christ under OT divine formula.
  - Offset `160227` (`Joel ii. 32`): *"...ot all Christendom. τοῖς ἐπικαλουμένοις. This goes back  to Joel ii. 32, and involves the thought of faith, the common bond of all...."*
    - *Rationale:* Commentary on 1 Cor 1:2 (printed p. 3): explicitly traces invocation formula to Joel 2:32, cross-references Rom 10:12-13, and analyzes Pauline christological transfer of OT Yahweh worship formula.
- **Ledger Status:** Admitted as secondary interpretive cross-reference evidence row `S03F-E014` (Commentary on 1 Cor 1:2, printed p. 3).

### B001-6: Romans 11:34 / Isaiah 40:13 — SUBSTANTIVE_CROSS_EPISTLE_COMPARISON
- **Total Measured Matches:** 2
- **Evaluated Scholarly Finding:** Commentary on 1 Cor 2:16 (printed pp. 50-51): analyzes clause retention in Rom 11:34 vs omission in 1 Cor 2:16.
- **Observed Exegetical Match Evidence:**
  - Offset `287850` (`Rom. xi. 34`): *"...καὶ τίς αὐτοῦ σύνβουλος ἐγένετο; This clause is retained in Rom. xi. 34, while és συνβιβάσει αὐτόν is omitted. The aorist (ἔγνω) be..."*
    - *Rationale:* Commentary on 1 Cor 2:16 (printed pp. 50-51): analyzes clause retention in Rom 11:34 vs omission in 1 Cor 2:16.
  - Offset `287731` (`Isa. xl. 13`): *"...nal norm. The quotation (τίς. . . αὐτόν) is from the LXX of Isa. xl. 13, adapted by the omission of the middle clause, καὶ τίς αὐτο..."*
    - *Rationale:* Commentary on 1 Cor 2:16 (printed pp. 50-51): explicitly compares 1 Cor 2:16 quotation of Isa 40:13 LXX with Rom 11:34 (omission vs retention of middle clause) and analyzes LXX νοῦν translating Hebrew ruach.
- **Ledger Status:** Admitted as substantive comparative evidence row `S03F-E013` (Commentary on 1 Cor 2:16, printed pp. 50–51; authentic edition uses unassimilated Hellenistic *nu* orthography `σύνβουλος`, `συνβιβάσει`).

---

## 7. Scholarly Verification Verdict

1. **B001-5** (Romans 10:13 / Joel 2:32) is dynamically adjudicated as **RELEVANT_INTERPRETIVE_CROSS_REFERENCE** based on observed evidence (Commentary on 1 Cor 1:2 (printed p. 3): explicitly connects invocation formula from Joel 2:32 to Rom 10:12-13, analyzing Pauline worship of Christ under OT divine formula.).
2. **B001-6** (Romans 11:34 / Isaiah 40:13) is dynamically adjudicated as **SUBSTANTIVE_CROSS_EPISTLE_COMPARISON** based on observed evidence (Commentary on 1 Cor 2:16 (printed pp. 50-51): analyzes clause retention in Rom 11:34 vs omission in 1 Cor 2:16.).
3. For targets (**B001-1**, **B001-3**, **B001-4**, **B001-7**, **B001-12**), **0 matches** were detected across all 504 pages under authenticated search patterns.
4. For targets (**B001-2** (2 hit(s))), only passing citation(s) were observed without substantive quotation discussion, confirming they are **NOT_DISCUSSED** in this volume.
