# S02F — Full-Volume Negative Search Verification Log

**Source ID:** `S02F`

**Source Work:** William Sanday and Arthur C. Headlam, *A Critical and Exegetical Commentary on the Epistle to the Romans* (ICC; New York: Charles Scribner's Sons, 1895 [first edition]).

**Provenance Locator:** Internet Archive: `https://archive.org/details/epistlecommentar00sanduoft`

**Full Volume Raw File:** `sanday_headlam_1895_romans_icc_ia_raw.pdf`

**Raw File Size:** 47,318,528 bytes (586 pages)

**Raw File SHA-256:** `4a6369a0595550c8c1b92b71613a73182fe4a82aa02cfc989633e6c4dc0b80af`

**Extracted Text Layer:** `/tmp/sanday_headlam_full_text.txt` (31,081 lines, 298,622 words)

**Extracted Text SHA-256:** `c426418d349f4c6836ef59170a488351e18fb917abbcae58fd492ec53a0a2bb1`

**Extraction Tool:** Poppler `pdftotext -layout` 23.03.0

---

## Positive-Control Validation (19th-Century Citation Typography)

Before executing negative target queries, the regex engine was validated against authentic citation strings appearing in this volume to ensure that period-plus-space formatting, Roman chapter numerals, and abbreviation styles are accurately detected:

| Positive Control Passage | Target Regular Expression | Measured Matches | Validation Status |
|---|---|---|---|
| 1 Cor 3:19 (Excursus p. 302, Note p. 340) | `\b(?:1|I|First)\s*Cor(?:\.|inthians)?\s*(?:3|iii)[\.:,]?\s*(?:19|xix)\b` | 2 matches | **PASS (Detected)** |
| Gen 15:6 (Rom 4:3 commentary, pp. 100, 102) | `\b(?:Gen|Genesis)(?:\.|\b)\s*(?:15|xv)[\.:,]?\s*(?:6|vi)\b` | 10 matches | **PASS (Detected)** |
| Isa 40:13 (Rom 11:34 note, p. 340) | `\b(?:Isa|Is|Isaiah)(?:\.|\b)\s*(?:40|xl)[\.:,]?\s*(?:13|xiii)\b` | 1 matches | **PASS (Detected)** |
| Joel 2:32 (Rom 10:13 note, p. 291) | `\b(?:Joel)(?:\.|\b)\s*(?:2|ii)[\.:,]?\s*(?:32|xxxii)\b` | 1 matches | **PASS (Detected)** |
| Gal 4:22 (Excursus p. 303) | `\b(?:Gal|Galatians)(?:\.|\b)\s*(?:4|iv)[\.:,]?\s*(?:22|xxii)\b` | 1 matches | **PASS (Detected)** |

---

## Executive Summary of Results

| Locus ID | B001 Target Passage | NT Citation Matches | OT Citation Matches | Lemma Matches | Result Status |
|---|---|---|---|---|---|
| `B001-8` | 1 Corinthians 1:19 / Isaiah 29:14 | 0 matches | 0 matches | 0 matches | **NO MATCH FOUND BY DOCUMENTED FULL-VOLUME TEXT SEARCH** |
| `B001-9` | 1 Corinthians 6:16 / Genesis 2:24 | 0 matches | 0 matches | 0 matches | **NO MATCH FOUND BY DOCUMENTED FULL-VOLUME TEXT SEARCH** |
| `B001-10` | 1 Corinthians 9:9 / Deuteronomy 25:4 | 0 matches | 0 matches | 0 matches | **NO MATCH FOUND BY DOCUMENTED FULL-VOLUME TEXT SEARCH** |
| `B001-11` | 1 Corinthians 10:7 / Exodus 32:6 | 0 matches | 0 matches | 0 matches | **NO MATCH FOUND BY DOCUMENTED FULL-VOLUME TEXT SEARCH** |
| `B001-12` | Galatians 3:13 / Deuteronomy 21:23 | 1 matches | 0 matches | 0 matches | **MATCH DETECTED (1 hit(s): 1 NT, 0 OT, 0 lemma)** |

---

## Detailed Search Target Breakdown

### B001-8: 1 Corinthians 1:19 / Isaiah 29:14

- **Target Loci:** NT `1 Cor 1:19` | OT `Isa 29:14`
- **Measured Counts:** NT: `0` | OT: `0` | Lemma: `0` (Total: `0`)
- **Outcome Classification:** `NO MATCH FOUND BY DOCUMENTED FULL-VOLUME TEXT SEARCH`

| Pattern Description | Category | Regular Expression | Flag | Matches |
|---|---|---|---|---|
| NT citation (Arabic/Roman, whitespace-tolerant) | NT | `\b(?:1|I|First)\s*Cor(?:\.|inthians)?\s*(?:1|i)[\.:,]?\s*(?:19|xix)\b` | `re.IGNORECASE` | 0 |
| OT citation (Arabic/Roman, whitespace-tolerant) | OT | `\b(?:Isa|Is|Isaiah)(?:\.|\b)\s*(?:29|xxix)[\.:,]?\s*(?:14|xiv)\b` | `re.IGNORECASE` | 0 |
| Greek lemma / phrase | lemma | `ἀπολῶ\s+τὴν\s+σοφίαν` | `re.IGNORECASE` | 0 |
| Greek unaccented | lemma | `απολω\s+την\s+σοφιαν` | `re.IGNORECASE` | 0 |
| Greek keyword (ἀθετήσω) | lemma | `\bἀθετήσω\b` | `re.IGNORECASE` | 0 |
| English key phrase | lemma | `destroy\s+the\s+wisdom\s+of\s+the\s+wise` | `re.IGNORECASE` | 0 |

### B001-9: 1 Corinthians 6:16 / Genesis 2:24

- **Target Loci:** NT `1 Cor 6:16` | OT `Gen 2:24`
- **Measured Counts:** NT: `0` | OT: `0` | Lemma: `0` (Total: `0`)
- **Outcome Classification:** `NO MATCH FOUND BY DOCUMENTED FULL-VOLUME TEXT SEARCH`

| Pattern Description | Category | Regular Expression | Flag | Matches |
|---|---|---|---|---|
| NT citation (Arabic/Roman, whitespace-tolerant) | NT | `\b(?:1|I|First)\s*Cor(?:\.|inthians)?\s*(?:6|vi)[\.:,]?\s*(?:16|xvi)\b` | `re.IGNORECASE` | 0 |
| OT citation (Arabic/Roman, whitespace-tolerant) | OT | `\b(?:Gen|Genesis)(?:\.|\b)\s*(?:2|ii)[\.:,]?\s*(?:24|xxiv)\b` | `re.IGNORECASE` | 0 |
| Greek lemma / phrase | lemma | `σάρκα\s+μίαν` | `re.IGNORECASE` | 0 |
| Greek unaccented | lemma | `σαρκα\s+μιαν` | `re.IGNORECASE` | 0 |
| English key phrase | lemma | `two\s+shall\s+be\s+one\s+flesh` | `re.IGNORECASE` | 0 |

### B001-10: 1 Corinthians 9:9 / Deuteronomy 25:4

- **Target Loci:** NT `1 Cor 9:9` | OT `Deut 25:4`
- **Measured Counts:** NT: `0` | OT: `0` | Lemma: `0` (Total: `0`)
- **Outcome Classification:** `NO MATCH FOUND BY DOCUMENTED FULL-VOLUME TEXT SEARCH`

| Pattern Description | Category | Regular Expression | Flag | Matches |
|---|---|---|---|---|
| NT citation (Arabic/Roman, whitespace-tolerant) | NT | `\b(?:1|I|First)\s*Cor(?:\.|inthians)?\s*(?:9|ix)[\.:,]?\s*(?:9|ix)\b` | `re.IGNORECASE` | 0 |
| OT citation (Arabic/Roman, whitespace-tolerant) | OT | `\b(?:Deut|Dt|Deuteronomy)(?:\.|\b)\s*(?:25|xxv)[\.:,]?\s*(?:4|iv)\b` | `re.IGNORECASE` | 0 |
| Greek lemma / verb 1 | lemma | `φιμώσεις\s+βοῦν` | `re.IGNORECASE` | 0 |
| Greek lemma / verb 2 | lemma | `κημώσεις\s+βοῦν` | `re.IGNORECASE` | 0 |
| Greek root (unaccented) | lemma | `(?:φιμωσ|κημωσ)` | `re.IGNORECASE` | 0 |
| English key phrase | lemma | `muzzle\s+the\s+ox` | `re.IGNORECASE` | 0 |

### B001-11: 1 Corinthians 10:7 / Exodus 32:6

- **Target Loci:** NT `1 Cor 10:7` | OT `Exod 32:6`
- **Measured Counts:** NT: `0` | OT: `0` | Lemma: `0` (Total: `0`)
- **Outcome Classification:** `NO MATCH FOUND BY DOCUMENTED FULL-VOLUME TEXT SEARCH`

| Pattern Description | Category | Regular Expression | Flag | Matches |
|---|---|---|---|---|
| NT citation (Arabic/Roman, whitespace-tolerant) | NT | `\b(?:1|I|First)\s*Cor(?:\.|inthians)?\s*(?:10|x)[\.:,]?\s*(?:7|vii)\b` | `re.IGNORECASE` | 0 |
| OT citation (Arabic/Roman, whitespace-tolerant) | OT | `\b(?:Exod|Ex|Exodus)(?:\.|\b)\s*(?:32|xxxii)[\.:,]?\s*(?:6|vi)\b` | `re.IGNORECASE` | 0 |
| Greek lemma / phrase | lemma | `φαγεῖν\s+καὶ\s+πεῖν` | `re.IGNORECASE` | 0 |
| Greek unaccented | lemma | `φαγειν\s+και\s+πειν` | `re.IGNORECASE` | 0 |
| Greek play verb | lemma | `ἀνέστησαν\s+παίζειν` | `re.IGNORECASE` | 0 |
| English key phrase | lemma | `rose\s+up\s+to\s+play` | `re.IGNORECASE` | 0 |

### B001-12: Galatians 3:13 / Deuteronomy 21:23

- **Target Loci:** NT `Gal 3:13` | OT `Deut 21:23`
- **Measured Counts:** NT: `1` | OT: `0` | Lemma: `0` (Total: `1`)
- **Outcome Classification:** `MATCH DETECTED (1 hit(s): 1 NT, 0 OT, 0 lemma)`

| Pattern Description | Category | Regular Expression | Flag | Matches |
|---|---|---|---|---|
| NT citation (Arabic/Roman, whitespace-tolerant) | NT | `\b(?:Gal|Galatians)(?:\.|\b)\s*(?:3|iii)[\.:,]?\s*(?:13|xiii)\b` | `re.IGNORECASE` | 1 |
| OT citation (Arabic/Roman, whitespace-tolerant) | OT | `\b(?:Deut|Dt|Deuteronomy)(?:\.|\b)\s*(?:21|xxi)[\.:,]?\s*(?:23|xxiii)\b` | `re.IGNORECASE` | 0 |
| Greek lemma / phrase | lemma | `ἐπικατάρατος\s+πᾶς` | `re.IGNORECASE` | 0 |
| Greek unaccented | lemma | `επικαταρατος\s+πας` | `re.IGNORECASE` | 0 |
| Greek hang on tree | lemma | `κρεμάμενος\s+ἐπὶ\s+ξύλου` | `re.IGNORECASE` | 0 |
| English key phrase | lemma | `cursed\s+is\s+every(?:one)?\s+that\s+hangeth` | `re.IGNORECASE` | 0 |

#### Measured Match Snippets:
- *Snippet (offset 774582):* `...and endures the Wrath of God in his       stead (Gal. iii, 13; 2 Cor. v. 21). The Resurrection is proof that th...`

---

## Bibliographic Structure of the Authorial Index

Programmatic inspection of the authorial **Index to the Notes** (printed pp. 437–450) established the following bibliographic facts:
- **Index Present:** `True` (bounds: offset 1850437 to offset 1904030)
- **End Delimiter Verified:** `True`
- **Section I. Subjects (pp. 437–442):** Present (`True`)
- **Section II. Latin Words (pp. 443–444):** Present (`True`)
- **Section III. Greek Words (pp. 445–450):** Present (`True`)
- **Sections Ordered:** `True`
- **Dedicated Scripture Passage Index (Index Locorum):** None detected within the bounded index structure (pp. 437–450; subject to OCR and typographical limits). The authorial index is organized exclusively into I. Subjects, II. Latin Words, and III. Greek Words.
- **Subject Index Positive Controls:**
  - Entry `Abraham`: `True`
  - Entry `Adam`: `True`
  - Entry `Old Testament, Use of the`: `True`

---

## Scholarly Qualitative Assessment of Detected Hits

### Assessment for B001-12 (Galatians 3:13 / Deuteronomy 21:23)

- **Pattern Breakdown:** `1` NT citation match(es), `0` OT citation match(es), `0` lemma match(es).
- **Verified Source Context (Printed p. 118):** The single NT citation (`Gal. iii, 13`) occurs on printed page 118 in a theological note on Rom 4:25 summarizing E. Schäder's 1893 monograph (*Die Bedeutung des lebendigen Christus für die Rechtfertigung nach Paulus*). It is cited parenthetically alongside 2 Cor 5:21 as a dogmatic proof text for Christ enduring divine wrath.
- **Absence of Text-Critical Analysis:** The Old Testament Vorlage (Deut 21:23) is not cited (`0 matches`), Greek quotation wording (`ἐπικατάρατος πᾶς ὁ κρεμάμενος ἐπὶ ξύλου`) is not present (`0 matches`), and the textual divergence between Gal 3:13 and Deut 21:23 is not analyzed.

---

## Methodological & Technical Limitations

1. **Digital Text Layer Scope:** The search was executed across the 31,081-line text layer extracted from `sanday_headlam_1895_romans_icc_ia_raw.pdf` via Poppler `pdftotext -layout 23.03.0`.
2. **OCR and Typographical Quality:** Nineteenth-century Greek typography, accented characters, font ligatures, line breaks, hyphenations, or scan artifacts could hypothetically cause a regex pattern to miss an irregular typographical instance. Stripping accents and testing truncated stems (e.g. `φιμωσ`, `κημωσ`) mitigates this limitation.
3. **Epistemological Constraint:** While a negative OCR/regex search proves that no matching citation strings or diagnostic Greek/English phrases exist in the machine-readable digital text layer, it constitutes empirical negative text-search evidence rather than a metaphysical proof of non-existence in the authors' unexpressed thoughts.
4. **Scope Preservation:** While the five specific non-Romans B001 passage comparisons (and their Old Testament Vorlagen) are not analyzed in this Romans commentary (with Gal 3:13 appearing only once as an incidental parenthetical proof text on p. 118), the Excursus on 'St. Paul's Use of the Old Testament' (printed pp. 302–307) addresses cross-Pauline quotation practice globally, including Emil Kautzsch's (1869) 84-quotation taxonomy and 1 Cor 3:19 / Job 5:13. These cross-Pauline findings are preserved in `citation_ledger.csv` under `S02F-E010` through `S02F-E014`.
