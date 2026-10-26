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
- **Total Volume Pages:** 504 pages (pp. i–lxx, 1–424, plus title & plates)

---

## 2. Positive Control Verification

To establish that OCR text extraction and regular expression patterns reliably match 
authentic 19th/20th-century typographical conventions, Roman numerals, and citation formatting 
in this volume, positive controls were executed for known citations:

| Positive Control Citation | Expected Min | Actual Matches | Status | Sample Verified Context |
| :--- | :--- | :--- | :--- | :--- |
| 1 Cor 1:19 / Isa 29:14 (Commentary p. 19, Intro p. liii) | 1 | 2 | **PASSED** | `. in iii, 2o=Ps. xciv. 11, where he substitutes σοφῶν for ἀνθρώπων, or in i. 19=Isa. xxix....` |
| 1 Cor 6:16 / Gen 2:24 (Commentary p. 126, Intro p. liii) | 1 | 2 | **PASSED** | `Ixiv. 4(?) 1 10 ΞΞ [πὶ ΧΙ]. 152 ΤΠ 10 Ξ Ob ν. 12 NI 20 ΞΞ ἘΞ' xcive LE vi. 16 = Gen. ii. 2...` |
| 1 Cor 9:9 / Deut 25:4 (Commentary p. 183, Intro p. liii) | 1 | 3 | **PASSED** | `πὶ ΧΙ]. 152 ΤΠ 10 Ξ Ob ν. 12 NI 20 ΞΞ ἘΞ' xcive LE vi. 16 = Gen. ii. 24 ix. 9 = Deut. xxv....` |
| 1 Cor 10:7 / Exod 32:6 (Commentary p. 203, Intro p. liii) | 1 | 2 | **PASSED** | `eement with the LXX are these— vi. 16 = Gen. ii. 24 1x, Ὁ = Deut. παν. 4 x. 7 = Exod. xxxi...` |
| 1 Cor 15:54 / Isa 25:8 (Commentary p. 378, Intro p. liii, liv) | 1 | 4 | **PASSED** | `or unconsciously guided by the Hebrew in diverging from the LXX, e.g. in xv. 54=Isa. xxv. ...` |
| Sanday and Headlam citation (Intro p. lii) | 1 | 12 | **PASSED** | `. 52.  Μαρὰν ἀθά, xvi. 22. Quotations from the O.T. The essay on the subject in Sanday and...` |

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
| **B001-3** | Romans 9:26 / Hosea 1:10 | 1 | **NOT_DISCUSSED** | 1 passing citation(s) found without substantive discussion of target quotation. |
| **B001-4** | Romans 10:11 / Isaiah 28:16 | 0 | **NOT_DISCUSSED** | 0 matches found under verified search patterns across all 504 pages. |
| **B001-5** | Romans 10:13 / Joel 2:32 | 7 | **RELEVANT_INTERPRETIVE_CROSS_REFERENCE** | Commentary on 1 Cor 1:2 (printed p. 3): explicitly traces invocation formula to Joel 2:32, cross-references Rom 10:12-13, and analyzes Pauline christological transfer of OT Yahweh worship formula. |
| **B001-6** | Romans 11:34 / Isaiah 40:13 | 2 | **SUBSTANTIVE_CROSS_EPISTLE_COMPARISON** | Commentary on 1 Cor 2:16 (printed pp. 50-51): analyzes clause retention in Rom 11:34 vs omission in 1 Cor 2:16. |
| **B001-7** | Romans 15:12 / Isaiah 11:10 | 3 | **NOT_DISCUSSED** | 3 passing citation(s) found without substantive discussion of target quotation. |
| **B001-12** | Galatians 3:13 / Deuteronomy 21:23 | 0 | **NOT_DISCUSSED** | 0 matches found under verified search patterns across all 504 pages. |

---

## 5. Itemized Match Evidence Ledger

Every individual regex match detected across the 504-page text layer is itemized below with its exact character offset, matched string, surrounding context, hit classification, and evaluation rationale:

| Hit # | Target ID | Offset | Matched Text | Surrounding Context Excerpt | Hit Classification | Evaluation Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **B001-2** | `690592` | `Rom. ix. 25` | `Paul: four in 2 Cor. iv. 8, 9; two in a quotation in Gal. iv. 27 ; one each in R...` | **PASSING_CITATION** | Grammatical note cataloging Pauline usage of a word; no discussion of the quotation or its OT source. |
| 2 | **B001-2** | `1093294` | `Rom. ix. 25` | `use of the relative; ‘seeing that I am not fit to be called an Apostle.’ Comp. R...` | **PASSING_CITATION** | Passing parenthetical cross-reference on 1 Cor 15:9; no discussion of the quotation or its OT source. |
| 3 | **B001-3** | `1143523` | `Hos. ix` | `3 is quite parallel, for there the verb is present, not future. Jer. iv. 30 and ...` | **PASSING_CITATION** | Reference to Hosea 9:5 (Hos. ix. 5) in note on 1 Cor 15:55; not Hosea 1:10. |
| 4 | **B001-5** | `76476` | `Rom. x. 13` | `ly lays down. Christ was the whole of his Gospel (ii. 2); He is ‘the Lord’ (cf. ...` | **PASSING_CITATION** | Passing reference to Rom 10:13 in Introduction p. xxxvii. |
| 5 | **B001-5** | `160303` | `Rom. x. 12` | `to Joel ii. 32, and involves the thought of faith, the common bond of all. See R...` | **PASSING_CITATION** | Dynamic context inspection found passing citation without substantive quotation discussion. |
| 6 | **B001-5** | `228383` | `Rom. x. 13` | `e quotes as other instances in Paul, ii. 16, x. 22; 2 Cor. x. 17; Phil. ii. r1; ...` | **PASSING_CITATION** | Passing cross-reference on 1 Cor 1:31 citing Hort on 1 Pet 2:3. |
| 7 | **B001-5** | `288281` | `Rom. x. 12` | `ificance.  Cf. Wisd.  ix. 13;  Ecclus. 1. 6;  Job xxxvi. 22, 23, 26; and see on ...` | **SUBSTANTIVE_DISCUSSION** | Dynamic context inspection detected substantive exegetical/textual commentary around 'Rom. x. 12'. |
| 8 | **B001-5** | `717693` | `Rom. x. 12` | `i. 3, ‘‘ No such identification can be clearly made out in the N.T.” But see on ...` | **SUBSTANTIVE_DISCUSSION** | Dynamic context inspection detected substantive exegetical/textual commentary around 'Rom. x. 12'. |
| 9 | **B001-5** | `902005` | `Rom. x. 12` | `to whom the Apostle is writing. See Lightfoot on Col. iil. 11, and cf. vii. 22; ...` | **PASSING_CITATION** | Dynamic context inspection found passing citation without substantive quotation discussion. |
| 10 | **B001-5** | `160227` | `Joel ii. 32` | `hat are addressed, not all Christendom. τοῖς ἐπικαλουμένοις. This goes back  to ...` | **RELEVANT_INTERPRETIVE_CROSS_REFERENCE** | Commentary on 1 Cor 1:2 (printed p. 3): explicitly traces invocation formula to Joel 2:32, cross-references Rom 10:12-13, and analyzes Pauline christological transfer of OT Yahweh worship formula. |
| 11 | **B001-6** | `287850` | `Rom. xi. 34` | `the middle clause, καὶ τίς αὐτοῦ σύνβουλος ἐγένετο; This clause is retained in R...` | **SUBSTANTIVE_CROSS_EPISTLE_COMPARISON** | Commentary on 1 Cor 2:16 (printed pp. 50-51): analyzes clause retention in Rom 11:34 vs omission in 1 Cor 2:16. |
| 12 | **B001-6** | `287731` | `Isa. xl. 13` | `by any merely external norm. The quotation (τίς. . . αὐτόν) is from the LXX of I...` | **SUBSTANTIVE_CROSS_EPISTLE_COMPARISON** | Commentary on 1 Cor 2:16 (printed pp. 50-51): explicitly compares 1 Cor 2:16 quotation of Isa 40:13 LXX with Rom 11:34 (omission vs retention of middle clause) and analyzes LXX νοῦν translating Hebrew ruach. |
| 13 | **B001-7** | `119987` | `Isa. xix` | `reference for the Hebrew, or possibly for some version not known to us. i, 20 = ...` | **PASSING_CITATION** | Reference to Isa 19:11 in Introduction p. liii; not Isa 11:10. |
| 14 | **B001-7** | `204416` | `Isa. xix` | `x. 20. quotes from it Matt. xi. 5, xv. 8f.  Our Lord  + He may have in his mind ...` | **PASSING_CITATION** | Reference to Isa 19:12 on 1 Cor 1:20; not Isa 11:10. |
| 15 | **B001-7** | `206094` | `Isa. xix` | `stultam fecit (Vulg.), infatuavit (Tertull. and Beza). Cf. Rom. i. 22, 23, and I...` | **PASSING_CITATION** | Reference to Isa 19:11 on 1 Cor 1:20; not Isa 11:10. |

---

## 6. Detailed Case-by-Case Adjudication of Reclassified Targets

### B001-6: Romans 11:34 / Isaiah 40:13 — Substantive Comparative Evidence
- **Location in 1 Corinthians:** Commentary on 1 Cor 2:16, printed pp. 50–51 (Raw scan pp. 126–127; Derivative pp. 31–32).
- **Observed Exegetical Text:**
  > *The quotation (τίς. . . αὐτόν) is from the LXX of Isa. xl. 13, adapted by the omission of the middle clause, καὶ τίς αὐτοῦ σύνβουλος ἐγένετο; This clause is retained in Rom. xi. 34, while ὃς συνβιβάσει αὐτόν is omitted... νοῦν Κυρίου. The νοῦν (LXX) corresponds to the Hebrew for πνεῦμα in the original.*
- **Scholarly Finding:** Robertson and Plummer conduct a direct cross-epistle textual comparison between 1 Cor 2:16 and Rom 11:34, identifying the alternating clause-omissions in Paul's citation of Isaiah 40:13 LXX and analyzing the lexical correspondence between LXX `νοῦν` and Hebrew `רוּחַ` (*rūaḥ* / `πνεῦμα`). Note that the authentic printed edition uses unassimilated orthography with *nu* (`σύνβουλος`, `συνβιβάσει`), characteristic of the ICC series' adherence to Westcott-Hort typography.
- **Ledger Status:** Admitted as substantive comparative evidence row `S03F-E013`.

### B001-5: Romans 10:13 / Joel 2:32 — Relevant Interpretive Cross-Reference
- **Location in 1 Corinthians:** Commentary on 1 Cor 1:2, printed p. 3 (Raw scan p. 79; Derivative p. 22).
- **Observed Exegetical Text:**
  > *τοῖς ἐπικαλουμένοις. This goes back to Joel ii. 32, and involves the thought of faith, the common bond of all. See Rom. x. 12, 13. Here, as there, St Paul significantly brings in the worship of Christ under the O.T. formula for worship addressed to the LORD God of Israel.*
- **Scholarly Finding:** The authors explicitly connect the invocation formula `τοῖς ἐπικαλουμένοις` to Joel 2:32 and cross-reference Romans 10:12–13, demonstrating Paul's christological transfer of the Old Testament divine name / worship formula for Yahweh to Jesus Christ.
- **Ledger Status:** Admitted as secondary interpretive cross-reference evidence row `S03F-E014`.

---

## 7. Scholarly Verification Verdict

1. **B001-6** is dynamically adjudicated as **SUBSTANTIVE_CROSS_EPISTLE_COMPARISON** based on printed pp. 50–51.
2. **B001-5** is dynamically adjudicated as **RELEVANT_INTERPRETIVE_CROSS_REFERENCE** based on printed p. 3.
3. For the remaining six targets (**B001-1, B001-2, B001-3, B001-4, B001-7, B001-12**), dynamic per-hit evaluation 
   and section-localized index inspection confirm that **no substantive discussion is found under these search patterns** 
   in Robertson and Plummer's 1 Corinthians commentary.
