# Shaped by the Septuagint

## How Greek Scripture Shaped the Gospels—and What History Remains

This is a public-facing research and book project designed as a serious crossover work: readable by educated non-specialists while using a method intended to withstand specialist scrutiny.


## Research progress

![Six-stage research roadmap](assets/progress.svg)

**Current: B001 — Pauline TXT pilot underway (TXT gate not yet complete)** ([canonical batch contract](research-queue/CURRENT_BATCH.md); [active draft research PR #2](https://github.com/aguacatero/septuagint-diaspora-book/pull/2)). The research constitution, evidence framework, and controlled workflow are established. The pilot tests twelve Pauline quotation comparisons before the [complete TXT corpus](research-queue/BACKLOG.md); NAR, CUL, HIS, and manuscript development follow reviewed research.

**Draft-pipeline checkpoint — October 31, 2026 (not yet merged into `main`):** 6 of 16 queued source packets have **source-level independent acceptance** (P01F, P02F, P03F, S01F, S02F, S03F). The sixth, **S03F (Robertson & Plummer, 1 Corinthians ICC)**, was accepted in Round 5 independent review ([#issuecomment-6460107612](https://github.com/aguacatero/septuagint-diaspora-book/pull/2#issuecomment-6460107612)) and promoted to cumulative notebook `SDP-01 Paul`. The seventh, **S04F (J. B. Lightfoot, Galatians)**, has completed source acquisition, single-source extraction in NotebookLM, full-volume fail-closed negative search, and 14-row citation ledger verification, and is now submitted for **Round 1 independent review** on draft PR #2. **Neither PR #2 nor B001 is merged/completed, and no additional six-stage milestone is accepted.**

*The roadmap tracks independently accepted research-to-book gates, not a percentage of scholarship completed, manuscript pages written, or confidence in the hypothesis. Candidate work and unreviewed LLM output do not count as accepted.*

<details>
<summary>Milestone gates (1/6 accepted)</summary>

- [x] **Foundation** — establish the project constitution, evidence registry design, and research workflow.
- [ ] **TXT: Textual analysis** — finish the Pauline pilot, complete quotation census, and author-by-author synthesis.
- [ ] **NAR: Narrative analysis** — complete reviewed scriptural narrative-generation studies.
- [ ] **CUL: Cultural comparison** — complete controlled Hellenistic and Greco-Roman literary comparisons.
- [ ] **HIS: Historical audit** — complete the independent, claim-by-claim historical residue review.
- [ ] **Book** — write and review the evidence-grounded manuscript.

</details>

*Contributors and LLM agents: see [AGENTS.md](AGENTS.md) for review-gated status updates and the [progress generator](scripts/update_progress.py).*

---

## Current research question

The project tests whether the canonical Gospel authors' demonstrable scriptural practice is better explained primarily by **Greek Jewish scriptural traditions** than by direct consultation of Hebrew Scripture; how scriptural texts may have shaped or generated Gospel narrative details; how those narratives participate in the wider Hellenistic and Greco-Roman literary environment; and what historical evidence remains after those literary processes are accounted for.

The conclusion is **not predetermined**. The method must be able to produce results contrary to the initiating hypothesis.


## Start here

1. [`docs/design/PROJECT_CONSTITUTION.md`](docs/design/PROJECT_CONSTITUTION.md) — authoritative methodology, corpus, boundaries, and book architecture.
2. [`research/README.md`](research/README.md) — evidence registry and stable evidence-ID system.
3. [`research/registry/SCHEMA.md`](research/registry/SCHEMA.md) — structured evidence contract.
4. [`research/TXT/`](research/TXT/) — textual-tradition and direct-Hebrew-consultation analysis.
5. [`research/NAR/`](research/NAR/) — scriptural narrative-generation analysis.
6. [`research/CUL/`](research/CUL/) — Hellenistic / Greco-Roman comparison controls.
7. [`research/HIS/`](research/HIS/) — claim-by-claim historical residue audit.

## Hermes / OpenRouter research workflow

If you are running this project through Hermes, start with [`HERMES_START.md`](HERMES_START.md).

The operating model is:

**GitHub contract → source-bound research in a staging branch → independent adversarial review → reviewed promotion → next source/batch.** The active B001 draft uses **Antigravity/Gemini + one-source-at-a-time NotebookLM** for extraction and ChatGPT for exact-SHA independent review ([serial workflow](https://github.com/aguacatero/septuagint-diaspora-book/blob/research/B001-notebooklm-serial/docs/workflow/NOTEBOOKLM_ANTIGRAVITY_SERIAL.md) on the draft branch). The Hermes/OpenRouter + Open Notebook instructions below describe the original `main` workflow and remain fallback/history until a reviewed transition is merged.

Key files:

- [`docs/workflow/RESEARCH_WORKFLOW.md`](docs/workflow/RESEARCH_WORKFLOW.md) — full volley and review process.
- [`docs/workflow/HERMES_INSTRUCTIONS.md`](docs/workflow/HERMES_INSTRUCTIONS.md) — exact operating rules for Hermes.
- [`research-queue/CURRENT_BATCH.md`](research-queue/CURRENT_BATCH.md) — the only active research task.
- [`research-queue/BACKLOG.md`](research-queue/BACKLOG.md) — dependency-ordered future batches.
- [`research/inbox/`](research/inbox/) — non-canonical staging area for machine-assisted research packets.

Hermes must not directly rewrite the project constitution or canonical evidence registry. Its job is to produce auditable candidate research, including counterevidence, for later review.

## Core methodological changes

- The old binary **“LXX vs. MT”** model is retired in favor of first-century textual pluriformity: Old Greek, other Jewish Greek traditions/revisions, Hebrew textual witnesses, authorial adaptation, oral/liturgical transmission, and indeterminate cases can all be classified.
- The project does **not** assume that Gospel authors were incapable of Hebrew. It tests demonstrable compositional use of Hebrew Scripture author-by-author.
- Explicit/identifiable quotations and allusions are tracked separately.
- Negative evidence and Hebrew-aligned readings remain visible rather than being explained away.
- Synoptic repetition is corrected for literary dependence; dependent texts are not automatically independent witnesses.
- Hellenistic parallels must pass chronology, accessibility, specificity, density, structural, Jewish-scriptural, genre, difference, and transmission controls.
- The historical-Jesus question is bracketed during literary analysis and deliberately reopened at the end from **zero assumed biography**.

## Primary corpus

- Mark
- Matthew
- Luke–Acts
- John
- undisputed Pauline letters

Markan priority is used as an operational baseline, not as a premise that must be true for the thesis to survive. Q is not used as evidence.

## Book architecture

**Part I — The Test**  
Definitions, textual pluriformity, evidence rules, controls, confidence, and falsification.

**Part II — Before the Gospels**  
Diaspora scriptural environment, control corpora, and undisputed Paul as the earliest surviving Christian authorial evidence in the primary corpus.

**Part III — The Evangelists**  
Mark, Matthew, Luke–Acts, and John audited independently through the textual framework.

**Part IV — Scripture Becomes Story**  
Testing scriptural coloring, shaping, co-construction, and probable narrative generation.

**Part V — The Hellenistic Narrative World**  
Controlled comparison with the wider Mediterranean literary environment.

**Part VI — What Is Left?**  
A claim-by-claim audit of the remaining historical evidence and the explanatory model that best fits it.

## Legacy files

`Core_Thesis.md`, `Book_Scholar_Outline.md`, `Book_Part1.md` through `Book_Part4.md`, and earlier files under `docs/plans/` document the historical development of the project. They contain useful research leads but also assumptions and claims that predate the current methodology.

They are retained for provenance and **must not be treated as verified current findings until migrated through the evidence registry**. See [`docs/design/LEGACY_MIGRATION_NOTES.md`](docs/design/LEGACY_MIGRATION_NOTES.md) and [`research/registry/corrections_log.md`](research/registry/corrections_log.md).

## Status

The architecture and foundation gate are established (**1/6 milestones accepted**). The current bounded Pauline TXT pilot (B001) is still in progress: the active [serial NotebookLM research branch / draft PR #2](https://github.com/aguacatero/septuagint-diaspora-book/pull/2) has six accepted **source packets** (P01F–S03F), with S03F accepted in its [Round 5 independent review](https://github.com/aguacatero/septuagint-diaspora-book/pull/2#issuecomment-6460107612) and promoted to cumulative notebook `SDP-01 Paul`. S04F (Lightfoot, Galatians) is now underway. This is draft/unmerged research, not accepted `main` evidence or completion of TXT. The complete quotation census across the defined primary corpus begins only after B001 passes its gates.
