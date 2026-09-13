# Source Acquisition and Open Notebook Ingestion

This workflow defines **Phase 0** for every research batch in *Shaped by the Septuagint*.

Hermes is allowed and expected to acquire the research corpus when it is not already present. Research should not begin from model memory or tertiary summaries simply because the relevant books have not yet been collected.

## Goal

Before passage-level analysis begins, assemble the strongest legally accessible source packet needed for the batch, import the usable sources into Open Notebook, and document any gaps.

GitHub remains the source of truth for project rules and research outputs. Open Notebook is the persistent local source warehouse.

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

Hermes may:

- locate the correct edition;
- download an openly available PDF or other usable full-text file;
- preserve the Internet Archive item URL and identifier;
- import the file into the appropriate Open Notebook notebook;
- record scan quality, page-number mapping, and OCR limitations.

Prefer page-image PDFs when exact pagination or original-language typography matters.

### Borrow-only / controlled-lending items

Hermes may use only the access that the user's authorized Internet Archive/Open Library session legitimately provides.

Hermes must not:

- bypass lending limits;
- remove or defeat DRM/access controls;
- obtain restricted files through undocumented circumvention;
- represent inaccessible pages as inspected.

If the authorized lending flow does not yield a file or view that can be reliably analyzed/imported into Open Notebook, record the source as `BORROW_REQUIRED` or `MANUAL_ACCESS_REQUIRED`, look for another lawful copy, and continue the batch where possible.

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

## Open Notebook ingestion

For each batch:

1. Create/reuse the notebook named in the batch contract.
2. Import every full-text source actually used in analysis.
3. Use stable, descriptive source labels, preferably `Author — Short Title — Year/Edition`.
4. Keep source metadata in the batch `source_manifest.csv` even when Open Notebook stores its own metadata.
5. Confirm ingestion completed successfully before querying the source.
6. Test retrieval with a known phrase/page from the document.
7. If page citations are important, verify that Open Notebook's extracted text can be traced back to the original scan/page.

Open Notebook-generated answers are navigation and synthesis aids. The underlying source remains the evidence.

## Required acquisition manifest

Every batch that performs source acquisition must create:

`research/inbox/<batch>/acquisition_manifest.csv`

Minimum fields:

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

Source acquisition is part of the research process, not a prerequisite the user is expected to complete manually.
