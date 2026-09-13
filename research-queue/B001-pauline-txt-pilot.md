# B001 — Pauline TXT Pilot

## Purpose

This is a workflow-validation batch, not the full Pauline census.

The goal is to test whether Hermes + OpenRouter + Open Notebook can produce reviewable, source-grounded TXT research packets that comply with the project constitution and registry schema.

The batch is intentionally limited to twelve quotations across Romans, 1 Corinthians, and Galatians.

## Governing files

Before beginning, read:

1. `docs/design/PROJECT_CONSTITUTION.md`
2. `docs/workflow/RESEARCH_WORKFLOW.md`
3. `docs/workflow/HERMES_INSTRUCTIONS.md`
4. `research/registry/SCHEMA.md`
5. `research/TXT/README.md`
6. `research/TXT/textual_classifications.md`
7. `research/TXT/hebrew_consultation_test.md`

If this batch file conflicts with those documents, the higher-level documents govern.

## Branch and output location

Create branch:

`research/B001-pauline-txt-pilot`

Write outputs only under:

`research/inbox/B001-pauline-txt-pilot/`

Do not edit canonical registry files.

## Assigned passages

Use the batch-local IDs below until reviewer promotion assigns canonical numbering.

| Batch ID | NT passage | Primary scriptural comparandum |
|---|---|---|
| `PAU-B001-01-TXT` | Romans 4:3 | Genesis 15:6 |
| `PAU-B001-02-TXT` | Romans 9:25 | Hosea 2:23 |
| `PAU-B001-03-TXT` | Romans 9:26 | Hosea 1:10 |
| `PAU-B001-04-TXT` | Romans 10:11 | Isaiah 28:16 |
| `PAU-B001-05-TXT` | Romans 10:13 | Joel 2:32 |
| `PAU-B001-06-TXT` | Romans 11:34 | Isaiah 40:13 |
| `PAU-B001-07-TXT` | Romans 15:12 | Isaiah 11:10 |
| `PAU-B001-08-TXT` | 1 Corinthians 1:19 | Isaiah 29:14 |
| `PAU-B001-09-TXT` | 1 Corinthians 6:16 | Genesis 2:24 |
| `PAU-B001-10-TXT` | 1 Corinthians 9:9 | Deuteronomy 25:4 |
| `PAU-B001-11-TXT` | 1 Corinthians 10:7 | Exodus 32:6 |
| `PAU-B001-12-TXT` | Galatians 3:13 | Deuteronomy 21:23 |

Do not assume the listed comparandum is the only relevant textual source. Record additional textual relationships if scholarship or the apparatus requires them.

## Research question for every passage

For each assigned passage, answer:

> Which known textual tradition or combination of processes best explains Paul's wording, and how much evidence does the passage provide for or against direct consultation of Hebrew Scripture?

The answer may be indeterminate.

## Required primary evidence

For every passage, attempt to obtain and record:

- relevant Pauline Greek text from a critical or academically reliable edition;
- relevant Old Greek/Septuagint wording from an academically reliable critical edition;
- materially relevant Greek variants/revisions when available;
- Hebrew wording from an academically reliable Hebrew edition/witness;
- relevant DSS/Qumran evidence if it materially bears on the textual question;
- apparatus information necessary to avoid a false Old-Greek-versus-MT binary.

If a critical edition is inaccessible, name the missing edition and use the strongest available substitute, clearly labeling the limitation.

Do not fabricate apparatus information from memory.

## Minimum secondary scholarship

For each passage, seek at least **two specialist scholarly treatments** relevant to Paul's use of Scripture or the specific textual problem.

Across the entire batch, the source manifest should include multiple scholarly viewpoints rather than a single author or school.

Prioritize:

1. specialist monographs on Paul's use of Scripture / Septuagint;
2. peer-reviewed articles on specific quotations/textual forms;
3. major critical commentaries where they discuss textual provenance;
4. scholarly reference works on Septuagint/textual criticism.

Tertiary summaries may be used to discover sources but should not anchor a candidate classification.

## Open Notebook setup

Use or create:

`SDP-01 Paul`

Ingest sources actually used in the analysis. Keep enough bibliographic metadata to identify every source outside Open Notebook.

If helpful, maintain `SDP-00 Method and Textual Traditions` for reusable methodological sources, but the B001 output must still list every source relied upon.

## Required output structure

Create:

```text
research/inbox/B001-pauline-txt-pilot/
├── README.md
├── source_manifest.csv
├── candidate_registry.csv
├── adversarial_review.md
├── unresolved_questions.md
├── run_log.md
└── passages/
    ├── PAU-B001-01-TXT.md
    ├── PAU-B001-02-TXT.md
    ├── PAU-B001-03-TXT.md
    ├── PAU-B001-04-TXT.md
    ├── PAU-B001-05-TXT.md
    ├── PAU-B001-06-TXT.md
    ├── PAU-B001-07-TXT.md
    ├── PAU-B001-08-TXT.md
    ├── PAU-B001-09-TXT.md
    ├── PAU-B001-10-TXT.md
    ├── PAU-B001-11-TXT.md
    └── PAU-B001-12-TXT.md
```

## `source_manifest.csv` minimum fields

Use:

```csv
source_id,source_type,author_or_editor,title,publication,year,edition_or_volume,pages_used,doi_isbn_or_url,open_notebook_label,access_status,notes
```

`access_status` should distinguish at least:

- `FULL_TEXT_VERIFIED`
- `PARTIAL_PREVIEW`
- `SECONDARY_CITATION_ONLY`
- `DISCOVERY_ONLY`
- `INACCESSIBLE`

A source marked `DISCOVERY_ONLY` or `INACCESSIBLE` must not be cited as if its argument was directly verified.

## `candidate_registry.csv`

Mirror the field order in `research/registry/master_registry.csv`.

For all new candidates:

- use the batch-local evidence IDs above;
- use `source = Paul`;
- use `module = TXT`;
- use `status = UNREVIEWED`;
- leave classification indeterminate when the evidence does not justify a stronger category;
- keep classification and confidence separate.

## Passage-report requirements

Each passage report must follow `docs/workflow/HERMES_INSTRUCTIONS.md` and must include:

1. research target;
2. primary textual evidence;
3. discriminating textual features;
4. direct-Hebrew consultation test;
5. secondary scholarly positions with page-level citations where possible;
6. provisional classification and confidence;
7. strongest counterevidence;
8. alternative explanations;
9. falsifier;
10. unresolved source gaps;
11. adversarial-review result.

## Adversarial requirements

After initial classification, run a deliberate challenge pass for every passage.

Prompts should ask the adversary to identify, among other things:

- overlooked Greek witnesses/revisions;
- possible different Hebrew Vorlage;
- authorial adaptation that reduces textual-source certainty;
- cases where the wording is non-discriminating;
- scholarship arguing against the provisional classification;
- overstatement of what quotation choice can prove about Paul's language competence.

Summarize passage-level changes in `adversarial_review.md`.

## Special warning: Galatians 3:13 / Deuteronomy 21:23

This case appears in legacy project material and must be treated as a fresh analysis.

Do not inherit any previous `mistranslation`, LXX-alignment, or Hebrew-use classification from legacy notes. Reconstruct the comparison from source evidence under the current TXT rules.

## Completion gate

The batch is ready for review only when:

- all 12 passage reports exist, or blocked passages have explicit blocked reports;
- every substantive secondary-source claim is traceable to a verified source/page or clearly marked otherwise;
- all primary textual claims identify the edition/witness used;
- `source_manifest.csv` and `candidate_registry.csv` are complete;
- each candidate has strongest counterevidence and alternatives;
- the adversarial pass has been completed;
- unresolved source gaps are explicit;
- canonical registry files have not been changed;
- the branch is committed and the commit SHA is reported.

## What success looks like

Success does **not** mean twelve passages support Greek-scriptural dominance.

Success means the batch produces twelve auditable research packets whose classifications could be promoted, revised, disputed, rejected, or left indeterminate without changing the method.
