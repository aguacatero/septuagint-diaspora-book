# B001 ChatGPT Independent Review Request

Antigravity rewrites this file for every source before requesting review.

## Current source

- Source ID: `S03F`
- Exact citation: Archibald Robertson and Alfred Plummer, *A Critical and Exegetical Commentary on the First Epistle of St Paul to the Corinthians* (International Critical Commentary; Edinburgh: T. & T. Clark / New York: Charles Scribner's Sons, 1911; Second Edition, 1914).
- Public/source locator: Internet Archive, `https://archive.org/details/criticalexegetic33robeuoft` (Internet Archive item ID: `criticalexegetic33robeuoft`).
- Raw full-scan hash: `robertson_plummer_1911_1corinthians_icc_ia_raw.pdf` (504 pages, 32,652,569 bytes, SHA-256: `4e7d0aa655aff66d84fca857387860d25dddd4c2be1c5aa2ea0446f11df78efd`).
- Target derivative section: `robertson_plummer_1911_1corinthians_icc.pdf` (63 authentic pages covering half-title/title page, preface pp. vii–viii, contents pp. ix–x, Introduction § VI 'Quotations from the O.T.' pp. lii–liv and § VII 'Text of 1 Corinthians' pp. lv–lxii, 1 Cor 1:17–25 pp. 17–22, 1 Cor 6:12–20 pp. 124–130, 1 Cor 9:7–14 pp. 181–188, 1 Cor 10:1–13 pp. 200–208, 1 Cor 15:50–58 pp. 376–381, Index I General pp. 403–406, Index II Greek words pp. 413–416; 11,717,060 bytes, SHA-256: `aea9d86460ff90f7e4fb3131a300f5ff7ce411cbec65c70acf480e5521821fe0`).
- Branch: `research/B001-notebooklm-serial`
- Draft PR: `2`
- Extraction status: Complete secondary route source packet extracted via NotebookLM from `robertson_plummer_1911_1corinthians_icc.pdf` as sole source in `SDP-B001-EXTRACT`, covering the four 1 Corinthians B001 comparisons (B001-8, B001-9, B001-10, B001-11) PLUS general Pauline quotation methodology from Introduction § VI (pp. lii–liv). Contains 12 verified evidence claims (`S03F-E001` through `S03F-E012`) in `citation_ledger.csv` (`verification_status=VERIFIED`, verified letter-for-letter against authentic printed page numbers).
- Non-Corinthians scope & negative-search verification: Documented full-volume text search across the complete 504-page text layer of the original volume (`robertson_plummer_1911_1corinthians_icc_ia_raw.pdf`, SHA-256: `4e7d0aa6...`, 32,652,569 bytes; Poppler pdftotext; validated with positive controls on typography) confirmed genuine absence of substantive discussion for B001-1 through B001-7 and B001-12 (see `full_volume_search_log.md` and `scripts/verify_s03f_negative_search.py`). Any occasional occurrences are passing parenthetical cross-references without commentary.
- Incorporated self-audit corrections: S03F-E001 preserves possibility framing ("possibly influenced by Psalm 33:10 LXX"); S03F-E006 preserves the author's explicit qualification on `πάντως` in 1 Cor 9:10 (does not mean oxen are not cared for at all by God).
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
