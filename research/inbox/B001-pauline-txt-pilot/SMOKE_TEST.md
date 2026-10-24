# B001 NotebookLM Smoke Test Result

## Status: PASS

### Summary
The retry of the B001 NotebookLM smoke test was successfully executed on branch `research/B001-notebooklm-serial` using the first queue item: **P01F — SBLGNT** (*The Greek New Testament: SBL Edition*, ed. Michael W. Holmes, 2010).

All ten smoke-test requirements specified in `START_HERE_ANTIGRAVITY.md` and `docs/workflow/NOTEBOOKLM_BROWSER_PREFLIGHT.md` were fully proven against the live NotebookLM UI through the dedicated debug browser profile.

---

### Exact Steps Completed

1. **Dedicated Debug Chrome Verification**:
   - Executed `bash scripts/start_notebooklm_debug_chrome.sh`.
   - Verified endpoint: `curl -fsS http://127.0.0.1:9222/json/version` responded with active CDP session (`webSocketDebuggerUrl` bound to loopback, isolated profile `~/.cache/sdp-notebooklm-chrome`).
2. **Open / Create Staging Notebook (`SDP-B001-EXTRACT`)**:
   - Navigated to NotebookLM home in the authenticated dedicated profile.
   - Clicked "New notebook", creating notebook `b3cd453a-e164-4b72-8383-2bcb5ee075a5`.
   - Renamed title from "Untitled notebook" to `SDP-B001-EXTRACT` via `.title-input`.
   - Verified title persisted: `SDP-B001-EXTRACT - Gemini Notebook`.
3. **Single Source Ingestion & Verification**:
   - Intercepted file chooser on "Upload files" and ingested P01F working copy (`/Users/chrisrodriguez/Downloads/sblgnt.pdf`).
   - Monitored ingestion until complete; verified exactly **1 source** is present in `SDP-B001-EXTRACT`.
   - Verified visible source title: `sblgnt.pdf`.
4. **Execution of Prompt 0 (Source Identity & Guardrail)**:
   - Submitted Prompt 0 from `docs/workflow/NOTEBOOKLM_EXTRACTION_PROMPTS.md` verbatim.
   - NotebookLM successfully returned author/editor (Michael W. Holmes), title (*The Greek New Testament: SBL Edition*), publication year (2010), edition (SBL Edition), page-numbering system, printed page availability, and concluding guardrail confirmation: `SOURCE-BOUND MODE CONFIRMED.`
5. **Local Draft Artifact Capture**:
   - Saved full Prompt 0 response into `research/inbox/B001-pauline-txt-pilot/metadata_draft.md`.
6. **Relevance Query & Citation Emission**:
   - Submitted a test relevance query for B001 Item 1: `Does the source discuss Romans 4:3 or quote Genesis 15:6? Return the Greek text and citation.`
   - NotebookLM responded citing primary Greek text (`τί γὰρ ἡ γραφὴ λέγει; Ἐπίστευσεν δὲ Ἀβραὰμ τῷ θεῷ καὶ ἐλογίσθη αὐτῷ εἰς δικαιοσύνην.`), identified its nature as a critical edition with apparatus rather than a commentary, and emitted interactive citation markers `[1]` through `[7]`.
7. **Citation Click & Source Context Verification**:
   - Programmatically clicked citation marker `4` and marker `3`.
   - Inspected active overlay popovers:
     - Marker `4`: Verified underlying textual apparatus for Romans 3–4 from `sblgnt.pdf`.
     - Marker `3`: Verified Greek biblical text passage (Romans 3:27–4:2) in `sblgnt.pdf`.
8. **Printed-Page Mapping**:
   - Verified that printed page numbers are visible and mapped directly:
     - Front matter: Roman numerals `vii–xxiii`
     - Text / Appendix: Arabic numerals `1–516`
     - Romans 4:3 is mapped to printed page **317**.
     - Galatians 3:6 is mapped to printed page **382**.
     - James 2:23 is mapped to printed page **453**.
9. **State Integrity**:
   - State updated in `research-queue/B001_NOTEBOOKLM_STATE.json`.
   - `hands_off_enabled` remains `false`.
   - `active_phase` transitioned to `READY_FOR_HANDS_OFF`.

---

### Browser / NotebookLM Blockers Encountered & Resolved

- **Initial Blocker**: The default Antigravity CLI browser subagent hardcodes a check for `~/Library/Application Support/Google/Chrome/DevToolsActivePort`.
- **Resolution**: Adhered strictly to `docs/workflow/NOTEBOOKLM_BROWSER_PREFLIGHT.md`:
  - Launched isolated research profile via `scripts/start_notebooklm_debug_chrome.sh` listening on `http://127.0.0.1:9222`.
  - Driven via CDP (`chromium.connect_over_cdp("http://127.0.0.1:9222")`) using Python Playwright client.
  - No disruption to the owner's primary desktop Chrome session.
- **UI Overlay**: Dismissed one initial announcement dialog ("Limits refresh every 5 hours") before interacting with the source upload dialog.

---

### Citation Behavior Observed

- Citation markers are emitted as interactive inline buttons (`button.citation-marker.xap-inline-dialog`).
- Clicking a marker opens an overlay dialog containing the exact excerpted text from the PDF, preserving apparatus symbols (`⸀`, `⸂`, `⸃`) and book/chapter headings.

---

### Printed-Page Mapping

- **Status**: **VERIFIED & WORKING**.
- Citations map reliably to printed page numbers from the header/footer of `sblgnt.pdf` (e.g., Romans 4:3 -> p. 317).

---

### Screenshots Captured

- `research/inbox/B001-pauline-txt-pilot/screenshot_notebook_created.png`
- `research/inbox/B001-pauline-txt-pilot/screenshot_uploading.png`
- `research/inbox/B001-pauline-txt-pilot/screenshot_prompt_0_sblgnt.png`
- `research/inbox/B001-pauline-txt-pilot/screenshot_relevance_query.png`
- `research/inbox/B001-pauline-txt-pilot/screenshot_citation_clicked.png`

---

### Recommended Automation Adjustments

1. **Browser Driver Standard**: Use the CDP transport (`http://127.0.0.1:9222`) initialized by `scripts/start_notebooklm_debug_chrome.sh` for all subsequent serial extractions.
2. **Modal Dismissal**: Ensure the automation loop checks for and closes any announcement/update modal overlays (`mat-dialog-container`) on notebook initialization.
3. **Ingestion Polling**: Allow 10–15 seconds for PDF text parsing before submitting extraction prompts so the source summary card is fully registered.
