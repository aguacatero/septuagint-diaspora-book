# P03F — Primary-Source Self-Audit

**Source ID:** P03F  
**Source Title:** *The Old Testament in Greek according to the Septuagint, Vol. III: Hosea–4 Maccabees*  
**Editor:** Henry Barclay Swete, D.D. (Cambridge University Press, 1894)  
**Source Class:** PRIMARY (Septuagint / Old Greek manual critical edition)  

---

## Audit Checks

1. **Exact Text & Diacritics:** Every Greek word, breathing, accent, and punctuation mark was checked against the high-resolution facsimile scans of Swete's 1894 Cambridge edition.
2. **Page Locators:** All page numbers (pp. 2, 3, 42, 122, 149, 151–152, 174) were verified directly against the running page headers, marginal book/chapter indicators, and printed footers of the volume.
3. **Apparatus Entries:** The 6 present apparatus units (Hos 1:10 on p. 2; Hos 2:23 on p. 3; Joel 2:32 on p. 42; Isa 28:16 on p. 149; Isa 29:14 on p. 152; Isa 40:13 on p. 174) were verified against the foot of the page, confirming uncial manuscript sigla (Codices B, א, A, Q, Γ, Z, correctors $B^*, B^{ab}, \aleph^*, \aleph^{c.a}, \aleph^{c.b}, A^*, A^a, Q^*, Q^{mg}$).
4. **Statements of Absence ("No Apparatus Entry"):** The single prophetic target with no apparatus entry at the target wording was directly confirmed by observing the variation units present on the page rather than inferred from the lack of commentary:
   - *Isaiah 11:10 (p. 122):* The apparatus at the foot of page 122 records only a scribal orthographic error in Codex A (`10 εθνω (sic) A`) and notes for 11:13–16 and 12:1–3; no entry exists for the target clause `ἡ ῥίζα τοῦ Ἰεσσαὶ καὶ ὁ ἀνιστάμενος ἄρχειν ἐθνῶν, ἐπ᾽ αὐτῷ ἔθνη ἐλπιοῦσιν`.
5. **Pentateuch Absences:** The 5 Pentateuch passages (Genesis 15:6, Genesis 2:24, Deuteronomy 25:4, Exodus 32:6, Deuteronomy 21:23) were verified as absent from Volume III (which covers Hosea through 4 Maccabees) and belonging properly to Volume I (*Genesis–IV Kings*, evaluated under accepted source P02F).
6. **Canonical Provenance Mapping:** Cross-source references to accepted P01F evidence strictly match the accepted canonical ledger rows:
   - Hos 2:23 / Rom 9:25 -> `P01F-P002`
   - Hos 1:10 / Rom 9:26 -> `P01F-P003`
   - Isa 28:16 / Rom 10:11 -> `P01F-P004`
   - Joel 2:32 / Rom 10:13 -> `P01F-P005`
   - Isa 40:13 / Rom 11:34 -> `P01F-P006`
   - Isa 11:10 / Rom 15:12 -> `P01F-P007`
   - Isa 29:14 / 1 Cor 1:19 -> `P01F-P008`

---

## Audit Verdict

**RESOLVED / ACCEPTED** (All itemized corrections incorporated into canonical ledger)

---

## Itemized Corrections

### 1. Page Span for Isaiah 29:14 (P03F-P007)
- **Observation:** Verse 14 is split across a page boundary: the verse begins at the bottom of Page 151 with the opening word `14 διά`, while the remainder of the verse (`τοῦτο ἰδοὺ προσθήσω τοῦ μεταθεῖναι τὸν λαὸν τοῦτον...`) and all textual apparatus entries for verse 14 appear at the top of Page 152.
- **Correction:** Locator is formally cited as `Pages 151–152` across `primary_text_ledger.csv`, `extraction.md`, `relevance_scan.md`, and `counterevidence.md`.

### 2. Disambiguation of Apparatus Notes in Isaiah 28:16 (P03F-P003)
- **Observation:** On page 149, `(θη sup ras A?vid)` is a distinct parenthetical note documenting that the letters `θη` of `καταισχυνθη` were written over an erasure in Codex Alexandrinus (A), whereas `οι γ' ... ου σπευσει Qmg` is the Hexaplaric reading of the Three (Aquila, Symmachus, Theodotion) recorded in the margin of Codex Marchalianus ($Q^{mg}$).
- **Correction:** Disambiguated the uncial correction of Codex A from the Hexaplaric marginal entry of $Q^{mg}$ in `primary_text_ledger.csv`, `extraction.md`, and `counterevidence.md`.

### 3. Latin Apparatus Precision in Isaiah 40:13 (P03F-P005)
- **Observation:** On page 174, the printed apparatus reads `συμβιβα] συμβιβασει אc.a (-βασι sed rurs ras σι) AQmgΓ`.
- **Correction:** Restored the printed Latin term `rurs` (*rursus*) to the apparatus reading: `(-βασι sed rurs ras σι)` across all ledgers.

### 4. Unaccented Apparatus Typography
- **Observation:** Swete’s apparatus prints Greek variant readings strictly without accents or breathings (e.g., `23 αγαπησω] ελεησω AQ | ηγαπημενην] ηλεημενην AQ` on p. 3; `10 κληθησονται] + εκει AQ` on p. 2).
- **Confirmation:** Swete's exact typographic convention of unaccented, unbreathed Greek typography is preserved across all apparatus entries in `primary_text_ledger.csv`, `extraction.md`, `relevance_scan.md`, and `counterevidence.md`.

### 5. Source-Bounded Primary Extraction & Scoped Witness Consensus
- **Confirmation:** All textual claims are source-bounded to Swete Vol. III. Witness consensus statements are explicitly scoped to "the witnesses collated by Swete at this locus (e.g. B, א, A, Q, Γ, Z as extant)."
