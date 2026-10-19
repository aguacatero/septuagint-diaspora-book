import pytest
import asyncio
from unittest.mock import AsyncMock, patch

from scripts.run_secondary_prompt import (
    validate_notebook_state,
    verify_tooltip_transition,
    validate_citations,
    verify_tab_invariants,
    EXPECTED_DEFAULT_SOURCE,
)

def test_validate_notebook_state_success():
    # Valid title and exact expected sole source
    validate_notebook_state("SDP-B001-EXTRACT", ["aageson_1984_pauls_use_of_scripture.pdf"])
    validate_notebook_state("Notebook: SDP-B001-EXTRACT (Staging)", ["aageson_1984_pauls_use_of_scripture.pdf"])

def test_validate_notebook_state_wrong_single_source_rejection():
    # Correct notebook title and single source, but WRONG document identity
    with pytest.raises(RuntimeError, match="Source identity invariant violated: expected sole source"):
        validate_notebook_state("SDP-B001-EXTRACT", ["thesis.pdf"])

    with pytest.raises(RuntimeError, match="Source identity invariant violated: expected sole source"):
        validate_notebook_state("SDP-B001-EXTRACT", ["unrelated_document.pdf"])

    with pytest.raises(RuntimeError, match="Source identity invariant violated: expected sole source"):
        validate_notebook_state("SDP-B001-EXTRACT", ["aageson_1984.pdf"])

def test_validate_notebook_state_configurable_expected_source():
    # Custom expected source
    validate_notebook_state("SDP-B001-EXTRACT", ["custom_source.pdf"], expected_source="custom_source.pdf")
    with pytest.raises(RuntimeError, match="Source identity invariant violated"):
        validate_notebook_state("SDP-B001-EXTRACT", ["wrong_source.pdf"], expected_source="custom_source.pdf")

def test_validate_notebook_state_invalid_title():
    # Wrong notebook title
    with pytest.raises(RuntimeError, match="does not match expected 'SDP-B001-EXTRACT'"):
        validate_notebook_state("SDP-01 Paul", ["aageson_1984_pauls_use_of_scripture.pdf"])
    
    with pytest.raises(RuntimeError, match="does not match expected 'SDP-B001-EXTRACT'"):
        validate_notebook_state("", ["aageson_1984_pauls_use_of_scripture.pdf"])

def test_validate_notebook_state_invalid_source_count():
    # 0 sources
    with pytest.raises(RuntimeError, match="Expected exactly 1 source in SDP-B001-EXTRACT, found 0"):
        validate_notebook_state("SDP-B001-EXTRACT", [])

    # Multiple sources
    with pytest.raises(RuntimeError, match="Expected exactly 1 source in SDP-B001-EXTRACT, found 2"):
        validate_notebook_state("SDP-B001-EXTRACT", ["aageson_1984_pauls_use_of_scripture.pdf", "other.pdf"])

def test_verify_tooltip_transition_success():
    # Dynamic update between different snippets
    count = verify_tooltip_transition("Initial snippet text...", "New distinct snippet text...", 1, 1)
    assert count == 1

    # Legitimate repeated excerpts across a few markers (e.g. same footnote)
    count = verify_tooltip_transition("Footnote 19 on LXX-A/B", "Footnote 19 on LXX-A/B", 2, 1, max_consecutive=15)
    assert count == 2
    count = verify_tooltip_transition("Footnote 19 on LXX-A/B", "Footnote 19 on LXX-A/B", 3, 2, max_consecutive=15)
    assert count == 3

def test_verify_tooltip_transition_stale_tooltip_rejection():
    # Tooltip that fails to update across more than max_consecutive markers (stuck overlay)
    with pytest.raises(RuntimeError, match="Stale tooltip detected at marker 16"):
        verify_tooltip_transition("Frozen overlay text...", "Frozen overlay text...", 16, 15, max_consecutive=15)

def test_verify_tooltip_transition_empty_snippet_rejection():
    with pytest.raises(RuntimeError, match="Stale/invalid tooltip invariant violated"):
        verify_tooltip_transition("Valid text...", "", 2, 1)

    with pytest.raises(RuntimeError, match="Stale/invalid tooltip invariant violated"):
        verify_tooltip_transition("Valid text...", "short", 2, 1)

def test_validate_citations_success():
    citations = [
        {"index": 0, "label": "1", "snippet": "In Romans 4:3, Paul cites Genesis 15:6..."},
        {"index": 1, "label": "2", "snippet": "Regarding Hosea 2:23 in Romans 9:25..."},
        {"index": 2, "label": "3", "snippet": "The textual variation in Galatians 3:13..."},
        {"index": 3, "label": "4", "snippet": "Finally, the katallasso group in 2 Cor 5..."},
    ]
    # Should pass without error
    validate_citations(citations, abstract_sample="Biblical Interpretation in Early Palestinian Judaism")

def test_validate_citations_empty_list():
    with pytest.raises(RuntimeError, match="Extraction invariant violated: no citations extracted"):
        validate_citations([])

def test_validate_citations_all_empty_snippets():
    citations = [
        {"index": 0, "label": "1", "snippet": ""},
        {"index": 1, "label": "2", "snippet": "   "},
        {"index": 2, "label": "3", "snippet": ""},
    ]
    with pytest.raises(RuntimeError, match="Extraction invariant violated: all citation snippets are empty"):
        validate_citations(citations)

def test_validate_citations_duplicate_capture_detected():
    # 5 identical snippets from capturing the wrong element
    duplicate_text = "Title: Paul's Use of Scripture. Abstract summary of thesis."
    citations = [
        {"index": i, "label": str(i + 1), "snippet": duplicate_text}
        for i in range(5)
    ]
    with pytest.raises(RuntimeError, match="all 5 citation snippets are identical \\(duplicate capture detected\\)"):
        validate_citations(citations)

def test_validate_citations_abstract_pollution_detected():
    # Snippets polluted with source-guide abstract text
    citations = [
        {"index": 0, "label": "1", "snippet": "A Comparative Study of Biblical Interpretation in Early Palestinian Judaism and Paul"},
        {"index": 1, "label": "2", "snippet": "A Comparative Study of Biblical Interpretation in Early Palestinian Judaism part 2"},
        {"index": 2, "label": "3", "snippet": "Different excerpt on Rom 9:25"},
        {"index": 3, "label": "4", "snippet": "Early Palestinian Judaism comparative notes"},
    ]
    with pytest.raises(RuntimeError, match="match the source guide / thesis abstract"):
        validate_citations(citations, abstract_sample="Early Palestinian Judaism")

def test_verify_tab_invariants_integration():
    async def _test():
        mock_ws = AsyncMock()
        state = {
            "title": "SDP-B001-EXTRACT",
            "sources": ["aageson_1984_pauls_use_of_scripture.pdf"],
            "abstract": "Source guide ABSTRACT: Paul's Use of Scripture"
        }
        with patch("scripts.run_secondary_prompt.evaluate", new=AsyncMock(return_value=state)):
            abstract = await verify_tab_invariants(mock_ws)
            assert abstract == state["abstract"]

    asyncio.run(_test())

def test_verify_tab_invariants_failure_on_wrong_notebook():
    async def _test():
        mock_ws = AsyncMock()
        state = {
            "title": "SDP-01 Paul",
            "sources": ["aageson_1984_pauls_use_of_scripture.pdf"],
            "abstract": ""
        }
        with patch("scripts.run_secondary_prompt.evaluate", new=AsyncMock(return_value=state)):
            with pytest.raises(RuntimeError, match="Connected notebook title 'SDP-01 Paul' does not match"):
                await verify_tab_invariants(mock_ws)

    asyncio.run(_test())

def test_verify_tab_invariants_failure_on_wrong_source():
    async def _test():
        mock_ws = AsyncMock()
        state = {
            "title": "SDP-B001-EXTRACT",
            "sources": ["wrong_source.pdf"],
            "abstract": ""
        }
        with patch("scripts.run_secondary_prompt.evaluate", new=AsyncMock(return_value=state)):
            with pytest.raises(RuntimeError, match="Source identity invariant violated"):
                await verify_tab_invariants(mock_ws)

    asyncio.run(_test())
