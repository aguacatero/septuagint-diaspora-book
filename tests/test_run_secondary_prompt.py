import pytest
import asyncio
from unittest.mock import AsyncMock, patch

from scripts.run_secondary_prompt import (
    validate_notebook_state,
    verify_marker_tooltip_binding,
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

def test_verify_marker_tooltip_binding_success_dynamic_movement():
    # Marker 0
    m0_pos = {"x": 100, "y": 200}
    t0_rect = {"left": 100, "top": 220, "x": 100, "y": 220, "width": 200, "height": 80}
    b0 = verify_marker_tooltip_binding(0, "1", m0_pos, t0_rect, "Snippet text for marker 0")
    assert b0["marker_idx"] == 0
    assert b0["snippet"] == "Snippet text for marker 0"

    # Marker 1 (distinct position, distinct snippet)
    m1_pos = {"x": 100, "y": 400}
    t1_rect = {"left": 100, "top": 420, "x": 100, "y": 420, "width": 200, "height": 80}
    b1 = verify_marker_tooltip_binding(1, "2", m1_pos, t1_rect, "Snippet text for marker 1", prev_binding=b0)
    assert b1["marker_idx"] == 1
    assert b1["snippet"] == "Snippet text for marker 1"

def test_verify_marker_tooltip_binding_legitimate_shared_excerpt():
    # Two markers citing the same excerpt (e.g. Footnote 19), with tooltip properly repositioning with marker
    m0_pos = {"x": 100, "y": 200}
    t0_rect = {"left": 100, "top": 220, "x": 100, "y": 220, "width": 200, "height": 80}
    shared_snippet = "Paul and LXX-B have forms of agapan, whereas LXX-A uses forms of eleein (Footnote 19)"
    b0 = verify_marker_tooltip_binding(0, "4", m0_pos, t0_rect, shared_snippet)

    # Next marker moved down by 60px, and tooltip also repositioned down by 60px
    m1_pos = {"x": 100, "y": 260}
    t1_rect = {"left": 100, "top": 280, "x": 100, "y": 280, "width": 200, "height": 80}
    b1 = verify_marker_tooltip_binding(1, "5", m1_pos, t1_rect, shared_snippet, prev_binding=b0)
    assert b1["marker_idx"] == 1
    assert b1["snippet"] == shared_snippet

def test_verify_marker_tooltip_binding_stale_retained_overlay_failure():
    # Marker moved from (100, 200) to (100, 300), but tooltip overlay remained statically retained at (100, 220)
    m0_pos = {"x": 100, "y": 200}
    t0_rect = {"left": 100, "top": 220, "x": 100, "y": 220, "width": 200, "height": 80}
    stale_snippet = "Snippet from marker 0 that failed to unmount or update"
    b0 = verify_marker_tooltip_binding(0, "1", m0_pos, t0_rect, stale_snippet)

    m1_pos = {"x": 100, "y": 300}
    # Tooltip has identical position (t_dist_y < 2, t_dist_x < 2) despite marker movement (m_dist_y = 100)
    t1_rect_stale = {"left": 100, "top": 220, "x": 100, "y": 220, "width": 200, "height": 80}
    with pytest.raises(RuntimeError, match="Stale retained overlay detected at marker 1"):
        verify_marker_tooltip_binding(1, "2", m1_pos, t1_rect_stale, stale_snippet, prev_binding=b0)

def test_verify_marker_tooltip_binding_detached_geometric_proximity_failure():
    # Tooltip rendered far away (> 300px vertical distance) from marker
    m_pos = {"x": 100, "y": 100}
    t_rect_far = {"left": 100, "top": 600, "x": 100, "y": 600, "width": 200, "height": 80}
    with pytest.raises(RuntimeError, match="Positive anchor binding failed at marker 0"):
        verify_marker_tooltip_binding(0, "1", m_pos, t_rect_far, "Snippet text that is detached from marker")

def test_verify_marker_tooltip_binding_empty_snippet_rejection():
    m_pos = {"x": 100, "y": 200}
    t_rect = {"left": 100, "top": 220, "x": 100, "y": 220, "width": 200, "height": 80}
    with pytest.raises(RuntimeError, match="Tooltip binding invariant violated at marker 0: snippet is empty or too short"):
        verify_marker_tooltip_binding(0, "1", m_pos, t_rect, "")

    with pytest.raises(RuntimeError, match="Tooltip binding invariant violated at marker 0: snippet is empty or too short"):
        verify_marker_tooltip_binding(0, "1", m_pos, t_rect, "short")
