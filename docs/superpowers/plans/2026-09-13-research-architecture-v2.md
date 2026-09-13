# Research Architecture V2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restructure the repository around the confirmed project constitution so the book is driven by a transparent, reproducible evidence registry rather than by a prewritten argumentative outline.

**Architecture:** Preserve the legacy manuscript files for provenance, but introduce a new authoritative `research/` apparatus with stable evidence IDs and four linked analytical modules: TXT, NAR, CUL, and HIS. Update top-level documentation to point readers to the constitution and registry before the legacy prose, and explicitly mark legacy claims as unverified until migrated through the new protocol.

**Tech Stack:** Markdown, CSV, JSON-compatible schemas/conventions, GitHub repository history.

**Spec:** `docs/design/PROJECT_CONSTITUTION.md`

## Global Constraints

- Primary corpus: Mark, Matthew, Luke–Acts, John, undisputed Pauline letters.
- Operational Synoptic baseline: Markan priority; Q is not used as evidence.
- Separate authorial Hebrew competence from demonstrable compositional use of Hebrew Scripture.
- Retire binary “LXX vs. MT” framing in favor of textual pluriformity.
- Retire “mistranslation” as a default category; it must be demonstrated.
- Complete census of explicit/identifiable quotations; allusions tracked separately.
- Negative, Hebrew-aligned, mixed, and indeterminate evidence must remain visible.
- No numerical pseudo-probabilities; use ordered classifications plus independent confidence labels.
- “Borrowed” is reserved for direct dependence or probable cultural influence.
- Historical-Jesus audit starts from zero assumed biography.
- Argumentative prose is downstream of the evidence registry.

---

### Task 1: Freeze the design and mark source of truth

**Files:**
- Create: `docs/design/PROJECT_CONSTITUTION.md`
- Create: `docs/design/LEGACY_MIGRATION_NOTES.md`

**Interfaces:**
- Consumes: confirmed Q1–Q34 design decisions.
- Produces: authoritative spec for all later research and manuscript work.

- [x] **Step 1: Commit the confirmed constitution**
- [ ] **Step 2: Write a migration note identifying legacy assumptions that are no longer authoritative**
- [ ] **Step 3: Verify the migration note points back to the constitution and does not silently rewrite historical files**
- [ ] **Step 4: Commit**

### Task 2: Create the evidence registry contract

**Files:**
- Create: `research/README.md`
- Create: `research/registry/SCHEMA.md`
- Create: `research/registry/master_registry.csv`
- Create: `research/registry/allusions_registry.csv`

**Interfaces:**
- Consumes: project constitution.
- Produces: stable evidence-ID conventions and fields used by TXT/NAR/CUL/HIS modules.

- [ ] **Step 1: Define stable IDs using `<SOURCE>-<NNN>-<MODULE>` with source prefixes such as MRK, MAT, LUK, ACT, JHN, PAU, CTL**
- [ ] **Step 2: Define master registry fields for source, passage, evidence type, source relationships, module links, classification, confidence, counterevidence, falsifier, and status**
- [ ] **Step 3: Create an explicit quotation census file with headers only**
- [ ] **Step 4: Create a separate allusion registry with stronger-threshold fields**
- [ ] **Step 5: Verify quotation and allusion records cannot be accidentally combined in summary statistics**
- [ ] **Step 6: Commit**

### Task 3: Define TXT module methodology

**Files:**
- Create: `research/TXT/README.md`
- Create: `research/TXT/textual_classifications.md`
- Create: `research/TXT/hebrew_consultation_test.md`

**Interfaces:**
- Consumes: registry IDs and textual-pluriformity rules.
- Produces: textual classifications and direct-Hebrew-consultation criteria.

- [ ] **Step 1: Define textual source classes including Old Greek strongly preferred, other Greek tradition preferred, Hebrew-direct plausible, authorial adaptation, mixed, indeterminate**
- [ ] **Step 2: Define confidence labels independently from classification**
- [ ] **Step 3: Encode the high bar for direct Hebrew consultation**
- [ ] **Step 4: Add John 19:37 as the canonical example of a counterexample that must be tested rather than relabeled**
- [ ] **Step 5: Commit**

### Task 4: Define NAR module methodology

**Files:**
- Create: `research/NAR/README.md`
- Create: `research/NAR/causal_ladder.md`

**Interfaces:**
- Consumes: TXT results and source-dependence relationships.
- Produces: classifications for scriptural coloring, shaping, co-construction, and probable narrative generation.

- [ ] **Step 1: Define the three competing causal models**
- [ ] **Step 2: Define evidentiary discriminators for moving up the causal ladder**
- [ ] **Step 3: State explicitly that literary dependence does not equal non-historicity**
- [ ] **Step 4: Commit**

### Task 5: Define CUL module methodology

**Files:**
- Create: `research/CUL/README.md`
- Create: `research/CUL/comparison_controls.md`

**Interfaces:**
- Consumes: Gospel narratives after TXT/NAR analysis.
- Produces: direct dependence, probable cultural influence, shared Mediterranean convention, or weak parallel classifications.

- [ ] **Step 1: Encode chronology, accessibility, specificity, density, order, Jewish control, genre control, differences, and transmission controls**
- [ ] **Step 2: Reserve “borrowed” for the top two classifications**
- [ ] **Step 3: State that failed parallels are removed rather than rescued**
- [ ] **Step 4: Commit**

### Task 6: Define HIS module methodology

**Files:**
- Create: `research/HIS/README.md`
- Create: `research/HIS/historical_claims.csv`
- Create: `research/HIS/source_independence.md`

**Interfaces:**
- Consumes: prior TXT/NAR/CUL results plus external evidence.
- Produces: claim-by-claim historical residue audit.

- [ ] **Step 1: Seed historical proposition rows for existence, Jewish identity, James, Cephas, crucifixion, Pilate, Nazareth, disciples, kingdom preaching**
- [ ] **Step 2: Define chronology, textual integrity, independence, proximity, proclamation dependence, source relationship, and alternatives fields**
- [ ] **Step 3: Make independence claim-specific rather than source-wide**
- [ ] **Step 4: Commit**

### Task 7: Define control corpora and corpus boundaries

**Files:**
- Create: `research/controls/README.md`
- Create: `research/controls/philo.md`
- Create: `research/controls/hebrews.md`
- Create: `research/controls/textual_pluriformity.md`
- Create: `research/corpus/PRIMARY_CORPUS.md`
- Create: `research/corpus/SYNOPTIC_DEPENDENCE.md`

**Interfaces:**
- Consumes: constitution corpus decisions.
- Produces: explicit boundaries preventing control evidence from being counted as primary evidence.

- [ ] **Step 1: Document control-corpus purposes and exclusions**
- [ ] **Step 2: State Markan priority as operational baseline, not dogma**
- [ ] **Step 3: State that dependent repetition is not independent attestation**
- [ ] **Step 4: Document Luke–Acts authorial-practice use versus historical-attestation use**
- [ ] **Step 5: Commit**

### Task 8: Update repository navigation without rewriting legacy research yet

**Files:**
- Modify: `README.md`
- Modify: `Core_Thesis.md`
- Modify: `Book_Scholar_Outline.md`

**Interfaces:**
- Consumes: all new research architecture docs.
- Produces: top-level navigation that prevents readers from mistaking legacy claims for current verified conclusions.

- [ ] **Step 1: Rewrite README around the new title, six-part architecture, constitution, and research registry**
- [ ] **Step 2: Add a clear supersession notice to `Core_Thesis.md` while preserving its historical contents below the notice**
- [ ] **Step 3: Add a clear supersession notice to `Book_Scholar_Outline.md` while preserving the legacy outline for provenance**
- [ ] **Step 4: Verify no top-level documentation claims the legacy outline is the current methodology**
- [ ] **Step 5: Commit**

### Task 9: Seed known corrections and negative controls

**Files:**
- Create: `research/registry/corrections_log.md`
- Populate initial rows in: `research/registry/master_registry.csv`

**Interfaces:**
- Consumes: previously identified red-alert cases.
- Produces: transparent record of claims requiring correction/reanalysis.

- [ ] **Step 1: Log Pliny language overclaim for reanalysis**
- [ ] **Step 2: Log John 19:37 / Zechariah 12:10 as a required counterexample analysis**
- [ ] **Step 3: Log Mark 1:2–3 “single-Isaiah LXX editorial decision” formulation as requiring reanalysis**
- [ ] **Step 4: Mark each as `UNVERIFIED_LEGACY` rather than silently supplying a replacement result**
- [ ] **Step 5: Commit**

### Task 10: Verification

**Files:**
- Review all files created/modified above.

**Interfaces:**
- Consumes: completed architecture.
- Produces: verified branch ready for review/merge before evidence classification begins.

- [ ] **Step 1: Confirm every constitutional requirement maps to at least one repository file**
- [ ] **Step 2: Scan for legacy “LXX vs. MT” framing in authoritative new files and remove accidental binary assumptions**
- [ ] **Step 3: Scan new files for predetermined historicity conclusions or blanket author-language claims**
- [ ] **Step 4: Confirm legacy files remain preserved, explicitly superseded rather than silently rewritten**
- [ ] **Step 5: Compare branch against `main` and review all changed paths**
