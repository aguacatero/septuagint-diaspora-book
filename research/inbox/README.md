# Research Inbox

This directory is the staging area for machine-assisted research packets.

Nothing under `research/inbox/` is canonical merely because it is committed.

Each batch must live under its own directory:

`research/inbox/<batch-id>-<short-name>/`

Required batch contents:

- `README.md` — batch summary and completion status
- `source_manifest.csv` — every source actually used
- `candidate_registry.csv` — provisional registry rows matching `research/registry/SCHEMA.md`
- `passages/` — one evidence report per assigned passage/case
- `adversarial_review.md` — strongest challenges to provisional findings
- `unresolved_questions.md` — blocked items, missing sources, unresolved conflicts
- `run_log.md` — tools/models used and major methodological choices

The reviewer decides what, if anything, is promoted from the inbox into the authoritative registry.
