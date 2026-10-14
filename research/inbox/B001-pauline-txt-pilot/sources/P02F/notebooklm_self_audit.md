# P02F — Primary-Source Self-Audit

**Source ID:** P02F  
**Source Title:** *The Old Testament in Greek according to the Septuagint, Vol. I: Genesis–IV Kings*  
**Editor:** Henry Barclay Swete, D.D. (3rd ed., Cambridge University Press, 1901)  
**Source Class:** PRIMARY (Septuagint / Old Greek manual critical edition)  

---

## Audit Checks

1. **Exact Text & Diacritics:** Every Greek word, breathing, accent, and punctuation mark was checked against the high-resolution facsimile scans of Swete's 1901 Cambridge edition.
2. **Page Locators:** All page numbers (pp. 4–5, 25, 169, 386, 392) were verified directly against the running page headers, marginal book/chapter indicators, and printed footers of the volume.
3. **Apparatus Entries:** The 3 present apparatus units (Gen 2:24 on p. 4; Exod 32:6 on p. 169; Deut 21:23 on p. 386) were verified against the foot of the page, confirming uncial manuscript sigla (Codices B, A, D, E, F, correctors $B^*$, $B^{ab}$, $A^*$, etc.).
4. **Statements of Absence ("No Apparatus Entry"):** The 2 Pentateuch passages with no apparatus entry at the target wording were directly confirmed by observing the variation units present on the page rather than inferred from the lack of commentary:
   - *Genesis 15:6 (p. 25):* The apparatus at the foot of page 25 records variants for Gen 14:20, 21, 23, 24 and 15:1, 7, 10, 12; no entry occurs for 15:6.
   - *Deuteronomy 25:4 (p. 392):* The apparatus at the foot of page 392 records variants for Deut 24:15–21 and 25:1, 2, 3, 5; the entries skip directly from verse 3 to verse 5, containing no entry for 25:4.
5. **Prophetic Absences:** The 7 prophetic passages (Hosea, Joel, Isaiah) were verified as absent from Volume I (which covers Genesis through IV Kings) and belonging properly to Volume III (*The Prophets*).

---

## Audit Verdict

**RESOLVED / ACCEPTED** (All itemized corrections incorporated into canonical ledger)

---

## Itemized Corrections

### 1. Punctuation Mark at Clause Boundary: Deuteronomy 21:23 (P02F-P005)
- **Previous Extraction:** Clause boundary before `καὶ οὐ μιανεῖτε` was transcribed with a high point (`·`).
- **Correction:** The printed text on page 386 uses a Greek colon (`:`): `...ὅτι κεκαταραμένος ὑπὸ θεοῦ πᾶς κρεμάμενος ἐπὶ ξύλου: καὶ οὐ μιανεῖτε τὴν γῆν...`. Punctuation updated across `primary_text_ledger.csv`, `extraction.md`, and `counterevidence.md`.

### 2. Unaccented Apparatus Typography
- **Observation:** Swete’s apparatus prints Greek variant readings strictly without accents or breathings (e.g., `24 τη γυναικι] προς την γυναικα DE` on p. 4; `23 ου κοιμ.] ουκ επικοιμ. AF | αυτο] αυτον AF | κεκατηραμενος AF | ου 2°] + μη AF | μιανειτε] μιανειται A μιανηται F` on p. 386).
- **Confirmation:** Swete's exact typographic convention of unaccented, unbreathed Greek typography is preserved across all apparatus entries in `primary_text_ledger.csv`, `extraction.md`, `relevance_scan.md`, and `counterevidence.md`.

### 3. Queue and State Synchronization (Review Comment 6159404391 Finding 1)
- **Observation:** `B001_NOTEBOOKLM_STATE.json` indicated `active_source_id: "P02F"`, `active_phase: "AWAITING_REVIEW"`, while row 2 in `research-queue/B001_NOTEBOOKLM_SOURCE_QUEUE.csv` remained marked `PENDING,NOT_REVIEWED`.
- **Correction:** Row 2 in `B001_NOTEBOOKLM_SOURCE_QUEUE.csv` synchronized to `status: IN_PROGRESS`, `review_status: AWAITING_REVIEW` to align the restartable state machine across all repository ledgers.

### 4. Elimination of Verbatim Claim on Exodus 32:6 (Review Comment 6159404391 Finding 2)
- **Observation:** Characterizing Exodus 32:6 as a "verbatim match" to 1 Corinthians 10:7 contradicted the source evidence: P02F prints `πιεῖν` (with $B^*$ itacistic `πειν` and $B^{ab}$, A `πιειν`), whereas accepted P01F-P011 prints `πεῖν`.
- **Correction:** Removed all "verbatim" descriptors. Replaced across `extraction.md`, `primary_text_ledger.csv`, `relevance_scan.md`, and `counterevidence.md` with: "close lexical and syntactic agreement with 1 Cor 10:7 (cf. accepted P01F-P011), with a drinking-infinitive form difference (P02F prints `πιεῖν` vs accepted P01F-P011 `πεῖν`)."

### 5. Source-Bounded Primary Extraction & Provenanced P01F Attribution (Review Comment 6159404391 Finding 3)
- **Observation:** Several notes in P02F contained unprovenanced assertions regarding Pauline wording. The PRIMARY route contract mandates strict source-bounding to the currently loaded witness.
- **Correction:** Scrupulously scoped all P02F evidence to the printed text and apparatus of Swete Vol. I. External comparisons with the Pauline textual tradition are explicitly attributed to their accepted P01F evidence IDs (`P01F-P001`, `P01F-P009`, `P01F-P010`, `P01F-P011`, `P01F-P012`) or reserved for downstream passage-level synthesis.

### 6. Scoped Witness-Consensus Language (Review Comment 6159404391 Finding 4)
- **Observation:** Unqualified phrases such as "unanimous agreement among collated uncials" could be misconstrued as claims regarding the entire Greek manuscript tradition rather than the specific witnesses collated by Swete.
- **Correction:** Scoped all witness-agreement language across `extraction.md`, `primary_text_ledger.csv`, `relevance_scan.md`, and `counterevidence.md` strictly to "the witnesses collated by Swete at this locus (e.g. B, A, D, E, F as extant)."

### 7. Corrected Canonical P01F Provenance IDs (Review Comment 6172657286 Finding)
- **Observation:** Review on commit `15568f9` identified that three P01F cross-source evidence IDs were misassigned in the revised prose/ledgers (`P01F-P007` cited for 1 Cor 6:16 instead of `P01F-P009`; `P01F-P008` cited for 1 Cor 10:7 instead of `P01F-P011`; `P01F-P002` cited for Gal 3:13 instead of `P01F-P012`).
- **Correction:** Re-aligned all cross-source IDs across `primary_text_ledger.csv`, `relevance_scan.md`, `extraction.md`, `counterevidence.md`, and `notebooklm_self_audit.md` to match the accepted P01F canonical ledger:
  - Gen 2:24 / 1 Cor 6:16 -> `P01F-P009`
  - Exod 32:6 / 1 Cor 10:7 -> `P01F-P011`
  - Deut 21:23 / Gal 3:13 -> `P01F-P012`
  - Verified Rom 4:3 (`P01F-P001`) and Deut 25:4 / 1 Cor 9:9 (`P01F-P010`) remain accurate.
