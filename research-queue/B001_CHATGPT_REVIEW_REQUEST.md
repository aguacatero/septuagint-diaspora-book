# B001 ChatGPT Independent Review Request

Antigravity rewrites this file for every source before requesting review.

## Current source

- Source ID: `S02F`
- Exact citation: William Sanday and Arthur C. Headlam, *A Critical and Exegetical Commentary on the Epistle to the Romans* (International Critical Commentary; New York: Charles Scribner's Sons, 1895 [first edition]).
- Public/source locator: Internet Archive, `https://archive.org/details/epistlecommentar00sanduoft` (University of Toronto / Victoria University copy, presented by Dr. Robert Dobbie; title page imprinted: New York: Charles Scribner's Sons, 1895; preface signed Midsummer, 1895).
- Raw full-scan hash: `sanday_headlam_1895_romans_icc_ia_raw.pdf` (586 pages, 47,318,528 bytes, SHA-256: `4a6369a0595550c8c1b92b71613a73182fe4a82aa02cfc989633e6c4dc0b80af`).
- Target derivative section: `sanday_headlam_1895_romans_icc.pdf` (40 authentic pages covering title/preface, textual criticism front matter pp. lviii–lxi, Rom 4:3 pp. 99–102, Rom 9:25–26 pp. 264–267, Rom 10:11–13 pp. 286–291, Excursus on Paul's Use of the OT pp. 302–307, Rom 11:34 pp. 340–342, Rom 15:12 pp. 398–401; 4,187,334 bytes, SHA-256: `4be4cad08705963505f13a38a12b8737040e531a6146b1fa4400c936cc37cf4c`).
- Branch: `research/B001-notebooklm-serial`
- Draft PR: `2`
- Extraction status: Complete secondary route source packet extracted via NotebookLM from `sanday_headlam_1895_romans_icc.pdf` as sole source in `SDP-B001-EXTRACT`, covering all 7 Romans B001 comparisons (B001-1 through B001-7) PLUS the dedicated Excursus on "St. Paul's Use of the Old Testament" (pp. 302–307). Contains 14 verified evidence claims (`S02F-E001` through `S02F-E014`) in `citation_ledger.csv` (`verification_status=VERIFIED`, verified letter-for-letter against authentic printed page numbers).
- Non-Romans scope & negative-search verification: Documented full-volume text search across the complete 586-page text layer of the original volume (`sanday_headlam_1895_romans_icc_ia_raw.pdf`, SHA-256: `4a6369a0...`, 47,318,528 bytes; Poppler pdftotext -layout 23.03.0) yielded NO MATCH FOUND BY DOCUMENTED FULL-VOLUME TEXT SEARCH (with documented OCR and pattern limitations; see `full_volume_search_log.md` and `scripts/verify_s02f_negative_search.py`) for 1 Cor 1:19/Isa 29:14, 1 Cor 6:16/Gen 2:24, 1 Cor 9:9/Deut 25:4, 1 Cor 10:7/Exod 32:6, or Gal 3:13/Deut 21:23. The Excursus's cross-Pauline methodological findings (Kautzsch's 84-quotation taxonomy, Job quotations, Hebrew memory vs Targum vs earlier LXX) are catalogued in `citation_ledger.csv` (`S02F-E010` through `S02F-E014`).
- Incorporated self-audit corrections: S02F-E003 authorial hedging ("seems to have used") restored; S02F-E004 exact observed mechanism ("naturally crept in from ἐκάλεσεν") restored; S02F-E007 cross-language verbatim claim removed in favor of "agrees with both in wording and meaning as assessed by the authors"; Excursus methodological atoms S02F-E010–E014 fully integrated.
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
- `excursus_extraction.md`
- `full_volume_search_log.md`
- `provenance_manifest.json`

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
