# START HERE — Antigravity B001 NotebookLM

This is the only file the owner needs to point Antigravity at.

**Durable agent requirement:** Read root [`AGENTS.md`](AGENTS.md) and check the `README.md` Research progress and Status sections at every run checkpoint. Record a material active source/review transition accurately while preserving the six-stage acceptance gate. Draft PR #2 must stay draft/unmerged; see `AGENTS.md` for the no-inflated-progress rule.

## First run: smoke test only

Copy/paste this into Antigravity with this repository open:

```text
Open aguacatero/septuagint-diaspora-book and checkout branch research/B001-notebooklm-serial.

Read START_HERE_ANTIGRAVITY.md, then read and obey ANTIGRAVITY_START.md, docs/workflow/NOTEBOOKLM_BROWSER_PREFLIGHT.md, and .agents/skills/notebooklm-serial-research/SKILL.md.

This is the FIRST RUN. Perform ONLY the NotebookLM smoke test described below. Do not start the full source queue and do not create the recurring schedule yet.

Use Google/Gemini models only. Use Antigravity's browser subagent to operate the normal NotebookLM UI. Do not use unofficial NotebookLM private APIs. Do not use Claude, Codex, paid OpenAI APIs, or chatgpt-relay/scripts/relay.sh run.

Before touching NotebookLM, run:

bash scripts/start_notebooklm_debug_chrome.sh

Verify:
curl -fsS http://127.0.0.1:9222/json/version

Then ensure the browser automation transport is connected to http://127.0.0.1:9222 as described in docs/workflow/NOTEBOOKLM_BROWSER_PREFLIGHT.md. Do not use the normal/default Chrome profile. If the dedicated research profile requires Google login, stop for the owner to sign in once and then resume.

Smoke-test source: the first queue item, P01F — SBLGNT.

Prove all of these before declaring PASS:
1. You can open/create SDP-B001-EXTRACT.
2. You can ensure it contains exactly one research source.
3. You can add P01F and verify the visible source identity.
4. NotebookLM completes ingestion.
5. You can run Prompt 0 from docs/workflow/NOTEBOOKLM_EXTRACTION_PROMPTS.md.
6. You can capture the answer into a local/repo-safe draft artifact.
7. You can run a small relevance query and receive a NotebookLM citation.
8. You can click/reopen that citation and verify the cited source context.
9. You can identify whether a printed page or reliable locator is available.
10. You can return to the repo and record the test result without losing state.

Do NOT perform the full P01F extraction during the smoke test.

Write the result to research/inbox/B001-pauline-txt-pilot/SMOKE_TEST.md with:
- PASS or FAIL
- exact steps completed
- browser/NotebookLM blockers
- citation behavior observed
- whether printed-page mapping worked
- screenshots/artifact locations if available
- recommended automation adjustments

Update research-queue/B001_NOTEBOOKLM_STATE.json:
- smoke_test_status = PASSED or FAILED
- active_phase = READY_FOR_HANDS_OFF only if every required step passed
- hands_off_enabled must remain false

Commit and push the smoke-test result to PR #2, then STOP.

Report the exact commit SHA and say:
READY FOR CHATGPT SMOKE-TEST REVIEW
```

## After ChatGPT approves the smoke test

Do not enable the hands-off loop until ChatGPT has reviewed the smoke-test commit.

After approval, the owner can paste:

```text
Resume aguacatero/septuagint-diaspora-book PR #2 on branch research/B001-notebooklm-serial.

Read START_HERE_ANTIGRAVITY.md, ANTIGRAVITY_START.md, and the NotebookLM serial-research skill.

The NotebookLM smoke test has passed independent ChatGPT review. Set hands_off_enabled=true and begin the serial B001 queue.

Process exactly one source at a time:
acquire -> single-source NotebookLM extraction -> citation verification -> GitHub source packet -> exact-SHA ChatGPT review -> corrections if required -> accepted promotion to SDP-01 Paul -> next source.

Create the hourly Antigravity resume schedule specified in ANTIGRAVITY_START.md only after confirming the smoke-test approval is present in PR #2.

Never process two sources concurrently. Never auto-merge PR #2. Stop only at an explicit access/login/owner decision blocker.
```

## Governing files

- `ANTIGRAVITY_START.md`
- `.agents/skills/notebooklm-serial-research/SKILL.md`
- `docs/workflow/NOTEBOOKLM_BROWSER_PREFLIGHT.md`
- `docs/workflow/NOTEBOOKLM_ANTIGRAVITY_SERIAL.md`
- `docs/workflow/NOTEBOOKLM_EXTRACTION_PROMPTS.md`
- `research-queue/B001_NOTEBOOKLM_SOURCE_QUEUE.csv`
- `research-queue/B001_NOTEBOOKLM_STATE.json`
- `research-queue/B001_CHATGPT_REVIEW_REQUEST.md`

## Safety gate

The hands-off loop is intentionally disabled until the one-time NotebookLM browser/citation smoke test passes independent review.
