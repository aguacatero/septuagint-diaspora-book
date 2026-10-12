---
name: notebooklm-serial-research
description: Run B001 as a restartable one-source-at-a-time NotebookLM research pipeline with Antigravity/Gemini orchestration, GitHub as canonical ledger, and independent ChatGPT exact-SHA review through chatgpt-relay.
---

# NotebookLM Serial Research Loop

## Purpose

Automate source -> extraction -> citation verification -> GitHub commit -> independent ChatGPT review -> cumulative synthesis, one source at a time.

This skill governs the active B001 research lane. It does not change the Project Constitution or TXT methodology.

## Non-negotiable rules

1. **One source at a time.** Never process a second source until the current source has passed the independent review gate.
2. **Two NotebookLM notebooks.**
   - `SDP-B001-EXTRACT`: temporary staging notebook. It MUST contain exactly one active research source during extraction.
   - `SDP-01 Paul`: cumulative synthesis notebook. Add a source here only after its extraction is accepted.
3. **GitHub is canonical.** NotebookLM chat, notes, reports, browser state, and local scratch files are disposable. Durable research belongs in this repository.
4. **Gemini-only orchestration.** Antigravity and its subagents use Google/Gemini models. Do not invoke Claude, Codex, paid OpenAI API, or `scripts/relay.sh run`.
5. **ChatGPT is the independent reviewer.** Reuse `aguacatero/chatgpt-relay/scripts/review_loop.py` as the exact-SHA review controller. Do not manufacture ChatGPT replies or let Gemini approve its own work.
6. **No unofficial NotebookLM private APIs.** Use Antigravity's browser subagent (or BrowserMCP when needed) against the normal NotebookLM UI. If browser automation cannot verify state, fail closed and record the blocker.
7. **Source-bounded extraction.** During extraction, ask only about the one source loaded in `SDP-B001-EXTRACT`. Do not synthesize claims from model memory or other sources.
8. **Citation provenance is mandatory.** Every substantive author claim and every direct quotation must retain a locator. If NotebookLM cannot expose a printed page or reliable source location, mark `LOCATOR_UNVERIFIED`.
9. **Primary-text claims are separate from secondary-author claims.** Do not turn a secondary author's assertion into a primary-text fact.
10. **No premature book prose.** Produce evidence records and argument maps first. Final prose comes after passage-level synthesis and review.

## State machine

Each queue item moves only through:

`PENDING -> ACQUIRED -> LOADED -> EXTRACTED -> CITATIONS_VERIFIED -> COMMITTED -> CHATGPT_REVIEW -> ACCEPTED -> SYNTHESIS_ADDED -> DONE`

A review finding returns the source to:

`REVISE -> EXTRACTED/CITATIONS_VERIFIED -> COMMITTED -> CHATGPT_REVIEW`

Never skip a state.

## Startup

1. Read:
   - `docs/design/PROJECT_CONSTITUTION.md`
   - `research-queue/CURRENT_BATCH.md`
   - `research-queue/B001_NOTEBOOKLM_SOURCE_QUEUE.csv`
   - `research-queue/B001_NOTEBOOKLM_STATE.json`
   - `docs/workflow/NOTEBOOKLM_ANTIGRAVITY_SERIAL.md`
   - `docs/workflow/NOTEBOOKLM_EXTRACTION_PROMPTS.md`
2. Confirm working branch is `research/B001-notebooklm-serial` or a descendant feature branch.
3. Confirm the active PR is DRAFT.
4. Resolve `CHATGPT_RELAY_ROOT` to a local clone of `aguacatero/chatgpt-relay`.
5. Confirm `gh auth status`, Python 3.11+, Chrome login to NotebookLM, and Antigravity browser control.
6. Resume the exact state in `B001_NOTEBOOKLM_STATE.json`; do not restart completed sources.

## Per-source execution

### Phase A — Select and acquire

- Select the lowest-order queue item with `status=PENDING`, unless state names an active source.
- Verify author/editor, title, year/edition, and lawful access.
- Prefer free/OA sources. Paid sources may remain bibliography references but are not required acquisition gates unless the owner explicitly changes policy.
- Record acquisition details and limitations.

### Phase B — Prepare the extraction notebook

Using Antigravity browser automation:

1. Open NotebookLM.
2. Open/create `SDP-B001-EXTRACT`.
3. Remove all previous research sources from that notebook.
4. Add only the current source.
5. Wait until ingestion is complete.
6. Verify the visible source title matches the queue item.
7. Confirm there is exactly one active research source before querying.
8. Run a known-phrase retrieval check when possible.

If any of these checks fail, stop and record the blocker. Do not query a mixed notebook.

### Phase C — Run deterministic extraction

Run the prompt sequence in `NOTEBOOKLM_EXTRACTION_PROMPTS.md` in order.

Write durable outputs under:

`research/inbox/B001-pauline-txt-pilot/sources/<SOURCE_ID>/`

Required files:

- `metadata.md`
- `relevance_scan.md`
- `extraction.md`
- `citation_ledger.csv`
- `argument_map.md`
- `counterevidence.md`
- `bibliography_leads.md`
- `notebooklm_self_audit.md`

Do not paste an entire copyrighted source into GitHub. Store only necessary short quotations and research notes.

### Phase D — Verify citations

For every row in `citation_ledger.csv`:

- reopen/click the NotebookLM citation;
- verify the cited text supports the recorded claim;
- capture printed page when visible;
- otherwise capture the best stable locator and mark page status;
- for Greek/Hebrew/apparatus claims, inspect the source image/text rather than trusting OCR alone;
- mark unsupported or ambiguous items as `REJECTED` or `UNCERTAIN`.

Do not allow a claim with `verification_status=UNVERIFIED` into the accepted evidence set.

### Phase E — Commit one source

Update:

- queue status for the current source;
- `B001_NOTEBOOKLM_STATE.json`;
- the source folder;
- `research/inbox/B001-pauline-txt-pilot/source_manifest.csv` when present;
- `research/inbox/B001-pauline-txt-pilot/acquisition_manifest.csv` when present;
- `research-queue/B001_CHATGPT_REVIEW_REQUEST.md`.

Commit only after the source packet is internally complete.

Commit message:

`B001 <SOURCE_ID>: NotebookLM extraction ready for review`

Record the resulting full SHA in the review request.

### Phase F — Independent ChatGPT review via chatgpt-relay controller

Do NOT use the legacy relay browser worker.

From `$CHATGPT_RELAY_ROOT`:

```bash
python3 scripts/review_loop.py start --repo aguacatero/septuagint-diaspora-book --pr <PR>
python3 scripts/review_loop.py tick --repo aguacatero/septuagint-diaspora-book --pr <PR>
python3 scripts/review_loop.py check-comments --repo aguacatero/septuagint-diaspora-book --pr <PR>
```

The independent reviewer must review the exact live HEAD SHA and the current `B001_CHATGPT_REVIEW_REQUEST.md`.

Required review questions:

- Are claims faithful to the source rather than stronger than it?
- Do cited snippets/locators support each evidence row?
- Did NotebookLM omit important qualifications or counterarguments?
- Are author claims distinguished from primary-text facts?
- Are quotations/context sufficient and not cherry-picked?
- Are unsupported claims, citation mismatches, or hallucinated pages present?
- Is this source packet safe to admit into cumulative synthesis?

A request-changes verdict returns to Phase C/D. An accepted review advances to Phase G.

### Phase G — Promote into cumulative synthesis

Only after independent acceptance:

1. Add the source to `SDP-01 Paul`.
2. Do not delete the source packet from GitHub.
3. Mark queue item `DONE` and set review metadata in state.
4. Advance to the next `PENDING` source.
5. Commit the state transition together with the next source's eventual extraction, or as a small checkpoint if needed.

## Browser failure handling

NotebookLM UI automation is inherently less stable than an API. On missing selectors, login prompts, CAPTCHAs, unexpected source counts, or citation panels that cannot be verified:

- stop;
- take an Antigravity artifact/screenshot;
- write the blocker to `run_log.md`;
- leave the current state unchanged;
- retry later from the same state.

Never guess what the UI did.

## Completion gate

B001 source extraction is complete only when every queue item is either:

- `DONE`, or
- explicitly `BLOCKED` with a documented source/access limitation.

Only then begin passage-level cross-source synthesis.

