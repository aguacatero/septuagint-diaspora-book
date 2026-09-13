# Research Volley Workflow

This project uses a controlled research volley between GitHub, Hermes/OpenRouter, Open Notebook, and human/LLM review.

## Source of truth

**GitHub `main` is authoritative.**

Open Notebook is the persistent source warehouse. Hermes/OpenRouter is the research workforce. Neither may silently redefine the project thesis, methodology, corpus, classifications, or canonical registry.

The governing order is:

1. `docs/design/PROJECT_CONSTITUTION.md`
2. `research/registry/SCHEMA.md`
3. module rules under `research/TXT/`, `research/NAR/`, `research/CUL/`, and `research/HIS/`
4. the active contract in `research-queue/CURRENT_BATCH.md`

If any generated instruction conflicts with those files, the files above win in that order.

## The volley

### 1. GitHub defines the research contract

Each batch specifies:

- research question;
- bounded corpus;
- required primary witnesses;
- minimum secondary-source requirements;
- expected deliverables;
- disallowed shortcuts;
- falsification/counterevidence requirements;
- completion gate.

### 2. Hermes performs research on a batch branch

Hermes must:

1. pull the latest `main`;
2. read the project constitution and current batch;
3. create a branch named `research/<batch-id>-<short-name>`;
4. use Open Notebook as the source library when available;
5. use OpenRouter models for extraction, comparison, adversarial review, and synthesis;
6. write all output under `research/inbox/<batch-id>-<short-name>/`;
7. commit the batch branch;
8. stop before modifying authoritative registry files.

Hermes must **not** merge its own branch into `main`.

## 3. Open Notebook is the source warehouse

Open Notebook should contain the actual primary texts, PDFs, articles, monographs, notes, and other source material used in a batch.

For every source promoted into a batch deliverable, record enough information to recover it independently:

- author/editor;
- title;
- publication/container;
- year;
- edition/volume where relevant;
- page(s) or section used;
- DOI/ISBN/stable URL where available;
- local/Open Notebook source label if useful.

A model-generated answer is **not a source**.

Notebook summaries can guide discovery but must never substitute for checking the underlying source.

## 4. OpenRouter is the analysis workforce

The workflow is model-agnostic. When practical, use separate passes for different roles:

- **Source scout:** identifies relevant primary and specialist secondary sources.
- **Extractor:** records exact passage data, page references, variants, and author claims.
- **Analyst:** applies project classifications without changing project rules.
- **Adversary:** searches for the strongest counterevidence and alternative explanations.
- **Verifier:** checks whether citations actually support the claims attributed to them.

At least one adversarial pass must occur before a candidate classification is submitted.

For consequential or disputed cases, prefer a second independent model-family review when available rather than asking the same model to approve its own work.

## 5. Staging versus canonical evidence

Hermes writes **candidate** evidence only.

Allowed staging locations:

- `research/inbox/<batch>/candidate_registry.csv`
- `research/inbox/<batch>/passages/*.md`
- `research/inbox/<batch>/source_manifest.csv`
- `research/inbox/<batch>/adversarial_review.md`
- `research/inbox/<batch>/unresolved_questions.md`
- `research/inbox/<batch>/run_log.md`

Hermes must not directly modify:

- `research/registry/master_registry.csv`
- `research/registry/allusions_registry.csv`
- `research/registry/corrections_log.md`
- `docs/design/PROJECT_CONSTITUTION.md`

Promotion to the canonical registry happens only after review.

## 6. Evidence discipline

Every proposed result must preserve negative evidence.

Do not:

- infer Hebrew consultation merely from an MT-type agreement;
- call a textual divergence a `mistranslation` unless the evidence demonstrates it;
- treat an allusion as an explicit quotation;
- count dependent Gospel repetitions as independent attestations;
- turn absence of evidence into proof of linguistic incapacity;
- use weak mythic resemblance as evidence of borrowing;
- invent page numbers, critical-edition readings, manuscript evidence, or bibliographic entries.

If a needed source cannot be obtained, mark the gap explicitly.

## 7. Source hierarchy

Prefer evidence in this order:

1. **Primary textual witnesses / critical editions** — NT Greek, Old Greek/Septuagint witnesses, Hebrew witnesses, DSS, ancient authors.
2. **Critical apparatuses and specialist reference works.**
3. **Peer-reviewed articles and specialist monographs.**
4. **Major academic handbooks and scholarly commentaries.**
5. **Tertiary/web summaries** for discovery only, not final evidentiary support when stronger sources are reasonably available.

A controversial claim should not rest only on Tier 5 material.

## 8. Batch review

A reviewer examines the branch for:

- source existence and relevance;
- page-level citation support;
- accurate quotation/transcription;
- textual-witness completeness;
- missing counterevidence;
- classification discipline;
- confidence calibration;
- unresolved ambiguity;
- compliance with the batch contract.

Possible outcomes for each candidate:

- promote;
- revise and resubmit;
- dispute;
- reject;
- defer pending source acquisition.

Rejected or corrected claims are preserved where methodologically useful.

## 9. Next volley

After review, accepted findings are promoted into `main`, corrections are recorded, and `research-queue/CURRENT_BATCH.md` is advanced to the next task.

The long-term goal is a repeatable loop:

**GitHub contract → Hermes/OpenNotebook research → candidate branch → adversarial review → canonical promotion → next contract.**
