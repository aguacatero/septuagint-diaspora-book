# B001 ChatGPT Independent Review Request

Antigravity rewrites this file for every source before requesting review.

## Current source

- Source ID: `P02F`
- Exact citation: *The Old Testament in Greek according to the Septuagint, Vol. I: Genesis–IV Kings*, ed. Henry Barclay Swete, D.D. (Cambridge University Press, 3rd ed. 1901)
- Public/source locator: `https://archive.org/details/oldtestamentingr0001henr`
- Branch: `research/B001-notebooklm-serial`
- Draft PR: `2`
- Extraction status: Complete primary route source packet revised and re-audited per PR comments 6159404391 and 6172657286.
- Re-review context: Addressed Comment 6172657286 provenance correction — replaced all P01F cross-source evidence IDs with their exact accepted canonical ledger mappings (1 Cor 6:16 -> P01F-P009; 1 Cor 10:7 -> P01F-P011; Gal 3:13 -> P01F-P012; Rom 4:3 -> P01F-P001; 1 Cor 9:9 -> P01F-P010) across primary_text_ledger.csv, relevance_scan.md, extraction.md, counterevidence.md, and notebooklm_self_audit.md.
- Review readiness: `READY`
- Review target: `LIVE_PR_HEAD`

## Files in scope

`research/inbox/B001-pauline-txt-pilot/sources/P02F/`
- `metadata.md`
- `relevance_scan.md`
- `extraction.md`
- `primary_text_ledger.csv`
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
REVIEWED_SHA: <reviewer inserts current live PR HEAD>

SOURCE_ID: P02F

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
