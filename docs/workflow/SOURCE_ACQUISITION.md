# Source Acquisition and NotebookLM Verification

This workflow defines **Phase 0** for every research batch in *Shaped by the Septuagint*.

The active Antigravity/Gemini research agent is responsible for locating and verifying the needed sources when they are not already present. Research should not begin from model memory or tertiary summaries simply because the relevant books have not yet been collected.

## Goal

Before passage-level analysis begins, assemble the strongest legally accessible source packet needed for the batch, stage lawfully accessible sources in the approved NotebookLM workflow, and document any gaps.

GitHub remains the durable source of truth for project rules and research packets. NotebookLM supports source retrieval and extraction; it is not canonical storage.

## Acquisition priority

Search in this order when practical:

1. **Primary/critical editions and official repositories** — publisher, university, scholarly project, manuscript repository, or other authoritative source.
2. **Open-access scholarly copies** — institutional repositories, author manuscripts, journal OA copies, public-domain scans.
3. **Internet Archive / Open Library** — especially public-domain and unrestricted full-text scans of books and older scholarship.
4. **Other lawful previews/discovery systems** — useful for locating editions and bibliographies, but not sufficient for a claim if the relevant page cannot be inspected.
5. **User-supplied or library-access copies** — when an important source cannot be lawfully acquired automatically.

Do not use piracy sites, credential bypasses, DRM circumvention, or fabricated download URLs.

## Internet Archive rules

Internet Archive is an approved discovery/acquisition route, subject to the access state of the item.

### Public-domain or unrestricted items

The research agent may:

- locate the correct edition;
- download an openly available PDF or other usable full-text file;
- preserve the Internet Archive item URL and identifier;
- import the file into the appropriate NotebookLM notebook;
- record scan quality, page-number mapping, and OCR limitations.

Prefer page-image PDFs when exact pagination or original-language typography matters.

### Borrow-only / controlled-lending items

The research agent may use only the access that the user's authorized Internet Archive/Open Library session legitimately provides.

The research agent must not:

- bypass lending limits;
- remove or defeat DRM/access controls;
- obtain restricted files through undocumented circumvention;
- represent inaccessible pages as inspected.

If the authorized lending flow does not yield a file or view that can be reliably analyzed/imported into NotebookLM, record the source as `BORROW_REQUIRED` or `MANUAL_ACCESS_REQUIRED`, look for another lawful copy, and continue the batch where possible.

## Edition identity

Before ingesting a book, verify as much of the following as possible:

- author/editor;
- exact title;
- publisher;
- publication year;
- edition/volume;
- translator, where relevant;
- ISBN/DOI/catalog identifier when available;
- Internet Archive/Open Library identifier when applicable.

Do not silently substitute a different edition when page-level citations are required.

## Scan and OCR quality checks

For scanned sources:

1. Open the title/copyright pages and verify edition identity.
2. Check at least one page containing Greek/Hebrew or technical notation.
3. Determine whether printed page numbers match PDF page numbers.
4. Note missing pages, foldouts, illegible text, or OCR corruption.
5. Do not rely on OCR alone for Greek/Hebrew readings or textual apparatus.

For exact quotations, textual variants, and apparatus readings, inspect the page image or authoritative digital text rather than trusting machine OCR.

## NotebookLM ingestion (active B001)

For the active B001 serial pipeline:

1. Fetch the live [PR #2](https://github.com/aguacatero/septuagint-diaspora-book/pull/2) state and source queue and use the authorized NotebookLM browser workflow. Do not use unofficial private APIs or bypass login and access controls.
2. Keep **exactly one source** in `SDP-B001-EXTRACT` during extraction. Identify the edition unambiguously and preserve page/section mapping.
3. Record verified source identity and metadata in the source packet and relevant manifests. Do not rely on NotebookLM's opaque source label.
4. Confirm ingestion and retrieval with a known passage, then reopen citations in original source context. For primary Greek/Hebrew material and apparatus, inspect authoritative text/page images, not OCR alone.
5. Stage the packet in GitHub for independent review. **Only after exact-SHA ACCEPT** may the source be promoted to cumulative `SDP-01 Paul`.
6. Record source gaps honestly; do not claim access when a work is unavailable.

NotebookLM-generated answers are navigation and extraction aids. The underlying source and verified GitHub packet are the evidence. For later batches, follow their own approved contracts.

## Required acquisition manifest

Every batch that performs source acquisition must create:

`research/inbox/<batch>/acquisition_manifest.csv`

Minimum fields (the legacy `open_notebook_label` column name is retained for compatibility, but now records the corresponding NotebookLM source label where used):

```csv
acquisition_id,requested_source,author_or_editor,title,year,edition_or_volume,provider,provider_identifier,provider_url,access_class,local_filename,open_notebook_label,ingestion_status,page_mapping_verified,ocr_quality,notes
```

Recommended `access_class` values:

- `PUBLIC_DOMAIN_FULL_TEXT`
- `OPEN_ACCESS_FULL_TEXT`
- `AUTHORIZED_FULL_TEXT`
- `BORROW_ONLY`
- `PARTIAL_PREVIEW`
- `MANUAL_ACCESS_REQUIRED`
- `NOT_FOUND`

Recommended `ingestion_status` values:

- `INGESTED_VERIFIED`
- `INGESTED_WITH_LIMITATIONS`
- `NOT_INGESTED`

## Source-gap report

Create:

`research/inbox/<batch>/source_gaps.md`

For every important unavailable source, record:

- exact citation sought;
- why it matters;
- acquisition attempts;
- access limitation;
- best substitute currently available;
- whether the missing source materially limits classification.

A batch can proceed with gaps, but the limitations must remain visible.

## Research gate

Do not begin final passage classifications until the minimum source packet defined by the batch is either:

- acquired and ingested; or
- explicitly marked unavailable with a documented substitute/limitation.

Source acquisition is part of the research process, not a prerequisite the user is expected to complete manually. See [current workflow](RESEARCH_WORKFLOW.md); superseded Open Notebook procedures are archived.
