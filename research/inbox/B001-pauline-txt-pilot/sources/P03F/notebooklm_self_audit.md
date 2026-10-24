# P03F — Primary-Source Self-Audit

**Source ID:** P03F  
**Source Title:** *The Old Testament in Greek according to the Septuagint, Vol. III: Hosea–4 Maccabees*  
**Editor:** Henry Barclay Swete, D.D. (Cambridge University Press, 1894)  
**Source Class:** PRIMARY (Septuagint / Old Greek manual critical edition)  

---

## Audit Checks

1. **Exact Text & Diacritics:** Every Greek word, breathing, accent, and punctuation mark was checked against the high-resolution facsimile scans of Swete's 1894 Cambridge edition.
2. **Page Locators:** All page numbers (pp. 2, 3, 42, 122, 149, 151–152, 174) were verified directly against the running page headers, marginal book/chapter indicators, and printed footers of the volume.
3. **Apparatus Entries:** All 7 prophetic loci (Hos 1:10 on p. 2; Hos 2:23 on p. 3; Joel 2:32 on p. 42; Isa 11:10 on p. 122; Isa 28:16 on p. 149; Isa 29:14 on p. 152; Isa 40:13 on p. 174) have their apparatus entries verified against the foot of the page, confirming uncial manuscript sigla (Codices B, א, A, Q, Γ, Z, correctors $B^*, B^{ab}, \aleph^*, \aleph^{c.a}, \aleph^{c.b}, A^*, A^a, Q^*, Q^{mg}$).
4. **Apparatus Entry at Isaiah 11:10:** Classified as `apparatus_present=YES` because the apparatus at the foot of page 122 contains `10 εθνω (sic) A`, documenting a scribal form of `ἐθνῶν` inside the target quotation phrase; confirmed that no additional variant is reported for the target clause among the witnesses Swete could collate at this locus.
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

### 6. Apparatus Classification for Isaiah 11:10 (P03F-P006)
- **Review Finding:** Isaiah 11:10 was previously classified as having no apparatus entry, but the page 122 apparatus records `10 εθνω (sic) A` inside the target quotation phrase containing `ἐθνῶν`.
- **Correction:** Changed to `apparatus_present=YES` with `10 εθνω (sic) A` recorded across `primary_text_ledger.csv`, `relevance_scan.md`, `extraction.md`, and `counterevidence.md`, while confirming that no substantive lexical or syntactic variants occur for the target clause among the witnesses collated by Swete at this locus.

### 7. Scoped Textual Support for Joel 2:32 (P03F-P004)
- **Review Finding:** Target clause in Joel 2:32 was described as having "complete unanimity" / "complete verbatim agreement," but the apparatus records minor formal variation in Sinaiticus (`αν] εαν א` and `επικαληται א*` [-λεσηται אc.a, -λησηται אc.b]).
- **Correction:** Replaced "complete unanimity" with statements that B, A, Q, and corrected Sinaiticus (אc.a) support the quotation wording, while explicitly preserving the apparatus variants in Sinaiticus.

### 8. Reframing Origin and Direction-of-Dependence Claims
- **Review Finding:** Textual notes previously contained claims about priority, Pauline invention, or scribal harmonization that went beyond what Swete's manual edition alone can establish (Isa 28:16 "not invented by Paul"; Isa 40:13/14 "secondary Christian scribal harmonization"; Isa 29:14 "distinctively Pauline").
- **Correction:** Reframed all such claims into strictly source-bounded statements ("attested in Swete-collated Greek OT witnesses," "matches the accepted Pauline reading," "not attested among witnesses collated by Swete"); deferred causal hypotheses, priority determinations, and harmonization theories to cross-source synthesis.

### 9. Direction-of-Dependence Neutrality at Isaiah 40:13/14 (P03F-P005)
- **Review Finding (Comment 6253912403):** `primary_text_ledger.csv` previously stated `א* and A interpolate Rom 11:35 into verse 14` and `extraction.md` stated they `add the wording of Romans 11:35 into verse 14`, treating Romans as the source of insertion when Swete's apparatus alone does not establish direction of dependence.
- **Correction:** Replaced directional wording across `primary_text_ledger.csv`, `extraction.md`, `relevance_scan.md`, and `counterevidence.md` with neutral attestation: `Swete records an addition in א* and A at Isaiah 40:14 (+ η τις προεδωκεν αυτω και ανταποδοθησεται [-δωθ. A] αυτω) corresponding closely to the wording of Romans 11:35; this edition alone does not determine the origin or direction of dependence.`

### 10. Attested Editorial Method in `argument_map.md`
- **Review Finding (Comment 6253912403):** `argument_map.md` previously presented unlocated speculative assertions (`least harmonized`, `objectively verifiable`, `subjective eclecticism`) as Swete's editorial rationale and presented reconstructed inferences as if explicitly reasoned by the editor.
- **Correction:** Rewrote `argument_map.md` as a descriptive map of Swete's explicitly attested editorial method in the Prophetic literature. Removed all speculative assertions and strictly segregated claims into `SWETE EXPLICIT CLAIM` (with exact preface citations: pp. v, vi–vii, viii), `EDITION-LEVEL OBSERVATION` (with printed page numbers: pp. 3, 42, 122, 149, 174), and `REVIEWER INFERENCE`.

### 11. Editorial Method Atoms P03F-E004 and P03F-E005 Grounding
- **Review Finding (Comment 6253912403):** `citation_ledger.csv` marked P03F-E004 and P03F-E005 `VERIFIED` with short quotes that did not directly support the specific propositions (`The general principles...` did not verify manuscript archetype claim; `In the notes... use has been made of the Codex Marchalianus` did not substantiate apparatus typography).
- **Correction:** Corrected P03F-E004 to cite Swete's explicit incorporation of Volume I general principles (`Preface, p. v: "The general principles upon which the edition is based were stated in the preface to the first volume..."`) combined with direct printed page observation of manuscript orthography and itacisms (e.g. `Σειών` for `Σιών` at Joel 2:32, p. 42; Isa 28:16, p. 149). Corrected P03F-E005 to distinguish directly observed apparatus typography (Greek minuscules without breathings or accents across pp. 3, 42, 149, 174) from explicit authorial preface claims, removing the non-supporting quote and classifying it accurately. Aligned `extraction.md` Part 2 accordingly.

### 12. Negative-Apparatus Silence Qualified & Consensus Language Scoped (P03F-P006, P03F-P007)
- **Review Finding (Comment 6254690575):** `extraction.md` Part 3 item 2 previously over-interpreted silence in a negative apparatus ("silence in the apparatus denotes agreement with B"), conflicting with Swete's explicit warning regarding Codex Γ (Preface, p. viii: "it will be precarious for the reader of this edition to draw conclusions from the silence of Γ, which may be due to the impossibility of deciphering its testimony"). Furthermore, passage-level descriptions at Isaiah 11:10 (P03F-P006) and Isaiah 29:14 (P03F-P007) risked converting no variant reported into affirmative unanimity of B/א/A/Q/Γ where coverage or decipherability is not established. In addition, `argument_map.md` section 4 placed an edition observation under `SWETE EXPLICIT CLAIM`.
- **Correction:**
  1. Qualified `extraction.md` Part 3 item 2 to state that silence in a negative apparatus indicates no variant reported rather than automatically proving positive agreement, preserving Swete's warning on Γ and the requirement to establish presence and legibility at the locus.
  2. Revised consensus language across `primary_text_ledger.csv`, `relevance_scan.md`, `extraction.md`, and `counterevidence.md` for Isaiah 11:10 (P03F-P006) and Isaiah 29:14 (P03F-P007) to use "no additional variant is reported among the witnesses Swete could collate at this locus," retaining `10 εθνω (sic) A` (`apparatus_present=YES`) at Isa 11:10 and the negative finding for `ἀθετήσω` at Isa 29:14, strictly scoped to Swete's recorded data without claiming unverified manuscript unanimity.
  3. In `argument_map.md` section 4, moved the uncited statement regarding absence of New Testament discussions from `SWETE EXPLICIT CLAIM` to `EDITION-LEVEL OBSERVATION`.

