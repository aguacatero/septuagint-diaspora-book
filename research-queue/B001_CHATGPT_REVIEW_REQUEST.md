# B001 ChatGPT Independent Review Request

Antigravity rewrites this file for every source before requesting review.

## Current source

- Source ID: `S08F`
- Review Round: `Round 3`
- Exact citation: J. Paul Tanner, *The New Covenant and Paul’s Quotations from Hosea in Romans 9:25–26*, *Bibliotheca Sacra*, Vol. 162, No. 645 (January–March 2005), pp. 95–110.
- Branch: `research/B001-notebooklm-serial`
- Draft PR: `2`
- Review readiness: `READY`
- Review target: `LIVE_PR_HEAD`
- Previous source disposition: `S07F ACCEPTED` in Round 3 independent review ([#issuecomment-6727995244](https://github.com/aguacatero/septuagint-diaspora-book/pull/2#issuecomment-6727995244)) at commit `001eb018739a5bf6c94abf5539990d44bc2ccaa0`, and promoted to cumulative notebook `SDP-01 Paul` with source-grounded retrieval verification.
- Round 1 review disposition: `SOURCE_PACKET: REVISE` ([#issuecomment-6733387261](https://github.com/aguacatero/septuagint-diaspora-book/pull/2#issuecomment-6733387261)) on SHA `1a5e5800592910ee8790c309f95b8a0e7af08422`.
- Round 2 review disposition: `SOURCE_PACKET: REVISE` ([#issuecomment-6759235942](https://github.com/aguacatero/septuagint-diaspora-book/pull/2#issuecomment-6759235942)) on SHA `a3dc8282d6733b9a88dfde97fb5c71d0d17ea79a`.

## Round 2 Findings Remediation Summary

1. **S08F-R2-F1 (Bibliographic Footnote Prefix Collision & Author/Title Authentication):**
   - Implemented `parse_source_locator` in `scripts/verify_s08f_negative_search.py` to parse exact numeric printed pages, PDF pages, and exact delimited footnote integers (e.g. `\bfn\.\s*(\d+)\b`). Replaced substring comparisons with integer equality checks, preventing prefix collisions (`fn. 2 -> fn. 20`).
   - Added authoritative per-lead `author` and `title` fields to `EXPECTED_BIBLIOGRAPHY_LEADS` for all 26 leads, enforcing that each lead block in `bibliography_leads.md` contains exactly one matching `Author` line and exactly one matching `Title` line.
   - Added fail-closed adversarial mutation tests in `tests/test_citation_ledger_crosswalk.py` for `fn. 2 -> fn. 20`, invented work title (`*Unrelated Work*`), and invented author (`Another Scholar`).
2. **S08F-R2-F2 (Strict Bracket Delimiters & Coordinated False PDF Pages):**
   - Enforced strict bracketed delimiters `[PDF p. X]` and exact parsed numeric comparisons in both `verify_ledger_witnesses()` and `verify_cross_artifact_consistency()`, eliminating open-ended prefix matching `[PDF p. 4`.
   - Added fail-closed adversarial mutation tests for a coordinated false PDF page (`PDF p. 4 -> PDF p. 40` in both ledger and extraction) and malformed/missing locator delimiters.
3. **S08F-R2-F3 (Field-Bound Quotation Verification):**
   - Isolated the named `- **Short Exact Quotation:**` line in each evidence block rather than searching the entire block, preventing altered quotations from being masked by notes copies.
   - Added a fail-closed adversarial mutation test for a corrupted quotation field with the original quote pasted into Notes.

## Source packet under review

`research/inbox/B001-pauline-txt-pilot/sources/S08F/`
- `metadata.md`
- `relevance_scan.md`
- `extraction.md`
- `citation_ledger.csv`
- `argument_map.md`
- `counterevidence.md`
- `bibliography_leads.md`
- `notebooklm_self_audit.md`
- `tanner_hosea_new_covenant_synthesis.md`
- `full_volume_search_log.md`
- `provenance_manifest.json`

Plus governing scripts and tests:
- `scripts/execute_s08f_prompts.py`
- `scripts/verify_s08f_negative_search.py`
- `tests/test_citation_ledger_crosswalk.py`

Plus governing method:
- `docs/design/PROJECT_CONSTITUTION.md`
- `research/TXT/textual_classifications.md`
- `research/TXT/hebrew_consultation_test.md`
- `docs/workflow/NOTEBOOKLM_ANTIGRAVITY_SERIAL.md`
- `docs/workflow/NOTEBOOKLM_EXTRACTION_PROMPTS.md`

## Review task

Evaluate source packet `S08F` against the governing method and source text.

Verify that:
1. All three Round 2 review findings (S08F-R2-F1, S08F-R2-F2, S08F-R2-F3) have been fully remediated.
2. All extracted claims in `citation_ledger.csv` and `extraction.md` are accurately grounded in J. Paul Tanner's 2005 article, with exact quotes and verified physical locators matching the monotonic formula $printed = PDF + 94$ across all 16 article pages (printed pp. 95–110 = PDF pp. 1–16).
3. The negative search log accurately distinguishes the extended treatment of B001-2 (Romans 9:25 / Hosea 2:23) and B001-3 (Romans 9:26 / Hosea 1:10), and the 10 confirmed absent loci.
4. The cross-artifact consistency checks pass without section-boundary bleed, duplicate locators, or malformed range bounds.
5. The extraction strictly avoids external model hallucination and accurately represents Tanner's thesis: Paul applies Hosea 1:10b and 2:23 to Gentile inclusion as a direct, partial phase of fulfillment through New Covenant participation, without superseding national promises to ethnic Israel.

Issue an independent verdict: `SOURCE_PACKET: ACCEPT`, `REVISE`, or `REJECT`.
Draft PR #2 remains unmerged (`MERGE: NO`).
Milestone progress remains strictly 1/6 accepted.
