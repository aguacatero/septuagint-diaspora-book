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
- **Book Sections Coverage:** 13/13 required book/testament sections pattern-bounded with verified start and end delimiters (zero unbounded spillovers)

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

| Target ID | Passage Locus | Total Hits | Context Hits | Local Hits | Research Classification | Summary of Scholarly Findings |
| :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| B001-1 | Romans 4:3 / Genesis 15:6 | 1 | 0 | 0 | NOT DISCUSSED | NOT DISCUSSED. Zero hits for Gen 15:6 anywhere in volume. Rom 4:3 appears once as incidental citation formula example (p. 94 n. 29). Both verified absent from respective Stellenregister sections. |
| B001-2 | Romans 9:25 / Hosea 2:23 | 65 | 6 | 6 | SUBSTANTIVE_DISCUSSION | SUBSTANTIVE DISCUSSION. Verified by 6 local contextual hits and crosswalked to S05-E001 (pp. 130): In Romans 9:25, Paul quotes Hosea 2:25 LXX, applying future promise verbs to Gentile believers to demonstrate that their calling into God's mercy aligns with scriptural prophecy. |
| B001-3 | Romans 9:26 / Hosea 1:10 | 79 | 4 | 4 | SUBSTANTIVE_DISCUSSION | SUBSTANTIVE DISCUSSION. Verified by 4 local contextual hits and crosswalked to S05-E002 (pp. 129): Paul combines Hosea 2:1 LXX with Hosea 2:25 LXX in Romans 9:25-26 to establish that Gentiles receive divine sonship in the very location of their former alienation. |
| B001-4 | Romans 10:11 / Isaiah 28:16 | 53 | 3 | 2 | SUBSTANTIVE_DISCUSSION | SUBSTANTIVE DISCUSSION. Verified by 2 local contextual hits and crosswalked to S05-E003, S05-E004 (pp. 45, 164): In Romans 10:11, Paul modifies Isaiah 28:16bβ LXX by changing οὐ μὴ καταισχυνθῇ to οὐ καταισχυνθήσεται to harmonize with the future-tense framework of the surrounding context, and prefixes πᾶς to emphasize universal salvation; Paul interprets the 'stone in Zion' (Isaiah 28:16) christologically: in Romans 9:33 as a dual stumbling-stone/salvation figure, and in Romans 10:11 as an unmixed universal promise of vindication for all who believe. |
| B001-5 | Romans 10:13 / Joel 2:32 | 11 | 3 | 3 | SUBSTANTIVE_DISCUSSION | SUBSTANTIVE DISCUSSION. Verified by 3 local contextual hits and crosswalked to S05-E005 (pp. 61): In Romans 10:13, Paul quotes Joel 3:5a LXX verbatim, using πᾶς to connect with Isaiah 28:16 in Rom 10:11 and transferring the Old Testament formula for calling on the Lord God to the confession of Jesus as Lord. |
| B001-6 | Romans 11:34 / Isaiah 40:13 | 28 | 8 | 8 | SUBSTANTIVE_DISCUSSION | SUBSTANTIVE DISCUSSION. Verified by 8 local contextual hits and crosswalked to S05-E006, S05-E007 (pp. 307, 397): In Romans 11:34, Paul quotes Isaiah 40:13 LXX; Wilk hypothesizes that Paul likely inserted ἤ before τίς σύμβουλος to split the citation into a two-part rhetorical question matching the paired concepts of God's wisdom and knowledge in Romans 11:33; Paul uses Isaiah 40:13 in Romans 11:34 to highlight that God's sovereign and unexpected plan for Israel's salvation—encompassing temporary hardening and Gentile inclusion—transcends human comprehension. |
| B001-7 | Romans 15:12 / Isaiah 11:10 | 45 | 2 | 2 | SUBSTANTIVE_DISCUSSION | SUBSTANTIVE DISCUSSION. Verified by 2 local contextual hits and crosswalked to S05-E008, S05-E009 (pp. 46, 394): In Romans 15:12, Paul quotes the substantive clauses of Isaiah 11:10a LXX verbatim, deliberately omitting ἐν τῇ ἡμέρᾳ ἐκείνῃ because he considers the promised 'Root of Jesse' to have already appeared in Jesus Christ; Wilk notes textual reservations on a possible Hebraizing Vorlage; Paul places Isaiah 11:10 at the climax of his quotation chain in Romans 15:9–12 to demonstrate that Christ's reign over the Gentiles grounds the united praise of Jewish and Gentile believers. |
| B001-8 | 1 Corinthians 1:19 / Isaiah 29:14 | 44 | 5 | 2 | SUBSTANTIVE_DISCUSSION | SUBSTANTIVE DISCUSSION. Verified by 2 local contextual hits and crosswalked to S05-E010, S05-E011 (pp. 45, 393): In 1 Corinthians 1:19, Paul cites Isaiah 29:14b LXX, substituting ἀθετήσω ('I will set aside') for LXX κρύψω ('I will hide'), possibly influenced by Psalm 32:10 LXX, to express that God actively invalidates human wisdom; Paul uses Isaiah 29:14 in 1 Corinthians 1:19 as scriptural proof that God's saving act in the cross of Christ intentionally destroys human intellectual self-reliance as a means of knowing God. |
| B001-9 | 1 Corinthians 6:16 / Genesis 2:24 | 0 | 0 | 0 | NOT DISCUSSED | NOT DISCUSSED. Zero hits for 1 Cor 6:16 or Gen 2:24 in the entire volume. Both verified absent from respective Stellenregister sections. |
| B001-10 | 1 Corinthians 9:9 / Deuteronomy 25:4 | 1 | 0 | 0 | PASSING_REFERENCE | PASSING REFERENCE. 1 Cor 9:9 and Deut 25:4 cited on p. 112 n. 58 strictly as introductory citation-formula analogy; no substantive textual analysis. Deut 25:4 absent from OT index. |
| B001-11 | 1 Corinthians 10:7 / Exodus 32:6 | 2 | 0 | 0 | PASSING_REFERENCE | PASSING REFERENCE. 1 Cor 10:7 cited on p. 319 n. 11 for phrase 'phagein kai piein'; Exod 32:6 has zero hits, absent from OT index. |
| B001-12 | Galatians 3:13 / Deuteronomy 21:23 | 2 | 0 | 0 | PASSING_TEXT_CRITICAL_NOTE | PASSING TEXT-CRITICAL NOTE. Crosswalked to S05-E012 (p. 47 n. 1). Paul assimilated Deut 21:23a kekateramenos to Gal 3:10 epikataratos. Deut 21:23 absent from OT index. |

## 4.1 Grounded Argument Witness Records & Locality Correlation

### B001-2 — Romans 9:25 / Hosea 2:23

- **Evidence Record `S05-E001` (Printed p. 130; PDF p. 142):**
  - **Author Claim:** In Romans 9:25, Paul quotes Hosea 2:25 LXX, applying future promise verbs to Gentile believers to demonstrate that their calling into God's mercy aligns with scriptural prophecy.
  - **Verified Quotation:** `Indem es Heiden diejenigen 'Auszeichnungen' verheißend zuspricht, 'die Israel besaß und besitzt', erweist es die Berechtigung der paulinischen Darstellung...`
  - **Segment 1:** page offset `[200..358]` (matched `Indem es Heiden diejenigen 'Auszeichnungen' verheißend zuspr`)

### B001-3 — Romans 9:26 / Hosea 1:10

- **Evidence Record `S05-E002` (Printed p. 129; PDF p. 141):**
  - **Author Claim:** Paul combines Hosea 2:1 LXX with Hosea 2:25 LXX in Romans 9:25-26 to establish that Gentiles receive divine sonship in the very location of their former alienation.
  - **Verified Quotation:** `In der Tat kann der Apostel die Zitatkombination ihrem Wortlaut zufolge kaum anders denn als Rede über Heiden verstanden haben...`
  - **Segment 1:** page offset `[1478..1604]` (matched `In der Tat kann der Apostel die Zitatkombination ihrem Wortl`)

### B001-4 — Romans 10:11 / Isaiah 28:16

- **Evidence Record `S05-E003` (Printed p. 45; PDF p. 57):**
  - **Author Claim:** In Romans 10:11, Paul modifies Isaiah 28:16bβ LXX by changing οὐ μὴ καταισχυνθῇ to οὐ καταισχυνθήσεται to harmonize with the future-tense framework of the surrounding context, and prefixes πᾶς to emphasize universal salvation.
  - **Verified Quotation:** `Die rein stilistische Modifikation — Paulus schreibt 'οὐ καταισχυνθήσεται' statt 'οὐ μὴ καταισχυνθῇ' — dürfte in dem Bestreben begründet sein, das Zitat in das von Futura durchzogene Umfeld einzupassen.`
  - **Segment 1:** page offset `[1137..1345]` (matched `Die rein stilistische Modifikation - Paulus schreibt 'oü xaT`)
- **Evidence Record `S05-E004` (Printed p. 164; PDF p. 176):**
  - **Author Claim:** Paul interprets the 'stone in Zion' (Isaiah 28:16) christologically: in Romans 9:33 as a dual stumbling-stone/salvation figure, and in Romans 10:11 as an unmixed universal promise of vindication for all who believe.
  - **Verified Quotation:** `So begreift er beide Jesajaworte als Hinweise auf Christus, der als eine, in sich identische Person nach der einen Seite Juden und Heiden Gerechtigkeit verleiht...`
  - **Segment 1:** page offset `[1435..1617]` (matched `So begreift er beide Jesajaworte als Hinweise auf Christus, `)

### B001-5 — Romans 10:13 / Joel 2:32

- **Evidence Record `S05-E005` (Printed p. 61; PDF p. 73):**
  - **Author Claim:** In Romans 10:13, Paul quotes Joel 3:5a LXX verbatim, using πᾶς to connect with Isaiah 28:16 in Rom 10:11 and transferring the Old Testament formula for calling on the Lord God to the confession of Jesus as Lord.
  - **Verified Quotation:** `...demgegenüber unterstreicht die Anspielung auf Joel 35a die Verbindung von κύριος-Homologie und Rettung.`
  - **Segment 1:** page offset `[1099..1201]` (matched `demgegenüber unterstreicht die Anspielung auf Joel 35a die V`)

### B001-6 — Romans 11:34 / Isaiah 40:13

- **Evidence Record `S05-E006` (Printed p. 307; PDF p. 319):**
  - **Author Claim:** In Romans 11:34, Paul quotes Isaiah 40:13 LXX; Wilk hypothesizes that Paul likely inserted ἤ before τίς σύμβουλος to split the citation into a two-part rhetorical question matching the paired concepts of God's wisdom and knowledge in Romans 11:33.
  - **Verified Quotation:** `Angesichts der schwachen Bezeugung von ἤ in der 𝔊-Tradition steht zu vermuten, daß Paulus es in Rom 1134, zur Angleichung an 1135, selbst eingefügt hat.`
  - **Segment 1:** page offset `[1764..1921]` (matched `Angesichts der schwachen Bezeugung von fj in der ©-Tradition`)
- **Evidence Record `S05-E007` (Printed p. 397; PDF p. 409):**
  - **Author Claim:** Paul uses Isaiah 40:13 in Romans 11:34 to highlight that God's sovereign and unexpected plan for Israel's salvation—encompassing temporary hardening and Gentile inclusion—transcends human comprehension.
  - **Verified Quotation:** `...bringt es den wunderbaren Charakter des — von Menschen nur demütig nach- und mitzuvollziehenden — Heilshandelns Gottes an Israel gebündelt zur Sprache.`
  - **Segment 1:** page offset `[748..898]` (matched `bringt es den wunderbaren Charakter des - von Menschen nur d`)

### B001-7 — Romans 15:12 / Isaiah 11:10

- **Evidence Record `S05-E008` (Printed p. 46; PDF p. 58):**
  - **Author Claim:** In Romans 15:12, Paul quotes the substantive clauses of Isaiah 11:10a LXX verbatim, deliberately omitting ἐν τῇ ἡμέρᾳ ἐκείνῃ because he considers the promised 'Root of Jesse' to have already appeared in Jesus Christ; Wilk notes textual reservations on a possible Hebraizing Vorlage.
  - **Verified Quotation:** `Diese Zeitangabe kann entfallen, da nach Meinung des Apostels — wie sie in Röm 158 zum Ausdruck kommt — die verheißene 'Wurzel Isais' mit Jesus Christus bereits erschienen ist.`
  - **Segment 1:** page offset `[406..581]` (matched `Diese Zeitangabe kann entfallen, da nach Meinung des Apostel`)
- **Evidence Record `S05-E009` (Printed p. 394; PDF p. 406):**
  - **Author Claim:** Paul places Isaiah 11:10 at the climax of his quotation chain in Romans 15:9–12 to demonstrate that Christ's reign over the Gentiles grounds the united praise of Jewish and Gentile believers.
  - **Verified Quotation:** `Sie erklärt Christus — wie ihn sein Evangelium bezeugt... zum Garanten der Gemeinschaft von Juden- und Heidenchristen...`
  - **Segment 1:** page offset `[469..523]` (matched `Sie erklärt Christus - wie ihn sein Evangelium bezeugt`)
  - **Segment 2:** page offset `[614..673]` (matched `zum Garanten der Gemeinschaft von Juden- und Heidenchristen`)

### B001-8 — 1 Corinthians 1:19 / Isaiah 29:14

- **Evidence Record `S05-E010` (Printed p. 45; PDF p. 57):**
  - **Author Claim:** In 1 Corinthians 1:19, Paul cites Isaiah 29:14b LXX, substituting ἀθετήσω ('I will set aside') for LXX κρύψω ('I will hide'), possibly influenced by Psalm 32:10 LXX, to express that God actively invalidates human wisdom.
  - **Verified Quotation:** `Demgegenüber läßt das — vielleicht durch Ps 3210(𝔊) vermittelte — Wort ἀθετεῖν... den Sinn der jesajanischen Prophetie in ihrer paulinischen Deutung deutlicher zutage treten.`
  - **Segment 1:** page offset `[842..923]` (matched `Demgegenüber läßt das - vielleicht durch Ps 32lo(@) vermitte`)
  - **Segment 2:** page offset `[980..1071]` (matched `den Sinn der jesajanischen Prophetie in ihrer paulinischen D`)
- **Evidence Record `S05-E011` (Printed p. 393; PDF p. 405):**
  - **Author Claim:** Paul uses Isaiah 29:14 in 1 Corinthians 1:19 as scriptural proof that God's saving act in the cross of Christ intentionally destroys human intellectual self-reliance as a means of knowing God.
  - **Verified Quotation:** `Sie erlaubt es Paulus, das Gericht Gottes über die Weisheit jüdischer und hellenistischer Provenienz als notwendige Kehrseite des Heilsgeschehens in Christus darzustellen...`
  - **Segment 1:** page offset `[414..584]` (matched `Sie erlaubt es Paulus, das Gericht Gottes über die Weisheit `)

### B001-10 — 1 Corinthians 9:9 / Deuteronomy 25:4

- **Passing Witness (`PASSING_CITATION_FORMULA_ANALOGY`, Printed p. 112; PDF p. 124):**
  - **Witness Excerpt:** `Parallele hierzu findet sich nämlich in 99`

### B001-11 — 1 Corinthians 10:7 / Exodus 32:6

- **Passing Witness (`PASSING_PHRASE_COMPARISON`, Printed p. 319; PDF p. 331):**
  - **Witness Excerpt:** `Gebrauch des Ausdrucks „cpa^eiv xai iteiv" in 107`

### B001-12 — Galatians 3:13 / Deuteronomy 21:23

- **Evidence Record `S05-E012` (Printed p. 47; PDF p. 59):**
  - **Author Claim:** In Galatians 3:13, Paul substitutes ἐπικατάρατος for Old Greek κεκατηραμένος in Deuteronomy 21:23a to assimilate to the wording of Deuteronomy 27:26 as cited in Galatians 3:10.
  - **Verified Quotation:** `Eine Analogie bietet Gal 313, wo Paulus — zur Angleichung an das Dtn-Zitat in Gal 310 — das Dtn 2123a eröffnende Wort κεκατηραμένος gegen ἐπικατάρατος austauscht...`
  - **Segment 1:** page offset `[1604..1788]` (matched `Eine Analogie bietet Gal 313, wo Paulus - zur A n g l e i c `)

## 5. Certification of Verification

- **Verification Status:** `VERIFIED_COMPLETE`
- **Adjudication Method:** `SOURCE_BOUND_EVIDENCE_CROSSWALK_AND_CONTEXT_VALIDATION`
- **Cryptographic Consistency:** Confirmed against authentic MDZ Digi20 scan.
- **Stellenregister Coverage:** 13/13 required book/testament sections pattern-bounded with verified start and end delimiters and verified non-empty (zero unbounded spillovers).
- **Negative Search Discipline:** Zero unsupported negative claims. Non-prophetic loci B001-1 (Rom 4:3 / Gen 15:6) and B001-9 (1 Cor 6:16 / Gen 2:24) are confirmed absent from both authorial index and substantive discussion; passing references (B001-10, B001-11, B001-12) are precisely localized.
