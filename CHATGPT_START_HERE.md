# CHATGPT START HERE — B001 Serial Research

This is the durable entrypoint for a **new ChatGPT session**.

The user should be able to paste only the URL to this file and say: **continue/review progress**.

## Live project

- Repo: `aguacatero/septuagint-diaspora-book`
- Active branch: `research/B001-notebooklm-serial`
- Draft PR: `#2`
- Antigravity entrypoint: `START_HERE_ANTIGRAVITY.md`
- ChatGPT review controller: `aguacatero/chatgpt-relay/scripts/review_loop.py`
- Never auto-merge PR #2.

## First actions in every new ChatGPT session

Do not trust a stale SHA written in a handoff.

1. Fetch live PR #2 and record the current full HEAD SHA.
2. Read:
   - `research-queue/B001_NOTEBOOKLM_STATE.json`
   - `research-queue/B001_NOTEBOOKLM_SOURCE_QUEUE.csv`
   - `research-queue/B001_CHATGPT_REVIEW_REQUEST.md`
   - `docs/design/PROJECT_CONSTITUTION.md`
   - `docs/workflow/NOTEBOOKLM_ANTIGRAVITY_SERIAL.md`
   - `docs/workflow/NOTEBOOKLM_EXTRACTION_PROMPTS.md`
3. Read the latest PR comments and check whether the **current live HEAD + active source** already has an independent ChatGPT review.
4. Then act according to state.

## State routing

### If `active_phase = AWAITING_REVIEW`

If the request says:
- a real non-TBD Source ID;
- `Review readiness: READY`;
- `Review target: LIVE_PR_HEAD`;

then independently review the named source packet at the **current live PR HEAD**.

The request file deliberately does not contain its own commit SHA. The reviewer resolves live HEAD at review time and writes:

`ISSUED_AT_PT: <YYYY-MM-DD HH:MM PT>`

`REVIEWED_SHA: <current full 40-character HEAD SHA>`

in the PR comment.

Check:
- source fidelity;
- citation/locator support;
- omissions and counterevidence;
- primary-text vs secondary-author distinctions;
- overstatement;
- page/locator fabrication;
- whether the packet follows the correct PRIMARY or SECONDARY extraction route;
- whether it is safe to promote into `SDP-01 Paul`.

Post `SOURCE_PACKET: ACCEPT` or `SOURCE_PACKET: REVISE` to PR #2. Every review comment must include `ISSUED_AT_PT` near the top so the owner can tell exactly when the verdict was issued. Do not edit Antigravity's research packet while acting as independent reviewer.

### If `active_phase` is extraction/work in progress

Report the current source and state. Do not fabricate completion. Antigravity owns NotebookLM/browser execution.

### If a source has an accepted exact-SHA review but has not advanced

Check whether Antigravity has consumed the review. If not, the next Antigravity run should promote the accepted source and advance.

### If the queue is complete

Review the passage-level cross-source synthesis against the Project Constitution before argumentative prose is produced.

## Governing division of labor

```text
Antigravity/Gemini -> NotebookLM browser execution + research packet creation
GitHub             -> canonical durable evidence ledger
ChatGPT            -> independent exact-live-SHA review
chatgpt-relay      -> review state/checkpoint control
```

NotebookLM is navigation/extraction, not canonical memory.

## Critical methodological rule

For `PRIMARY` queue items, the packet must extract the actual target text and apparatus into `primary_text_ledger.csv`. A primary critical edition must not be treated as if relevance requires prose "discussion."

For `SECONDARY` queue items, extract the scholar's claims, reasoning, qualifications, disagreements, and bibliography leads into the citation ledger and associated files.

## Current-batch boundary

Do not begin later research batches until B001 has passed the defined completion/review gates.


## Owner-facing progress format

When the user asks for status, lead with:

```text
STATUS AS OF: YYYY-MM-DD HH:MM PT
Source: <SOURCE_ID>
Live HEAD: <SHA>
State: <state>
Last independent review: <verdict + timestamp>
Waiting on: <who/what>
Owner action: <NONE or explicit action>
Progress: <accepted sources>/<total queue sources>
```

Then explain only meaningful blockers or recent changes.
