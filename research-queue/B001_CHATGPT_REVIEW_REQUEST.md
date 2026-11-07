# B001 ChatGPT Independent Review Request

Antigravity rewrites this file for every source before requesting review.

## Current source

- Source ID: `S05` (S04F ACCEPTED and promoted to SDP-01 Paul)
- Review Round: `Round 10` (Remediation of Round 9 findings S05-R9-F1, S05-R9-F2, and item 5 provenance precision)
- Exact citation: Florian Wilk, *Die Bedeutung des Jesajabuches für Paulus* (Forschungen zur Religion und Literatur des Alten und Neuen Testaments 179; Göttingen: Vandenhoeck & Ruprecht, 1998).
- Digital scan provenance: Munich Digitization Center (MDZ) / Bayerische Staatsbibliothek (BSB) Digi20 collection (URN: `urn:nbn:de:bvb:12-bsb00044375-3`; MDZ ID: `bsb00044375`; SHA-256: `700323565f6687163dc92f410779b054b763ee10bf3f745f5c2370b5455aa1b3`).
- Branch: `research/B001-notebooklm-serial`
- Draft PR: `2`
- Review readiness: `READY`
- Review target: `LIVE_PR_HEAD`
- Previous source disposition: `S04F ACCEPTED` in Round 5 independent review ([#issuecomment-6561683809](https://github.com/aguacatero/septuagint-diaspora-book/pull/2#issuecomment-6561683809)) at commit `f3c5153ff2b2bbe901bda82dfa2050f9726b50bd`, and promoted to cumulative notebook `SDP-01 Paul` with source-grounded retrieval verification.
- Round 9 Review disposition: `REVISE` ([#issuecomment-6699437543](https://github.com/aguacatero/septuagint-diaspora-book/pull/2#issuecomment-6699437543) at commit `1b3569c158e3ad126439000a46d6fdd2f9e179e6`; findings S05-R9-F1, S05-R9-F2, and item 5 remediated in full for Round 10).

## Source evidence packet under review

`research/inbox/B001-pauline-txt-pilot/sources/S05/`
- `metadata.md`
- `relevance_scan.md` (bounds Part V to pp. 381–408; literature list pp. 409–442; Stellenregister pp. 443–461)
- `extraction.md` (includes S05-E012 for Gal 3:13 / Deut 21:23; authentic p. 307 Anm. 23 quotation 'steht zu vermuten'; authentic p. 397 quotation 'wunderbaren Charakter'; pure Greek 'καταισχυνθῇ' and 'ἀθεteῖν')
- `citation_ledger.csv` (12 verified evidence rows: S05-E001 through S05-E012; pure Greek words; authentic German pre-reform 'läßt'; exact text-layer page-bounded verified quotes; dual locators `[PDF p. X; printed p. Y]` where $X = Y + 12$; E006 at printed p. 307 / PDF p. 319 Anm. 23; E007 at printed p. 397 / PDF p. 409)
- `argument_map.md` (includes section 8 for B001-12; authentic quotation 'steht zu vermuten' at p. 307 Anm. 23; p. 397 for E007)
- `counterevidence.md` (authentic quotation 'steht zu vermuten' at p. 307 Anm. 23)
- `bibliography_leads.md`
- `notebooklm_self_audit.md` (authentic quotation 'steht zu vermuten' at p. 307 Anm. 23; p. 397 for E007)
- `full_volume_search_log.md` (regenerated via dynamic adjudication with strict hit-to-source-span authentication against `pages`, authoritative derived snippets directly from local page text layer `[-300..+450]`, strict local-window alignment rejecting distant authentic snippets, fail-closed when `pages` unavailable, pinned invariant $PDF = printed + 12$ rejecting conflicting `pdf_page`, bounded token equality $\ge 5$ chars under set intersection, and transparent "source-reviewed/extraction judgment, awaiting independent review" provenance labels)
- `provenance_manifest.json`

Plus source-specific governing verification scripts and test fixtures:
- `scripts/verify_s05_negative_search.py` (fail-closed start and end delimiter verification across 13 required sections with zero spillover; form-specific Greek OCR mappings without `\w+` fallbacks; single-digit and multi-digit numeral verification with strict token boundaries `(?<![\w\d])...(?![\w\d])`; parenthesized/bracketed/multi-line bibliographic context exclusion; `authenticate_hit()` enforcing pinned $PDF = printed + 12$ invariant, deriving canonical snippets directly from local page window `[-300..+450]`, and validating caller snippets against the local window; `authenticate_and_bind_hit()` binding hits to same-page verified witnesses within $\le 500$ chars with bounded token equality $\ge 5$ chars, broad stopword filtering, and threshold of $\ge 2$ shared tokens or $\ge 1$ token $\ge 8$ chars; `build_markdown_report()` distinguishing automated lexical locality from source-reviewed argument assessment and emitting `MANUAL_REVIEW_REQUIRED` whenever any check fails)
- `tests/fixtures/s05_authorial_index_fixture.txt` (SHA-256: `16f301c5be9320c07637ebf54025674a6a40e0911ebe6f9fee2e7a74d4f8ae24`)
- `tests/fixtures/s05_authorial_index_scripture_ledger.json`
- `tests/test_citation_ledger_crosswalk.py` (106 unit tests passing across repo, including adversarial tests 4n–4p, 4q for distant authentic snippet rejection, and 4r for conflicting printed/PDF page rejection)

Plus governing method:
- `docs/design/PROJECT_CONSTITUTION.md`
- `research/TXT/textual_classifications.md`
- `research/TXT/hebrew_consultation_test.md`
- `docs/workflow/NOTEBOOKLM_ANTIGRAVITY_SERIAL.md`
- `docs/workflow/NOTEBOOKLM_EXTRACTION_PROMPTS.md`

## Review task

Review the S05 Round 10 evidence packet at the exact live HEAD of draft PR #2.

1. **Strict Local-Window Snippet Alignment & Authoritative Derived Snippet Enforcement (Remediation of S05-R9-F1):**
   - Confirm that `authenticate_hit()` ALWAYS derives the canonical authoritative snippet directly from `page_text[max(0, p_start - 300):min(len(page_text), p_end + 450)]` after offset verification, and uses this derived snippet for phrase and argument adjudication.
   - Confirm that if a caller supplies a snippet, it is strictly validated against the bounded local text window `[-300..+450]` around the hit; text from distant portions of the page or neighboring pages is rejected.
   - Verify adversarial regression in Case 4q: correct citation offset on p. 130 paired with an authentic but distant snippet (>1,000 chars away) containing configured analytical terms fails local window alignment, returns `MANUAL_REVIEW_REQUIRED`, and cannot open a substantive gate; and when no snippet is supplied, `derived_snippet` does not contain the distant terms.

2. **Pinned Page Invariant Enforcement: PDF = Printed + 12 (Remediation of S05-R9-F2):**
   - Confirm that `authenticate_hit()` strictly derives `pdf_page = hp + 12` and rejects any contradictory caller-supplied `pdf_page` (e.g. `printed_page: 130, pdf_page: 20`).
   - Confirm that the printed/PDF pair is asserted on every authenticated hit.
   - Verify adversarial regression in Case 4r: `printed_page: 130, pdf_page: 20` fails with `Contradictory pdf_page 20 (expected 142 for printed page 130)`.

3. **Provenance Precision (Remediation of Item 5):**
   - Confirm that generated labels in §4.1 use "source-reviewed/extraction judgment, awaiting independent review" rather than asserting unperformed independent human review.

4. **Disposition:**
   - Issue an explicit `ACCEPT` or `REJECT` disposition referencing the exact commit SHA reviewed.
   - If accepted, confirm readiness for promotion to cumulative synthesis notebook `SDP-01 Paul`.
