# Research Apparatus

This directory is the authoritative research layer for *Shaped by the Septuagint*.

The manuscript is downstream of this apparatus. Evidence is classified here before it is used rhetorically in chapters.

## Stable evidence IDs

Use the form:

`<SOURCE>-<NNN>-<MODULE>`

Source prefixes:
- `MRK` — Mark
- `MAT` — Matthew
- `LUK` — Luke
- `ACT` — Acts
- `JHN` — John
- `PAU` — undisputed Pauline corpus
- `CTL` — control corpus or external control datum
- `EXT` — external historical source used in HIS (for example Josephus or Tacitus)

Modules:
- `TXT` — textual tradition
- `NAR` — narrative generation
- `CUL` — Hellenistic / Greco-Roman comparison
- `HIS` — historical residue

A single underlying datum may have linked module records. Example:

- `MAT-001-TXT` — textual form of Matthew 1:23 / Isaiah 7:14
- `MAT-001-NAR` — whether the textual form contributes causally to the infancy narrative
- `MAT-001-CUL` — comparative cultural analysis, if warranted
- `MAT-001-HIS` — historical claim that remains after literary analysis

## Status values

Use only explicit statuses:

- `UNREVIEWED`
- `IN_REVIEW`
- `CLASSIFIED`
- `DISPUTED`
- `UNVERIFIED_LEGACY`
- `REJECTED`

`REJECTED` means a proposed evidentiary claim failed the project's controls. Rejected cases remain visible.

## Confidence

Confidence is independent of classification:

- Very High
- High
- Moderate
- Low
- Very Low

Do not convert these labels into numeric probabilities.

## Research sequence

1. Complete quotation census and textual classification (`TXT`).
2. Analyze narrative causation where warranted (`NAR`).
3. Analyze Hellenistic / Greco-Roman comparison after TXT/NAR (`CUL`).
4. Reopen historical questions claim-by-claim (`HIS`).

See `docs/design/PROJECT_CONSTITUTION.md` for governing rules.
