# B001 ChatGPT Independent Review Request

Antigravity rewrites this file for every source before requesting review.

## Current source

- Source ID: `S05` (S04F ACCEPTED and promoted to SDP-01 Paul)
- Review Round: `Round 8` (Remediation of Round 7 findings S05-R7-F1, S05-R7-F2, and S05-R5-M1 qualify)
- Exact citation: Florian Wilk, *Die Bedeutung des Jesajabuches für Paulus* (Forschungen zur Religion und Literatur des Alten und Neuen Testaments 179; Göttingen: Vandenhoeck & Ruprecht, 1998).
- Digital scan provenance: Munich Digitization Center (MDZ) / Bayerische Staatsbibliothek (BSB) Digi20 collection (URN: `urn:nbn:de:bvb:12-bsb00044375-3`; MDZ ID: `bsb00044375`; SHA-256: `700323565f6687163dc92f410779b054b763ee10bf3f745f5c2370b5455aa1b3`).
- Branch: `research/B001-notebooklm-serial`
- Draft PR: `2`
- Review readiness: `READY`
- Review target: `LIVE_PR_HEAD`
- Previous source disposition: `S04F ACCEPTED` in Round 5 independent review ([#issuecomment-6561683809](https://github.com/aguacatero/septuagint-diaspora-book/pull/2#issuecomment-6561683809)) at commit `f3c5153ff2b2bbe901bda82dfa2050f9726b50bd`, and promoted to cumulative notebook `SDP-01 Paul` with source-grounded retrieval verification.
- Round 7 Review disposition: `REVISE` ([#issuecomment-6622483872](https://github.com/aguacatero/septuagint-diaspora-book/pull/2#issuecomment-6622483872) at commit `b24bb02a6561288b62248e76210d397f37c9c889`; findings S05-R7-F1, S05-R7-F2, and S05-R5-M1 qualify remediated in full for Round 8).

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
- `full_volume_search_log.md` (regenerated via dynamic adjudication with strict hit-to-source-span authentication against `pages`, same-page local argument passage binding within $\le 500$ chars of verified witness segments plus shared semantic argument tokens, parenthesized/bracketed/multi-line bibliographic filtering, fail-closed `MANUAL_REVIEW_REQUIRED` report certification gate, and bounded/source-reviewed passing-reference judgments)
- `provenance_manifest.json`

Plus source-specific governing verification scripts and test fixtures:
- `scripts/verify_s05_negative_search.py` (fail-closed start and end delimiter verification across 13 required sections with zero spillover; form-specific Greek OCR mappings without `\w+` fallbacks; single-digit and multi-digit numeral verification with strict token boundaries `(?<![\w\d])...(?![\w\d])`; parenthesized/bracketed/multi-line bibliographic context exclusion; `authenticate_and_bind_hit()` authenticating caller-provided hit offsets/snippets against `pages` and binding strictly to same-page verified witnesses within $\le 500$ chars with shared argument tokens; `min_substantive_hits` enforced on `bound_locus_hits`; `build_markdown_report()` emitting `MANUAL_REVIEW_REQUIRED` whenever any control, index, or target fails)
- `tests/fixtures/s05_authorial_index_fixture.txt` (SHA-256: `16f301c5be9320c07637ebf54025674a6a40e0911ebe6f9fee2e7a74d4f8ae24`)
- `tests/fixtures/s05_authorial_index_scripture_ledger.json`
- `tests/test_citation_ledger_crosswalk.py` (106 unit tests passing across repo, including adversarial tests 4c–4m for context certification, parenthesized/multi-line bibliographic filtering, unauthenticated/fabricated hit spans, distant same-page hits, ±2-page neighbor hits, and fail-closed report certification, 7b–7k for Greek/OCR/numeric verbatim integrity, and 8a–8c for dual and primary locator integrity)

Plus governing method:
- `docs/design/PROJECT_CONSTITUTION.md`
- `research/TXT/textual_classifications.md`
- `research/TXT/hebrew_consultation_test.md`
- `docs/workflow/NOTEBOOKLM_ANTIGRAVITY_SERIAL.md`
- `docs/workflow/NOTEBOOKLM_EXTRACTION_PROMPTS.md`

## Review task

Review the S05 Round 8 evidence packet at the exact live HEAD of draft PR #2.

1. **Parenthesized/Bracketed/Multi-Line Incidental Bibliographic Filtering (Remediation of S05-R7-F1):**
   - Confirm that `is_incidental_context()` detects bibliographic and incidental references containing parentheses `()`, brackets `[]`, author-year citations (`Literatur: Müller (1990), Rom 9,25; ...`, `Vgl. Weber (1992), Rom 9,25; ...`), multi-line citation lists, and incidental quotations up to 140 characters after the cue (`vgl.`, `siehe`, `s.o.`, `s.u.`, `s.`, `z.B.`, `dazu s.`, `Literatur:`, `gegen`, `so z.B.`), while restricting post-match analytical predicate checks to the local clause before `;`/`.`/`:`.
   - Verify adversarial regressions in Case 4i (`tests/test_citation_ledger_crosswalk.py`) confirm that parenthesized author-year references and multi-line bibliographic lists are rejected as incidental and cannot satisfy `min_substantive_hits`.

2. **Strict Hit-to-Source-Span Authentication, Same-Page Argument Passage Binding, and Fail-Closed Report Gate (Remediation of S05-R7-F2):**
   - Confirm that `authenticate_and_bind_hit()` authenticates every caller-provided hit against the actual page text (`pages[pdf_page - 1]`), verifying that `page_offset` matches `match` and that `snippet` is an authentic substring of the page text.
   - Confirm that `adjudicate_target()` eliminates ±2-page proximity labeling and binds substantive hits strictly to verified witness segments on the **same printed page** within $\le 500$ characters that share $\ge 1$ non-trivial semantic argument token ($\ge 5$ chars), requiring `min_substantive_hits` to be satisfied by `bound_locus_hits` and verifying that every required `evidence_id` has at least one bound local argument hit.
   - Confirm that `build_markdown_report()` checks `positive_controls`, `index_audit`, and `adjudications` before certifying §5, emitting `MANUAL_REVIEW_REQUIRED` instead of `VERIFIED_COMPLETE` whenever any check fails.
   - Verify adversarial regressions in `tests/test_citation_ledger_crosswalk.py`:
     - Case 4j: fabricated/unauthenticated hit snippets or offsets not present in `pages` are rejected.
     - Case 4k: same-page hits $> 500$ characters away from the verified witness span (or lacking shared argument tokens) fail binding and cannot satisfy `min_substantive_hits`.
     - Case 4l: hits on neighboring pages (±1 or ±2 pages from the verified witness page) are rejected as unbound.
     - Case 4m: `build_markdown_report()` emits `MANUAL_REVIEW_REQUIRED` (and never `VERIFIED_COMPLETE`) when any target adjudication fails.

3. **Bounded/Source-Reviewed Passing-Reference Classification (Remediation of S05-R5-M1 Qualify):**
   - Confirm that `PASSING_REFERENCE` and `PASSING_TEXT_CRITICAL_NOTE` verify that zero contradictory substantive hits exist elsewhere in the volume (`not elsewhere_substantive`) and explicitly label their negative/passing classification in `full_volume_search_log.md` as a `bounded/source-reviewed judgment`.

4. **Disposition:**
   - Issue an explicit `ACCEPT` or `REJECT` disposition referencing the exact commit SHA reviewed.
   - If accepted, confirm readiness for promotion to cumulative synthesis notebook `SDP-01 Paul`.
