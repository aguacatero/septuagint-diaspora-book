# Hermes Operating Instructions

These instructions govern Hermes research runs for *Shaped by the Septuagint*.

## Start-of-run checklist

Before doing research:

1. Pull the latest `main`.
2. Read `docs/design/PROJECT_CONSTITUTION.md`.
3. Read `docs/workflow/RESEARCH_WORKFLOW.md`.
4. Read `docs/workflow/SOURCE_ACQUISITION.md`.
5. Read `research/registry/SCHEMA.md`.
6. Read the module rules relevant to the batch.
7. Read `research-queue/CURRENT_BATCH.md`.
8. Create the research branch named by the batch contract.

Do not rely on remembered instructions from an earlier run when repo instructions are available.

## Core behavior

Your job is to produce **reviewable research packets**, not to prove the book's thesis.

You must actively seek findings that weaken the working hypothesis.

Do not silently resolve uncertainty. Mark it.

Do not promote staged findings into canonical registry files.

## Phase 0 — Source acquisition and ingestion

Unless the active batch explicitly says its source packet is already complete, begin by acquiring the sources needed for the batch.

Follow `docs/workflow/SOURCE_ACQUISITION.md`.

Your responsibilities include:

- identify the exact editions and specialist works required;
- search lawful sources, including Internet Archive/Open Library where appropriate;
- download public-domain, open-access, or otherwise authorized full-text copies when available;
- never bypass borrowing restrictions, DRM, authentication, or access controls;
- import usable full-text sources into the batch's Open Notebook notebook;
- verify edition identity, scan quality, page mapping, and ingestion;
- create `acquisition_manifest.csv`;
- create `source_gaps.md`;
- continue with documented substitutes when a source cannot be acquired and the batch can still proceed.

Do not begin final passage classifications until the batch's minimum source packet has been acquired/ingested or the missing sources have been explicitly documented with their limitations.

## Use of Open Notebook

When Open Notebook is available:

- create or reuse the notebook named by the active batch;
- ingest the actual sources, not only model summaries;
- preserve filenames/source titles so another researcher can locate them;
- query sources for exact passages, page references, textual variants, author arguments, and counterarguments;
- inspect the underlying source before citing a Notebook-generated answer;
- record missing/inaccessible sources in `source_gaps.md` and `unresolved_questions.md`.

Suggested persistent notebooks:

- `SDP-00 Method and Textual Traditions`
- `SDP-01 Paul`
- `SDP-02 Mark`
- `SDP-03 Matthew`
- `SDP-04 Luke-Acts`
- `SDP-05 John`
- later notebooks for NAR, CUL, and HIS only after those phases are activated.

## Use of OpenRouter models

Do not require one model to do every role.

A recommended pattern is:

1. **Discovery pass** — inexpensive model to identify candidate sources/search terms.
2. **Acquisition pass** — verify bibliographic identity, locate lawful full text, and prepare Open Notebook ingestion.
3. **Extraction pass** — model focused on exact source extraction and structured notes.
4. **Reasoning pass** — strongest appropriate model to compare textual witnesses and apply the project method.
5. **Adversarial pass** — independent prompt/model asked to disprove the provisional classification.
6. **Citation verification pass** — verify source/page/claim correspondence before commit.

For disputed cases, use a different model family for the adversarial pass when practical.

Do not report model consensus as scholarly evidence. Models are research assistants; sources carry the evidence.

## Required passage report

Every passage report under `research/inbox/<batch>/passages/` must contain:

### 1. Research target

- candidate evidence ID;
- NT passage;
- proposed scriptural source(s);
- whether the datum is being treated as quotation, textual variant, or other evidence type.

### 2. Primary textual evidence

Record, with editions/witnesses where available:

- NT Greek wording relevant to the comparison;
- Old Greek / Septuagint wording;
- significant Greek variants or revisions;
- Hebrew wording/witness;
- relevant DSS/Qumran witness if applicable;
- important textual apparatus notes.

Do not substitute an English translation for the underlying textual comparison when Greek/Hebrew evidence is material.

### 3. Source comparison

Explain which features actually discriminate among possible textual traditions.

Separate:

- exact lexical agreement;
- syntax/order;
- shared wording common to multiple traditions;
- authorial adaptation;
- evidence that is non-discriminating.

### 4. Direct-Hebrew test

Apply `research/TXT/hebrew_consultation_test.md` explicitly.

If the passage agrees with a Hebrew form against Old Greek, test known/possible Greek revisions, alternative Greek forms, oral/liturgical transmission, authorial adaptation, and unknown intermediary explanations before proposing direct Hebrew consultation.

### 5. Secondary scholarship

Record the strongest relevant scholarly positions with page-level citations where possible.

Include disagreement, not only support.

### 6. Provisional classification

Provide:

- module classification;
- confidence;
- whether it supports the working hypothesis: yes/no/mixed/indeterminate;
- strongest counterevidence;
- alternative explanations;
- falsifier;
- unresolved source gaps.

Classification remains provisional until external review.

### 7. Adversarial result

State the strongest case against the provisional result and whether it changed the classification or confidence.

## Citation rules

Never fabricate:

- quotations;
- page numbers;
- DOI/ISBN values;
- manuscript readings;
- edition details;
- scholarly positions.

If exact page verification is unavailable, write `PAGE NOT VERIFIED` rather than guessing.

If a source is encountered only through another scholar's citation, label it as a secondary citation until the original is checked.

## Candidate registry rules

`candidate_registry.csv` should mirror the canonical registry fields in `research/registry/SCHEMA.md`.

Use `UNREVIEWED` for new Hermes candidates unless a reviewer has explicitly assigned another canonical status.

Candidate evidence IDs must follow the stable ID system but are not canonical merely because an ID has been assigned.

Do not overwrite an existing canonical ID. If uncertain about numbering, use a temporary batch-local ID such as `PAU-B001-01-TXT` and flag it for reviewer mapping.

## Stop conditions

Stop and record the problem rather than improvising when:

- a required primary witness cannot be accessed and no adequate substitute exists;
- critical source metadata cannot be verified;
- two strong sources materially conflict and the conflict cannot be resolved;
- the current batch contract is ambiguous;
- a requested conclusion would require violating the constitution;
- a passage cannot be confidently distinguished as quotation versus allusion.

## End-of-run checklist

Before committing:

- all required batch passages have a report or an explicit blocked-status entry;
- `acquisition_manifest.csv` exists when acquisition was performed;
- `source_gaps.md` exists;
- `source_manifest.csv` exists;
- `candidate_registry.csv` exists;
- `adversarial_review.md` exists;
- `unresolved_questions.md` exists;
- `run_log.md` records models/tools used and major process choices;
- no canonical registry files were modified;
- no unsupported `verified` claims appear in the packet.

Commit the research packet to the batch branch and report the branch name + commit SHA for review.
