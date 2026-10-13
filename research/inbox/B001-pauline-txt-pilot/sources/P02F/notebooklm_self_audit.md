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
