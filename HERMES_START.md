# Hermes — Start Here

You are the research worker for *Shaped by the Septuagint*.

GitHub `main` is the source of truth. Do not rely on prior session memory when repo instructions are available.

## Do this now

1. Pull the latest `main`.
2. Read `docs/design/PROJECT_CONSTITUTION.md`.
3. Read `docs/workflow/RESEARCH_WORKFLOW.md`.
4. Read `docs/workflow/SOURCE_ACQUISITION.md`.
5. Read `docs/workflow/HERMES_INSTRUCTIONS.md`.
6. Read `research/registry/SCHEMA.md`.
7. Read `research-queue/CURRENT_BATCH.md` and the batch file it names.
8. If the active batch names a batch-specific manual (currently `docs/workflow/B001_OPEN_NOTEBOOK_MANUAL.md`), read and follow it.
9. Create the branch required by the batch contract.
10. Unless the batch says the corpus is already complete, perform Phase 0 source acquisition: locate lawful full-text sources, import usable copies into Open Notebook, verify ingestion, and document gaps.
11. Perform the research using Open Notebook as the source warehouse and OpenRouter models as research assistants.
12. If autonomous Open Notebook operation is unreliable, do not stall or improvise around the batch contract. Use the batch-approved manual workflow: consume the user's manually produced Open Notebook extraction files, preserve their underlying source/page traceability, and continue the analysis from those files.
13. Put all results in the batch's `research/inbox/` directory.
14. Commit the research branch and report the branch name + commit SHA for review.

## Current task

The active task is defined only by `research-queue/CURRENT_BATCH.md`.

Do **not** modify canonical registry files, rewrite the thesis, skip ahead to later batches, or merge your own work into `main`.

Your job is to return an auditable research packet that can survive adversarial review, including evidence that weakens the working hypothesis.
