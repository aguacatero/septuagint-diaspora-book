# S01F — NotebookLM Self-Audit

**Source:** James W. Aageson, *Paul's Use of Scripture: A Comparative Study of Biblical Interpretation in Early Palestinian Judaism and the New Testament With Special Reference to Romans 9–11* (D.Phil. thesis, Oxford University, 1983/1984).  
**Source Class:** SECONDARY  
**Mode:** SOURCE-BOUND SELF-AUDIT

---

## Result: AUDIT IN PROGRESS (STAGED FOR RE-REVIEW)

This self-audit records the comprehensive verification of all source packet artifacts for S01F (James W. Aageson, Oxford D.Phil. thesis, 1983/1984) across Review Round 1 (`#issuecomment-6256189064`) and Review Round 2 (`#issuecomment-6257901373`). All itemized findings have been addressed in code, tests, and canonical ledgers.

---

### Review Round 2 Resolutions (GitHub PR #2 `#issuecomment-6257901373`)

#### 1. S01F-E014 Author Claim Scope Clarification (Finding 2 — MED)
- **Review Finding:** `citation_ledger.csv` `author_claim` previously stated an unqualified "sole difference in Gen 2:24 between 1 Cor 6:16 and Eph 5:31," creating an internal contradiction with the row's `qualification` (which properly restricted the claim to the shared core clause).
- **Resolution:**
  - Updated `author_claim` in `citation_ledger.csv` to state the clause-scope limitation directly:
    *"Within the shared core quotation (ἔσονται οἱ δύο εἰς σάρκα μίαν), Paul's only difference in Gen 2:24 between 1 Cor 6:16 and Eph 5:31 is the introductory formula γάρ, φησίν added for syntax; Eph 5:31 serves as an outside-primary-corpus comparator."*
  - Aligned `Author's Claim` in `extraction.md` word-for-word.
  - Distinguishes Aageson's authorial claim from the broader manuscript reality that Eph 5:31 quotes the preceding clause omitted in 1 Cor 6:16, while preserving the deuteropauline boundary per `PROJECT_CONSTITUTION.md`.

#### 2. Exact Expected Source Identity Invariant (Finding 3 — MED)
- **Review Finding:** `validate_notebook_state` previously only checked that notebook title contained `SDP-B001-EXTRACT` and `len(sources) == 1`, but did not check *which* source was loaded, allowing arbitrary single PDFs (e.g. `thesis.pdf` or `unrelated.pdf`) to pass.
- **Resolution:**
  - Upgraded `validate_notebook_state` in `scripts/run_secondary_prompt.py` and `scripts/extract_all_messages.py` to require exact match with `expected_source` (default `aageson_1984_pauls_use_of_scripture.pdf`).
  - Added fail-closed checks rejecting mismatches, wrong single sources, multiple sources, or empty source lists.
  - Added regression unit tests in `tests/test_run_secondary_prompt.py`:
    - `test_validate_notebook_state_wrong_single_source_rejection` (rejects `thesis.pdf`, `unrelated_document.pdf`, `aageson_1984.pdf`).
    - `test_validate_notebook_state_configurable_expected_source` (verifies per-run configurable source identity).
    - `test_verify_tab_invariants_failure_on_wrong_source` (evaluates CDP mock rejecting wrong loaded source).

#### 3. Deterministic Machine-Readable Citation Pointers (Finding 4 — LOW)
- **Review Finding:** S01F-E018 cited descriptive text ("Prompt 2 / Marker collapsed under more_horiz after Marker 27") rather than the exact index in committed `prompt_2_raw.json`.
- **Resolution:**
  - Verified exact passage-bearing capture for S01F-E018 at `citations[index=116], label=28` in `prompt_2_raw.json` (containing Deuteronomy 21:23 omission discussion).
  - Adopted a uniform, deterministic, machine-readable locator convention across all 18 rows in `citation_ledger.csv` and `extraction.md`: `Prompt 2 / citations[index=X], label=Y`.

#### 4. Hover-Tooltip Association & Stale-Tooltip Invariants (Finding 5 — LOW)
- **Review Finding:** Tooltip polling did not verify whether a tooltip was newly spawned or updated versus a retained tooltip from a previous marker.
- **Resolution:**
  - Added `verify_tooltip_transition` invariant tracking consecutive duplicate captures across marker iterations.
  - While legitimate repeated excerpts representing shared source locations (e.g., identical footnote captures across adjacent citations) are explicitly permitted, runs exceeding `max_consecutive=15` are rejected with `RuntimeError` as stuck/stale overlays.
  - Added unit test fixtures in `tests/test_run_secondary_prompt.py` (`test_verify_tooltip_transition_success`, `test_verify_tooltip_transition_stale_tooltip_rejection`, `test_verify_tooltip_transition_empty_snippet_rejection`).
  - Test suite now has 16 deterministic tests passing (16/16 via `pytest`).

---

### Review Round 1 Itemized Summary (GitHub PR #2 `#issuecomment-6256189064`)

- **Finding 1 (Tooltip Scoping):** Citation tooltips scoped strictly to Angular CDK overlay container (`.cdk-overlay-container .cdk-overlay-pane.citation-tooltip-panel`), eliminating sidebar abstract capture. Authentic snippets re-extracted across Prompts 2, 3, and 4.
- **Finding 2 (Page Provenance):** Directly verified all 18 evidence items against physical Oxford D.Phil. thesis PDF (`aageson_1984_pauls_use_of_scripture.pdf`). S01F-E004 corrected to p. 178 (cf. p. 81); S01F-E015 corrected to p. 114 n. 120.
- **Finding 3 (Argument Map Restructuring):** Reorganized all 12 sections of `argument_map.md` into 3 strict headers separating author statements, structural paraphrases, and researcher falsification tests.
- **Finding 4 (Ephesians Scope):** Addressed in Round 1 and completed in Round 2 CSV `author_claim`.
- **Finding 5 (Automation Invariants):** Connection, submission, generation stabilization, and extraction invariants implemented.
- **Finding 6 (Pagination Normalization):** Normalized pagination to 315 numbered thesis pages (pp. 1–280 text, 281–284 appendix, 285–315 bibliography, plus front matter i–iv; 325 total PDF pages).

---

### Audit Checklist Status (Checks 1–7)
1. **Check #1 (Direct Support):** PASS. Every claim is supported by direct quotation and verified physical thesis page numbers.
2. **Check #2 (Direct Quotation Precision):** PASS. Greek font strings normalized to Unicode Greek matching the printed thesis text verbatim.
3. **Check #3 (Printed Page-Numbering Precision):** PASS. All 18 evidence items cite verified printed thesis pages (1–315 range).
4. **Check #4 (Preservation of Authorial Hedging):** PASS. Probabilistic and conditional phrasing preserved ("probably came about", "cannot be certain").
5. **Check #5 (Other Scholars Disambiguated):** PASS. Goppelt, Ellis, and Barrett clearly distinguished from Aageson's evaluations.
6. **Check #6 (Inference vs Direct Statement Separation):** PASS. All 12 argument map sections cleanly divided into explicit source claims, reviewer structural paraphrases, and researcher falsification tests.
7. **Check #7 (Model Knowledge Contamination):** PASS. Zero outside knowledge introduced; all claims source-bound to S01F.
