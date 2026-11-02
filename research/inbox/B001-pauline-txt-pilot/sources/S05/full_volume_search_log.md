# S05 Full-Volume Search & Verification Log

**Source ID:** S05  
**Author:** Florian Wilk  
**Title:** *Die Bedeutung des Jesajabuches für Paulus* (FRLANT 179)  
**Imprint:** Göttingen: Vandenhoeck & Ruprecht, 1998  
**MDZ URN:** `urn:nbn:de:bvb:12-bsb00044375-3`  

## 1. Cryptographic Invariants & Source Integrity

- **Raw Scan Path:** `/Users/chrisrodriguez/Downloads/wilk_1998_jesaja_paulus_mdz_raw.pdf`
- **Raw Scan Bytes:** `96225856` (matches expected `96225856`)
- **Raw Scan SHA-256:** `700323565f6687163dc92f410779b054b763ee10bf3f745f5c2370b5455aa1b3` (matches expected `700323565f6687163dc92f410779b054b763ee10bf3f745f5c2370b5455aa1b3`)
- **Extracted Text Path:** `/tmp/wilk_full_text.txt`
- **Extracted Text Size:** `1470319` bytes, `1439712` characters, `31875` lines
- **Extracted Text SHA-256:** `d4f091259e403cf44a52c10e08944a24fd3b6a55c9069f53438898d05d1d4b62` (matches expected `d4f091259e403cf44a52c10e08944a24fd3b6a55c9069f53438898d05d1d4b62`)
- **Pagination Mapping:** `PDF page = Printed page + 12` uniformly across all 461 printed pages (TOC pp. VII-XII, Main text pp. 1-408, Literaturverzeichnis pp. 409-442, Stellenregister pp. 443-461).

## 2. Positive Control Verification

| Control Name | Regex Pattern | Expected Min | Actual Hits | Status |
| :--- | :--- | :---: | :---: | :---: |
| B001-4 Rom 10:11 / Isa 28:16 (Substantive locus pp. 47, 60-64, 162-166) | `\b(?:Rom\|Röm)\b\.?\s*(?:10\s*[:\.,]?\s*11\|1011\|lOll)\b` | 5 | 14 | PASSED |
| B001-6 Rom 11:34 / Isa 40:13 (Substantive locus pp. 268, 307-311, 358f.) | `\b(?:Rom\|Röm)\b\.?\s*(?:11\s*[:\.,]?\s*34\|1134)\b` | 5 | 12 | PASSED |
| B001-7 Rom 15:12 / Isa 11:10 (Substantive locus pp. 146-158, 169-171) | `\b(?:Rom\|Röm)\b\.?\s*(?:15\s*[:\.,]?\s*12\|1512\|15i2)\b` | 5 | 22 | PASSED |
| B001-8 1 Cor 1:19 / Isa 29:14 (Substantive locus pp. 101-105, 160-162) | `\b(?:1\s*Kor\|IKor)\b\.?\s*(?:1\s*[:\.,]?\s*19\|119)\b` | 5 | 30 | PASSED |
| B001-2 Rom 9:25 / Hos 2:23 [LXX 2:25] (Substantive locus pp. 34, 187, 211-214) | `\b(?:Rom\|Röm)\b\.?\s*(?:9\s*[:\.,]?\s*25\|925)\b` | 3 | 10 | PASSED |
| B001-3 Rom 9:26 / Hos 1:10 [LXX 2:1] (Substantive locus pp. 37, 51f., 185-188) | `\b(?:Rom\|Röm)\b\.?\s*(?:9\s*[:\.,]?\s*26\|926)\b` | 2 | 2 | PASSED |
| B001-5 Rom 10:13 / Joel 2:32 [LXX 3:5] (Substantive locus pp. 47, 61-64, 164f., 175) | `\b(?:Rom\|Röm)\b\.?\s*(?:10\s*[:\.,]?\s*13\|1013)\b` | 3 | 3 | PASSED |
| B001-12 Gal 3:13 assimilation note (Commentary footnote p. 47 n. 1, p. 94 n. 32) | `\bGal\b\.?\s*(?:3\s*[:\.,]?\s*[1l]3f?\|3[1l]3f?)\b` | 1 | 2 | PASSED |
| Stellenregister authorial heading (Printed p. 443) | `Stellenregister[\s\S]{0,100}Im\s+Register\s+bleiben` | 1 | 1 | PASSED |
| Index Section 1: Verzeichnis der untersuchten Zitate und Anspielungen | `V\s*e\s*r\s*z\s*e\s*i\s*c\s*h\s*n\s*i\s*s[\s\S]{0,60}Z\s*i\s*t\s*a\s*t\s*e` | 1 | 2 | PASSED |

## 3. Authorial Stellenregister Verification (pp. 443–461)

- **Stellenregister Start Offset:** `1406338`
- **Stellenregister End Offset:** `1435186`
- **Structural Sections Verified:** 8/8 passed

### Structural Sections Ledger

| Section Name | Found in Index |
| :--- | :---: |
| Zitate und Anspielungen heading | YES |
| Jesajabuches heading | YES |
| Paulinischen Briefe heading | YES |
| Uebrige Stellen heading | YES |
| Altes Testament heading | YES |
| Neues Testament heading | YES |
| Juedische Texte heading | YES |
| Christliche Texte heading | YES |

### Per-Locus Index Inventory

| Target ID | Passage | Expected in Index | Index Verification Status | Rationale / Locator |
| :--- | :--- | :---: | :--- | :--- |
| B001-1 | Romans 4:3 / Genesis 15:6 | NO | VERIFIED ABSENT (BOOK INDEXED; TARGET ABSENT) | None (unindexed; Rom 4:1, 4:6, 4:9-12 indexed, 4:3 absent; Gen 15:12 indexed, 15:6 absent) |
| B001-2 | Romans 9:25 / Hosea 2:23 | YES | VERIFIED INDEX ENTRY | Hosea 2:25 LXX indexed p. 448 (citing pp. 34, 37, 51f., 128ff., 185, 187f., 208, 211-214, 393); Rom 9:25 indexed p. 453 |
| B001-3 | Romans 9:26 / Hosea 1:10 | YES | VERIFIED INDEX ENTRY | Hosea 2:1 LXX indexed p. 448 (citing pp. 37, 51f., 128ff., 185-188, 208, 211-214, 393); Rom 9:26 indexed p. 453 |
| B001-4 | Romans 10:11 / Isaiah 28:16 | YES | VERIFIED INDEX ENTRY | Section 1.1 '2816 (Rom lOll)' p. 443; Section 1.2 'Rom lOll (2816)' p. 445 |
| B001-5 | Romans 10:13 / Joel 2:32 | YES | VERIFIED INDEX ENTRY | Joel 3:5 LXX indexed p. 448 (citing pp. 24, 47, 61f., 164f., 175, 390); Rom 10:13 indexed p. 453 |
| B001-6 | Romans 11:34 / Isaiah 40:13 | YES | VERIFIED INDEX ENTRY | Section 1.1 '4013 (Rom 1134)' p. 444; Section 1.2 'Rom 1134 (4013)' p. 445 |
| B001-7 | Romans 15:12 / Isaiah 11:10 | YES | VERIFIED INDEX ENTRY | Section 1.1 'llio (Rom 15i2)' p. 443; Section 1.2 'Rom 15i2 (llio)' p. 446 |
| B001-8 | 1 Corinthians 1:19 / Isaiah 29:14 | YES | VERIFIED INDEX ENTRY | Section 1.1 '2914 (IKor 119)' p. 443; Section 1.2 'IKor 119 (2914)' p. 446 |
| B001-9 | 1 Corinthians 6:16 / Genesis 2:24 | NO | VERIFIED ABSENT (BOOK INDEXED; TARGET ABSENT) | None (unindexed; 1 Cor 6:1, 6:4, 6:6 indexed, 6:16 absent; Gen 2:21 indexed, 2:24 absent) |
| B001-10 | 1 Corinthians 9:9 / Deuteronomy 25:4 | YES | VERIFIED INDEX ENTRY | 1 Cor 9:9 indexed p. 454 (citing p. 112); Deut 25:4 absent from OT index p. 447 |
| B001-11 | 1 Corinthians 10:7 / Exodus 32:6 | YES | VERIFIED INDEX ENTRY | 1 Cor 10:7 indexed p. 454 (citing p. 319); Exod 32:6 absent from OT index p. 447 |
| B001-12 | Galatians 3:13 / Deuteronomy 21:23 | YES | VERIFIED INDEX ENTRY | Gal 3:13 indexed p. 456 (citing p. 47); Deut 21:23 absent from OT index p. 447 |

## 4. Full-Volume Search & Dynamic Locus Adjudication

| Target ID | Passage Locus | Full-Volume Hits | Research Classification | Summary of Scholarly Findings |
| :--- | :--- | :---: | :--- | :--- |
| B001-1 | Romans 4:3 / Genesis 15:6 | 1 | NOT DISCUSSED | NOT DISCUSSED. Zero hits for Gen 15:6 anywhere in volume. Rom 4:3 appears once as incidental citation formula example (p. 94 n. 29). Unindexed. |
| B001-2 | Romans 9:25 / Hosea 2:23 | 17 | SUBSTANTIVE_DISCUSSION | SUBSTANTIVE DISCUSSION. Extracted in S05-E001 (pp. 34, 187, 211-214). Paul conflates Hos 2:25 and 2:1 LXX with chiasm and vocabulary assimilation. |
| B001-3 | Romans 9:26 / Hosea 1:10 | 6 | SUBSTANTIVE_DISCUSSION | SUBSTANTIVE DISCUSSION. Extracted in S05-E002 (pp. 37, 51f., 185-188, 208, 211-214). Conflated Hosea citation applied to Gentiles and Israel remnant. |
| B001-4 | Romans 10:11 / Isaiah 28:16 | 53 | SUBSTANTIVE_DISCUSSION | SUBSTANTIVE EXTENDED DISCUSSION. Extracted in S05-E003, S05-E004 (pp. 47, 60-64, 162-166, 224-226). G-R text with authorial pas prefix and indicative substitution. |
| B001-5 | Romans 10:13 / Joel 2:32 | 4 | SUBSTANTIVE_DISCUSSION | SUBSTANTIVE DISCUSSION. Extracted in S05-E005 (pp. 47, 61-64, 164f., 175). Verbatim OG Joel 3:5 linked with Isa 28:16 via pas catchword. |
| B001-6 | Romans 11:34 / Isaiah 40:13 | 28 | SUBSTANTIVE_DISCUSSION | SUBSTANTIVE EXTENDED DISCUSSION. Extracted in S05-E006, S05-E007 (pp. 268, 307-311, 358f.). Old Greek quotation with authorial e insertion splitting citation into two questions matching Rom 11:33. |
| B001-7 | Romans 15:12 / Isaiah 11:10 | 39 | SUBSTANTIVE_DISCUSSION | SUBSTANTIVE EXTENDED DISCUSSION. Extracted in S05-E008, S05-E009 (pp. 146-158, 169-171, 214f., 237-239). Verbatim Old Greek with deliberate theological omission of en te hemera ekeine. |
| B001-8 | 1 Corinthians 1:19 / Isaiah 29:14 | 41 | SUBSTANTIVE_DISCUSSION | SUBSTANTIVE EXTENDED DISCUSSION. Extracted in S05-E010, S05-E011 (pp. 101-105, 160-162, 246-248). Old Greek with deliberate substitution of atheteso for krypso from Ps 32:10 LXX. |
| B001-9 | 1 Corinthians 6:16 / Genesis 2:24 | 0 | NOT DISCUSSED | NOT DISCUSSED. Zero hits for 1 Cor 6:16 or Gen 2:24 in the entire volume. Unindexed. |
| B001-10 | 1 Corinthians 9:9 / Deuteronomy 25:4 | 1 | PASSING_REFERENCE | PASSING REFERENCE. 1 Cor 9:9 and Deut 25:4 cited on p. 112 n. 58 strictly as introductory citation-formula analogy; no substantive textual analysis. Deut 25:4 absent from OT index. |
| B001-11 | 1 Corinthians 10:7 / Exodus 32:6 | 2 | PASSING_REFERENCE | PASSING REFERENCE. 1 Cor 10:7 cited on p. 319 n. 11 for phrase 'phagein kai piein'; Exod 32:6 has zero hits, absent from OT index. |
| B001-12 | Galatians 3:13 / Deuteronomy 21:23 | 1 | PASSING_TEXT_CRITICAL_NOTE | PASSING TEXT-CRITICAL NOTE. Extracted in S05-E012 (p. 47 n. 1). Paul assimilated Deut 21:23a kekateramenos to Gal 3:10 epikataratos. Deut 21:23 absent from OT index. |

## 5. Certification of Verification

- **Verification Status:** `VERIFIED_COMPLETE`
- **Cryptographic Consistency:** Confirmed against authentic MDZ Digi20 scan.
- **Negative Search Discipline:** Zero unsupported negative claims. Non-prophetic loci B001-1 (Rom 4:3 / Gen 15:6) and B001-9 (1 Cor 6:16 / Gen 2:24) are confirmed absent from authorial index and substantive discussion; passing references (B001-10, B001-11, B001-12) are precisely localized.
