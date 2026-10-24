# B001 ChatGPT Independent Review Request

Antigravity rewrites this file for every source before requesting review.

## Current source

- Source ID: `S02F`
- Exact citation: William Sanday and Arthur C. Headlam, *A Critical and Exegetical Commentary on the Epistle to the Romans* (International Critical Commentary; Edinburgh: T&T Clark; New York: Charles Scribner's Sons, 1895).
- Public/source locator: Internet Archive, `https://archive.org/details/acriticalandexe00headgoog`, raw IA full scan `sanday_headlam_1895_romans_icc_ia_raw.pdf`; target-normalized 40-page section `sanday_headlam_1895_romans_icc.pdf`.
- Branch: `research/B001-notebooklm-serial`
- Draft PR: `2`
- Extraction status: Complete secondary route source packet extracted via NotebookLM from `sanday_headlam_1895_romans_icc.pdf` as sole source in `SDP-B001-EXTRACT`, covering all 7 Romans B001 comparisons (B001-1 through B001-7) + Excursus on Paul's use of the Old Testament (pp. 302–307). Non-Romans loci (1 Cor 1:19, 6:16, 9:9, 10:7, Gal 3:13) are outside the commentary scope and explicitly not discussed. Contains 9 verified evidence claims (`S02F-E001` through `S02F-E009`) in `citation_ledger.csv` (`verification_status=VERIFIED`, verified against authentic printed page numbers), structural argument map, counterevidence/qualifications, bibliography leads, and self-audit.
- Review readiness: `READY`
- Review target: `LIVE_PR_HEAD`

## Files in scope

`research/inbox/B001-pauline-txt-pilot/sources/S02F/`
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

SOURCE_ID: S02F

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
