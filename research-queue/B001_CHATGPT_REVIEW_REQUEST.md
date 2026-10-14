# B001 ChatGPT Independent Review Request

Antigravity rewrites this file for every source before requesting review.

## Current source

- Source ID: `P03F`
- Exact citation: *The Old Testament in Greek according to the Septuagint, Vol. III: Hosea–4 Maccabees*, ed. Henry Barclay Swete, D.D. (Cambridge University Press, 1894)
- Public/source locator: `https://archive.org/details/oldtestamenting03swet`
- Branch: `research/B001-notebooklm-serial`
- Draft PR: `2`
- Extraction status: Complete primary route source packet extracted via NotebookLM from `swete_lxx_vol3_p03f_target.pdf` as sole source in `SDP-B001-EXTRACT`, covering the 7 B001 prophetic loci (Hosea 2:23, Hosea 1:10, Isaiah 28:16, Joel 2:32, Isaiah 40:13, Isaiah 11:10, Isaiah 29:14), with verified uncial apparatus collations (Codices B, א, A, Q, Γ, Z) and exact P01F cross-source canonical ledger attributions.
- Review readiness: `READY`
- Review target: `LIVE_PR_HEAD`

## Files in scope

`research/inbox/B001-pauline-txt-pilot/sources/P03F/`
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
ISSUED_AT_PT: <YYYY-MM-DD HH:MM PT>
REVIEWED_SHA: <reviewer inserts current live PR HEAD>

SOURCE_ID: P03F

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
