# S06F — NotebookLM Source-Bounded Self-Audit

Audit of the extractions against Mireia Ryšková’s published article, *The Reception of the Book of Isaiah in Paul’s Letter to the Romans*, *AUC Theologica*, Vol. 9, No. 2 (2019), pp. 95–116.

---

## Itemized Audit Findings and Applied Corrections

### 1. Qualification on the Origin of the Composite Stone Citation in Romans 9:33
- **Source Location:** Printed p. 105 [PDF p. 11]; Section 5 (Rom 9:33).
- **Initial Extraction Defect:** Stated as settled fact that Paul personally merged Isaiah 28:16 and Isaiah 8:14 into a composite quotation.
- **Source Observation:** On printed page 105, Ryšková explicitly presents the origin of the composite text as an unresolved scholarly debate:
  > "Some scholars (Koch and Dodd, for example) believe that the combination is a pre-Pauline tradition (Koch oral; Dodd written) and that Paul is therefore quoting from Isaiah on the basis of an existing text... Shum is certain that Paul is quoting directly from a scroll of Isaiah he might have had access to in Corinth." (p. 105, fn. 35–36).
- **Applied Correction:** Reframed evidence claim `S06F-E004` to open neutrally: *"Romans 9:33 contains a composite quotation conflating Isaiah 28:16 and Isaiah 8:14; its immediate origin is contested in scholarship between a pre-Pauline oral/written composite tradition (Koch, Dodd) and Paul's direct compilation from an Isaiah scroll (Shum)..."*, with full qualifications carried into `extraction.md`, `argument_map.md`, and `isaiah_in_romans_synthesis.md`.

### 2. Preservation of Disjunctive Possibilities and Qualified Job Echo in Romans 11:34–35
- **Source Location:** Printed p. 112 [PDF p. 18]; Section 12 (Rom 11:34–35).
- **Initial Extraction Defect:** Converted Ryšková's disjunctive explanation into a single definitive claim and treated Job 41:11 as a definite quotation.
- **Source Observation:** On printed page 112, Ryšková uses explicitly disjunctive language regarding Paul's technique: Paul is *"either quoting by heart from his great knowledge of Isaiah or using Isaiah’s language automatically, naturally"*, and describes the link in Rom 11:35 to Job 41:11 (LXX 41:3) as a *"possible echo"*, not a settled quotation.
- **Applied Correction:** Refined claim `S06F-E006` to state that Paul quotes almost word-for-word from LXX Isaiah 40:13 *"accompanied by a possible echo of Job 41:11 (LXX 41:3) in Rom 11:35—either quoting from memory or drawing automatically on biblical idiom to express God's unsearchable sovereignty"*.

### 3. Explicit Attribution to Shum for Christological Co-Sovereignty Formulation
- **Source Location:** Printed p. 106 [PDF p. 12]; Section 6 (Rom 10:11).
- **Initial Extraction Defect:** Attributed the formulation that Christ is "co-sovereign and co-unique with God the Father" directly to Ryšková without noting her footnote attribution.
- **Source Observation:** On printed page 106, Ryšková makes this statement while citing Shiu-Lun Shum (*Paul's Use of Isaiah in Romans*, p. 223) in footnote 40.
- **Applied Correction:** Explicitly noted in claim `S06F-E003` (and its supporting qualifications and notes) that the characterization of Christ as "co-sovereign and co-unique with God the Father" relies directly on Shiu-Lun Shum's monograph (2002, p. 223, cited in fn. 40).

---

## Systematic Audit Across the Seven Core Checks

1. **Direct Source Support (Check #1):** Verified. All extracted claims for Rom 9:33, Rom 10:11, Rom 10:13, Rom 11:34, and Rom 15:12 correspond directly to Ryšková's text.
2. **Quotation Accuracy (Check #2):** Verified. All short exact quotations in `citation_ledger.csv` match the printed text of *AUC Theologica* 9/2 (2019) across their full lengths without ellipses or omissions.
3. **Observed Printed Page Numbers (Check #3):** Verified. All locators are authenticated to printed pages 95–116 and strictly conform to the monotonic formula $\text{printed} = \text{PDF} + 94$.
4. **Possibility vs. Certainty (Check #4):** Addressed. Qualifications on Rom 9:33 composite origin and Rom 11:34 quotation technique are preserved.
5. **Scholar Attribution (Check #5):** Addressed. Explicit attributions for Koch, Dodd, Shum, and Wilk are maintained throughout.
6. **Qualifications and Textual Variants (Check #6):** Addressed. Textual variations (LXX vs. MT, addition of πᾶς, selective omissions) are recorded accurately.
7. **No General Model Knowledge (Check #7):** Verified. No external model assertions or extraneous claims have been introduced into the evidence packet.

---

## 3. Independent Review Acceptance & Cumulative Promotion (Round 4)
- **Review Verdict:** `SOURCE_PACKET: ACCEPT`, `MERGE: NO` ([#issuecomment-6717257302](https://github.com/aguacatero/septuagint-diaspora-book/pull/2#issuecomment-6717257302)) at live PR HEAD `645ebf78eb919e2356d9cc6d093b3ca59261d002`.
- **Cumulative Promotion:** S06F (`ryskova_2019_isaiah_romans.pdf`) promoted into cumulative synthesis notebook `SDP-01 Paul` via `scripts/promote_to_sdp01.py` on 2026-11-07.
- **Ingestion & Settle:** File uploaded and settled in 10s; cumulative sources in `SDP-01 Paul` reached 9 (`aageson_1984_pauls_use_of_scripture.pdf`, `lightfoot_1914_galatians.pdf`, `robertson_plummer_1911_1corinthians_icc.pdf`, `ryskova_2019_isaiah_romans.pdf`, `sanday_headlam_1895_romans_icc.pdf`, `sblgnt.pdf`, `swete_lxx_vol1_p02f_target.pdf`, `swete_lxx_vol3_p03f_target.pdf`, `wilk_1998_jesaja_paulus.pdf`).
- **Source-Attributed Retrieval Verification:** Probe query ("In Mireia Ryšková's The Reception of the Book of Isaiah in Paul's Letter to the Romans, what is her analysis regarding Paul's insertion of pas in Romans 10:11 and the application of Isaiah 28:16 to Christ?") succeeded with response length 555 chars and 1 verified citation marker.
