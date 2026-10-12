# NotebookLM + Antigravity Serial Research Pipeline

## Decision

B001 moves from Open Notebook to NotebookLM for source-grounded extraction.

The project keeps the same scholarly method and GitHub evidence architecture. Only the ingestion/extraction layer changes.

## Architecture

```text
FREE/OA SOURCE
     |
     v
Antigravity source acquisition
     |
     v
SDP-B001-EXTRACT (NotebookLM)
[EXACTLY ONE SOURCE]
     |
     v
structured extraction + citation verification
     |
     v
GitHub source packet
     |
     v
exact-SHA ChatGPT review
(chatgpt-relay review controller)
     |
  +--+--+
  |     |
REVISE ACCEPT
  |     |
  +<----+----> SDP-01 Paul cumulative notebook
                   |
                   v
            next source in queue
```

## Why two NotebookLM notebooks

A single large notebook is convenient for synthesis but risky for deterministic source extraction. It allows accidental cross-source answers and makes automated citation checking harder.

Use:

### 1. `SDP-B001-EXTRACT`

A disposable staging notebook containing exactly one current source.

Purpose:
- source-specific extraction;
- exact author-position capture;
- citation verification;
- bibliography mining;
- no cross-source synthesis.

### 2. `SDP-01 Paul`

The cumulative research notebook.

A source is added only after its extraction packet passes independent review.

Purpose:
- later passage-level comparison;
- cross-source agreement/disagreement mapping;
- synthesis after the serial extraction phase.

## Why Antigravity can drive this

Antigravity 2.0/IDE provides a browser subagent capable of Chrome/DOM interaction and scheduled/background tasks. That is the preferred transport for the normal NotebookLM UI.

If using Antigravity CLI instead, BrowserMCP/Playwright can provide browser control, but the built-in browser subagent is preferred when available.

## Why not use an unofficial NotebookLM client

Consumer NotebookLM does not provide a stable, supported public automation API for this workflow. Reverse-engineered private RPC clients exist, but they are brittle and can change without notice.

For this project:
- consumer NotebookLM -> browser automation;
- optional future Gemini Notebook Enterprise -> supported Cloud API;
- no private/undocumented consumer RPC dependency in the canonical pipeline.

## Canonical durability

NotebookLM is not the database.

The durable record is:

```text
research/inbox/B001-pauline-txt-pilot/
  sources/
    <SOURCE_ID>/
      metadata.md
      relevance_scan.md
      extraction.md
      citation_ledger.csv
      argument_map.md
      counterevidence.md
      bibliography_leads.md
      notebooklm_self_audit.md
```

Every significant claim should be reconstructable without the original NotebookLM chat history.

## Serial execution rule

At most one source may be in `EXTRACTED`, `CITATIONS_VERIFIED`, `COMMITTED`, or `CHATGPT_REVIEW` state at a time.

The next source cannot begin until the previous source is accepted or explicitly blocked.

This is intentionally slower than parallel fan-out. The benefit is:
- clean provenance;
- simpler recovery after failure;
- less source contamination;
- exact per-source review;
- auditable Git history.

## ChatGPT Relay role

Use `aguacatero/chatgpt-relay` as the **review control plane**, not as the NotebookLM driver.

The existing `scripts/review_loop.py` already provides:
- exact-SHA review binding;
- stale-review rejection;
- restartable checkpoints;
- PR comment discovery;
- deduplication;
- fail-closed behavior.

Do not run the legacy `scripts/relay.sh run` from this pipeline because that path uses the older Claude/Haiku browser worker.

The desired division is:

```text
Antigravity/Gemini -> NotebookLM + repo implementation
ChatGPT            -> independent review
chatgpt-relay      -> exact-SHA handoff/checkpoint protocol
GitHub             -> shared canonical medium
```

## Review request contract

Before each independent review, Antigravity rewrites:

`research-queue/B001_CHATGPT_REVIEW_REQUEST.md`

It must contain:
- source ID and exact citation;
- current branch and PR;
- full 40-character HEAD SHA;
- paths changed for this source;
- exact review scope;
- source URL/identifier when public;
- extraction limitations;
- required verdict format.

ChatGPT should review only the named source packet plus governing methodology unless it finds a cross-cutting problem.

## Per-source output philosophy

NotebookLM should produce **evidence atoms**, not finished book prose.

Each atom needs:
- evidence ID;
- source ID;
- claim stated by the author;
- short supporting quotation when needed;
- page/locator;
- NotebookLM citation verification status;
- passage relevance;
- qualification/counterargument;
- confidence in extraction, not confidence in the historical thesis.

Later synthesis may combine accepted atoms.

## Schedule strategy

Antigravity may run this as a scheduled/background task, but the state file is authoritative.

Each scheduled invocation should:

1. inspect current state;
2. do work only on the active source;
3. stop when it reaches an external gate:
   - source access problem;
   - NotebookLM login/browser problem;
   - independent review pending;
   - owner-only decision;
4. never spin in a polling loop.

A later invocation resumes from state.

## Future API upgrade

Gemini Notebook Enterprise now exposes supported notebook/source APIs and its service includes source-interaction/query operations. If the owner later chooses Enterprise, replace only the browser adapter; keep the queue, extraction schema, GitHub packets, and review gate unchanged.

