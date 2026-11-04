# B001 ChatGPT Independent Review Request

Antigravity rewrites this file for every source before requesting review.

## Current source

- Source ID: `S05` (S04F ACCEPTED and promoted to SDP-01 Paul)
- Review Round: `Round 7` (Remediation of Round 6 findings S05-R6-F1, S05-R6-F2, S05-R5-F3/S05-R6-F3, S05-R5-M1)
- Exact citation: Florian Wilk, *Die Bedeutung des Jesajabuches für Paulus* (Forschungen zur Religion und Literatur des Alten und Neuen Testaments 179; Göttingen: Vandenhoeck & Ruprecht, 1998).
- Digital scan provenance: Munich Digitization Center (MDZ) / Bayerische Staatsbibliothek (BSB) Digi20 collection (URN: `urn:nbn:de:bvb:12-bsb00044375-3`; MDZ ID: `bsb00044375`; SHA-256: `700323565f6687163dc92f410779b054b763ee10bf3f745f5c2370b5455aa1b3`).
- Branch: `research/B001-notebooklm-serial`
- Draft PR: `2`
- Review readiness: `READY`
- Review target: `LIVE_PR_HEAD`
- Previous source disposition: `S04F ACCEPTED` in Round 5 independent review ([#issuecomment-6561683809](https://github.com/aguacatero/septuagint-diaspora-book/pull/2#issuecomment-6561683809)) at commit `f3c5153ff2b2bbe901bda82dfa2050f9726b50bd`, and promoted to cumulative notebook `SDP-01 Paul` with source-grounded retrieval verification.
- Round 6 Review disposition: `REVISE` ([#issuecomment-6591853184](https://github.com/aguacatero/septuagint-diaspora-book/pull/2#issuecomment-6591853184) at commit `cd377951ffb571db16ecfb5abb4cf3e5fb2d49db`; findings S05-R6-F1, S05-R6-F2, S05-R6-F3, and S05-R5-M1 remediated in full for Round 7).

## Source evidence packet under review

`research/inbox/B001-pauline-txt-pilot/sources/S05/`
- `metadata.md`
- `relevance_scan.md` (bounds Part V to pp. 381–408; literature list pp. 409–442; Stellenregister pp. 443–461)
- `extraction.md` (includes S05-E012 for Gal 3:13 / Deut 21:23; authentic p. 307 Anm. 23 quotation 'steht zu vermuten'; authentic p. 397 quotation 'wunderbaren Charakter'; pure Greek 'καταισχυνθῇ' and 'ἀθετεῖν')
- `citation_ledger.csv` (12 verified evidence rows: S05-E001 through S05-E012; pure Greek words; authentic German pre-reform 'läßt'; exact text-layer page-bounded verified quotes; dual locators `[PDF p. X; printed p. Y]` where $X = Y + 12$; E006 at printed p. 307 / PDF p. 319 Anm. 23; E007 at printed p. 397 / PDF p. 409)
- `argument_map.md` (includes section 8 for B001-12; authentic quotation 'steht zu vermuten' at p. 307 Anm. 23; p. 397 for E007)
- `counterevidence.md` (authentic quotation 'steht zu vermuten' at p. 307 Anm. 23)
- `bibliography_leads.md`
- `notebooklm_self_audit.md` (authentic quotation 'steht zu vermuten' at p. 307 Anm. 23; p. 397 for E007)
- `full_volume_search_log.md` (regenerated via dynamic adjudication with form-specific Greek OCR signatures, single-digit and bounded numeral verification, bound local contextual hit records with page offsets and matched citations, reviewed argument evaluations, primary source locator checks, and bounded negative-search rationale)
- `provenance_manifest.json`

Plus source-specific governing verification scripts and test fixtures:
- `scripts/verify_s05_negative_search.py` (fail-closed start and end delimiter verification across 13 required sections with zero spillover; form-specific Greek OCR mappings without `\w+` fallbacks; single-digit and multi-digit numeral verification with strict token boundaries `(?<![\w\d])...(?![\w\d])` and numeric-adjacency-sensitive separators; incidental bibliographic context exclusion; bound local contextual hits with page offsets and reviewed argument judgments; primary source locator parsing ignoring secondary `vgl.` references)
- `tests/fixtures/s05_authorial_index_fixture.txt` (SHA-256: `16f301c5be9320c07637ebf54025674a6a40e0911ebe6f9fee2e7a74d4f8ae24`)
- `tests/fixtures/s05_authorial_index_scripture_ledger.json`
- `tests/test_citation_ledger_crosswalk.py` (106 unit tests passing across repo, including adversarial tests 4c–4h for context certification and incidental bibliographic filtering, 7b–7k for Greek/OCR/numeric verbatim integrity, and 8a–8c for dual and primary locator integrity)

Plus governing method:
- `docs/design/PROJECT_CONSTITUTION.md`
- `research/TXT/textual_classifications.md`
- `research/TXT/hebrew_consultation_test.md`
- `docs/workflow/NOTEBOOKLM_ANTIGRAVITY_SERIAL.md`
- `docs/workflow/NOTEBOOKLM_EXTRACTION_PROMPTS.md`

## Review task

Review the S05 Round 7 evidence packet at the exact live HEAD of draft PR #2.

1. **Form-Specific Greek/OCR and Bounded Single/Multi-Digit Numeral Verbatim Verification (Remediation of S05-R6-F1):**
   - Confirm that `GREEK_OCR_MAP` eliminates all broad `\w+` fallbacks (`xaTai\w+`, `XExax\w+`, `enixax\w+`), binding each Greek word strictly to its exact Unicode spelling or form-specific MDZ OCR signature (`καταισχυνθήσεται` -> `xaTaiov_uvv-f\|GETat` vs `καταισχυνθῇ` -> `xaTaiGvuVTTrj`).
   - Confirm that `verify_page_bounded_quote()` includes all 1-digit and multi-digit numeric tokens (`is_numeric_token`), enforces strict non-word/non-digit boundaries (`(?<![\w\d])...(?![\w\d])`) so `1134` cannot match inside `11134`, and excludes digits from `SEP_NON_NUMERIC` whenever adjacent to numeric tokens.
   - Verify adversarial regressions in `tests/test_citation_ledger_crosswalk.py`:
     - Case 7g: altered single-digit numerals (`chapter 1 and verse 2` vs `chapter 9 and verse 8`) rejected.
     - Case 7h: adjacent numeral insertion (`Rom 1134` vs `Rom 11134`) rejected.
     - Case 7i: swapped critical Greek forms (`οὐ καταισχυνθήσεται` vs `οὐ μὴ καταισχυνθῇ`) rejected.
     - Case 7j: swapped Greek OCR signatures (`xaTaiGvuVTTrj` vs `xaTaiov_uvv-f|GETat`) rejected.
     - Case 7k: arbitrary OCR prefixes (`xaTaiWRONG` / `xaTaiOTHER`) rejected.

2. **Bound Contextual Hits, Incidental Bibliographic Filtering, and Reviewed Argument Evaluations (Remediation of S05-R6-F2):**
   - Confirm that `is_incidental_context()` filters out citation hits occurring in incidental bibliographic lists (`vgl.`, `siehe`, `s.`, `z.B.`, `Literatur:`) lacking authorial analytical predicates, preventing incidental multi-word phrase occurrences from satisfying substantive thresholds (verified by Case 4h).
   - Confirm that every local substantive hit is bound to a verified evidence-ledger witness record (`linked_evidence_id`), authenticated with its printed page, PDF page, page offset `[start..end]`, matched citation string, matched analytical phrases, context excerpt, and explicit reviewed argument evaluation (`REVIEWED_ARGUMENT_JUDGMENTS`).
   - Confirm that `full_volume_search_log.md` §4.1 records both the verified evidence records and the bound local contextual hits with their exact offsets and reviewed interpretations.

3. **Primary Source Locator Parsing and Dual Citation Invariants (Remediation of S05-R6-F3):**
   - Confirm that `verify_evidence_ledger_integrity()` parses the primary locator segment prior to any `(vgl. ...)` or `;` delimiter, ensuring that a wrong primary page cannot pass via a secondary `vgl.` reference (verified by Case 8c).

4. **Grounded Passing References and Negative-Search Rationale (Remediation of S05-R5-M1):**
   - Confirm that passing references B001-10 (p. 112 n. 58), B001-11 (p. 319 n. 11), and B001-12 (p. 47 n. 1) document extended page-level context excerpts alongside explicit bounded negative-search rationale (confirming absence of Deut 25:4, Exod 32:6, and Deut 21:23 from the authorial Stellenregister).

5. **Disposition:**
   - Issue an explicit `ACCEPT` or `REJECT` disposition referencing the exact commit SHA reviewed.
   - If accepted, confirm readiness for promotion to cumulative synthesis notebook `SDP-01 Paul`.
