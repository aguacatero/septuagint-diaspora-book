# Current Research Batch

**Active batch:** `B001-pauline-txt-pilot`

**Active automation branch:** `research/B001-notebooklm-serial`

**Primary orchestrator:** Antigravity / Gemini

**NotebookLM staging notebook:** `SDP-B001-EXTRACT`

**NotebookLM cumulative notebook:** `SDP-01 Paul`

**Module:** TXT

**Goal:** Test the research volley on a bounded set of Pauline quotations before scaling to the complete undisputed-Paul quotation census.

## Active workflow

Read and execute, in order:

1. `ANTIGRAVITY_START.md`
2. `.agents/skills/notebooklm-serial-research/SKILL.md`
3. `research-queue/B001-pauline-txt-pilot.md`
4. `docs/workflow/NOTEBOOKLM_ANTIGRAVITY_SERIAL.md`
5. `docs/workflow/NOTEBOOKLM_EXTRACTION_PROMPTS.md`
6. `research-queue/B001_NOTEBOOKLM_SOURCE_QUEUE.csv`
7. `research-queue/B001_NOTEBOOKLM_STATE.json`

## Execution rule

Process **one source at a time**.

For each source:

`acquire -> NotebookLM single-source extraction -> citation verification -> GitHub commit -> independent ChatGPT exact-SHA review -> accepted promotion to SDP-01 Paul -> next source`

Do not begin the next source while the current source is awaiting review or revision.

## ChatGPT review transport

Use the reusable review controller from `aguacatero/chatgpt-relay`:

`scripts/review_loop.py`

Do not run the legacy Claude/Haiku browser worker (`scripts/relay.sh run`) from this Gemini-only research lane.

The current source review request lives at:

`research-queue/B001_CHATGPT_REVIEW_REQUEST.md`

## Legacy Open Notebook workflow

`docs/workflow/B001_OPEN_NOTEBOOK_MANUAL.md` is retained as historical/fallback documentation, but it is **not the active ingestion workflow** while this branch is in use.

Open Notebook extraction artifacts must not be mixed into the NotebookLM serial lane unless explicitly migrated and re-verified.

## Batch boundary

Do not begin later backlog work until Batch B001 has been reviewed and the workflow has been adjusted if necessary.
