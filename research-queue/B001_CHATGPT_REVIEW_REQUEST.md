# B001 ChatGPT Independent Review Request

Antigravity rewrites this file for every source before requesting review.

## Current source

- Source ID: `S01F`
- Exact citation: James W. Aageson, *Paul's Use of Scripture: A Comparative Study of Biblical Interpretation in Early Palestinian Judaism and the New Testament With Special Reference to Romans 9–11* (Doctor of Philosophy thesis, Mansfield College, Faculty of Theology, University of Oxford, Michaelmas 1983 / degree granted 1984)
- Public/source locator: Oxford University Research Archive (ORA), DOI: 10.5287/ora-7rgnn1ox1, `https://ora.ox.ac.uk/objects/uuid:3925520e-0524-4eb0-b9ed-d34140c0a915`
- Branch: `research/B001-notebooklm-serial`
- Draft PR: `2`
- Extraction status: Complete secondary route source packet extracted via NotebookLM from `aageson_1984_pauls_use_of_scripture.pdf` as sole source in `SDP-B001-EXTRACT`, covering all 12 B001 comparisons, with 18 verified evidence claims (`S01F-E001` through `S01F-E018`) in `citation_ledger.csv` (`verification_status=VERIFIED`, verified against physical thesis page numbers), structural argument map, counterevidence/disagreements, bibliography leads, and self-audit.
- Review readiness: `READY`
- Review target: `LIVE_PR_HEAD`

## Files in scope

`research/inbox/B001-pauline-txt-pilot/sources/S01F/`
- `metadata.md`
- `relevance_scan.md`
- `extraction.md`
- `citation_ledger.csv`
- `argument_map.md`
- `counterevidence.md`
- `bibliography_leads.md`
- `notebooklm_self_audit.md`

Plus governing method:

- `docs/design/PROJECT_CONSTITUTION.md`
- `research/TXT/textual_classifications.md`
- `research/TXT/hebrew_consultation_test.md`
- `docs/workflow/NOTEBOOKLM_ANTIGRAVITY_SERIAL.md`
- `docs/workflow/NOTEBOOKLM_EXTRACTION_PROMPTS.md`

## Review task

Independently audit the current source packet.

Check:

1. fidelity to what the source actually says;
2. citation/locator support for each evidence row;
3. omitted qualifications, counterarguments, or relevant discussion;
4. author-view vs reported-other-scholar confusion;
5. primary-text fact vs secondary-author claim confusion;
6. overstatement from possibility -> probability/certainty;
7. unsupported page numbers or fabricated source details;
8. cherry-picking or context loss;
9. whether the packet is safe to admit into cumulative synthesis.

Do not reward agreement with the project's hypothesis. Negative, indeterminate, or contrary evidence is valid.

## Required response format

```text
ISSUED_AT_PT: <YYYY-MM-DD HH:MM PT>
REVIEWED_SHA: <reviewer inserts current live PR HEAD>

SOURCE_ID: S01F

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
