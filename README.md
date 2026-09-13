# Shaped by the Septuagint

## How Greek Scripture Shaped the Gospels—and What History Remains

This is a public-facing research and book project designed as a serious crossover work: readable by educated non-specialists while using a method intended to withstand specialist scrutiny.

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

**GitHub contract → Hermes/OpenRouter + Open Notebook research → staged research branch → adversarial review → canonical promotion to `main` → next batch.**

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

The research architecture is established. The active next step is the bounded Hermes/OpenRouter TXT pilot defined in `research-queue/CURRENT_BATCH.md`; after review, the workflow will scale to the complete quotation census across the defined primary corpus.
