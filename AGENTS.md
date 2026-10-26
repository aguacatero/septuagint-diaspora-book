# Agent instructions — Shaped by the Septuagint

These instructions apply to **every AI assistant or human contributor** working in this repository, including ChatGPT, Hermes, OpenRouter agents, Claude, Gemini, Codex, and other agents. This file is a durable **note to future ChatGPT sessions**; do not rely on chat memory alone.

## Before any work

1. Read `docs/design/PROJECT_CONSTITUTION.md`, `docs/workflow/RESEARCH_WORKFLOW.md`, and `research-queue/CURRENT_BATCH.md`.
2. Inspect the public status in `README.md` (the **Research progress** section), the [backlog](research-queue/BACKLOG.md), and the source-of-truth state on `main`.
3. Respect the staged-research / reviewed-promotion boundary. Do not let a polished draft, generated summary, or unreviewed branch masquerade as accepted evidence.

## Mandatory public-progress maintenance

**Every agent must check the README at the end of every task and update it whenever accepted project status has changed.** This is a required end-of-task step, not an optional cosmetic change.

- The six **Research progress** checkboxes in `README.md` are the source of truth for the *six-gate roadmap*. Keep all six present.
- Change a milestone's `[ ]` to `[x]` **only after the entire milestone has met its documented review gate and its results have been accepted into `main`**. Finishing one batch (e.g., B001) does **not** finish the entire TXT milestone. Do not count unreviewed candidates or use a speculative percentage.
- When a reviewed batch is promoted, update `README.md`'s **Current** label and any status wording to match `research-queue/CURRENT_BATCH.md`. Keep the backlog/current-batch file and README consistent, even if the number of accepted gates does not change.
- After editing milestones, run `python3 scripts/update_progress.py`. It regenerates the accepted/active/pending status tiles in `assets/progress.svg` from the milestone checkboxes and the active module in `research-queue/CURRENT_BATCH.md`. Commit **both** `README.md` and `assets/progress.svg` along with the relevant accepted status change.
- Before proposing, committing, or reporting a completed change, run `python3 scripts/update_progress.py --check`. Fix any out-of-sync files. The repository's progress CI also runs this check.
- Do **not** edit the SVG by hand or invent accepted gates. The generator ensures that accepted counts and current-module tiles agree with the canonical status files.

## Material draft progress is still reportable

**Never let `README.md`'s `## Research progress` or `## Status` lag behind a material, verified change in the active workflow—even when the change is inside a draft PR.** At the end of **every agent run**, compare those sections with `research-queue/CURRENT_BATCH.md`, the active branch's state/queue files, and the *latest exact-SHA independent review on the live PR*. Update the README in the same commit as a project-status change whenever feasible, or in an immediate documentation follow-up. Review-only or no-change runs must explicitly record that the README was checked and remains accurate.

- Report the active **batch, source ID, source-queue position and total, source-level accepted count, latest independent reviewer disposition and blockers, and a dated status/source link** when those facts materially change. Distinguish **live PR review verdict** from an **unconsumed/stale queue state**.
- Separate **source packet accepted on a draft research branch**, **promoted into a cumulative research notebook**, **accepted into `main`**, and **whole milestone gate accepted**. A draft source accepted by the reviewer is **not** an accepted TXT gate and never justifies checking a milestone box or changing `assets/progress.svg` to DONE.
- The README may summarize in-progress draft work, provided it clearly labels it **DRAFT / UNMERGED** and cites the branch or PR; it must never imply that provisional findings are canonical. If the branch HEAD changes, an earlier exact-SHA review does **not** automatically validate the new HEAD.
- **Review both README sections and the underlying six checkboxes**, not merely the SVG. `scripts/update_progress.py --check` checks milestone/SVG synchronization but cannot establish the accuracy or freshness of descriptive source/review status.
- Before a long-lived research branch is merged, reconcile its README and agent instructions with the current `main` versions so merging cannot silently restore older project status or drop the progress tracker. Do not merge autonomously.
- If a write is blocked, carry forward an explicit progress correction and the blocker in the handoff; do not assert that an uncommitted update was published.

## The research branch is not the public authority

- **Research agents such as Hermes** work on batch branches, generate candidate materials, and submit them for review. They **must not** mark a milestone complete or push progress changes to `main` without authorization.
- Research agents must include a **README progress assessment** in their end-of-run handoff: what was done, what remains unreviewed, whether the public `Currently underway` label should change after promotion, and whether any milestone gate is now satisfied.
- **The reviewer/promoter (human or LLM with permission)** is responsible for updating `main`'s README and SVG **in the same promotion cycle** as the accepted batch/status change.
- If you lack write access, provide an explicit README/progress handoff rather than claiming the public README was updated. Do not invent completion evidence.

## End-of-task report

State whether README progress was **updated** or **checked and unchanged**. If updated, name the new count and link the commit/PR. If waiting on review or permission, state the blocker. This step also applies to future ChatGPT sessions that open this repository directly.
