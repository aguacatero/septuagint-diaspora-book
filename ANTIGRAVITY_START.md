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


## Required definition of DONE

**README reconciliation is part of the work, not an optional follow-up.** At the end of every interactive or scheduled task (including no-change polling), read `AGENTS.md` and check the README against the live state, queue, and latest independent review. After any source/state change run:

```bash
python3 scripts/sync_readme_checkpoint.py
python3 scripts/sync_readme_checkpoint.py --check
python3 scripts/update_progress.py --check
```

Commit and push README changes with the research state transition before declaring `DONE` or advancing the queue. Review-only/no-change polls still run the checks and explicitly state `README: CHECKED AND UNCHANGED` when true. If sync, review reconciliation, commit/push, or either check fails, task status is `BLOCKED`/`IN_PROGRESS`, **never `DONE`**; report the blocker. A source awaiting an independent review remains `AWAITING_REVIEW`, and draft source acceptance must not be recorded as an accepted milestone or merged to `main`.

## Background schedule

After the first successful interactive smoke test of the NotebookLM browser flow, create an Antigravity recurring task that resumes this workflow **hourly**.

Scheduled-run instruction:

```text
Open aguacatero/septuagint-diaspora-book on branch research/B001-notebooklm-serial. Read ANTIGRAVITY_START.md and resume B001 from research-queue/B001_NOTEBOOKLM_STATE.json. Work only on the single active source. If the source is awaiting independent ChatGPT review, check PR #2 comments through the chatgpt-relay review controller; apply required corrections when present or, after an accepted exact-SHA review, promote the source to SDP-01 Paul and advance to the next queue item. Stop at any login, source-access, citation-verification, owner-only, or review-pending gate. Never process two sources concurrently and never merge the PR. At the end of EVERY invocation, satisfy the Required definition of DONE in this file: sync/check the README and milestone graphic, commit/push necessary README changes before completing the task, or report BLOCKED/IN_PROGRESS. Include README: UPDATED or README: CHECKED AND UNCHANGED in the handoff.
```

Use Antigravity's `/schedule` capability (or the equivalent scheduled-task UI). Hourly is intentionally conservative; the workflow is state-driven, not speed-driven.


## Required human-readable status format

Every Antigravity pipeline report shown to the owner MUST begin with a Pacific-time timestamp and use this compact structure:

```text
### B001 Pipeline Check — YYYY-MM-DD HH:MM PT
Iteration: <N>
Source: <SOURCE_ID> — <short title>
Live HEAD: <full 40-character SHA>
State: <ACTIVE_PHASE>
Last review: <ACCEPT|REVISE|NONE> — <review timestamp if known>
Action taken: <one concise sentence>
Waiting on: <CHATGPT REVIEW|ANTIGRAVITY WORK|OWNER|NOTHING>
Owner action: <NONE or explicit action>
```

Use America/Los_Angeles local time. Include the date every time; never output only an iteration number or relative phrase such as "next hour."

For longer reports, put the timestamped status block first, then details below it. The owner must be able to understand current state from the first 8 lines alone.
