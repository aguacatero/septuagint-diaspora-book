# B001 Open Notebook Manual

## Purpose and authority

This is the manual execution guide for `B001-pauline-txt-pilot` when Hermes cannot reliably operate Open Notebook itself.

The approved division of labor is:

**GitHub contract -> human-operated Open Notebook extraction -> Hermes/OpenRouter analysis -> adversarial review -> candidate research packet -> reviewer promotion.**

Open Notebook is a **source warehouse and extraction/navigation layer**, not the project manager and not the final classifier. Model-generated Notebook answers are not evidence. The underlying books, critical editions, page images, textual witnesses, and apparatuses are the evidence.

This guide is subordinate to, in order:

1. `docs/design/PROJECT_CONSTITUTION.md`
2. `research/registry/SCHEMA.md`
3. `research/TXT/README.md`
4. `research/TXT/textual_classifications.md`
5. `research/TXT/hebrew_consultation_test.md`
6. `research-queue/B001-pauline-txt-pilot.md`

If this guide conflicts with one of those files, the higher-level file governs.

---

# 1. Do not expand the scope

The active notebook is:

`SDP-01 Paul`

The active corpus is only these twelve cases:

| Batch ID | NT passage | Primary scriptural comparandum |
|---|---|---|
| `PAU-B001-01-TXT` | Romans 4:3 | Genesis 15:6 |
| `PAU-B001-02-TXT` | Romans 9:25 | Hosea 2:23 |
| `PAU-B001-03-TXT` | Romans 9:26 | Hosea 1:10 |
| `PAU-B001-04-TXT` | Romans 10:11 | Isaiah 28:16 |
| `PAU-B001-05-TXT` | Romans 10:13 | Joel 2:32 |
| `PAU-B001-06-TXT` | Romans 11:34 | Isaiah 40:13 |
| `PAU-B001-07-TXT` | Romans 15:12 | Isaiah 11:10 |
| `PAU-B001-08-TXT` | 1 Corinthians 1:19 | Isaiah 29:14 |
| `PAU-B001-09-TXT` | 1 Corinthians 6:16 | Genesis 2:24 |
| `PAU-B001-10-TXT` | 1 Corinthians 9:9 | Deuteronomy 25:4 |
| `PAU-B001-11-TXT` | 1 Corinthians 10:7 | Exodus 32:6 |
| `PAU-B001-12-TXT` | Galatians 3:13 | Deuteronomy 21:23 |

Do not start Mark, Matthew, Luke-Acts, John, diaspora sociolinguistics, Greco-Roman parallels, historical-Jesus material, or final book prose during B001.

---

# 2. Exact source packet to acquire

The list below is the **target B001 source packet**. Acquire the exact edition where lawfully accessible. If an exact item cannot be obtained, do not stall indefinitely: record it in `source_gaps.md`, identify the strongest lawful substitute, and state whether the gap limits classification.

Do not use piracy sites, DRM circumvention, fabricated URLs, or unauthorized copies.

## 2A. Primary textual and apparatus sources

These sources establish the textual data. They are not interchangeable with secondary scholarship.

### P01 — Pauline Greek New Testament

**Nestle-Aland, _Novum Testamentum Graece_, 28th revised edition (NA28). Deutsche Bibelgesellschaft, 2012.**

Preferred standard ISBN: `978-3-438-05140-0`.

Use for:

- exact Pauline Greek wording;
- NT textual variants and apparatus where material.

Open Notebook label:

`P01 — NA28 — Novum Testamentum Graece — 2012`

### P02 — Working Septuagint baseline

**Alfred Rahlfs; revised by Robert Hanhart, _Septuaginta: Id est Vetus Testamentum graece iuxta LXX interpretes_. Revised edition. Deutsche Bibelgesellschaft, 2006.**

ISBN: `978-3-438-05119-6`.

Use for:

- a consistent whole-corpus Greek baseline;
- navigation and first-pass comparison.

Do **not** treat Rahlfs-Hanhart as a substitute for the Göttingen critical editions when Göttingen is available for the relevant book.

Open Notebook label:

`P02 — Rahlfs-Hanhart — Septuaginta — 2006`

### P03 — Göttingen Genesis

**John William Wevers, ed., _Genesis_. Septuaginta: Vetus Testamentum Graecum I. Göttingen: Vandenhoeck & Ruprecht, 1974.**

Use for:

- Genesis 15:6;
- Genesis 2:24;
- Old Greek reconstruction and apparatus.

Open Notebook label:

`P03 — Göttingen LXX — Genesis — Wevers 1974`

### P04 — Göttingen Exodus

**John William Wevers, with Udo Quast, eds., _Exodus_. Septuaginta: Vetus Testamentum Graecum II/1. Göttingen: Vandenhoeck & Ruprecht, 1991.**

Use for:

- Exodus 32:6;
- Old Greek reconstruction and apparatus.

Open Notebook label:

`P04 — Göttingen LXX — Exodus — Wevers-Quast 1991`

### P05 — Göttingen Deuteronomy

**John William Wevers, with Udo Quast, eds., _Deuteronomium_. Septuaginta: Vetus Testamentum Graecum III/2. 2nd revised edition. Göttingen: Vandenhoeck & Ruprecht, 2006.**

Use for:

- Deuteronomy 25:4;
- Deuteronomy 21:23;
- Old Greek reconstruction and apparatus.

Open Notebook label:

`P05 — Göttingen LXX — Deuteronomium — Wevers-Quast 2006`

### P06 — Göttingen Twelve Prophets

**Joseph Ziegler, ed., _Duodecim Prophetae_. Septuaginta: Vetus Testamentum Graecum XIII. Use the 3rd edition (Göttingen, 1984) where available.**

Use for:

- Hosea 2:23;
- Hosea 1:10;
- Joel 2:32;
- Old Greek reconstruction and apparatus.

Open Notebook label:

`P06 — Göttingen LXX — Duodecim Prophetae — Ziegler 1984`

### P07 — Göttingen Isaiah

**Joseph Ziegler, ed., _Isaias_. Septuaginta: Vetus Testamentum Graecum XIV. 3rd edition. Göttingen: Vandenhoeck & Ruprecht, 1983.**

Use for:

- Isaiah 28:16;
- Isaiah 40:13;
- Isaiah 11:10;
- Isaiah 29:14;
- Old Greek reconstruction and apparatus.

Open Notebook label:

`P07 — Göttingen LXX — Isaias — Ziegler 1983`

### P08 — Hebrew baseline and apparatus

**Karl Elliger and Wilhelm Rudolph, eds.; 5th revised edition prepared by Adrian Schenker, _Biblia Hebraica Stuttgartensia_ (BHS). Deutsche Bibelgesellschaft, 1997.**

Preferred standard ISBN: `978-3-438-05218-6`.

Use for:

- Leningrad Codex / MT-type Hebrew wording;
- BHS apparatus;
- comparison against Greek witnesses.

Do not equate this medieval MT-type witness with “the Hebrew text Paul had.”

Open Notebook label:

`P08 — BHS — Biblia Hebraica Stuttgartensia — 1997`

### P09 — Qumran biblical witnesses

**Eugene Ulrich, ed., _The Biblical Qumran Scrolls: Transcriptions and Textual Variants_. Supplements to Vetus Testamentum 134. Leiden: Brill, 2010.**

ISBN: `978-90-04-18038-3`.

Use only where a relevant Qumran witness survives and materially bears on the case.

Open Notebook label:

`P09 — Ulrich — Biblical Qumran Scrolls — 2010`

---

## 2B. Core secondary scholarship on Paul and Scripture

These are the first books to ingest after the primary editions.

### S01 — Christopher D. Stanley

**Christopher D. Stanley, _Paul and the Language of Scripture: Citation Technique in the Pauline Epistles and Contemporary Literature_. Cambridge University Press, 1992.**

The CUP digital edition published in 2011 is acceptable if the original printed pagination is preserved and verified.

Priority: **REQUIRED CORE**.

Use for:

- citation technique;
- Paul's wording relative to known textual forms;
- authorial modification;
- memory versus written source questions;
- Romans, Corinthians, and Galatians quotation analysis.

Open Notebook label:

`S01 — Stanley — Paul and the Language of Scripture — 1992`

### S02 — Dietrich-Alex Koch

**Dietrich-Alex Koch, _Die Schrift als Zeuge des Evangeliums: Untersuchungen zur Verwendung und zum Verständnis der Schrift bei Paulus_. Beiträge zur historischen Theologie 69. Mohr, 1986.**

Original ISBN: `978-3-16-144990-1`.

An unrevised 2025 Mohr Siebeck eBook is acceptable if it preserves the original work and pagination is traceable.

Priority: **REQUIRED CORE**.

Use for:

- the textual basis of Paul's quotations;
- literalness/freedom in citation;
- Pauline scriptural usage across the major letters.

Open Notebook label:

`S02 — Koch — Die Schrift als Zeuge des Evangeliums — 1986`

### S03 — Richard B. Hays

**Richard B. Hays, _Echoes of Scripture in the Letters of Paul_. Yale University Press, 1989.**

A later Yale paperback is acceptable, but record the exact edition because pagination may differ.

Priority: **REQUIRED CORE**.

Use for:

- intertextual context;
- how Paul activates broader scriptural contexts;
- possible authorial adaptation and literary function.

Do not use Hays alone to settle textual provenance.

Open Notebook label:

`S03 — Hays — Echoes of Scripture in the Letters of Paul — 1989`

### S04 — J. Ross Wagner

**J. Ross Wagner, _Heralds of the Good News: Isaiah and Paul “In Concert” in the Letter to the Romans_. Supplements to Novum Testamentum 101. Leiden: Brill, 2002.**

ISBN: `978-90-04-11691-7`.

Priority: **REQUIRED FOR ROMANS/ISAIAH CASES**.

Especially relevant to:

- Romans 10:11 / Isaiah 28:16;
- Romans 11:34 / Isaiah 40:13;
- Romans 15:12 / Isaiah 11:10;
- the larger Isaiah texture of Romans 9–11 and 15.

Open Notebook label:

`S04 — Wagner — Heralds of the Good News — 2002`

### S05 — Florian Wilk

**Florian Wilk, _Die Bedeutung des Jesajabuches für Paulus_. Forschungen zur Religion und Literatur des Alten und Neuen Testaments 179. Göttingen: Vandenhoeck & Ruprecht, 1998.**

ISBN: `978-3-525-53863-0`.

Priority: **REQUIRED FOR ISAIAH CASES**.

Use as an independent specialist treatment of Isaiah in Paul.

Open Notebook label:

`S05 — Wilk — Die Bedeutung des Jesajabuches für Paulus — 1998`

### S06 — Steve Moyise

**Steve Moyise, _Paul and Scripture: Studying the New Testament Use of the Old Testament_. Baker Academic / SPCK, 2010.**

North American ISBN: `978-0-8010-3924-9`.

Priority: **REQUIRED ORIENTATION / BIBLIOGRAPHY DISCOVERY**.

Use for:

- orientation to debates;
- identifying specialist sources;
- comparison of scholarly positions.

Do not let this general survey serve as one of the two specialist passage treatments unless it actually gives substantive passage-specific analysis.

Open Notebook label:

`S06 — Moyise — Paul and Scripture — 2010`

---

## 2C. Required letter-level commentaries

These are gap-fillers and independent passage-level checks. Use them when they discuss textual provenance, quotation form, or Pauline adaptation—not merely general theology.

### S07 — Romans commentary

**C. E. B. Cranfield, _A Critical and Exegetical Commentary on the Epistle to the Romans_. International Critical Commentary. Vol. I, 1975; Vol. II, 1979. T&T Clark.**

Use:

- Vol. I for Romans 4:3;
- Vol. II for Romans 9:25, 9:26, 10:11, 10:13, 11:34, and 15:12.

Open Notebook labels:

`S07a — Cranfield — Romans ICC Vol 1 — 1975`

`S07b — Cranfield — Romans ICC Vol 2 — 1979`

### S08 — 1 Corinthians commentary

**Anthony C. Thiselton, _The First Epistle to the Corinthians_. New International Greek Testament Commentary. Eerdmans, 2000.**

Print ISBN: `978-0-8028-2449-3`.

Use for:

- 1 Corinthians 1:19;
- 1 Corinthians 6:16;
- 1 Corinthians 9:9;
- 1 Corinthians 10:7.

Open Notebook label:

`S08 — Thiselton — First Epistle to the Corinthians — 2000`

### S09 — Galatians commentary

**J. Louis Martyn, _Galatians: A New Translation with Introduction and Commentary_. Anchor Bible 33A. Doubleday, 1997.**

ISBN: `978-0-385-08838-1`.

Use especially for:

- Galatians 3:13 / Deuteronomy 21:23.

Open Notebook label:

`S09 — Martyn — Galatians — 1997`

---

## 2D. Required specialist gap-fillers for the Pentateuch and Minor Prophets

These sources reduce reliance on general Pauline monographs and provide focused textual context.

### S10 — Wevers on Genesis

**John William Wevers, _Notes on the Greek Text of Genesis_. Septuagint and Cognate Studies 35. Scholars Press, 1993.**

Use for Genesis 15:6 and Genesis 2:24.

Open Notebook label:

`S10 — Wevers — Notes on Greek Genesis — 1993`

### S11 — Wevers on Exodus

**John William Wevers, _Notes on the Greek Text of Exodus_. Scholars Press / SBL, 1990.**

Use for Exodus 32:6.

Open Notebook label:

`S11 — Wevers — Notes on Greek Exodus — 1990`

### S12 — Wevers on Deuteronomy

**John William Wevers, _Notes on the Greek Text of Deuteronomy_. Septuagint and Cognate Studies. Scholars Press / SBL, 1995.**

Use for Deuteronomy 25:4 and Deuteronomy 21:23.

Open Notebook label:

`S12 — Wevers — Notes on Greek Deuteronomy — 1995`

### S13 — Minor Prophets in the New Testament

**Maarten J. J. Menken and Steve Moyise, eds., _The Minor Prophets in the New Testament_. Library of New Testament Studies 377. T&T Clark, 2009.**

ISBN: `978-0-567-03305-5`.

Especially use the Pauline treatment for:

- Romans 9:25 / Hosea 2:23;
- Romans 9:26 / Hosea 1:10;
- Romans 10:13 / Joel 2:32.

Open Notebook label:

`S13 — Menken-Moyise — Minor Prophets in the New Testament — 2009`

### S14 — Deuteronomy in the New Testament

**Steve Moyise and Maarten J. J. Menken, eds., _Deuteronomy in the New Testament_. Library of New Testament Studies 358. T&T Clark International, 2007.**

Print ISBN: `978-0-567-04549-2`.

Especially use the chapters on Paul for:

- 1 Corinthians 9:9 / Deuteronomy 25:4;
- Galatians 3:13 / Deuteronomy 21:23.

Open Notebook label:

`S14 — Moyise-Menken — Deuteronomy in the New Testament — 2007`

---

# 3. Source sufficiency rule

The source list above is a **target packet**, not permission to pretend every source discusses every passage.

For each of the twelve B001 passages, final classification requires:

1. the best available primary textual evidence;
2. at least **two substantive specialist scholarly treatments** relevant to Paul's use of the passage or the specific textual problem;
3. visible disagreement/counterevidence when it exists.

A book counts toward the two-treatment minimum **only if it actually discusses the relevant passage or textual problem substantively**.

If Stanley says nothing about a passage, his book does not count for that passage. If a commentary merely paraphrases the verse without discussing textual provenance or quotation technique, it does not count either.

When fewer than two qualifying treatments remain after the packet above is extracted:

1. search the bibliographies of S01–S14;
2. acquire the most relevant peer-reviewed article, specialist monograph chapter, or critical commentary section;
3. ingest it into `SDP-01 Paul`;
4. run the same secondary-source extraction prompt below;
5. record the acquisition in `acquisition_manifest.csv` and `source_manifest.csv`.

Do not use web summaries as the second specialist source.

---

# 4. Step-by-step Open Notebook workflow

## Step 1 — Create or open the notebook

Open Notebook and create or reuse:

`SDP-01 Paul`

Do not create twelve separate notebooks unless source isolation is impossible in your Open Notebook build.

## Step 2 — Acquire sources lawfully

For each P01–P09 and S01–S14 item:

1. locate the exact edition;
2. prefer publisher, university, scholarly project, institutional repository, JSTOR, Internet Archive/Open Library where lawful, or your own legitimate library copy;
3. record unavailable items immediately rather than forgetting them;
4. do not substitute editions silently.

If a source is borrow-only and cannot be reliably imported or inspected, mark it `BORROW_REQUIRED` or `MANUAL_ACCESS_REQUIRED` and continue with the strongest lawful substitute.

## Step 3 — Verify the file before ingestion

Before uploading each source:

1. inspect the title page;
2. inspect the copyright/publication page;
3. confirm author/editor, title, publisher, year, edition/volume;
4. record ISBN/DOI/stable identifier where available;
5. inspect at least one page containing Greek/Hebrew or apparatus symbols;
6. determine whether printed page numbers match PDF page numbers;
7. note missing or illegible pages;
8. note whether OCR corrupts Greek, Hebrew, accents, sigla, superscripts, or apparatus notation.

For scanned critical editions, page images outrank OCR.

## Step 4 — Ingest and label consistently

Import the full text when lawfully available.

Rename or label the source using the exact `P##` / `S##` labels above.

Do not use filenames like `book.pdf`, `scan2.pdf`, or `romans.pdf`.

## Step 5 — Verify Open Notebook retrieval

After ingestion:

1. search a phrase you can see on a known printed page;
2. confirm Open Notebook retrieves the correct source;
3. confirm the displayed/extracted text can be mapped back to the printed page;
4. for Greek/Hebrew, compare at least one retrieved passage against the page image;
5. set `page_mapping_verified = true` only when this works.

If retrieval is poor, mark `INGESTED_WITH_LIMITATIONS` rather than pretending it is reliable.

## Step 6 — Extract each secondary book separately

For **each S01–S14 source**, isolate that source in Open Notebook.

Preferred method:

- select only the one source being queried.

If your Open Notebook version does not support source scoping:

- temporarily disable/unselect all other sources; or
- use a temporary isolation notebook for that one source.

Do not accept a “per-book extraction” that quietly cites multiple sources.

Run **Prompt A** below unchanged.

## Step 7 — Save each secondary extraction

Save/copy the result into:

`research/inbox/B001-pauline-txt-pilot/open-notebook-extractions/secondary/`

Use filenames such as:

- `S01-stanley-1992.md`
- `S02-koch-1986.md`
- `S03-hays-1989.md`
- `S04-wagner-2002.md`
- `S05-wilk-1998.md`
- `S06-moyise-2010.md`
- `S07a-cranfield-romans-v1-1975.md`
- `S07b-cranfield-romans-v2-1979.md`
- `S08-thiselton-1corinthians-2000.md`
- `S09-martyn-galatians-1997.md`
- `S10-wevers-genesis-1993.md`
- `S11-wevers-exodus-1990.md`
- `S12-wevers-deuteronomy-1995.md`
- `S13-minor-prophets-nt-2009.md`
- `S14-deuteronomy-nt-2007.md`

If a source is unavailable, create no fake extraction. Record the gap.

## Step 8 — Extract the primary editions separately

For **each P01–P09 source**, isolate the source and run **Prompt B** below unchanged.

Save/copy the results into:

`research/inbox/B001-pauline-txt-pilot/open-notebook-extractions/primary/`

Use filenames matching the source IDs, e.g.:

- `P01-na28-2012.md`
- `P03-gottingen-genesis-1974.md`
- `P07-gottingen-isaiah-1983.md`
- `P08-bhs-1997.md`

## Step 9 — Manually verify primary-language claims

Before passing the extraction to Hermes:

1. open every page used for an exact Greek/Hebrew reading;
2. visually compare the Open Notebook transcription to the page image;
3. manually correct only when you can see the source clearly;
4. annotate the correction as manual verification;
5. do not guess an apparatus symbol or reconstruct missing text from memory.

Use:

`MANUAL IMAGE VERIFICATION REQUIRED`

whenever a reading remains uncertain.

## Step 10 — Check scholarly coverage passage by passage

Make a simple working matrix with the twelve B001 IDs as rows and S01–S14 as columns.

Mark a source only when the extraction says `Discussed: YES` and the discussion is substantive to textual provenance, quotation form, authorial adaptation, or direct-Hebrew relevance.

If any passage has fewer than two qualifying secondary treatments, acquire a passage-specific source before final classification.

## Step 11 — Run the cross-source dossier prompt once

After all available P01–P09 and S01–S14 sources have been ingested and per-source extractions are complete:

1. enable/select the full verified B001 source packet;
2. run **Prompt C** below once;
3. save the output as:

`research/inbox/B001-pauline-txt-pilot/open-notebook-extractions/B001-cross-source-dossier.md`

This dossier is a navigation/synthesis aid. It does not replace the per-source extractions or underlying pages.

## Step 12 — Hand control back to Hermes

Once the extractions are saved, tell Hermes to resume the B001 batch using **Prompt D** below.

Hermes must then:

- read the governing repo files;
- inspect the manual Open Notebook extraction packet;
- verify source/page support;
- perform the TXT classifications;
- run the direct-Hebrew test;
- conduct an adversarial pass;
- build the required B001 research packet;
- commit only to `research/B001-pauline-txt-pilot`;
- stop before canonical registry promotion or merge.

---

# 5. Prompt A — exact secondary-source extraction prompt

Copy this prompt unchanged for every scholarly monograph, article, edited-volume chapter, or commentary source.

```text
You are performing SOURCE EXTRACTION for Batch B001 of the research project Shaped by the Septuagint.

Use ONLY the currently selected source.

Do not use general knowledge, other notebook sources, remembered scholarship, or assumptions about this author's views.

Your task is NOT to prove or disprove the project's hypothesis and NOT to assign the project's final classification. Your task is to extract exactly what this source says and the evidence it uses.

If the source does not explicitly discuss a requested passage or textual issue, write:

NOT DISCUSSED

Do not infer a position from the author's general theology or from what other scholars say the author believes.

## B001 passages

PAU-B001-01-TXT — Romans 4:3 / Genesis 15:6
PAU-B001-02-TXT — Romans 9:25 / Hosea 2:23
PAU-B001-03-TXT — Romans 9:26 / Hosea 1:10
PAU-B001-04-TXT — Romans 10:11 / Isaiah 28:16
PAU-B001-05-TXT — Romans 10:13 / Joel 2:32
PAU-B001-06-TXT — Romans 11:34 / Isaiah 40:13
PAU-B001-07-TXT — Romans 15:12 / Isaiah 11:10
PAU-B001-08-TXT — 1 Corinthians 1:19 / Isaiah 29:14
PAU-B001-09-TXT — 1 Corinthians 6:16 / Genesis 2:24
PAU-B001-10-TXT — 1 Corinthians 9:9 / Deuteronomy 25:4
PAU-B001-11-TXT — 1 Corinthians 10:7 / Exodus 32:6
PAU-B001-12-TXT — Galatians 3:13 / Deuteronomy 21:23

For every passage the source actually discusses, extract the following.

### 1. Location
- Printed page number(s)
- Chapter/section if identifiable
- PDF page number only as a secondary locator
- If printed pagination cannot be verified, write PAGE NOT VERIFIED

### 2. Author's textual-source position
State only what the author actually argues concerning the form of Scripture behind Paul's wording.

Distinguish where possible among:
- Old Greek / Septuagint
- another Jewish Greek textual form or revision
- Hebrew textual evidence
- alternative Hebrew Vorlage
- mixed/composite quotation
- quotation from memory
- oral/liturgical transmission
- authorial alteration or adaptation
- unknown textual intermediary
- indeterminate

Do NOT translate one of these categories into a project classification unless the author explicitly makes that claim.

### 3. Primary textual evidence used by the author
Record all concrete evidence the author invokes, including when available:
- Pauline Greek wording
- Old Greek / Septuagint wording
- other Greek readings or revisions
- Hebrew wording or witnesses
- Dead Sea Scroll / Qumran evidence
- manuscript variants
- critical-apparatus information
- differences in vocabulary
- differences in syntax
- differences in word order
- omissions
- additions
- conflations
- grammatical changes

Preserve Greek and Hebrew forms exactly as printed when reliable extraction is possible.

If OCR appears unreliable, write MANUAL IMAGE VERIFICATION REQUIRED rather than silently correcting it.

### 4. Discriminating features
Explain which textual features the author regards as actually useful for identifying Paul's source and which agreements are non-discriminating because they occur in multiple textual traditions.

### 5. Paul's modification of the source
Record whether the author thinks Paul:
- quotes relatively exactly;
- alters wording intentionally;
- assimilates one text to another;
- combines texts;
- adapts grammar to his argument;
- cites from memory;
- or cannot confidently be separated from his textual source.

Give the author's reasoning.

### 6. Direct-Hebrew relevance
Does the author claim or imply that Paul directly consulted Hebrew Scripture for this passage?

If YES:
- state the exact reasoning;
- identify what evidence is specifically Hebrew-dependent;
- record whether Greek alternatives are considered.

If NO:
- record what textual mechanism the author thinks explains the reading instead.

If the author does not address direct Hebrew consultation, write NOT ADDRESSED.

### 7. Counterevidence and uncertainty
Extract anything in the source that weakens its own preferred explanation:
- competing readings;
- textual uncertainty;
- alternative reconstructions;
- disagreements with other scholars;
- ambiguous evidence;
- lost or unknown textual forms;
- uncertainty about Paul's Vorlage.

Do not omit qualifications.

### 8. Scholarly disagreement
Identify scholars the author cites who disagree materially about the textual form or quotation technique.

For each:
- scholar;
- work if supplied;
- position attributed to them;
- page/footnote where this discussion occurs.

Do not treat the author's characterization as verification of the other scholar's original position.

### 9. Bibliography leads
List every cited article, monograph, commentary, critical edition, or textual study that appears especially relevant to this B001 passage and should be acquired separately.

Include complete citation information when the source supplies it.

### 10. Short supporting quotations
Provide up to three short quotations from the source that most clearly capture its argument.

Each quotation must:
- be no longer than 25 words;
- include the printed page number;
- reproduce the source exactly.

If exact wording cannot be verified, omit the quotation.

## Output format

Begin with:

# SOURCE IDENTITY

Author/editor:
Title:
Publication:
Year:
Edition/volume:
Language:
Printed pagination verified: YES / NO
Extraction limitations:

Then create one section for EACH of the twelve B001 IDs.

Example:

## PAU-B001-01-TXT — Romans 4:3 / Genesis 15:6

Discussed: YES / NO

Pages:

Author's textual-source position:

Primary textual evidence:

Discriminating features:

Pauline adaptation/citation technique:

Direct-Hebrew relevance:

Counterevidence/uncertainty:

Scholarly disagreement:

Bibliography leads:

Short supporting quotations:

Extraction notes:

If the passage is not discussed, include only:

Discussed: NO
NOT DISCUSSED

Finally provide:

# SOURCE-WIDE METHODOLOGICAL CLAIMS

Extract claims from this book that affect how Paul's quotation technique should generally be analyzed, especially:
- whether Paul normally works from Greek Scripture;
- degree of freedom in quotation;
- textual pluriformity;
- memory versus written copies;
- revision or alternative Greek forms;
- ability to reconstruct Paul's Vorlage;
- limits on inferring Hebrew consultation.

Every claim must have printed-page support.

# B001 BIBLIOGRAPHY LEADS

Consolidate the most important sources cited by this author that should be added to the research corpus.

# UNRESOLVED EXTRACTION PROBLEMS

Record illegible Greek/Hebrew, uncertain pagination, inaccessible pages, OCR problems, unclear citations, or places where source verification is required.

Do not fill these gaps from memory.
```

---

# 6. Prompt B — exact primary-text / apparatus extraction prompt

Copy this prompt unchanged for NA28, Rahlfs-Hanhart, each Göttingen volume, BHS, Qumran textual editions, and other primary/critical editions.

```text
You are extracting PRIMARY TEXTUAL EVIDENCE for Batch B001 of Shaped by the Septuagint.

Use ONLY the currently selected primary text, critical edition, apparatus, manuscript reference work, or textual edition.

Do not use secondary scholarship or model memory to fill missing information.

The B001 comparisons are:

PAU-B001-01-TXT — Romans 4:3 / Genesis 15:6
PAU-B001-02-TXT — Romans 9:25 / Hosea 2:23
PAU-B001-03-TXT — Romans 9:26 / Hosea 1:10
PAU-B001-04-TXT — Romans 10:11 / Isaiah 28:16
PAU-B001-05-TXT — Romans 10:13 / Joel 2:32
PAU-B001-06-TXT — Romans 11:34 / Isaiah 40:13
PAU-B001-07-TXT — Romans 15:12 / Isaiah 11:10
PAU-B001-08-TXT — 1 Corinthians 1:19 / Isaiah 29:14
PAU-B001-09-TXT — 1 Corinthians 6:16 / Genesis 2:24
PAU-B001-10-TXT — 1 Corinthians 9:9 / Deuteronomy 25:4
PAU-B001-11-TXT — 1 Corinthians 10:7 / Exodus 32:6
PAU-B001-12-TXT — Galatians 3:13 / Deuteronomy 21:23

Only report passages for which this source contains relevant primary textual evidence.

For each relevant passage:

1. Identify the edition, volume, editor, year, and textual tradition represented.

2. Give the exact ancient-language wording relevant to the comparison.

3. Preserve orthography and word order as printed where possible.

4. Identify significant variants or apparatus entries.

For every variant record:
- witness or witness group;
- reading;
- whether the reading is Old Greek, a later Greek revision, Hebrew witness, MT-type witness, DSS/Qumran witness, or another textual form when the edition identifies it;
- location in the apparatus;
- printed page or section.

5. Do NOT collapse all Greek witnesses into “the LXX.”

Clearly distinguish:
- reconstructed Old Greek;
- Greek revisions;
- alternate Greek witnesses;
- uncertain readings.

6. Do NOT collapse all Hebrew evidence into “the Masoretic Text.”

Clearly distinguish:
- medieval MT-type text;
- DSS/Qumran witnesses;
- other attested Hebrew readings;
- reconstructed or proposed Hebrew Vorlagen.

7. Identify every feature that could discriminate among Paul's possible textual sources:
- lexical agreement;
- morphology;
- syntax;
- word order;
- addition;
- omission;
- pronouns;
- divine names/titles;
- number;
- tense/aspect;
- conflation;
- unique wording.

8. Do not interpret Paul's motives unless the selected source itself contains commentary.

9. If Greek/Hebrew OCR is uncertain, write:
MANUAL IMAGE VERIFICATION REQUIRED

10. If an apparatus symbol or reading cannot be reliably interpreted, reproduce what can be read and write:
APPARATUS INTERPRETATION NOT VERIFIED

11. Never reconstruct a missing reading from memory.

Output:

# SOURCE IDENTITY

Edition:
Editor(s):
Volume:
Year:
Textual tradition:
Pagination verified:
OCR/image limitations:

# RELEVANT B001 PASSAGES

For each applicable ID:

## [B001 ID]

Passage:

Exact wording:

Relevant variants/witnesses:

Discriminating features visible in this source:

Apparatus notes:

Printed page/section:

Manual verification required:

# SOURCE LIMITATIONS

List anything this edition cannot establish by itself.
```

---

# 7. Prompt C — exact cross-source dossier prompt

Run this once only after per-source extraction is complete.

```text
Using ONLY the verified sources currently contained in this Open Notebook, construct a source dossier for each of the twelve B001 Pauline quotation cases.

Do not attempt to prove the project's hypothesis.

Do not erase disagreement between sources.

Do not treat model synthesis as evidence.

For each B001 case, produce:

1. NT passage and proposed scriptural comparandum.

2. Primary textual evidence:
- Pauline Greek;
- reconstructed Old Greek where available;
- materially relevant alternative Greek readings/revisions;
- relevant Hebrew witness or witnesses;
- DSS/Qumran evidence when available;
- important apparatus evidence.

Every reading must identify its edition/witness.

3. Discriminating textual features:
Separate:
- exact lexical agreement;
- syntax/word order;
- readings shared across traditions;
- readings unique enough to discriminate;
- probable Pauline modification;
- non-discriminating evidence.

4. Scholarly positions:
For every scholar who directly discusses the case provide:
- scholar;
- position;
- evidence cited;
- printed page number(s).

Do not merge scholars into a consensus statement where they disagree.

5. Direct-Hebrew evidence:
Identify whether any source supplies evidence that Paul's wording specifically requires or materially benefits from direct Hebrew consultation.

Separate:
- simple Hebrew agreement;
- Hebrew-specific morphology;
- Hebrew-specific wordplay;
- consonantal ambiguity;
- syntax;
- other evidence unavailable in the relevant Greek forms.

6. Greek alternatives to direct Hebrew:
Identify:
- alternate Greek witnesses;
- Hebraizing revisions;
- possible lost Greek forms;
- oral/liturgical transmission;
- inherited quotation forms;
- authorial adaptation.

7. Strongest evidence favoring an Old Greek explanation.

8. Strongest evidence against an Old Greek explanation.

9. Strongest evidence favoring direct Hebrew consultation.

10. Strongest evidence against direct Hebrew consultation.

11. Authorial adaptation:
State what changes may plausibly belong to Paul rather than his source text.

12. Unresolved scholarly disagreement.

13. Missing evidence or source gaps.

14. Additional scholarship cited by the current sources that should be acquired before classification.

15. Citation ledger:
List every substantive claim in the dossier with its supporting source and printed page.

DO NOT invent missing page numbers.

Use PAGE NOT VERIFIED where necessary.

DO NOT issue a final B001 project classification.

The purpose of this dossier is to give the downstream analyst enough evidence to apply the project's TXT classification vocabulary and Direct Hebrew Consultation Test independently.
```

---

# 8. Prompt D — exact Hermes handoff after manual Open Notebook work

Paste this into Hermes after the Open Notebook extraction files have been saved into the B001 inbox.

```text
Resume Batch B001-pauline-txt-pilot from the current GitHub repository state.

GitHub main is authoritative. Pull latest main first.

Read, in governing order:
1. docs/design/PROJECT_CONSTITUTION.md
2. docs/workflow/RESEARCH_WORKFLOW.md
3. docs/workflow/SOURCE_ACQUISITION.md
4. docs/workflow/HERMES_INSTRUCTIONS.md
5. docs/workflow/B001_OPEN_NOTEBOOK_MANUAL.md
6. research/registry/SCHEMA.md
7. research/TXT/README.md
8. research/TXT/textual_classifications.md
9. research/TXT/hebrew_consultation_test.md
10. research-queue/CURRENT_BATCH.md
11. research-queue/B001-pauline-txt-pilot.md

The Open Notebook source work was performed manually because autonomous Open Notebook operation was unreliable.

Treat files under:
research/inbox/B001-pauline-txt-pilot/open-notebook-extractions/

as extraction/navigation notes, NOT as primary evidence by themselves.

For every substantive claim, preserve the underlying source identity and printed-page support. Flag anything that cannot be traced back to a verified source/page. Do not fill source gaps from model memory.

Your job now is to complete the B001 research packet:
- verify acquisition/source manifests;
- identify any remaining source gaps;
- ensure each of the 12 passages has at least two substantive specialist secondary treatments or is explicitly blocked;
- compare Pauline Greek, Old Greek, other Greek traditions/revisions, Hebrew witnesses, DSS/Qumran evidence where relevant, and apparatus material;
- apply the Direct Hebrew Consultation Test explicitly;
- assign only provisional TXT classifications and confidence values allowed by the repo;
- preserve counterevidence, alternatives, falsifiers, and indeterminate results;
- run an independent adversarial pass for every passage;
- perform citation verification;
- write all required files only under research/inbox/B001-pauline-txt-pilot/;
- do not modify canonical registry files;
- work on branch research/B001-pauline-txt-pilot;
- commit the completed packet and report the branch name and commit SHA;
- do not merge the branch into main.

Do not start B002 or later phases.
```

---

# 9. What Open Notebook is allowed to decide

Open Notebook may:

- locate passages inside ingested sources;
- extract an author's stated argument;
- extract bibliography leads;
- collate candidate textual readings for later manual verification;
- identify places where scholars disagree;
- organize source-grounded notes.

Open Notebook must **not** be trusted by itself to:

- determine the final Old Greek reconstruction;
- decode uncertain critical-apparatus sigla;
- correct corrupted Greek/Hebrew OCR from model memory;
- decide that Paul consulted Hebrew merely because a reading resembles MT;
- assign canonical registry status;
- convert scholarly disagreement into a fabricated consensus;
- invent page numbers, readings, or bibliography.

---

# 10. Completion checklist for the manual Open Notebook stage

Before handing the batch back to Hermes, verify:

- [ ] `SDP-01 Paul` exists.
- [ ] Every acquired source has a stable `P##` or `S##` label.
- [ ] Exact edition identity has been checked.
- [ ] Printed-page/PDF-page mapping is known or explicitly unverified.
- [ ] Greek/Hebrew OCR limitations are documented.
- [ ] Prompt A was run independently on each available S01–S14 source.
- [ ] Prompt B was run independently on each available P01–P09 source.
- [ ] Primary-language readings used in analysis were checked against page images where possible.
- [ ] Unavailable sources are recorded in `source_gaps.md`.
- [ ] Every B001 passage has at least two qualifying specialist secondary treatments, or the missing treatment is explicitly flagged.
- [ ] Prompt C was run once against the full verified packet.
- [ ] Extraction files were saved under `research/inbox/B001-pauline-txt-pilot/open-notebook-extractions/`.
- [ ] No final TXT classification was delegated to Open Notebook.
- [ ] Hermes received Prompt D and resumed the batch from GitHub main.

The manual stage is successful when it produces a **traceable source packet**, including negative evidence and unresolved uncertainty—not when it makes all twelve passages support the working hypothesis.
