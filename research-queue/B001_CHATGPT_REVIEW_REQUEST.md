# B001 ChatGPT Independent Review Request

Antigravity rewrites this file for every source before requesting review.

## Current source

- Source ID: `S03F`
- Review Round: `Round 3 (Revisions Addressing S03F-R2 Review Findings)`
- Exact citation: Archibald Robertson and Alfred Plummer, *A Critical and Exegetical Commentary on the First Epistle of St Paul to the Corinthians* (International Critical Commentary; Edinburgh: T. & T. Clark / New York: Charles Scribner's Sons, 1911; Second Edition, 1914).
- Public/source locator: Internet Archive, `https://archive.org/details/criticalexegetic33robeuoft` (Internet Archive item ID: `criticalexegetic33robeuoft`).
- Raw full-scan hash: `robertson_plummer_1911_1corinthians_icc_ia_raw.pdf` (504 pages, 32,652,569 bytes, SHA-256: `4e7d0aa655aff66d84fca857387860d25dddd4c2be1c5aa2ea0446f11df78efd`).
- Target derivative section: `robertson_plummer_1911_1corinthians_icc.pdf` (71 authentic pages covering half-title/title page, preface pp. vii–viii, contents pp. ix–x, Introduction § VI 'Quotations from the O.T.' pp. lii–liv and § VII 'Text of 1 Corinthians' pp. lv–lxii, 1 Cor 1:1–3 pp. 1–3, 1 Cor 1:17–25 pp. 17–22, 1 Cor 2:13–3:4 pp. 48–52, 1 Cor 6:12–20 pp. 124–130, 1 Cor 9:7–14 pp. 181–188, 1 Cor 10:1–13 pp. 200–208, 1 Cor 15:50–58 pp. 376–381, Index I General pp. 403–406, Index II Greek words pp. 413–416; 13,305,176 bytes, SHA-256: `5d25c57f60179c4995d481911b37e48bbc71781d637ea35144a35aa4cf56829e`).
- Branch: `research/B001-notebooklm-serial`
- Draft PR: `2`
- Extraction status: Complete secondary route source packet extracted via NotebookLM from `robertson_plummer_1911_1corinthians_icc.pdf` (71 pages) as sole source in `SDP-B001-EXTRACT`, covering the four direct 1 Corinthians loci (B001-8, B001-9, B001-10, B001-11), general Pauline quotation methodology (B001-GENERAL), substantive cross-epistle comparison on Isa 40:13 / Rom 11:34 (B001-6), and relevant secondary interpretive discussion on Joel 2:32 / Rom 10:12–13 (B001-5). Contains 14 verified evidence claims (`S03F-E001` through `S03F-E014`) in `citation_ledger.csv` (`verification_status=VERIFIED`, verified letter-for-letter against authentic printed page numbers and reconciled derivative page locators).
- Round 2 Review Findings Addressed:
  - `[S03F-R2-F1] Resolved`: Replaced hardcoded target outcomes in `scripts/verify_s03f_negative_search.py` with `VERIFIED_MATCH_CATALOG` annotating all 11 matches across the 527k-word text corpus. Added dynamic `adjudicate_hit` and `adjudicate_target` logic, generated an itemized Match Evidence Ledger table in `full_volume_search_log.md`, and added an adversarial regression test in `tests/test_harden_source_switch.py` verifying that injected hits dynamically alter locus classification to `SUBSTANTIVE_DISCUSSION`.
  - `[S03F-R2-F2] Resolved`: Bounded index positive controls now check specific sections (Index I: `Allegorical interpretation`, `Assimilation`, `Aquila`; Index II: `ἀδάπανος`, `ἀλοάω`; Index III: `Caritas`, `underling`). Script strictly verifies index ordering, detects and fails closed on unexpected 4th indexes or Scripture index headings (`INDEX OF SCRIPTURE`, `IV. BIBLICAL REFERENCES`), covered by comprehensive unit tests.
  - `[S03F-R2-F3] Resolved`: Updated `test_verify_s03f_negative_search_rejects_tampered_text` in `tests/test_harden_source_switch.py` to run unconditionally in CI without requiring the 32MB raw PDF download, using fixture isolation and monkeypatching.
  - `[S03F-R2-F4] Resolved`: Reconciled all derivative PDF page locators across `citation_ledger.csv`, `extraction.md`, `relevance_scan.md`, `counterevidence.md`, and `provenance_manifest.json` to the exact 71-page derivative PDF:
    - Intro: printed p. lii = derivative p. 9; p. liii = p. 10; p. liv = p. 11; p. lxii = p. 19.
    - 1 Cor 1:1–3: printed p. 3 = derivative p. 22.
    - 1 Cor 1:17–25: printed p. 19 = derivative p. 25.
    - 1 Cor 2:13–3:4: printed pp. 50–51 = derivative pp. 31–32 (was mislabeled 32–33).
    - 1 Cor 6:12–20: printed p. 126 = derivative p. 36 (was mislabeled 37).
    - 1 Cor 9:7–14: printed pp. 183–184 = derivative pp. 43–44 (was mislabeled 45–46).
    - 1 Cor 10:1–13: printed pp. 203–204 = derivative pp. 52–53 (was mislabeled 53–54).
    - Indexes: raw scan pp. 479–482, 489–492 = derivative pp. 64–71.
  - `[S03F-R2-F5] Resolved`: Visually and textually verified on printed p. 50 (derivative p. 31) that Robertson & Plummer print unassimilated Hellenistic orthography with nu (`σύνβουλος`, `συνβιβάσει`), adhering to Westcott-Hort editorial practice in the ICC series. Documented in `S03F-E013` notes and commentary analysis.
  - `[S03F-R2-F6] Resolved`: Softened `S03F-E011` notes from asserting "conscious argumentative adaptation" to tentative authorial inference ("seems to make changes" for argument suitability) rather than asserting conscious dogmatic alteration or textual corruption. Softened `relevance_scan.md` description for B001-8 (1 Cor 1:19) from "intentional substitution" to tentative Pauline adaptation per customary freedom of citation.
- Non-Corinthians scope & negative-search verification: Documented full-volume text search across the complete 504-page text layer of the original volume (`robertson_plummer_1911_1corinthians_icc_ia_raw.pdf`, SHA-256: `4e7d0aa6...`, 32,652,569 bytes; Poppler pdftotext; cryptographically bound and positive-controlled) confirmed that for the remaining six loci (B001-1, B001-2, B001-3, B001-4, B001-7, B001-12), no substantive discussion is found under documented search patterns (see `full_volume_search_log.md` with itemized Match Evidence Ledger, and `scripts/verify_s03f_negative_search.py`).
- Review readiness: `READY`
- Review target: `LIVE_PR_HEAD`

## Files in scope

`research/inbox/B001-pauline-txt-pilot/sources/S03F/`
- `metadata.md`
- `relevance_scan.md`
- `extraction.md`
- `citation_ledger.csv`
- `argument_map.md`
- `counterevidence.md`
- `bibliography_leads.md`
- `notebooklm_self_audit.md`
- `intro_quotations_extraction.md`
- `full_volume_search_log.md`
- `provenance_manifest.json`

Plus governing scripts and tests:
- `scripts/build_s03f_derivative.py`
- `scripts/verify_s03f_negative_search.py`
- `tests/test_citation_ledger_crosswalk.py`
- `tests/test_harden_source_switch.py`

Plus governing method:
- `docs/design/PROJECT_CONSTITUTION.md`
- `research/TXT/textual_classifications.md`
- `research/TXT/hebrew_consultation_test.md`
- `docs/workflow/NOTEBOOKLM_ANTIGRAVITY_SERIAL.md`
- `docs/workflow/NOTEBOOKLM_EXTRACTION_PROMPTS.md`

## Review task

Independently audit the revised source packet (Round 2).

Check:

1. fidelity to what the source actually says;
2. citation/locator support for each evidence row (14 rows);
3. whether Round 1 findings (S03F-R1-F1, F2, F3, M1, M2) are fully and accurately addressed;
4. whether B001-6 (Isa 40:13) and B001-5 (Joel 2:32) are properly integrated;
5. whether text-critical and literary qualifications are preserved without overstatement;
6. author-view vs reported-other-scholar confusion;
7. primary-text fact vs secondary-author claim confusion;
8. whether the packet is safe to admit into cumulative synthesis.

Do not reward agreement with the project's hypothesis. Negative, indeterminate, or contrary evidence is valid.

## Required response format

```text
ISSUED_AT_PT: <YYYY-MM-DD HH:MM PT>
REVIEWED_SHA: <reviewer inserts current live PR HEAD>

SOURCE_ID: S03F

## Findings
- [HIGH|MED|LOW] ...

## Evidence
...

## Required corrections
...

SOURCE_PACKET: ACCEPT|REVISE
MERGE: YES|NO
REQUEST CHANGES: YES|NO
```

For per-source review, `MERGE: YES` means "this source packet is acceptable to advance within the draft research branch"; it does **not** authorize final repository merge.
