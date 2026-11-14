# S09F — NotebookLM & PDF Self-Audit

**Source ID:** S09F  
**Source File:** `oliver_2015_romans_10.pdf` (Willem Oliver, *HTS* 71(3), 2015, Art. #2929, 12 pp.)  
**Ledger Status:** 10 verified evidence items (`S09F-E001`–`S09F-E010`) mapped across `B001-4`, `B001-5`, and `B001-CONTEXT`.

---

## 1. Canonical Locus Alignment & Scope Discipline

| B001 ID | Canonical Comparison | Status | Verified Pages in Oliver (2015) | Depth | Assigned Evidence IDs |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `B001-4` | Romans 10:11 / Isaiah 28:16 | `YES` | Printed p. 3, p. 4, p. 5, p. 7, p. 10, p. 11 | `Substantive` | `S09F-E005`, `S09F-E009`, `S09F-E010` |
| `B001-5` | Romans 10:13 / Joel 2:32 | `YES` | Printed p. 4, p. 5, p. 7, p. 8, p. 9, p. 10, p. 11 | `Substantive` | `S09F-E005`, `S09F-E006`, `S09F-E007` |
| `B001-CONTEXT` | Pericope Context (Rom 10:5–10 & Encasement) | Contextual Only | Printed p. 3, p. 4, p. 5, p. 9 | Ancillary / Contextual | `S09F-E001`, `S09F-E002`, `S09F-E003`, `S09F-E004`, `S09F-E008` |
| All other 10 loci (`B001-1`–`3`, `B001-6`–`12`) | Canonical table entries | `NO` | — | `N/A` | Exhaustive PDF search negative (`full_volume_search_log.md`) |

**Round 2 Scope Remediations:**
- **Canonical `B001-4` restored:** `B001-4` is strictly **`Romans 10:11 / Isaiah 28:16`**, never `Romans 10:6–8 / Deuteronomy 30:12–14`. Five Rom 10:5–10 / encasement items (`S09F-E001`–`E004`, `E008`) were moved to `B001-CONTEXT`, while direct `B001-4` claims (`S09F-E009`, `S09F-E010`) were extracted alongside shared `S09F-E005`.
- **No fabricated text-critical claims:** Neither Oliver nor this packet attributes to Oliver the claim that Paul added `πᾶς` to LXX Isa 28:16; any comparison of `P01F-P004` (`SBLGNT`) vs. `P03F-P003` (`Swete LXX`) is explicitly segregated as a Project Primary-Text Note. Likewise, for `B001-5` (`S09F-E006`), the project primary-text observation that Rom 10:13 omits introductory `καὶ ἔσται` from LXX Joel 3:5a and introduces explanatory `γάρ` is clearly distinguished from Oliver's heraldic interpretation.
- **Verbatim fidelity:** `S09F-E003` quotes Oliver's exact nuance (*"Paul does not cite these words, but implicates them in his own context"*, p. 4), and `S09F-E004` restores printed **`4-3-2-1`** (documenting the p. 9 `4-3-2-\n1` line wrap verified with `pdftotext -layout`).

---

## 2. Ledger–Extraction–Synthesis Crosswalk Audit

1. **Citation Ledger vs. Extraction Parity:** Every `evidence_id` (`S09F-E001`–`S09F-E010`), `b001_id`, `author_claim`, `short_quote`, `printed_page`, `source_locator`, and `notebooklm_citation` matches byte-for-byte / normalized-token equality between `citation_ledger.csv` and `extraction.md`.
2. **Negative Search Audit:** Exhaustive automated pattern verification across all 12 PDF pages of `oliver_2015_romans_10.pdf` confirms `YES` exclusively on `B001-4` and `B001-5` and `NO` across all 10 remaining B001 loci (`PC01`–`PC11` programmatic witness checks pass).
3. **Bibliographic Audit Honesty:** All 26 entries in `bibliography_leads.md` have been reconciled word-for-word against Oliver (2015) pp. 1–12 (`References` on pp. 11–12) and body/footnote witness checks inside `oliver_2015_romans_10.pdf`. Internal PDF text-layer matching is documented strictly as **source-witness provenance**, not as independent external library/DOI verification.
