# Antigravity Start — B001 NotebookLM Serial Research

Read and obey:

1. `.agents/skills/notebooklm-serial-research/SKILL.md`
2. `docs/workflow/NOTEBOOKLM_BROWSER_PREFLIGHT.md`
3. `research-queue/CURRENT_BATCH.md`
4. `docs/workflow/NOTEBOOKLM_ANTIGRAVITY_SERIAL.md`
5. `docs/workflow/NOTEBOOKLM_EXTRACTION_PROMPTS.md`
6. `research-queue/B001_NOTEBOOKLM_SOURCE_QUEUE.csv`
7. `research-queue/B001_NOTEBOOKLM_STATE.json`

Goal: process the B001 corpus **one source at a time**, using NotebookLM for source-bounded extraction, verifying citations, committing the source packet to GitHub, and stopping at the independent ChatGPT review gate before advancing.

Before any NotebookLM browser work, run `bash scripts/start_notebooklm_debug_chrome.sh` and require `curl -fsS http://127.0.0.1:9222/json/version` to succeed. The automation browser must use the dedicated research Chrome profile/endpoint defined in `NOTEBOOKLM_BROWSER_PREFLIGHT.md`, not the owner's normal Chrome profile.

Use Google/Gemini models for Antigravity orchestration. Use the `aguacatero/chatgpt-relay` reusable review controller for exact-SHA review handoff. Do not use the legacy Claude/Haiku relay worker.

Do not begin the next source until the current source packet is independently accepted.


## Background schedule

After the first successful interactive smoke test of the NotebookLM browser flow, create an Antigravity recurring task that resumes this workflow **hourly**.

Scheduled-run instruction:

```text
Open aguacatero/septuagint-diaspora-book on branch research/B001-notebooklm-serial. Read ANTIGRAVITY_START.md and resume B001 from research-queue/B001_NOTEBOOKLM_STATE.json. Work only on the single active source. If the source is awaiting independent ChatGPT review, check PR #2 comments through the chatgpt-relay review controller; apply required corrections when present or, after an accepted exact-SHA review, promote the source to SDP-01 Paul and advance to the next queue item. Stop at any login, source-access, citation-verification, owner-only, or review-pending gate. Never process two sources concurrently and never merge the PR.
```

Use Antigravity's `/schedule` capability (or the equivalent scheduled-task UI). Hourly is intentionally conservative; the workflow is state-driven, not speed-driven.
