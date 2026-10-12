# B001 NotebookLM Extraction Prompts

Run these prompts in order against `SDP-B001-EXTRACT` after verifying that the notebook contains exactly one research source.

Always keep the current source as the only selected source.

---

## Prompt 0 — Source identity and guardrail

> Work only from the currently loaded source. Do not use outside knowledge. First identify the source's author/editor, exact title, publication year, edition/volume if visible, and the page-numbering system. State whether printed page numbers are visible and whether your citations can be mapped to them. If any bibliographic detail is not visible in the source, write UNKNOWN rather than guessing. End with: SOURCE-BOUND MODE CONFIRMED.

Save to `metadata.md`.

---

## Prompt 1 — Exhaustive B001 relevance scan

> Work only from this source. Search the entire source for substantive discussion relevant to any of these B001 comparisons:
>
> 1. Romans 4:3 / Genesis 15:6
> 2. Romans 9:25 / Hosea 2:23
> 3. Romans 9:26 / Hosea 1:10
> 4. Romans 10:11 / Isaiah 28:16
> 5. Romans 10:13 / Joel 2:32
> 6. Romans 11:34 / Isaiah 40:13
> 7. Romans 15:12 / Isaiah 11:10
> 8. 1 Corinthians 1:19 / Isaiah 29:14
> 9. 1 Corinthians 6:16 / Genesis 2:24
> 10. 1 Corinthians 9:9 / Deuteronomy 25:4
> 11. 1 Corinthians 10:7 / Exodus 32:6
> 12. Galatians 3:13 / Deuteronomy 21:23
>
> Return a table with: B001 ID, discussed YES/NO, page/locator, depth (passing/substantive/extended), and a one-sentence description of what the author addresses. Do not infer relevance from the book's topic alone. If the passage is not actually discussed, write NOT DISCUSSED.

Save to `relevance_scan.md`.

---

## Prompt 2 — Evidence extraction

> Work only from this source. For every B001 item marked substantive or extended, extract the author's actual position.
>
> For each distinct claim provide:
> - proposed evidence ID: <SOURCE_ID>-E###;
> - B001 passage ID;
> - the author's claim in neutral language;
> - one short exact quotation that directly supports the claim, preferably <=25 words;
> - printed page number if visible, otherwise the best source locator;
> - your NotebookLM citation;
> - textual evidence the author invokes;
> - whether the author is making a textual-critical, exegetical, literary, historical, or methodological claim;
> - qualifications or conditions stated by the author;
> - extraction confidence HIGH/MEDIUM/LOW.
>
> Do not merge separate claims. Do not silently supply premises that the author does not state. If you cannot find direct support, omit the claim.

Save prose to `extraction.md` and normalize rows into `citation_ledger.csv`.

Recommended CSV fields:

```csv
evidence_id,source_id,b001_id,claim_type,author_claim,short_quote,printed_page,source_locator,notebooklm_citation,verification_status,qualification,extraction_confidence,notes
```

Set `verification_status=UNVERIFIED` initially.

---

## Prompt 3 — Argument map

> Work only from this source. For each substantive B001 discussion, map the author's reasoning as:
>
> QUESTION -> EVIDENCE -> INFERENCE -> CONCLUSION
>
> Then list:
> - assumptions the author explicitly acknowledges;
> - alternative explanations the author considers;
> - alternative explanations the author does not address but that are visible from the author's own presentation;
> - what evidence would weaken or falsify the author's conclusion, if the source states this.
>
> Distinguish what the source explicitly says from your structural paraphrase.

Save to `argument_map.md`.

---

## Prompt 4 — Counterevidence and disagreements

> Work only from this source. Extract every place where the author:
> - expresses uncertainty;
> - discusses a competing textual form;
> - notes a Hebrew/Greek ambiguity;
> - allows authorial adaptation, oral transmission, liturgical transmission, or an unknown textual form;
> - disagrees with another scholar;
> - acknowledges evidence that weakens the preferred interpretation.
>
> Give page/locator and citation for each item. If none are present for a B001 passage, write NONE FOUND IN THIS SOURCE, not NONE EXISTS.

Save to `counterevidence.md`.

---

## Prompt 5 — Bibliography leads

> Work only from this source. For each substantive B001 discussion, list the sources in footnotes/bibliography that the author relies on or disputes and that look directly relevant to the textual problem. Give the cited author, title or abbreviated title, year if visible, pages if visible, and why it matters. Do not invent full bibliographic details that are not visible.

Save to `bibliography_leads.md`.

---

## Prompt 6 — NotebookLM self-audit

> Audit your own extraction against this source only.
>
> Check:
> 1. Did you attribute any claim to the author without direct source support?
> 2. Did any quotation omit nearby words that materially change its meaning?
> 3. Did you infer a printed page number rather than observe it?
> 4. Did you convert an author's possibility into a probability or certainty?
> 5. Did you confuse the author's description of another scholar with the author's own view?
> 6. Did you miss a qualification, objection, textual variant, or counterexample near any extracted passage?
> 7. Did you rely on general model knowledge?
>
> Return CORRECTIONS REQUIRED or NO CORRECTIONS FOUND, followed by itemized corrections with citations.

Save to `notebooklm_self_audit.md`.

---

# Human/agent citation verification pass

NotebookLM's generated answer is navigation, not evidence.

After the prompts, Antigravity must click/reopen each citation and update `citation_ledger.csv`:

- `VERIFIED` — citation visibly supports the row;
- `UNCERTAIN` — partial/ambiguous support;
- `REJECTED` — citation does not support the row;
- `LOCATOR_UNVERIFIED` — text support is visible but printed page could not be established.

Only `VERIFIED` rows enter accepted synthesis.

