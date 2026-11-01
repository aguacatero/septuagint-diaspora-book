# Research Workflow — Antigravity, NotebookLM, GitHub, independent ChatGPT review

This is the **current** operating workflow. It replaces the former Hermes/OpenRouter + Open Notebook setup, which is preserved only for historical reference in [legacy workflow archives](../archive/legacy-workflows/README.md).

## Source of truth and boundaries

- [Project Constitution](../design/PROJECT_CONSTITUTION.md) sets scholarly and ethical requirements.
- [Registry schema](../../research/registry/SCHEMA.md) and TXT/NAR/CUL/HIS module rules determine acceptable evidence.
- `main` stores the accepted project state and [current batch contract](../../research-queue/CURRENT_BATCH.md).
- Active B001 **execution** state and verified source packets are on [draft PR #2](https://github.com/aguacatero/septuagint-diaspora-book/pull/2); fetch the live PR HEAD before any operation.
- [Proposed Gospel-origins investigations](../../research-queue/proposals/2026-11-01-gospel-origins-mark-mazdean-post70.md) are a future backlog, not active research or accepted results.

## One-source-at-a-time B001 loop

1. **Read live state.** Antigravity/Gemini reads `START_HERE_ANTIGRAVITY.md`, `ANTIGRAVITY_START.md`, the serial NotebookLM workflow, source queue, and state JSON **from PR #2's live HEAD**. Do not restart or change the active source from a copied handoff.
2. **Acquire lawfully.** Confirm edition, author, source integrity, page mapping, licenses/access restrictions, and record missing sources. Follow [source acquisition](SOURCE_ACQUISITION.md).
3. **Extract one source.** Use `SDP-B001-EXTRACT` with exactly one source at a time. Run the source-class-specific prompts: a PRIMARY packet extracts the actual ancient texts/apparatus; a SECONDARY packet records scholar claims and locators. NotebookLM outputs are aids, not independent evidence.
4. **Verify and stage.** Check citations against original texts and pages. Store candidate structured data and a readable packet in GitHub. Note omissions, contrary evidence, scope, uncertainties and all provenance.
5. **Independent exact-SHA review.** ChatGPT reviews the named source packet at the **current live PR HEAD** using the review-loop controller. It responds `SOURCE_PACKET: ACCEPT` or `SOURCE_PACKET: REVISE` with a full SHA, time and specific supporting/revising reasons. The extractor may not review/approve its own packet.
6. **Remediate or promote.** On REVISE, fix the packet and submit a fresh commit for fresh exact-SHA review. On ACCEPT, only the accepted source is promoted into cumulative NotebookLM `SDP-01 Paul` with retrieval verification, then the queue advances.
7. **Do not merge automatically.** PR #2 remains draft/unmerged. Whole-batch acceptance, canonical registry promotion, and milestone checks are separate later decisions.

The live specifications, extraction prompts, and browser-preflight documents are in the B001 branch: [current serial workflow](https://github.com/aguacatero/septuagint-diaspora-book/blob/research/B001-notebooklm-serial/docs/workflow/NOTEBOOKLM_ANTIGRAVITY_SERIAL.md).

## Required research packet standards

For each candidate claim or passage, record:

- source and edition identity, access/class, claim, exact primary passage, scholarly page/section/citation locator;
- textual witnesses and variants relevant to the Greek/Hebrew comparison, without a simplistic LXX-versus-Masoretic binary;
- separate quotations, allusions and thematic resemblance;
- manuscript limitations, possible oral/liturgical transmission, authorial redaction, textual pluriformity, alternative readings and strong counterexamples;
- claim-by-claim source support, confidence, competing interpretations, falsifier, unresolved items, and an adversarial pass.

Never invent source pages, timestamps, quotations, apparatus readings, author positions or evidence IDs. If a source or page is inaccessible, label it explicitly. A video is a research lead until its actual transcript and claims are verified.

## Research phases and approval

The program remains sequential: **TXT textual audit → NAR narrative-generation analysis → CUL controlled cultural comparison → HIS historical evidence audit → book**, after the Foundation gate. Proposed Mark, Iranian/John, Pauline-authorship and universal post-70 chronology topics must pass their own contracts and reviews before changing canonical evidence or the Constitution.

Only a reviewer/promoter with authorization can admit independently reviewed evidence to `research/registry/` and mark completed milestones. The README and `assets/progress.svg` must match accepted status; run `python3 scripts/update_progress.py --check`. Source-level acceptance on a draft branch is not approval of a whole milestone.

## Historical workflows

The prior Hermes operating instructions, Open Notebook manual, and related instructions are kept under [docs/archive/legacy-workflows](../archive/legacy-workflows/README.md). They must not be used to drive current B001 execution.
