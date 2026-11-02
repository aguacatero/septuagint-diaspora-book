# B001 ChatGPT Independent Review Request

Antigravity rewrites this file for every source before requesting review.

## Current source

- Source ID: `S05` (S04F ACCEPTED and promoted to SDP-01 Paul)
- Review Round: `Round 6` (Remediation of Round 5 findings S05-R5-F1, S05-R5-F2, S05-R5-F3, S05-R5-M1)
- Exact citation: Florian Wilk, *Die Bedeutung des Jesajabuches für Paulus* (Forschungen zur Religion und Literatur des Alten und Neuen Testaments 179; Göttingen: Vandenhoeck & Ruprecht, 1998).
- Digital scan provenance: Munich Digitization Center (MDZ) / Bayerische Staatsbibliothek (BSB) Digi20 collection (URN: `urn:nbn:de:bvb:12-bsb00044375-3`; MDZ ID: `bsb00044375`; SHA-256: `700323565f6687163dc92f410779b054b763ee10bf3f745f5c2370b5455aa1b3`).
- Branch: `research/B001-notebooklm-serial`
- Draft PR: `2`
- Review readiness: `READY`
- Review target: `LIVE_PR_HEAD`
- Previous source disposition: `S04F ACCEPTED` in Round 5 independent review ([#issuecomment-6561683809](https://github.com/aguacatero/septuagint-diaspora-book/pull/2#issuecomment-6561683809)) at commit `f3c5153ff2b2bbe901bda82dfa2050f9726b50bd`, and promoted to cumulative notebook `SDP-01 Paul` with source-grounded retrieval verification.
- Round 5 Review disposition: `REVISE` ([#issuecomment-6589956404](https://github.com/aguacatero/septuagint-diaspora-book/pull/2#issuecomment-6589956404) at commit `4ffbcacd6a13db84019c27661e1f13f38545008f`; findings S05-R5-F1, S05-R5-F2, S05-R5-F3, S05-R5-M1 remediated in full for Round 6).

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
- `full_volume_search_log.md` (regenerated via dynamic adjudication with full-token Greek and numeric verbatim verification, argument-witness locality correlation requiring local locus hits, grounded passing references, contrary context detection, and pattern-bounded Stellenregister coverage)
- `provenance_manifest.json`

Plus source-specific governing verification scripts and test fixtures:
- `scripts/verify_s05_negative_search.py` (fail-closed start and end delimiter verification across 13 required sections with zero spillover; full-token Greek, numeric, and script verbatim verification against `pages[pdf_page - 1]` with Sperrsatz handling and MDZ OCR Greek signatures; argument-witness locality correlation requiring local locus hits `len(locus_hits) >= min_substantive` within $|\Delta p| \le 2$; multi-word analytical concepts; enforced dual citation arithmetic $X = Y + 12$ and locator cross-validation; grounded passing references B001-10, B001-11, B001-12; dynamic summary generation with witness records)
- `tests/fixtures/s05_authorial_index_fixture.txt` (SHA-256: `16f301c5be9320c07637ebf54025674a6a40e0911ebe6f9fee2e7a74d4f8ae24`)
- `tests/fixtures/s05_authorial_index_scripture_ledger.json`
- `tests/test_citation_ledger_crosswalk.py` (106 unit tests passing across repo, including adversarial tests 4c, 4d, 4e, 4f, 4g for context certification, 7b, 7c, 7d, 7e, 7f for page-bounded quote integrity, and 8a, 8b for dual locator integrity)

Plus governing method:
- `docs/design/PROJECT_CONSTITUTION.md`
- `research/TXT/textual_classifications.md`
- `research/TXT/hebrew_consultation_test.md`
- `docs/workflow/NOTEBOOKLM_ANTIGRAVITY_SERIAL.md`
- `docs/workflow/NOTEBOOKLM_EXTRACTION_PROMPTS.md`

## Review task

Review the S05 Round 6 evidence packet at the exact live HEAD of draft PR #2.

1. **Full-Token Greek, Numeric, and Script Verbatim Verification (Remediation of S05-R5-F1):**
   - Confirm that `verify_page_bounded_quote()` extracts and verifies all Unicode words, Greek characters, and numbers (`[\w𝔊©@]+`), dropping zero Greek or numeric tokens.
   - Confirm that `GREEK_OCR_MAP` maps authentic Unicode Greek tokens to MDZ OCR signatures (`οὐ`, `καταισχυνθήσεται`, `μὴ`, `καταισχυνθῇ`, `κύριος`, `ἤ`, `𝔊`, `ἀθετεῖν`, `κεκατηραμένος`, `ἐπικατάρατος`), preserving exact readings without allowing altered Greek (e.g. `λόγος`, `πνεῦμα`) to pass.
   - Confirm that separator `SEP` enforces strict punctuation, whitespace, and footnote references without arbitrary character bridging.
   - Verify adversarial regression Case 7e (altered Greek rejected) and Case 7f (altered numerals rejected) in `tests/test_citation_ledger_crosswalk.py`.

2. **Argument-to-Hit Certification Soundness and Witness Locality (Remediation of S05-R5-F2):**
   - Confirm that generic single words have been removed from `GENERAL_SCHOLARLY_TERMS` and target catalogs, replaced exclusively with multi-word analytical concepts.
   - Confirm that the substantive threshold is enforced on local locus hits within $|\Delta p| \le 2$ (`len(locus_hits) >= min_substantive`), preventing combinations of distant hits from satisfying substantive requirements.
   - Confirm that verified argument witness records link approved substantive conclusions to an authenticated quotation, page, offset, passage target, and explicit argument judgment in `full_volume_search_log.md` section 4.1.
   - Verify adversarial regression Case 4f (same-page generic incidental hits rejected) and Case 4g (1-local + 2-distant hits rejected).

3. **Displayed Dual Locator Invariants and Validation (Remediation of S05-R5-F3):**
   - Confirm that `verify_evidence_ledger_integrity()` explicitly parses displayed dual citations in `notebooklm_citation` (`[PDF p. X; printed p. Y]`) and enforces $X = Y + 12$ and $Y = \text{printed\_page}$.
   - Confirm cross-validation of `source_locator` asserting `S. <printed_page>`.
   - Verify adversarial regression Case 8a (inconsistent dual citation rejected) and Case 8b (inconsistent locator page rejected).

4. **Grounded Passing References (Remediation of S05-R5-M1):**
   - Confirm that passing reference determinations for B001-10 (p. 112 n. 58), B001-11 (p. 319 n. 11), and B001-12 (p. 47 n. 1) are grounded in verified textual witnesses rather than preselected classifications.

5. **Fail-Closed Book Coverage and Delimiters:**
   - Confirm authorial Stellenregister parsing positively verifies BOTH start AND end delimiters across all 13 required sections with zero spillover.

6. **Cryptographic Invariants and Source Integrity:**
   - Verify raw scan SHA-256 (`700323565f6687163dc92f410779b054b763ee10bf3f745f5c2370b5455aa1b3`).
   - Verify extracted text layer SHA-256 (`d4f091259e403cf44a52c10e08944a24fd3b6a55c9069f53438898d05d1d4b62`).

7. **Disposition:**
   - Issue an explicit `ACCEPT` or `REJECT` disposition referencing the exact commit SHA reviewed.
   - If accepted, confirm readiness for promotion to cumulative synthesis notebook `SDP-01 Paul`.
