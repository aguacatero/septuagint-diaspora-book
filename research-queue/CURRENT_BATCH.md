# Current Research Batch — B001 Pauline textual pilot

**Active batch:** `B001-pauline-txt-pilot`  
**Module:** `TXT` — textual comparison  
**Canonical research objective:** Test twelve selected Pauline quotations against Greek and Hebrew textual traditions before expanding to a full quotation census. This pilot does **not** pre-judge authorship or chronology of Paul's letters.  
**Active execution branch:** `research/B001-notebooklm-serial` ([draft PR #2](https://github.com/aguacatero/septuagint-diaspora-book/pull/2)) — **DRAFT / UNMERGED**.

## Current tools and division of labor

- **Antigravity/Gemini:** serial source acquisition, NotebookLM browser operation, source packet preparation and remediation.
- **NotebookLM:** exactly one active source in `SDP-B001-EXTRACT` for extraction; promote independently accepted sources to cumulative `SDP-01 Paul`.
- **GitHub:** durable source packets, citations, state, source queue and immutable exact-SHA review comments.
- **ChatGPT:** independent source packet review through the existing review-loop controller. Only reviewed `ACCEPT` permits the next source to be promoted; `REVISE` requires remediation.

Read the live branch's `START_HERE_ANTIGRAVITY.md`, `CHATGPT_START_HERE.md`, `docs/workflow/NOTEBOOKLM_ANTIGRAVITY_SERIAL.md`, `research-queue/B001_NOTEBOOKLM_STATE.json`, and `research-queue/B001_NOTEBOOKLM_SOURCE_QUEUE.csv` **at current PR HEAD**. Do not trust dated examples or copy an old SHA.

## Research boundary

The assigned twelve passages remain defined in [the B001 contract](B001-pauline-txt-pilot.md). The active PR #2 source queue has sixteen source packets; this **does not** alter the twelve-passage corpus.

**Latest README checkpoint (November 1, 2026):** seven of sixteen source packets had independent source-level acceptance, S05 (Florian Wilk) was next for acquisition. This is a dated snapshot, **not live status**: check PR #2 before reporting anything newer.

**Main roadmap:** Foundation accepted; TXT active; NAR, CUL, HIS and Book pending (1 of 6 accepted). Neither acceptance of an individual source nor its promotion to `SDP-01 Paul` means B001 or TXT is complete.

Do not begin later batches before B001's documented review gates. **Never auto-merge PR #2.** The [new Gospel-origins proposals](proposals/2026-11-01-gospel-origins-mark-mazdean-post70.md) are future work, not added B001 sources.

## Historical references

`docs/workflow/B001_OPEN_NOTEBOOK_MANUAL.md`, `HERMES_START.md` and `docs/workflow/HERMES_INSTRUCTIONS.md` now redirect to archives. They are **not** the running procedure.
