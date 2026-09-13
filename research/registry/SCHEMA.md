# Evidence Registry Schema

The master registry records identifiable quotations and other primary evidence units. Allusions are stored separately in `allusions_registry.csv` and must not be combined with quotation statistics.

## Master registry fields

| Field | Purpose |
|---|---|
| `evidence_id` | Stable ID, e.g. `JHN-019-TXT` |
| `source` | Mark, Matthew, Luke, Acts, John, Paul, control, external |
| `passage` | Primary source passage |
| `evidence_type` | quotation, textual_variant, external_attestation, control, other |
| `target_or_comparandum` | Scriptural or other text being compared |
| `source_relationship` | independent, dependent, possibly_dependent, shared_tradition, unknown, not_applicable |
| `module` | TXT, NAR, CUL, HIS |
| `classification` | Module-specific ordered category |
| `confidence` | Very High, High, Moderate, Low, Very Low |
| `supports_working_hypothesis` | yes, no, mixed, indeterminate |
| `counterevidence` | Strongest evidence against classification |
| `alternative_explanations` | Plausible rivals that must be considered |
| `falsifier` | Finding that would materially weaken/reverse classification |
| `status` | UNREVIEWED, IN_REVIEW, CLASSIFIED, DISPUTED, UNVERIFIED_LEGACY, REJECTED |
| `notes` | Short methodological notes only |
| `linked_ids` | Related TXT/NAR/CUL/HIS records |

## Classification discipline

Classification and confidence are separate. A record may have a strong classification with low confidence or an indeterminate classification with high confidence.

Do not infer direct Hebrew consultation from simple agreement with an MT-type reading against reconstructed Old Greek. Known/possible Greek revisions, alternative Hebrew Vorlagen, authorial adaptation, oral/liturgical transmission, and unknown Greek intermediaries must be considered first.

## Quotation / allusion separation

`master_registry.csv` is the authoritative census for explicit or identifiable quotations and other primary evidence units selected by the protocol.

`allusions_registry.csv` is separate. An allusion can link into NAR analysis only after passing stronger specificity and density controls. Allusion rows must never be included in quotation-frequency denominators.
