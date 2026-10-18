# S01F — NotebookLM Self-Audit

**Source:** James W. Aageson, *Paul's Use of Scripture: A Comparative Study of Biblical Interpretation in Early Palestinian Judaism and the New Testament With Special Reference to Romans 9–11* (D.Phil. thesis, Oxford University, 1983/1984).  
**Source Class:** SECONDARY  
**Mode:** SOURCE-BOUND SELF-AUDIT

---

## Result: AUDIT IN PROGRESS (STAGED FOR RE-REVIEW)

This self-audit records the comprehensive verification of all source packet artifacts for S01F (James W. Aageson, Oxford D.Phil. thesis, 1983/1984) following the independent review findings in GitHub PR #2 (`#issuecomment-6256189064`). All 6 review findings have been resolved in full.

---

### Itemized Review Findings and Resolutions

#### Finding 1: Browser Automation Scoping & Raw Extraction Fixes
- **Root Cause Identified:** In `scripts/run_secondary_prompt.py`, citation overlay queries included `.source-panel`, which matched the persistent left sidebar displaying the thesis abstract ("Title: Paul's Use of Scripture..."). This caused duplicate abstract captures across markers in initial raw outputs.
- **Resolution:**
  1. Scoped citation snippet extraction strictly to the active Angular CDK overlay container (`.cdk-overlay-container .cdk-overlay-pane.citation-tooltip-panel` and `.cdk-overlay-pane:has(.citation-tooltip)`), completely excluding persistent source panels, sidebars, and search tools.
  2. Implemented handling for collapsed/grouped citation markers (`button.citation-marker` containing `mat-icon: more_horiz` with `aria-label="Show additional citations"`), expanding and processing grouped citations.
  3. Added fail-closed validation (`validate_citations`) that raises `RuntimeError` if extracted snippets are identical across distinct markers or match the general abstract text.

#### Finding 2: Direct Physical Page Verification (S01F-E001 through S01F-E018)
- **Methodology:** Direct verification of all 18 evidence items against the complete physical Oxford D.Phil. thesis PDF (`aageson_1984_pauls_use_of_scripture.pdf`, 325 total PDF pages, 315 numbered thesis pages, preliminary pages i–iv; text offset $N_{pdf} = N_{thesis} + 10$).
- **Verified Page Alignments & Corrections:**
  - `S01F-E001` (Rom 4:3 / Gen 15:6): Printed **p. 83** (PDF p. 93) — transposition of ἐπίστευσεν and Ἀβραάμ without altering semantic sense.
  - `S01F-E002` (Rom 4:3 / Gen 15:6): Printed **p. 131** (PDF p. 141) — narrative sequence of Genesis prioritized prior to circumcision.
  - `S01F-E003` (Rom 9:25 / Hos 2:23): Printed **p. 69 n. 19** (PDF p. 79) — LXX-B alignment on forms of ἀγαπᾶν against LXX-A ἐλεεῖν.
  - `S01F-E004` (Rom 9:25 / Hos 2:23): Printed **p. 178; cf. p. 81** (PDF pp. 188, 91) — **Corrected from p. 79 to p. 178**. Direct quote ("The substitution of καλέσω for ἐρῶ in the citation from Hosea 2:25 LXX, has resulted in a verbal connection...") is on p. 178; foundational note on p. 81.
  - `S01F-E005` (Rom 9:26 / Hos 1:10): Printed **pp. 69–70 n. 19** (PDF pp. 79–80) — LXX-A verbatim agreement prefixing ἐκεῖ and omitting καὶ αὐτοί.
  - `S01F-E006` (Rom 9:26 / Hos 1:10): Printed **p. 179** (PDF p. 189) — verbal catchword link between υἱοὶ θεοῦ ζῶντος (9:26) and υἱῶν Ἰσραήλ (9:27).
  - `S01F-E007` (Rom 10:11 / Isa 28:16): Printed **p. 69 n. 19** (PDF p. 79) — LXX-A alignment including ἐπʼ αὐτῷ against LXX-B.
  - `S01F-E008` (Rom 10:11 / Isa 28:16): Printed **p. 83; cf. p. 183** (PDF pp. 93, 193) — insertion of πᾶς motivated by catchword association with Joel 3:5.
  - `S01F-E009` (Rom 10:13 / Joel 2:32): Printed **p. 126** (PDF p. 136) — key catchwords πᾶς and ἐπικαλέσασθαι grounding universal Jew/Greek salvation.
  - `S01F-E010` (Rom 11:34 / Isa 40:13): Printed **p. 69 n. 19** (PDF p. 79) — LXX-A word order σύμβουλος αὐτοῦ against LXX-B transposition.
  - `S01F-E011` (Rom 11:34 / Isa 40:13): Printed **p. 84** (PDF p. 94) — citation of distinct clauses of Isa 40:13 in Rom 11:34 and 1 Cor 2:16 for epistolary context.
  - `S01F-E012` (Rom 15:12 / Isa 11:10): Printed **p. 91 n. 16** (PDF p. 101) — catena verbal connection centering on ἔθνη; stylistic omission of temporal phrase (pp. 74–76).
  - `S01F-E013` (1 Cor 1:19 / Isa 29:14): Printed **p. 92** (PDF p. 102) — citation as thematic and verbal catalyst for subsequent cross wisdom exposition.
  - `S01F-E014` (1 Cor 6:16 / Gen 2:24): Printed **pp. 82–83** (PDF pp. 92–93) — parenthetical introductory formula γάρ, φησίν added for syntactical integration within shared core quotation.
  - `S01F-E015` (1 Cor 6:16 / Gen 2:24): Printed **p. 114 n. 120** (PDF p. 124) — **Corrected from p. 106 n. 85 to p. 114 n. 120**. Direct quote ("In four instances, 'narrative' passages are used in contexts which pertain to ethics; [n. 120: I Cor. 6:16 (Gen. 2:24)...]") verified on p. 114.
  - `S01F-E016` (1 Cor 9:9 / Deut 25:4): Printed **p. 148** (PDF p. 158) — application of Deut 25:4 to apostolic right of material support; textual variant κημώσεις noted on p. 68 n. 15.
  - `S01F-E017` (1 Cor 10:7 / Exod 32:6): Printed **p. 154** (PDF p. 164) — use of τύπος and τυπικῶς as parenetic warning rather than formal typology.
  - `S01F-E018` (Gal 3:13 / Deut 21:23): Printed **p. 79** (PDF p. 89) — theological omission of ὑπὸ θεοῦ to safeguard divine image; raw prompt marker identified following Marker 27 under collapsed `more_horiz`.

#### Finding 3: Argument Map Tripartite Restructuring
- **Resolution:** Reorganized all 12 sections of `argument_map.md` into 3 strict, unambiguous headers:
  1. `### AAGESON EXPLICIT STATEMENT (Source-Grounded)`: Author's direct claims, citations, explicit assumptions, and author-considered alternatives (e.g. Goppelt, Ellis, memory lapse) with exact page references.
  2. `### REVIEWER STRUCTURAL PARAPHRASE`: Rigorous 4-element analytical reconstruction (QUESTION, EVIDENCE, INFERENCE, CONCLUSION).
  3. `### REVIEWER-GENERATED ALTERNATIVES & FALSIFICATION TESTS`: Distinctly labeled researcher counterfactuals and falsification criteria, strictly separated from authorial claims.

#### Finding 4: Reconciled S01F-E014 Clause Scope & Corpus Boundary
- **Resolution:**
  - Clarified that Aageson's statement ("the only difference between the two references is that the introductory formula, γάρ, φησίν, has been included for syntactical reasons as part of the reference in I Corinthians") applies strictly to the shared core quotation (`ἔσονται οἱ δύο εἰς σάρκα μίαν`).
  - Explicitly noted that Ephesians 5:31 quotes the preceding clause (`ἀντὶ τούτου καταλείψει ἄνθρωπος...`), which is absent from 1 Corinthians 6:16.
  - Classified Ephesians 5:31 as an outside-primary-corpus comparator in compliance with `PROJECT_CONSTITUTION.md` (distinguishing the undisputed primary Pauline corpus from deuteropauline comparators).

#### Finding 5: Automation Invariants & Deterministic Test Suite
- **Resolution:**
  - Implemented fail-closed invariants in `scripts/run_secondary_prompt.py`:
    - `validate_notebook_state`: Ensures connected tab matches `SDP-B001-EXTRACT` and contains exactly 1 loaded source.
    - `validate_citations`: Fails closed against empty snippets, duplicate captures, or thesis abstract text pollution.
    - Submit retry loop with `RuntimeError` on failure.
    - Generation stabilization loop with `TimeoutError` on timeout.
  - Added deterministic unit test suite in `tests/test_run_secondary_prompt.py` covering all invariant functions and integration mocks (10/10 tests passing via `pytest`).

#### Finding 6: Thesis Pagination Normalization
- **Resolution:** Reconciled pagination across `metadata.md`, `notebooklm_self_audit.md`, `citation_ledger.csv`, and `extraction.md`:
  - Front matter: Roman numerals pp. i–iv (4 pages)
  - Main text (Chapters I–VI and Conclusion): pp. 1–280 (280 pages)
  - Appendix: pp. 281–284 (4 pages)
  - Bibliography: pp. 285–315 (31 pages)
  - Total Numbered Pages: 315 pages (325 total physical PDF pages; constant PDF offset $N_{pdf} = N_{thesis} + 10$).

---

### Audit Checklist Status (Checks 1–7)
1. **Check #1 (Direct Support):** PASS. Every claim is supported by direct quotation and verified physical thesis page numbers.
2. **Check #2 (Direct Quotation Precision):** PASS. Greek font strings normalized to Unicode Greek matching the printed thesis text verbatim.
3. **Check #3 (Printed Page-Numbering Precision):** PASS. All 18 evidence items cite verified printed thesis pages (1–315 range).
4. **Check #4 (Preservation of Authorial Hedging):** PASS. Probabilistic and conditional phrasing preserved ("probably came about", "cannot be certain").
5. **Check #5 (Other Scholars Disambiguated):** PASS. Goppelt, Ellis, and Barrett clearly distinguished from Aageson's evaluations.
6. **Check #6 (Inference vs Direct Statement Separation):** PASS. All 12 argument map sections cleanly divided into explicit source claims, reviewer structural paraphrases, and researcher falsification tests.
7. **Check #7 (Model Knowledge Contamination):** PASS. Zero outside knowledge introduced; all claims source-bound to S01F.
