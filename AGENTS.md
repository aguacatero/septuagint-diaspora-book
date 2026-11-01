# Agent instructions — Shaped by the Septuagint

These rules apply to every contributor and AI research/review agent. **Gemini in Antigravity, NotebookLM, GitHub, and independent ChatGPT review** are the current B001 workflow; Hermes/OpenRouter and Open Notebook are retired from active work.

## Authority and entrypoints

1. Read [the Project Constitution](docs/design/PROJECT_CONSTITUTION.md) and [research workflow](docs/workflow/RESEARCH_WORKFLOW.md). They govern evidence and promotion; do not silently change them.
2. Read [the current batch contract](research-queue/CURRENT_BATCH.md), then get the **live** [B001 draft PR #2](https://github.com/aguacatero/septuagint-diaspora-book/pull/2) HEAD and its state, queue and start-here documents. Operational state on the B001 branch is newer than historical instructions on `main`.
3. Consult `research/registry/SCHEMA.md`, the relevant module controls, [the backlog](research-queue/BACKLOG.md), and the README.
4. Work on an appropriate research or documentation branch, not directly in the accepted evidence registry. **PR #2 remains draft / unmerged; no automatic merge.** The owner may authorize separate documentation PR merges without authorizing research promotion.

## Source fidelity and review discipline

- A primary textual packet requires actual primary text and variant/apparatus verification, not merely commentary about a passage.
- A secondary scholarship packet requires accurate claims, qualifications, opposing scholarship, bibliographic provenance, and precise locators.
- NotebookLM is a source-navigation/extraction tool, **not canonical memory or proof**; the verified packet and review history live in GitHub.
- A draft, model summary, or compelling hypothesis is not an accepted finding. Record uncertainties, negative evidence, access gaps, and competing explanations.
- Research agents prepare one source at a time; independent ChatGPT reviews the **live exact commit SHA** and records `ACCEPT` or `REVISE`. Only independently accepted packets enter the cumulative `SDP-01 Paul` research notebook.
- Research branches must not modify `research/registry/master_registry.csv`, `research/registry/allusions_registry.csv`, `research/registry/corrections_log.md`, or the Project Constitution without an explicit reviewed promotion.

## Mandatory public-progress check

At the end of **every task**, compare README's **Research progress** section with:

- `research-queue/CURRENT_BATCH.md` on `main`;
- the active branch's `B001_NOTEBOOKLM_STATE.json` and source queue;
- the latest **independent exact-SHA review** on live PR #2.

Keep these distinctions explicit: source packet accepted on a draft branch; source promoted to cumulative NotebookLM synthesis; evidence accepted on `main`; and an entire six-stage milestone accepted. **A draft source acceptance is not a completed TXT gate.**

The six roadmap checkboxes in README are authoritative for progress visualization. Change a checkbox from `[ ]` to `[x]` **only when a complete milestone passes its gate and is promoted into `main`**. Before and after any progress edit:

1. Run `python3 scripts/update_progress.py` only when milestone/batch state really changes.
2. Run `python3 scripts/update_progress.py --check` and keep `assets/progress.svg` synchronized.
3. Never edit the SVG manually, invent percentages, or count proposed research as accepted.
4. Keep verified material draft progress dated and visibly labeled **DRAFT / UNMERGED**. Do not erase accepted source-packet milestones when refreshing the README.

A long-lived draft branch may contain older README or instruction files: reconcile them with current `main` before any eventual approved merge. Do not merge live research merely to synchronize documentation.

## End-of-task handoff

Report: changed files / commits / PR links; active batch, source, review status, blockers; whether the README was **updated** or **checked and unchanged**; and whether `update_progress.py --check` passed. If tools were unavailable, record that instead of claiming verification.

## Historical tool documentation

The former Hermes/OpenRouter and Open Notebook workflows are preserved in [legacy workflow archives](docs/archive/legacy-workflows/README.md). Their root-level historical entrypoint files are redirects, not executable instructions. The actual B001 operational entrypoints are `START_HERE_ANTIGRAVITY.md` and `CHATGPT_START_HERE.md` **on the active PR #2 branch**.
