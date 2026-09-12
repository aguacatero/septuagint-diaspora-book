# Design: Remove Q Source and Focus on Four Canonical Gospels + Deep Dive

## Purpose
Remove all references to the hypothetical Q source from the manuscript and shift focus to the four canonical gospels (Mark, Matthew, Luke, John) as the primary textual witnesses. Additionally, include a deep-dive body of work that reinforces the LXX-dependence hypothesis with evidence from early non-canonical gospels (as speculative, bracketed material) and extensive historical/literary/contextual evidence from the 1st century Jewish-Christian milieu.

## Changes Made
1. **Removed Q references** from:
   - Core_Thesis.md (line 11, line 81)
   - Book_Part2.md (removed Q appendix note)
   - Book_Scholar_Outline.md (Chapter 3 title, goal, method, appendix A)
   - README.md (overview, chapter structure)
   - SOURCES.md (section header)
2. **Updated references** to reflect Mark, Matthew, Luke, John as the core gospels.
3. **Added bracketed speculative treatment** for non-canonical early gospels (Gospel of Thomas, Gospel of Peter, Gospel of Mary, etc.) as per user request.

## Design Sections

### Architecture Overview
- The book's argument remains layered: solid core (LXX dependence in Mark/Matthew/Luke/John + Paul) + speculative appendix (mythic parallels, non-canonical gospels).
- No code or software changes; this is a textual/content redesign.

### Components and Responsibilities
- **Core Thesis (Core_Thesis.md)**: States the primary corpus as the four gospels + Paul, removes Q.
- **Chapter Outlines (Book_Scholar_Outline.md)**: 
  - Chapter 3 now focuses on Mark and Matthew (with plans to expand to Luke and John in future writes).
  - Appendix A updated to Mark and Matthew only.
- **Evidence Protocol**: Unchanged; every claim must still have primary text, dating, LXX/MT comparison, NT alignment, mainstream counter, counter-counter, confidence, falsifier.
- **Non-Canonical Gospels**: To be added as a bracketed, speculative subsection in an appendix (likely Appendix C) with clear labeling that they are not part of the core argument.

### Data Flow
- Research flows from primary sources (critical editions of LXX, MT, NA28/UBS5 for NT) → claim–evidence matrix per gospel → outline chapters → manuscript.

### Error Handling Approach
- N/A for content; however, the evidence protocol includes falsifiability conditions for each claim.

### Testing Strategy
- Each claim in the outline must be verified against primary sources.
- The predictive framework (Chapter 7) provides concrete checks (e.g., LXX-only manuscript discoveries, absence of Hebrew gospel).
- Future work: run verification tasks using the writing-plans skill to create tasks for each claim.

## Next Steps
1. Commit this design doc.
2. Use the writing-plans skill to create a detailed implementation plan (task list) for fleshing out the chapters with the new focus.
3. Execute the plan via subagent-driven development (TDD) or manual execution as preferred.

## Related Files
- Core_Thesis.md
- Book_Scholar_Outline.md
- Book_Part1.md through Book_Part4.md
- README.md
- SOURCES.md

---
## /grill-me Results (Stress-Test)
- Evidence boundary locked: core = Mark/Matthew/Luke/John + Paul + climate; bracketed = non-canon gospels + mythic parallels; Q excluded.
- Counter framework complete: A (Paul Hebrew) + B (Mark Vorlage) in P2 framework; C (Thomas earlier) + D (Dura-Europos date) to be bracketed.
- Frontier resolved (Q3 + Q4): 9-field matrix enforced; commit sequence a→b→c.
- Pending: subagent `research_findings` (background) — will be integrated when delivered.
