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

## 3. Bounded Index Structure Inspection

Inspection of the volume's back matter confirms bounded and ordered index structure:
- **Index I: General** (Authors and Subjects, pp. 403–414): Verified present.
- **Index II: Greek Words** (pp. 415–422): Verified present.
- **Index III: Latin and English Words** (pp. 423–424): Verified present.
- **Independent End Delimiter:** Verified (`Printed by Morrison & Gibb Limited, Edinburgh`).
- **Ordered Sequence Check:** Verified (`Index I < Index II < Index III < End Delimiter`).
- **Positive Control Entries:** Verified (`Allegorical interpretation`, `Assimilation`, `Aquila`, `ἀδάπανος`, `ἀλοάω`, `Caritas`, `underling`).
- **Scripture Passage Index:** Verified absent (confirming Dr. Plummer's preface note that the index is a general author/subject and lexical index).

---

## 4. Target Query Verification Across All 504 Pages (Dynamic Adjudication)

Robertson and Plummer's commentary is dedicated to **1 Corinthians**. The B001 research corpus 
includes twelve specific Pauline quotation comparisons. Four belong directly to 1 Corinthians 
(B001-8, B001-9, B001-10, B001-11). The remaining eight loci (B001-1 through B001-7, B001-12) 
were scanned across the entire 504-page volume to evaluate presence, cross-epistle comparison, or genuine absence:

| B001 ID | Comparison Target | Measured Matches | Scholarly Classification | Evaluated Context & Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **B001-1** | Romans 4:3 / Genesis 15:6 | 0 | **NOT_DISCUSSED** | No substantive discussion or cross-reference found in volume. |
| **B001-2** | Romans 9:25 / Hosea 2:23 | 2 | **NOT_DISCUSSED** | Two passing cross-reference occurrences (notes on 2 Cor 4:8 and 1 Cor 15:9); no substantive discussion of target quotation. |
| **B001-3** | Romans 9:26 / Hosea 1:10 | 1 | **NOT_DISCUSSED** | One passing citation on p. 204 in note on 1 Cor 10:7; no substantive discussion. |
| **B001-4** | Romans 10:11 / Isaiah 28:16 | 0 | **NOT_DISCUSSED** | No substantive discussion or cross-reference found in volume. |
| **B001-5** | Romans 10:13 / Joel 2:32 | 7 | **RELEVANT_INTERPRETIVE_CROSS_REFERENCE** | Substantive secondary interpretive discussion on 1 Cor 1:2 (printed p. 3): traces τοῖς ἐπικαλουμένοις to Joel 2:32 and Rom 10:12-13, analyzing Pauline application of OT Yahweh worship formula to Christ. |
| **B001-6** | Romans 11:34 / Isaiah 40:13 | 2 | **SUBSTANTIVE_CROSS_EPISTLE_COMPARISON** | Substantive comparative textual discussion on 1 Cor 2:16 (printed pp. 50-51): compares 1 Cor 2:16 quotation of Isa 40:13 with Rom 11:34 (omission vs retention of middle clause καὶ τίς αὐτοῦ σύνβουλος ἐγένετο) and analyzes LXX νοῦν translating Hebrew ruach. |
| **B001-7** | Romans 15:12 / Isaiah 11:10 | 3 | **NOT_DISCUSSED** | Passing citations on pp. 354, 358 (notes on 1 Cor 15:25, 27); no substantive discussion of target quotation. |
| **B001-12** | Galatians 3:13 / Deuteronomy 21:23 | 0 | **NOT_DISCUSSED** | No substantive discussion or cross-reference found in volume. |

---

## 5. Detailed Case-by-Case Adjudication of Reclassified Targets

### B001-6: Romans 11:34 / Isaiah 40:13 — Substantive Comparative Evidence
- **Location in 1 Corinthians:** Commentary on 1 Cor 2:16, printed pp. 50–51 (Raw scan pp. 126–127; Derivative pp. 32–33).
- **Observed Exegetical Text:**
  > *τίς γὰρ ἔγνω νοῦν Κυρίου; ὃς συνβιβάσει αὐτόν; From Isa. xl. 13 (LXX), but shortened by the omission of the middle clause, καὶ τίς αὐτοῦ σύνβουλος ἐγένετο; This clause is retained in Rom. xi. 34, while ὃς συνβιβάσει αὐτόν is omitted... νοῦν Κυρίου. The νοῦν (LXX) corresponds to the Hebrew for πνεῦμα in the original.*
- **Scholarly Finding:** Robertson and Plummer conduct a direct cross-epistle textual comparison between 1 Cor 2:16 and Rom 11:34, identifying the alternating clause-omissions in Paul's citation of Isaiah 40:13 LXX and analyzing the lexical correspondence between LXX `νοῦν` and Hebrew `רוּחַ` (*rūaḥ* / `πνεῦμα`).
- **Ledger Status:** Admitted as substantive comparative evidence row `S03F-E013`.

### B001-5: Romans 10:13 / Joel 2:32 — Relevant Interpretive Cross-Reference
- **Location in 1 Corinthians:** Commentary on 1 Cor 1:2, printed p. 3 (Raw scan p. 79; Derivative p. 22).
- **Observed Exegetical Text:**
  > *τοῖς ἐπικαλουμένοις. This goes back to Joel ii. 32, and involves the thought of faith, the common bond of all. See Rom. x. 12, 13. Here, as there, St Paul significantly brings in the worship of Christ under the O.T. formula for worship addressed to the LORD God of Israel.*
- **Scholarly Finding:** The authors explicitly connect the invocation formula `τοῖς ἐπικαλουμένοις` to Joel 2:32 and cross-reference Romans 10:12–13, demonstrating Paul's christological transfer of the Old Testament divine name / worship formula for Yahweh to Jesus Christ.
- **Ledger Status:** Admitted as secondary interpretive cross-reference evidence row `S03F-E014`.

---

## 6. Scholarly Verification Verdict

1. **B001-6** is reclassified as **substantive comparative textual evidence** based on printed pp. 50–51.
2. **B001-5** is reclassified as **relevant secondary interpretive evidence** based on printed p. 3.
3. For the remaining six targets (**B001-1, B001-2, B001-3, B001-4, B001-7, B001-12**), documented text searches 
   and bounded index inspection confirm that **no substantive discussion is found under these search patterns** 
   in Robertson and Plummer's 1 Corinthians commentary.
