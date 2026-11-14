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

**Round 2–4 Scope & Provenance Remediations:**
- **Canonical `B001-4` restored:** `B001-4` is strictly **`Romans 10:11 / Isaiah 28:16`**, never `Romans 10:6–8 / Deuteronomy 30:12–14`. Five Rom 10:5–10 / encasement items (`S09F-E001`–`E004`, `E008`) were moved to `B001-CONTEXT`, while direct `B001-4` claims (`S09F-E009`, `S09F-E010`) were extracted alongside shared `S09F-E005`.
- **No fabricated text-critical claims:** Neither Oliver nor this packet attributes to Oliver the claim that Paul added `πᾶς` to LXX Isa 28:16; project collation of **`P01F-P004`** (`SBLGNT` Rom 10:11) vs. **`P03F-P003`** (`Swete LXX` Isa 28:16) and **`P01F-P005`** (`SBLGNT` Rom 10:13) vs. **`P03F-P004`** (`Swete LXX` Joel 2:32 [LXX 3:5] — showing Paul omits introductory `καὶ ἔσται` and inserts postpositive `γάρ`) is explicitly segregated in `counterevidence.md`.
- **Verbatim fidelity:** `S09F-E003` quotes Oliver's exact nuance (*"Paul does not cite these words, but implicates them in his own context"*, p. 4), and `S09F-E004` restores printed **`4-3-2-1`** (documenting the p. 9 `4-3-2-\n1` line wrap verified with `pdftotext -layout`).

---

## 2. Raw NotebookLM Anchor Reconciliation (`S09F-E001`–`S09F-E010`)

To eliminate ambiguity between exploratory browser captures and the 10 committed ledger rows (`S09F-E001`–`S09F-E010`), exact raw provenance is reconciled below:

- **Original 8 rows (`S09F-E001`–`S09F-E008`):** Distilled from the **72** exploratory hover-verified CDP citation anchors in `prompt_2_raw.json` (plus `prompt_4_raw.json` for prophetic/missiological framing), with each distilled row's `notebooklm_citation` label (`[2]`, `[5]`, `[7]`, `[9]`, `[11]`, `[13]`, `[1]`) matching the corresponding hover-verified snippet in `prompt_2_raw.json`.
- **Added `B001-4` row `S09F-E009`:** Directly backed by `prompt_2_raw.json` hover-verified citation `label="8"` (`[8]`, Printed p. 3: Paul's use of `καταισχύνω` in v. 11 linking back to `ἐπαισχύνομαι` in Rom 1:16 as references to `Is 28:16 LXX`).
- **Added `B001-4` row `S09F-E010`:** Directly backed by `prompt_4_raw.json` hover-verified citation `label="12"` (`Prompt 4 / label=12`, Printed p. 3 fn. 5: Oliver's methodological caution against Aho `1981:308` on Isaiah 28:16).
- **Manifest structural metadata:** `provenance_manifest.json` records `Figures 1-3` accurately on **pp. 4, 6, 9** (`Figure 1` p. 4; `Figure 2` p. 6; `Figure 3` p. 9).

---

## 3. Ledger–Extraction–Synthesis Crosswalk & Bibliographic Audit

1. **Citation Ledger vs. Extraction Parity:** Every `evidence_id` (`S09F-E001`–`S09F-E010`), `b001_id`, `author_claim`, `short_quote`, `printed_page`, `source_locator`, and `notebooklm_citation` matches byte-for-byte / normalized-token equality between `citation_ledger.csv` and `extraction.md`.
2. **Negative Search Audit:** Exhaustive automated pattern verification across all 12 PDF pages of `oliver_2015_romans_10.pdf` confirms `YES` exclusively on `B001-4` and `B001-5` and `NO` across all 10 remaining B001 loci, with all **12 positive controls (`PC01–PC12`)** verified against their target pages.
3. **Bibliographic Audit Honesty:** All 26 selected bibliographic leads plus 2 supplemental direct-locus `B001-4` leads (`Robert Jewett (2007)` and `R. Barry Matlock (2010)`) = **28 leads total** in `bibliography_leads.md` are reconciled against Oliver (2015) pp. 1–12 (`References` on pp. 11–12) and exact body/footnote witnesses. Internal PDF text-layer matching is documented strictly as **source-witness provenance**, while J. F. Hart (`1999`) additionally records verified external JOTGES metadata (`Vol. 12, No. 23, Autumn 1999, pp. 3–35`) separately from Oliver's raw printed container (`12, 23`).
