# B001 ChatGPT Independent Review Request

Antigravity rewrites this file for every source before requesting review.

## Current source

- Source ID: `S05` (S04F ACCEPTED and promoted to SDP-01 Paul)
- Review Round: `Round 9` (Remediation of Round 8 findings S05-R8-F1 and S05-R8-F2)
- Exact citation: Florian Wilk, *Die Bedeutung des Jesajabuches für Paulus* (Forschungen zur Religion und Literatur des Alten und Neuen Testaments 179; Göttingen: Vandenhoeck & Ruprecht, 1998).
- Digital scan provenance: Munich Digitization Center (MDZ) / Bayerische Staatsbibliothek (BSB) Digi20 collection (URN: `urn:nbn:de:bvb:12-bsb00044375-3`; MDZ ID: `bsb00044375`; SHA-256: `700323565f6687163dc92f410779b054b763ee10bf3f745f5c2370b5455aa1b3`).
- Branch: `research/B001-notebooklm-serial`
- Draft PR: `2`
- Review readiness: `READY`
- Review target: `LIVE_PR_HEAD`
- Previous source disposition: `S04F ACCEPTED` in Round 5 independent review ([#issuecomment-6561683809](https://github.com/aguacatero/septuagint-diaspora-book/pull/2#issuecomment-6561683809)) at commit `f3c5153ff2b2bbe901bda82dfa2050f9726b50bd`, and promoted to cumulative notebook `SDP-01 Paul` with source-grounded retrieval verification.
- Round 8 Review disposition: `REVISE` ([#issuecomment-6640701933](https://github.com/aguacatero/septuagint-diaspora-book/pull/2#issuecomment-6640701933) at commit `4be235e946942f6f7d85caf7e7a56aeb2eb0fbd1`; findings S05-R8-F1 and S05-R8-F2 remediated in full for Round 9).

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
- `full_volume_search_log.md` (regenerated via dynamic adjudication with strict hit-to-source-span authentication against `pages`, authoritative derived snippets from page text layer, fail-closed when `pages` unavailable, bounded token equality $\ge 5$ chars under set intersection excluding broad argument stopwords, requiring $\ge 2$ shared semantic argument tokens or $\ge 1$ token $\ge 8$ chars, and explicit distinction between automated lexical locality and human-reviewed argument assessment)
- `provenance_manifest.json`

Plus source-specific governing verification scripts and test fixtures:
- `scripts/verify_s05_negative_search.py` (fail-closed start and end delimiter verification across 13 required sections with zero spillover; form-specific Greek OCR mappings without `\w+` fallbacks; single-digit and multi-digit numeral verification with strict token boundaries `(?<![\w\d])...(?![\w\d])`; parenthesized/bracketed/multi-line bibliographic context exclusion; `authenticate_hit()` failing closed when `pages` unavailable, enforcing exact normalized source-span correspondence, and deriving authoritative snippets from page text; `authenticate_and_bind_hit()` binding hits to same-page verified witnesses within $\le 500$ chars with bounded token equality $\ge 5$ chars, broad stopword filtering, and threshold of $\ge 2$ shared tokens or $\ge 1$ token $\ge 8$ chars; `build_markdown_report()` distinguishing automated lexical locality from human-reviewed argument assessment and emitting `MANUAL_REVIEW_REQUIRED` whenever any check fails)
- `tests/fixtures/s05_authorial_index_fixture.txt` (SHA-256: `16f301c5be9320c07637ebf54025674a6a40e0911ebe6f9fee2e7a74d4f8ae24`)
- `tests/fixtures/s05_authorial_index_scripture_ledger.json`
- `tests/test_citation_ledger_crosswalk.py` (106 unit tests passing across repo, including adversarial tests 4n–4p for fabricated snippet rejection despite >50% real page words, fail-closed behavior when `pages` is None or empty, stopword exclusion, substring non-containment, and bounded token equality length/threshold rules)

Plus governing method:
- `docs/design/PROJECT_CONSTITUTION.md`
- `research/TXT/textual_classifications.md`
- `research/TXT/hebrew_consultation_test.md`
- `docs/workflow/NOTEBOOKLM_ANTIGRAVITY_SERIAL.md`
- `docs/workflow/NOTEBOOKLM_EXTRACTION_PROMPTS.md`

## Review task

Review the S05 Round 9 evidence packet at the exact live HEAD of draft PR #2.

1. **Strict Source-Span Authentication and Authoritative Derived Snippet Window (Remediation of S05-R8-F1):**
   - Confirm that `authenticate_hit()` fails closed if `pages` is None or empty (`len(pages) == 0`).
   - Confirm that `authenticate_hit()` requires exact normalized source-span correspondence if a caller supplies a snippet, rejecting fabricated caller-supplied snippets containing prose absent from the page context even when composed of >50% authentic page vocabulary.
   - Confirm that authoritative hit snippets are derived directly from `page_text` around validated hit offsets using a bounded window `[-300..+450]`, and that analytical phrases are evaluated against this authentic derived snippet rather than unverified caller prose.
   - Verify adversarial regressions in `tests/test_citation_ledger_crosswalk.py`:
     - Case 4n: hit with valid citation offset on p. 130 but fabricated analytical snippet containing >50% real page words fails authentication and binding, resulting in `MANUAL_REVIEW_REQUIRED`.
     - Case 4o: fail-closed behavior when `pages is None` or `pages == []` in `authenticate_hit` and `authenticate_and_bind_hit`.

2. **Bounded Semantic Argument Token Integrity and Separation of Text Locality from Argument Analysis (Remediation of S05-R8-F2):**
   - Confirm that `authenticate_and_bind_hit()` enforces semantic token length $\ge 5$ characters (`[\w]{5,}`), excludes broad German/theological stopwords (`paulus`, `apostel`, `zitat`, `heiden`, `juden`, `angesichts`, etc.), and employs bounded token equality (set intersection `wit_tokens & snip_tokens`) preventing substring containment (e.g. `teil` in `mitteilen` vs `urteil`).
   - Confirm that witness binding requires $\ge 2$ shared semantic argument tokens (or $\ge 1$ distinctive token of length $\ge 8$).
   - Confirm that automated verification results are explicitly identified as lexical locality (`Automated lexical locality: hit matched on printed p. ... within X chars of verified witness ...; shared argument tokens: ...`), while human-reviewed scholarly argument interpretations are distinctly labeled under `- **Human-Reviewed Argument Assessment (Scholarly Provenance):**` with explicit reviewer-judgment provenance and rationale for each evidence claim.
   - Verify adversarial regressions in `tests/test_citation_ledger_crosswalk.py`:
     - Case 4p: hits sharing only stopwords fail binding; hits sharing substring fragments fail binding; single 6-letter tokens fail binding; 2 shared tokens $\ge 5$ chars pass binding; single 8+ letter tokens pass binding.

3. **Disposition:**
   - Issue an explicit `ACCEPT` or `REJECT` disposition referencing the exact commit SHA reviewed.
   - If accepted, confirm readiness for promotion to cumulative synthesis notebook `SDP-01 Paul`.
