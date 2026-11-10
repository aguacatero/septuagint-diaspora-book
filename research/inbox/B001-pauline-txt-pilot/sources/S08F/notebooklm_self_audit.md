# S08F — NotebookLM Self-Audit

Source-bounded extraction self-audit for J. Paul Tanner, *The New Covenant and Paul’s Quotations from Hosea in Romans 9:25–26*, *Bibliotheca Sacra*, Vol. 162, No. 645 (January–March 2005), pp. 95–110.

---

## 1. Seven Core Extraction Integrity Checks

### Check 1: Attribution Integrity
- **Question:** Did you attribute any claim to the author without direct source support?
- **Finding:** VERIFIED. Every extracted claim (`S08F-E001` through `S08F-E008`) maps directly to explicit English statements in the text of Tanner (2005) and has been authenticated verbatim against the born-digital PDF text layer. Douglas J. Moo's grammatical and textual observation (quoted in footnote 4 on p. 99) regarding Paul changing Hosea's "I will say" to "I will call" (*καλέσω*) to match Romans 9:24 is explicitly attributed to Moo via Tanner's footnote.

### Check 2: Quotation Context Integrity
- **Question:** Did any quotation omit nearby words that materially change its meaning?
- **Finding:** VERIFIED. All quotations preserve their exact syntactic and contextual boundaries without splicing:
  - `S08F-E001` captures the full contextual inference: *"it seems clear that Paul was citing these verses to establish the point that God's \"vessels of mercy\" include Gentiles."* (Printed p. 98 [PDF p. 4]).
  - `S08F-E002` captures the full causal clause: *"Paul quoted from a Greek rendering of Hosea and the fact that he reversed the order of the clauses"* (Printed p. 99 [PDF p. 5, fn. 4]).
  - `S08F-E003` captures the complete historical restriction: *"Nothing in the context of these passages makes reference to Gentiles, nor did Hosea imply that the fulfillment of these promises would be with Gentiles."* (Printed p. 100 [PDF p. 6]).
  - `S08F-E004` captures the parenthetical qualification: *"verses 25-26 affirm that the conversion of Gentiles is a direct fulfillment of Hosea's prophecy (though not the complete fulfillment)."* (Printed p. 102 [PDF p. 8]).
  - `S08F-E005` preserves the full, unspliced covenantal sentence: *"It was the New Covenant that made it possible for the Jewish remnant to become \"the people of God.\" The context of Hosea (particularly the mention of a \"covenant\" in Hosea 2:18) confirms this. Since it was the New Covenant that made it possible for Gentiles to become part of the church, the \"not my people\" in the Hosea passages ultimately had Gentiles in view."* (Printed p. 110 [PDF p. 16]).
  - `S08F-E006` captures the anti-supersessionist thesis: *"Paul was not operating by some new theological dictum whereby Israel no longer meant Israel. Instead he had come to understand the Gentile aspect of fulfillment."* (Printed p. 103 [PDF p. 9]).
  - `S08F-E007` captures the distinction between ethnic Israel and the remnant: *"In Romans 11 the apostle clarified this distinction between ethnic Israel in unbelief and the believing Israelite \"remnant.\" God's covenant promises to Israel have not failed, because God will fulfill them with the believing remnant."* (Printed p. 96 [PDF p. 2]).
  - `S08F-E008` captures the clause inversion explanation: *"reversed the order of the clauses (perhaps to stress the \"My people\" aspect of the promise and God's \"call\" to them)."* (Printed p. 99 [PDF p. 5]).

### Check 3: Locator and Pagination Integrity
- **Question:** Did you infer a printed page number rather than observe it?
- **Finding:** VERIFIED. Physical page inspection of `tanner_2005_hosea_romans_9.pdf` confirmed that every page contains its exact printed page number in the header margin region, establishing the strictly monotonic invariant $printed = PDF + 94$ across all 16 article pages (PDF pp. 1–16 = printed pp. 95–110). PDF page 17 contains standard ATLA user preservation terms. Header locality and proximity to running journal markers (`BiBLiOTHECA SACRA` or article title) are enforced deterministically by the verifier script.

### Check 4: Modal Qualification Integrity
- **Question:** Did you convert an author's possibility into a probability or certainty?
- **Finding:** VERIFIED. Tanner's epistemic framing is carefully preserved:
  - In `S08F-E001`, Tanner notes that Paul does not introduce Hosea with the words "Now concerning the Gentiles," but infers that *"it seems clear"* that Paul was citing them to establish Gentile inclusion based on the contextual sandwich between Rom 9:22–24 and Rom 9:30–31 (p. 98).
  - In `S08F-E004`, Tanner qualifies that Gentile conversion is a *"direct fulfillment... (though not the complete fulfillment)"* because national promises remain to be fulfilled with ethnic Israel (p. 102).

### Check 5: Authorial vs. Disputed Voice Distinction
- **Question:** Did you confuse the author's description of another scholar with the author's own view?
- **Finding:** VERIFIED. Tanner's own position is rigorously distinguished from the scholarly views he disputes:
  - Disputed national-Israel-only position of McClain (1973), Battle (1981), and Turner (1985) (p. 98 fn. 2, 3).
  - Disputed replacement theology / "spiritual Israel" equation of Ladd (1977) and Moo (1996) (pp. 95–96, 101, 109–110).
  - Disputed mere "analogy" view of Chisholm (1985), Witmer (1983), and S. Lewis Johnson (1992) (pp. 101–102 fn. 8).
  - Disputed "nonparticipating mediator" thesis of Richard Daniels (1999) (p. 104 fn. 13).
  - Disputed oversight of covenant in Hosea 2:18 by Wood (1985) and Andersen & Freedman (1980) (p. 107 fn. 18).

### Check 6: Proximate Qualifications and Textual Variants
- **Question:** Did you miss a qualification, objection, textual variant, or counterexample near any extracted passage?
- **Finding:** VERIFIED. All textual modifications identified in Tanner's analysis—Paul quoting a Greek rendering rather than the Hebrew MT, reversing clause order in Hosea 2:23, modifying the verb to *καλέσω*, selectively quoting only Hosea 1:10b while omitting the Abrahamic promise in 1:10a—are documented with exact page and footnote references. Proximate theological qualifications (e.g., that New Covenant spiritual status does not confer the land/national promises reserved for ethnic Israel) are explicitly maintained.

### Check 7: External Knowledge Independence
- **Question:** Did you rely on general model knowledge?
- **Finding:** VERIFIED. All extractions, argument mappings, counterevidence evaluations, and bibliographic entries derive exclusively from `tanner_2005_hosea_romans_9.pdf`.

---

## 2. Verification Against Born-Digital Volume

- **Volume File:** `tanner_2005_hosea_romans_9.pdf`
- **File Size:** 1,440,727 bytes
- **SHA-256 Digest:** `88263a92f5edf99217238123198ff580a91203ecca68111aaed614a1a932a64a`
- **Article Pages:** 16 pages (printed pp. 95–110; PDF pp. 1–16)
- **Total Ingested Pages:** 17 pages (including ATLA terms page on PDF p. 17)
- **Monotonic Pagination Invariant:** $printed = PDF + 94$ across all 16 article pages.
- **Negative Search Verification:**
  - `B001-2` (Rom 9:25 / Hos 2:23): Extended Discussion (22 verified hits across pp. 95–110).
  - `B001-3` (Rom 9:26 / Hos 1:10): Extended Discussion (6 verified hits across pp. 99–101).
  - Remaining 10 B001 targets (B001-1, B001-4 through B001-12): Confirmed absent (0 hits across all 16 pages).
- **Automated Verifier:** `scripts/verify_s08f_negative_search.py` runs with zero discrepancies in `--check-only` mode.

---

## 3. Round 1 Review Findings Remediation Audit

All four findings from ChatGPT Round 1 review ([#issuecomment-6733387261](https://github.com/aguacatero/septuagint-diaspora-book/pull/2#issuecomment-6733387261)) were remediated:

1. **S08F-R1-F1 (Bibliographic Containers & Footnote Locators):** Corrected Richard Daniels container to *Faith and Mission* 16 (1999): 64–98 on p. 104, fn. 13; McClain & Battle to p. 98, fn. 2; Wolff to p. 107, fn. 18; Light to p. 106, fn. 17; Ladd to p. 109, fn. 22; full 26-lead inventory audited.
2. **S08F-R1-F2 (Cross-Artifact Verifier Hardening & Adversarial Tests):** Bound extraction to discrete evidence blocks, bound synthesis to subsections, and authenticated structured bibliography witnesses.
3. **S08F-R1-F3 (Reconciled Target Loci Drift):** Reconciled `citation_ledger.csv` rows `S08F-E004` through `E007` to `b001_id = "B001-2, B001-3"`, matching `extraction.md`.
4. **S08F-R1-F4 (Methodological Scoping & Premise Demarcation):** Demarcated Tanner's confessional/theological premises (Acts 10–11, Eph 3) in `argument_map.md`.

---

## 4. Round 2 Review Findings Remediation Audit

All three findings from ChatGPT Round 2 review ([#issuecomment-6759235942](https://github.com/aguacatero/septuagint-diaspora-book/pull/2#issuecomment-6759235942)) have been fully remediated:

1. **S08F-R2-F1 (Bibliographic Footnote Prefix Collision & Author/Title Authentication):**
   - Implemented `parse_source_locator` in `scripts/verify_s08f_negative_search.py` to extract exact numeric printed page(s), PDF page(s), and exact delimited footnote integers (e.g., `\bfn\.\s*(\d+)\b`).
   - Replaced substring matching with exact integer comparisons, eliminating prefix collisions such as `fn. 2 -> fn. 20`.
   - Added authoritative per-lead `author` and `title` metadata fields to `EXPECTED_BIBLIOGRAPHY_LEADS` for all 26 leads, enforcing that each lead block in `bibliography_leads.md` contains exactly one matching `Author` line and exactly one matching `Title` line.
   - Added fail-closed adversarial mutation tests in `tests/test_citation_ledger_crosswalk.py` for `fn. 2 -> fn. 20`, invented work title (`*Unrelated Work*`), and invented author (`Another Scholar`).

2. **S08F-R2-F2 (Strict Bracket Delimiters & Coordinated False PDF Pages):**
   - Enforced strict bracketed delimiters `[PDF p. X]` and exact parsed numeric comparisons in both `verify_ledger_witnesses()` and `verify_cross_artifact_consistency()`, eliminating open-ended prefix matching `[PDF p. 4`.
   - Parsed and compared exact numeric printed and PDF pages between ledger rows, extraction blocks, and authoritative specifications.
   - Added fail-closed adversarial mutation tests for a coordinated false PDF page (`PDF p. 4 -> PDF p. 40` in both ledger and extraction) and malformed/missing locator delimiters.

3. **S08F-R2-F3 (Field-Bound Quotation Verification):**
   - Isolated the named `- **Short Exact Quotation:**` line in each evidence block rather than searching the entire block, preventing altered quotations from being masked by notes copies.
   - Normalized and compared only the extracted field quote against the ledger quote.
   - Added a fail-closed adversarial mutation test for a corrupted quotation field with the original quote pasted into Notes.

---

## 5. Round 3 Review Findings Remediation Audit

Both findings from ChatGPT Round 3 review ([#issuecomment-6768652597](https://github.com/aguacatero/septuagint-diaspora-book/pull/2#issuecomment-6768652597)) have been fully remediated:

1. **S08F-R3-F1 (Strict Locator Parser Accepts Duplicate/Conflicting PDF Pages & Footnotes):**
   - Enhanced `parse_source_locator` in `scripts/verify_s08f_negative_search.py` with strict structural checks:
     - Exactly one opening `[` and one closing `]` bracket pair.
     - At most one `\bfn\.\s*\d+\b` reference anywhere in the string.
     - Strict start-to-finish full-string regex grammar (`^...$`) that rejects any unparsed trailing text, multiple brackets, or malformed suffixes.
     - Built-in monotonic pagination formula verification ($printed = PDF + 94$).
   - Added unit assertions and cross-artifact adversarial tests in `tests/test_citation_ledger_crosswalk.py` covering:
     - Conflicting appended PDF brackets (`Printed p. 98 [PDF p. 4] [PDF p. 40]`) in extraction and ledger.
     - Conflicting appended footnotes (`Printed p. 98 [PDF p. 4], fn. 2, fn. 20; Section 2`).
     - Malformed trailing locator fragments (`Printed p. 98 [PDF p. 4] trailing_garbage`).
     - Monotonic pagination violations (`Printed p. 98 [PDF p. 5]`).

2. **S08F-R3-F2 (Authoritative Publication Year & Unambiguous Primary Container Validation):**
   - Added authoritative `year: <int>` field to all 26 bibliographic leads in `EXPECTED_BIBLIOGRAPHY_LEADS`.
   - Enforced tri-partite agreement among:
     - Header year in `### Author (YYYY)`.
     - Authoritative year in `lead["year"]`.
     - Parsed year in `- **Publication Year:** YYYY (...)`.
   - Parsed parenthetical publication details to isolate the primary container (`*Journal Name*` for journals, `<City>: <Publisher>` for books), enforcing exact normalized equality against `lead["container"]`. This rejects false primary containers even if the expected container is mentioned as a cross-reference.
   - Added fail-closed adversarial mutation tests in `tests/test_citation_ledger_crosswalk.py` for:
     - Fabricated publication year in `Publication Year` line (2099 vs 1999).
     - Fabricated header year (2099 vs 1999).
     - Misleading primary container with expected container mentioned as a cross-reference.

---

## 6. Review Readiness & Submission

- **Active Source:** `S08F`
- **Source Deliverable Directory:** `research/inbox/B001-pauline-txt-pilot/sources/S08F/`
- **Status:** `REMEDIATED / READY_FOR_ROUND_4_REVIEW`
- **Review Target:** `LIVE_PR_HEAD`
- **Review Loop:** Independent exact-SHA evaluation by ChatGPT on Draft PR #2.
