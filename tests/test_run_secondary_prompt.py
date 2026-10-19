import pytest
import asyncio
import sys
from pathlib import Path
from unittest.mock import AsyncMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

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
    # [Simulated helper unit test]
    # Marker 0
    m0_pos = {"x": 100, "y": 200}
    t0_rect = {"left": 100, "top": 220, "x": 100, "y": 220, "width": 200, "height": 80}
    b0 = verify_marker_tooltip_binding(0, "1", m0_pos, t0_rect, "Snippet text for marker 0", handshake_verified=True)
    assert b0["marker_idx"] == 0
    assert b0["snippet"] == "Snippet text for marker 0"

    # Marker 1 (distinct position, distinct snippet)
    m1_pos = {"x": 100, "y": 400}
    t1_rect = {"left": 100, "top": 420, "x": 100, "y": 420, "width": 200, "height": 80}
    b1 = verify_marker_tooltip_binding(1, "2", m1_pos, t1_rect, "Snippet text for marker 1", handshake_verified=True, prev_binding=b0)
    assert b1["marker_idx"] == 1
    assert b1["snippet"] == "Snippet text for marker 1"

def test_verify_marker_tooltip_binding_legitimate_shared_excerpt():
    # [Simulated helper unit test]
    # Two markers citing the same excerpt (e.g. Footnote 19), with tooltip properly repositioning with marker
    m0_pos = {"x": 100, "y": 200}
    t0_rect = {"left": 100, "top": 220, "x": 100, "y": 220, "width": 200, "height": 80}
    shared_snippet = "Paul and LXX-B have forms of agapan, whereas LXX-A uses forms of eleein (Footnote 19)"
    b0 = verify_marker_tooltip_binding(0, "4", m0_pos, t0_rect, shared_snippet, handshake_verified=True)

    # Next marker moved down by 60px, and tooltip also repositioned down by 60px
    m1_pos = {"x": 100, "y": 260}
    t1_rect = {"left": 100, "top": 280, "x": 100, "y": 280, "width": 200, "height": 80}
    b1 = verify_marker_tooltip_binding(1, "5", m1_pos, t1_rect, shared_snippet, handshake_verified=True, prev_binding=b0)
    assert b1["marker_idx"] == 1
    assert b1["snippet"] == shared_snippet

def test_verify_marker_tooltip_binding_stale_retained_overlay_failure():
    # [Simulated helper unit test]
    # Marker moved from (100, 200) to (100, 300), but tooltip overlay remained statically retained at (100, 220)
    m0_pos = {"x": 100, "y": 200}
    t0_rect = {"left": 100, "top": 220, "x": 100, "y": 220, "width": 200, "height": 80}
    stale_snippet = "Snippet from marker 0 that failed to unmount or update"
    b0 = verify_marker_tooltip_binding(0, "1", m0_pos, t0_rect, stale_snippet, handshake_verified=True)

    m1_pos = {"x": 100, "y": 300}
    # Tooltip has identical position (t_dist_y < 2, t_dist_x < 2) despite marker movement (m_dist_y = 100)
    t1_rect_stale = {"left": 100, "top": 220, "x": 100, "y": 220, "width": 200, "height": 80}
    with pytest.raises(RuntimeError, match="Stale retained overlay detected at marker 1"):
        verify_marker_tooltip_binding(1, "2", m1_pos, t1_rect_stale, stale_snippet, handshake_verified=True, prev_binding=b0)

def test_verify_marker_tooltip_binding_detached_geometric_proximity_failure():
    # [Simulated helper unit test]
    # Tooltip rendered far away (> 300px vertical distance) from marker
    m_pos = {"x": 100, "y": 100}
    t_rect_far = {"left": 100, "top": 600, "x": 100, "y": 600, "width": 200, "height": 80}
    with pytest.raises(RuntimeError, match="Positive anchor binding failed at marker 0"):
        verify_marker_tooltip_binding(0, "1", m_pos, t_rect_far, "Snippet text that is detached from marker", handshake_verified=True)

def test_verify_marker_tooltip_binding_empty_snippet_rejection():
    # [Simulated helper unit test]
    m_pos = {"x": 100, "y": 200}
    t_rect = {"left": 100, "top": 220, "x": 100, "y": 220, "width": 200, "height": 80}
    with pytest.raises(RuntimeError, match="Tooltip binding invariant violated at marker 0: snippet is empty or too short"):
        verify_marker_tooltip_binding(0, "1", m_pos, t_rect, "")

    with pytest.raises(RuntimeError, match="Tooltip binding invariant violated at marker 0: snippet is empty or too short"):
        verify_marker_tooltip_binding(0, "1", m_pos, t_rect, "short")

def test_verify_marker_tooltip_binding_handshake_failure():
    # [Simulated helper unit test]
    # If the pre-hover overlay clear handshake fails (retained from prior marker without clean dismiss), fail closed
    m_pos = {"x": 100, "y": 200}
    t_rect = {"left": 100, "top": 220, "x": 100, "y": 220, "width": 200, "height": 80}
    with pytest.raises(RuntimeError, match="Observable marker-to-tooltip handshake failed at marker 0"):
        verify_marker_tooltip_binding(0, "1", m_pos, t_rect, "Valid snippet text here...", handshake_verified=False)

def test_verify_marker_tooltip_binding_missing_geometry_fails_closed():
    # [Simulated helper unit test]
    # If marker_pos or tooltip_rect metadata is missing, fail closed immediately
    with pytest.raises(RuntimeError, match="missing geometric rect metadata"):
        verify_marker_tooltip_binding(0, "1", None, {"left": 100, "top": 220}, "Valid snippet text here...", handshake_verified=True)

    with pytest.raises(RuntimeError, match="missing geometric rect metadata"):
        verify_marker_tooltip_binding(0, "1", {"x": 100, "y": 200}, None, "Valid snippet text here...", handshake_verified=True)

def test_verify_marker_tooltip_binding_centered_scroll_counterexample():
    # Deterministic counterexample from review Finding 3:
    # scrollIntoView({block:'center'}) brings adjacent markers to nearly identical coordinates
    # marker0=(100,200), tooltip=(100,220); marker1=(100,205), same frozen tooltip=(100,220)
    m0_pos = {"x": 100, "y": 200}
    t0_rect = {"left": 100, "top": 220, "x": 100, "y": 220, "width": 200, "height": 80}
    snippet0 = "Footnote 19 on LXX-A/B agreement in Rom 9:26"
    b0 = verify_marker_tooltip_binding(0, "4", m0_pos, t0_rect, snippet0, handshake_verified=True)

    # 1. Counterexample: marker moved slightly (y=205 vs 200), but tooltip overlay remained statically retained at y=220.
    # Must fail closed immediately rather than passing as legitimate!
    m1_pos = {"x": 100, "y": 205}
    t1_rect_frozen = {"left": 100, "top": 220, "x": 100, "y": 220, "width": 200, "height": 80}
    with pytest.raises(RuntimeError, match="Stale retained overlay detected at marker 1"):
        verify_marker_tooltip_binding(1, "5", m1_pos, t1_rect_frozen, snippet0, handshake_verified=True, prev_binding=b0)

    # 2. Legitimate shared excerpt: tooltip properly repositions with marker (y=225)
    t1_rect_repositioned = {"left": 100, "top": 225, "x": 100, "y": 225, "width": 200, "height": 80}
    b1 = verify_marker_tooltip_binding(1, "5", m1_pos, t1_rect_repositioned, snippet0, handshake_verified=True, prev_binding=b0)
    assert b1["marker_idx"] == 1
    assert b1["snippet"] == snippet0

    # 3. If handshake was NOT verified (stale retention without unmount), fail closed
    with pytest.raises(RuntimeError, match="Observable marker-to-tooltip handshake failed"):
        verify_marker_tooltip_binding(2, "6", m1_pos, t1_rect_repositioned, snippet0, handshake_verified=False, prev_binding=b1)

def test_extraction_loop_transition_sequence_success_25_markers():
    """
    Loop-level integration test: simulates 25 successive markers with distinct excerpts.
    Verifies that preserving old_snippet before updating prev_binding completes cleanly
    with consecutive_duplicates == 1 throughout, avoiding false freeze detection.
    """
    prev_binding = None
    consecutive_duplicates = 0

    for idx in range(25):
        snippet = f"Distinct passage excerpt text for marker index {idx} in thesis Chapter {idx % 5 + 1}."
        m_label = str(idx + 1)
        pos = {"x": 100, "y": 200 + (idx % 5) * 40}
        t_rect = {"left": 100, "top": 220 + (idx % 5) * 40, "x": 100, "y": 220 + (idx % 5) * 40, "width": 250, "height": 70}

        # Invariant 4: Check transition against old_snippet
        old_snippet = prev_binding.get("snippet", "") if prev_binding else ""
        consecutive_duplicates = verify_tooltip_transition(
            old_snippet, snippet, idx, consecutive_duplicates, max_consecutive=15
        )
        assert consecutive_duplicates == 1, f"Expected duplicate count 1 for distinct marker {idx}, got {consecutive_duplicates}"

        # Invariant 5: Update prev_binding with handshake
        prev_binding = verify_marker_tooltip_binding(
            idx, m_label, pos, t_rect, snippet, handshake_verified=True, prev_binding=prev_binding
        )
        assert prev_binding["snippet"] == snippet

def test_extraction_loop_legitimate_repeated_excerpts_and_freeze_rejection():
    """
    Loop-level test: validates legitimate clusters of repeated snippets (e.g. 5 identical from same footnote),
    followed by distinct snippets, and verifies that an actual prolonged freeze (> 15 identical) fails closed.
    """
    prev_binding = None
    consecutive_duplicates = 0

    # First 5 markers cite the same footnote
    shared_footnote = "Footnote 19 on Codex Alexandrinus and Vaticanus variants in Romans 9-11"
    for idx in range(5):
        m_label = str(idx + 1)
        pos = {"x": 100, "y": 200 + idx * 10}
        t_rect = {"left": 100, "top": 220 + idx * 10, "x": 100, "y": 220 + idx * 10, "width": 250, "height": 70}

        old_snippet = prev_binding.get("snippet", "") if prev_binding else ""
        consecutive_duplicates = verify_tooltip_transition(
            old_snippet, shared_footnote, idx, consecutive_duplicates, max_consecutive=15
        )
        prev_binding = verify_marker_tooltip_binding(
            idx, m_label, pos, t_rect, shared_footnote, handshake_verified=True, prev_binding=prev_binding
        )
    assert consecutive_duplicates == 5

    # Marker 5 switches to a new distinct snippet
    new_snippet = "Different text from Chapter V on Deuteronomic law"
    old_snippet = prev_binding.get("snippet", "")
    consecutive_duplicates = verify_tooltip_transition(
        old_snippet, new_snippet, 5, consecutive_duplicates, max_consecutive=15
    )
    assert consecutive_duplicates == 1  # Successfully reset!

    # Now simulate a true frozen overlay persisting for 16 consecutive markers
    frozen_snippet = "Frozen overlay that never changes"
    consecutive_duplicates = 0
    prev_binding = None
    with pytest.raises(RuntimeError, match="Stale tooltip detected at marker 15"):
        for idx in range(20):
            old_snippet = prev_binding.get("snippet", "") if prev_binding else ""
            consecutive_duplicates = verify_tooltip_transition(
                old_snippet, frozen_snippet, idx, consecutive_duplicates, max_consecutive=15
            )
            prev_binding = verify_marker_tooltip_binding(
                idx, str(idx), {"x": 100, "y": 200}, {"left": 100, "top": 220, "x": 100, "y": 220, "width": 200, "height": 80},
                frozen_snippet, handshake_verified=True, prev_binding=prev_binding
            )


# ==============================================================================
# Mocked CDP/DOM Collector Sequence Unit Tests (Review Round 5 Finding 4)
# ==============================================================================
from scripts.extract_all_messages import extract_message_citations

@pytest.mark.anyio
async def test_collector_ineffective_escape_fails_closed(tmp_path):
    """
    Mocked CDP/DOM collector sequence test:
    Exercises pre-hover overlay dismissal where mouse is moved to (0, 0),
    overlay remains visible, Escape key is dispatched, but overlay still
    lingers. Collector must fail closed with RuntimeError rather than proceeding.
    """
    mock_ws = AsyncMock()
    out_file = str(tmp_path / "out.json")

    async def mock_eval(ws, expr):
        if "more_horiz" in expr:
            return None
        if "markerCount" in expr:
            return {"text": "Message content", "markerCount": 1}
        if "lingeringIds" in expr:
            # Persistent stuck overlay that never dismisses even after Escape
            return {"cleared": False, "visibleCount": 1, "lingeringIds": ["cdk-overlay-99"]}
        return None

    with patch("scripts.extract_all_messages.call_cdp", new=AsyncMock()), \
         patch("scripts.extract_all_messages.evaluate", new=mock_eval), \
         patch("scripts.extract_all_messages.asyncio.sleep", new=AsyncMock()):
        with pytest.raises(RuntimeError, match=r"Fail-closed: CDK overlay container failed to dismiss prior to hovering marker 0.*lingering overlay pane IDs: \['cdk-overlay-99'\]"):
            await extract_message_citations(mock_ws, 0, out_file)

@pytest.mark.anyio
async def test_collector_unchanged_retained_overlay_fails_closed(tmp_path):
    """
    Mocked CDP/DOM collector sequence test:
    Exercises consecutive markers where marker 1 moves, but the DOM returns
    an unchanged retained overlay with identical position and snippet from marker 0.
    Collector must fail closed with stale retained overlay detection.
    """
    mock_ws = AsyncMock()
    out_file = str(tmp_path / "out.json")

    marker_idx_queried = 0

    async def mock_eval(ws, expr):
        nonlocal marker_idx_queried
        if "more_horiz" in expr:
            return None
        if "markerCount" in expr:
            return {"text": "Message content with two markers", "markerCount": 2}
        if "lingeringIds" in expr:
            return {"cleared": True, "visibleCount": 0, "lingeringIds": []}
        if "scrollIntoView" in expr:
            # Marker 0 at y=200, Marker 1 displaced to y=300
            m_y = 200 if marker_idx_queried == 0 else 300
            res = {
                "x": 100, "y": m_y,
                "rect": {"left": 90, "top": m_y - 10, "right": 110, "bottom": m_y + 10, "width": 20, "height": 20},
                "label": str(marker_idx_queried + 1)
            }
            marker_idx_queried += 1
            return res
        if "vDist <= 100" in expr:
            # Tooltip remains statically frozen at y=220 for both markers!
            return [{
                "paneId": "cdk-overlay-0",
                "text": "Statically retained snippet text from marker 0 that never unmounted",
                "rect": {"left": 90, "top": 220, "width": 200, "height": 50, "x": 90, "y": 220},
                "vDist": 10,
                "hOverlap": True
            }]
        return None

    with patch("scripts.extract_all_messages.call_cdp", new=AsyncMock()), \
         patch("scripts.extract_all_messages.evaluate", new=mock_eval), \
         patch("scripts.extract_all_messages.asyncio.sleep", new=AsyncMock()):
        with pytest.raises(RuntimeError, match="Stale retained overlay detected at marker 1"):
            await extract_message_citations(mock_ws, 0, out_file)

@pytest.mark.anyio
async def test_collector_unrelated_visible_panel_fails_closed(tmp_path):
    """
    Mocked CDP/DOM collector sequence test:
    Exercises trigger-bound query when an unrelated detached panel exists in CDK
    overlay container, so no pane matches vDist <= 100 && hOverlap.
    Collector must fail closed rather than binding to the detached panel.
    """
    mock_ws = AsyncMock()
    out_file = str(tmp_path / "out.json")

    async def mock_eval(ws, expr):
        if "more_horiz" in expr:
            return None
        if "markerCount" in expr:
            return {"text": "Message content", "markerCount": 1}
        if "lingeringIds" in expr:
            return {"cleared": True, "visibleCount": 0, "lingeringIds": []}
        if "scrollIntoView" in expr:
            return {
                "x": 100, "y": 200,
                "rect": {"left": 90, "top": 190, "right": 110, "bottom": 210, "width": 20, "height": 20},
                "label": "1"
            }
        if "vDist <= 100" in expr:
            # Query returned empty because only unrelated panels (> 100px away or disconnected) exist
            return []
        return None

    with patch("scripts.extract_all_messages.call_cdp", new=AsyncMock()), \
         patch("scripts.extract_all_messages.evaluate", new=mock_eval), \
         patch("scripts.extract_all_messages.asyncio.sleep", new=AsyncMock()):
        with pytest.raises(RuntimeError, match=r"Fail-closed: could not establish fresh, trigger-bound tooltip handshake for marker 0 \(label 1\)"):
            await extract_message_citations(mock_ws, 0, out_file)

@pytest.mark.anyio
async def test_collector_multiple_conflicting_panels_fails_closed(tmp_path):
    """
    Mocked CDP/DOM collector sequence test:
    Exercises trigger-bound query when multiple conflicting overlay panes match
    vDist <= 100 && hOverlap. Collector must fail closed immediately.
    """
    mock_ws = AsyncMock()
    out_file = str(tmp_path / "out.json")

    async def mock_eval(ws, expr):
        if "more_horiz" in expr:
            return None
        if "markerCount" in expr:
            return {"text": "Message content", "markerCount": 1}
        if "lingeringIds" in expr:
            return {"cleared": True, "visibleCount": 0, "lingeringIds": []}
        if "scrollIntoView" in expr:
            return {
                "x": 100, "y": 200,
                "rect": {"left": 90, "top": 190, "right": 110, "bottom": 210, "width": 20, "height": 20},
                "label": "1"
            }
        if "vDist <= 100" in expr:
            # 2 conflicting panes matching trigger bounds
            return [
                {
                    "paneId": "cdk-overlay-1",
                    "text": "First conflicting tooltip text on passage A",
                    "rect": {"left": 90, "top": 218, "width": 200, "height": 50, "x": 90, "y": 218},
                    "vDist": 8, "hOverlap": True
                },
                {
                    "paneId": "cdk-overlay-2",
                    "text": "Second conflicting tooltip text on passage B",
                    "rect": {"left": 90, "top": 220, "width": 200, "height": 50, "x": 90, "y": 220},
                    "vDist": 10, "hOverlap": True
                }
            ]
        return None

    with patch("scripts.extract_all_messages.call_cdp", new=AsyncMock()), \
         patch("scripts.extract_all_messages.evaluate", new=mock_eval), \
         patch("scripts.extract_all_messages.asyncio.sleep", new=AsyncMock()):
        with pytest.raises(RuntimeError, match="Fail-closed: Multiple conflicting trigger-bound overlays detected for marker 0"):
            await extract_message_citations(mock_ws, 0, out_file)

@pytest.mark.anyio
async def test_collector_centered_scroll_fresh_handshake_success(tmp_path):
    """
    Mocked CDP/DOM collector sequence test:
    Exercises successive markers where scrollIntoView({block: 'center'}) places
    markers at near-identical coordinates (y=200 vs y=204).
    Verifies that pre-hover cleared verification + fresh trigger-bound overlay
    tracking (unique paneId and shifted rect) passes cleanly and produces
    complete replayable audit records.
    """
    mock_ws = AsyncMock()
    out_file = str(tmp_path / "out.json")

    marker_idx_queried = 0

    async def mock_eval(ws, expr):
        nonlocal marker_idx_queried
        if "more_horiz" in expr:
            return None
        if "markerCount" in expr:
            return {"text": "Message text with centered markers", "markerCount": 2}
        if "lingeringIds" in expr:
            return {"cleared": True, "visibleCount": 0, "lingeringIds": []}
        if "scrollIntoView" in expr:
            m_y = 200 if marker_idx_queried == 0 else 204
            res = {
                "x": 100, "y": m_y,
                "rect": {"left": 90, "top": m_y - 10, "right": 110, "bottom": m_y + 10, "width": 20, "height": 20},
                "label": str(marker_idx_queried + 1)
            }
            marker_idx_queried += 1
            return res
        if "vDist <= 100" in expr:
            if marker_idx_queried == 1:
                return [{
                    "paneId": "cdk-overlay-1",
                    "text": "First passage excerpt on Romans 9:25 from printed page 69",
                    "rect": {"left": 90, "top": 218, "width": 200, "height": 50, "x": 90, "y": 218},
                    "vDist": 8, "hOverlap": True
                }]
            else:
                return [{
                    "paneId": "cdk-overlay-2",
                    "text": "Second distinct passage excerpt on Romans 9:26 from page 70",
                    "rect": {"left": 90, "top": 222, "width": 200, "height": 50, "x": 90, "y": 222},
                    "vDist": 8, "hOverlap": True
                }]
        return None

    with patch("scripts.extract_all_messages.call_cdp", new=AsyncMock()), \
         patch("scripts.extract_all_messages.evaluate", new=mock_eval), \
         patch("scripts.extract_all_messages.asyncio.sleep", new=AsyncMock()):
        await extract_message_citations(mock_ws, 0, out_file)

    # Verify output file and audit records
    import json
    with open(out_file) as f:
        data = json.load(f)

    assert len(data["citations"]) == 2
    for c in data["citations"]:
        audit = c["audit"]
        assert audit["pre_hover_cleared"] is True
        assert audit["trigger_bound"] is True
        assert audit["handshake_verified"] is True
        assert audit["vertical_dist"] == 8
        assert audit["overlay_pane_id"].startswith("cdk-overlay-")
        assert "marker_rect" in audit and "tooltip_rect" in audit

