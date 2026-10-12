# ChatGPT Handoff — B001 NotebookLM Smoke Test

**Use this file to resume in a new ChatGPT session after Antigravity runs the one-time smoke test.**

## Repository state

- Repo: `aguacatero/septuagint-diaspora-book`
- Branch: `research/B001-notebooklm-serial`
- Draft PR: `#2`
- Antigravity entrypoint: `START_HERE_ANTIGRAVITY.md`
- Active workflow: NotebookLM serial extraction
- Review controller: `aguacatero/chatgpt-relay/scripts/review_loop.py`
- Legacy relay worker is forbidden for this lane.

## Why a smoke test is required

The scholarly workflow is deterministic, but consumer NotebookLM is being driven through a browser UI rather than a stable public automation API.

Before unattended operation, verify the real environment can reliably:

1. create/open the staging notebook;
2. enforce exactly one active source;
3. ingest the intended source;
4. submit deterministic prompts;
5. collect answer text;
6. expose a source-grounded citation;
7. reopen the citation;
8. verify the cited context;
9. capture a page or reliable locator;
10. return results to GitHub without corrupting state.

The test does not need to perform the full P01F extraction.

## What Antigravity should produce

Expected file:

`research/inbox/B001-pauline-txt-pilot/SMOKE_TEST.md`

Expected state fields:

```json
{
  "smoke_test_status": "PASSED|FAILED",
  "active_phase": "READY_FOR_HANDS_OFF|SMOKE_TEST_REQUIRED",
  "hands_off_enabled": false
}
```

Antigravity should commit/push the test and report:

`READY FOR CHATGPT SMOKE-TEST REVIEW`

with an exact full SHA.

## ChatGPT review task

When resuming:

1. Fetch live PR #2 and exact HEAD SHA.
2. Read `SMOKE_TEST.md` and the state file.
3. Inspect any screenshots/artifacts Antigravity made available.
4. Confirm the test actually demonstrated the ten browser/citation capabilities above.
5. Check that Antigravity did not silently use outside model knowledge as NotebookLM evidence.
6. Check that exactly one source was active.
7. Check that citation reopening was demonstrated, not merely that NotebookLM displayed a citation marker.
8. Check that state remains restartable and `hands_off_enabled=false`.
9. Review any automation adjustments Antigravity proposes.

### PASS

If the smoke test is genuinely sufficient:

- post an exact-SHA PR comment stating `SMOKE_TEST: ACCEPT`;
- authorize Antigravity to set `hands_off_enabled=true`;
- authorize creation of the hourly Antigravity resume schedule defined in `ANTIGRAVITY_START.md`;
- do not merge PR #2.

### FAIL

Post `SMOKE_TEST: REVISE` with exact corrections. Keep `hands_off_enabled=false`.

## Full-loop behavior after PASS

```text
one source
  -> NotebookLM single-source extraction
  -> citation verification
  -> GitHub commit
  -> ChatGPT exact-SHA source review
  -> fix/re-review as needed
  -> add accepted source to SDP-01 Paul
  -> next source
```

GitHub remains canonical. NotebookLM is an extraction/navigation layer, not the durable research record.

## User-facing next step

The user should only need to open Antigravity with the repository and paste the FIRST RUN prompt from `START_HERE_ANTIGRAVITY.md`.
