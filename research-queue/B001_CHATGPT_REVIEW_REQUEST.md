# B001 ChatGPT Independent Review Request

Antigravity rewrites this file for every source before requesting review.

## Current source

- Source ID: `S04F` (S03F ACCEPTED and promoted to SDP-01 Paul)
- Review Round: `PRE-ACQUISITION / PENDING EXTRACTION`
- Exact citation: J. B. Lightfoot, *Saint Paul's Epistle to the Galatians: A Revised Text with Introduction, Notes, and Dissertations* (London: Macmillan and Co., 1914).
- Branch: `research/B001-notebooklm-serial`
- Draft PR: `2`
- Review readiness: `NOT_READY`
- Review target: `NONE`
- Previous source disposition: `S03F ACCEPTED` in Round 5 independent review ([#issuecomment-6460107612](https://github.com/aguacatero/septuagint-diaspora-book/pull/2#issuecomment-6460107612)) at commit `c518c27339c9f1df4e9c17154361b6944de35f2b`, and promoted to cumulative notebook `SDP-01 Paul` with source-grounded retrieval verification.

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

Independently audit the revised source packet (Round 5).

Check:

1. fidelity to what the source actually says;
2. citation/locator support for each evidence row (14 rows);
3. whether Round 1, Round 2, Round 3, and Round 4 findings (including `S03F-R4-F1`) are fully and accurately addressed;
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
