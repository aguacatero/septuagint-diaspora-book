import asyncio
import json
import sys
import time
import urllib.request
import websockets

EXPECTED_DEFAULT_SOURCE = "aageson_1984_pauls_use_of_scripture.pdf"

def validate_notebook_state(title: str, sources: list, expected_source: str = EXPECTED_DEFAULT_SOURCE):
    """
    Validates that:
    1. Connected notebook title matches SDP-B001-EXTRACT.
    2. Exactly one source is loaded in the staging notebook.
    3. The loaded source matches expected_source exactly (rejecting wrong single sources,
       mismatches, duplicates, or ambiguous titles).
    """
    if not title or "SDP-B001-EXTRACT" not in title:
        raise RuntimeError(f"Connected notebook title '{title}' does not match expected 'SDP-B001-EXTRACT'")
    if len(sources) != 1:
        raise RuntimeError(f"Expected exactly 1 source in SDP-B001-EXTRACT, found {len(sources)}: {sources}")
    actual_source = sources[0].strip()
    if actual_source != expected_source:
        raise RuntimeError(
            f"Source identity invariant violated: expected sole source '{expected_source}', "
            f"but found '{actual_source}'"
        )

def verify_marker_tooltip_binding(
    marker_idx: int,
    marker_label: str,
    marker_pos: dict,
    tooltip_rect: dict,
    snippet: str,
    handshake_verified: bool = False,
    active_pane_id: str = None,
    prev_binding: dict = None
) -> dict:
    """
    Enforces a positive, fail-closed binding between a hovered/clicked marker
    and the captured tooltip overlay:
    1. Non-empty, valid snippet.
    2. Observable handshake verification: for subsequent markers, the overlay must
       have been confirmed cleared/unmounted prior to trigger activation.
    3. Geometric anchor metadata: fails closed if marker or tooltip rect metadata is missing
       or lacks required numeric coordinates.
    4. Proximity bounds (secondary defense): tooltip must be vertically proximate (<= 300px)
       and horizontally aligned (<= 400px).
    5. Retained stale overlay detection: detects frozen overlays across centered markers,
       adjacent markers with small displacements, and static retained panels.
    6. Permits legitimate identical snippets only when positive anchor ownership and
       fresh activation are proven.
    """
    if not snippet or len(snippet.strip()) < 10:
        raise RuntimeError(f"Tooltip binding invariant violated at marker {marker_idx}: snippet is empty or too short")

    if not handshake_verified:
        raise RuntimeError(
            f"Observable marker-to-tooltip handshake failed at marker {marker_idx}: overlay was not confirmed "
            f"cleared prior to hover activation or was retained from a previous marker."
        )

    if not isinstance(marker_pos, dict) or "x" not in marker_pos or "y" not in marker_pos:
        raise RuntimeError(
            f"Positive anchor binding failed at marker {marker_idx}: missing geometric rect metadata (marker_pos)."
        )

    if not isinstance(tooltip_rect, dict) or not any(k in tooltip_rect for k in ("top", "y")) or not any(k in tooltip_rect for k in ("left", "x")):
        raise RuntimeError(
            f"Positive anchor binding failed at marker {marker_idx}: missing geometric rect metadata (tooltip_rect)."
        )

    my = marker_pos.get("y", 0)
    mx = marker_pos.get("x", 0)
    ty = tooltip_rect.get("top", tooltip_rect.get("y", 0))
    tx = tooltip_rect.get("left", tooltip_rect.get("x", 0))
    th = tooltip_rect.get("height", 0)
    tw = tooltip_rect.get("width", 0)

    # Vertical proximity check (secondary defense): tooltip is anchored near trigger
    v_dist = min(abs(ty - my), abs(ty + th - my))
    if v_dist > 300:
        raise RuntimeError(
            f"Positive anchor binding failed at marker {marker_idx}: tooltip vertical distance "
            f"({v_dist:.1f}px) exceeds attachment threshold (300px). Suspected retained stale overlay."
        )

    # Horizontal proximity check
    h_dist = min(abs(tx - mx), abs(tx + tw - mx))
    if h_dist > 400:
        raise RuntimeError(
            f"Positive anchor binding failed at marker {marker_idx}: tooltip horizontal distance "
            f"({h_dist:.1f}px) exceeds attachment threshold (400px)."
        )

    # Stale retention check across consecutive markers
    if prev_binding:
        prev_snip = prev_binding.get("snippet", "")
        prev_pos = prev_binding.get("marker_pos", {})
        prev_rect = prev_binding.get("tooltip_rect", {})

        if snippet == prev_snip and prev_pos and prev_rect:
            t_dist_y = abs(ty - prev_rect.get("top", prev_rect.get("y", 0)))
            t_dist_x = abs(tx - prev_rect.get("left", prev_rect.get("x", 0)))
            m_dist_y = abs(my - prev_pos.get("y", 0))
            m_dist_x = abs(mx - prev_pos.get("x", 0))

            # 1. Any marker displacement with completely static tooltip overlay
            # Catches small displacements (e.g. 5px, 15px centered scroll variations)
            if (m_dist_y > 2 or m_dist_x > 2) and t_dist_y < 2 and t_dist_x < 2:
                raise RuntimeError(
                    f"Stale retained overlay detected at marker {marker_idx}: marker moved from "
                    f"({prev_pos.get('x')}, {prev_pos.get('y')}) to ({marker_pos.get('x')}, {marker_pos.get('y')}), "
                    f"but tooltip overlay position remained completely static at ({tx}, {ty})."
                )

            # 2. Centered-marker case (same coordinates) with identical static tooltip
            if t_dist_y < 2 and t_dist_x < 2 and not handshake_verified:
                raise RuntimeError(
                    f"Stale retained overlay detected at marker {marker_idx}: centered marker retained static overlay "
                    f"without verified dismissal handshake."
                )

    return {
        "marker_idx": marker_idx,
        "marker_label": marker_label,
        "marker_pos": marker_pos,
        "tooltip_rect": tooltip_rect,
        "snippet": snippet,
        "active_pane_id": active_pane_id,
        "handshake_verified": handshake_verified
    }

def verify_tooltip_transition(
    prev_snippet: str,
    current_snippet: str,
    marker_idx: int,
    consecutive_duplicate_count: int,
    max_consecutive: int = 15
) -> int:
    """
    Tracks duplicate count across successive citations.
    """
    if not current_snippet or len(current_snippet.strip()) < 10:
        raise RuntimeError(f"Stale/invalid tooltip invariant violated at marker {marker_idx}: snippet is empty or too short")

    if prev_snippet and current_snippet == prev_snippet:
        consecutive_duplicate_count += 1
        if consecutive_duplicate_count > max_consecutive:
            raise RuntimeError(
                f"Stale tooltip detected at marker {marker_idx}: snippet has remained unchanged across "
                f"{consecutive_duplicate_count} consecutive markers. Suspected retained/stuck overlay panel."
            )
    else:
        consecutive_duplicate_count = 1

    return consecutive_duplicate_count

def validate_citations(citations: list, abstract_sample: str = ""):
    """
    Enforces fail-closed invariants on extracted citation snippets:
    - Non-empty citations list
    - Not all snippets empty
    - No duplicate capture across distinct markers
    - No abstract pollution matching persistent left sidebar
    """
    if not citations:
        raise RuntimeError("Extraction invariant violated: no citations extracted")

    snippets = [c.get("snippet", "").strip() for c in citations]
    non_empty = [s for s in snippets if s]

    if not non_empty:
        raise RuntimeError("Extraction invariant violated: all citation snippets are empty")

    if len(non_empty) > 3 and len(set(non_empty)) == 1:
        raise RuntimeError(
            f"Extraction invariant violated: all {len(non_empty)} citation snippets are identical "
            "(duplicate capture detected)"
        )

    if abstract_sample:
        abstract_matches = sum(1 for s in non_empty if abstract_sample.lower() in s.lower())
        if abstract_matches > len(non_empty) * 0.5:
            raise RuntimeError(
                f"Extraction invariant violated: {abstract_matches}/{len(non_empty)} citation snippets "
                "match the source guide / thesis abstract rather than inline citation tooltips"
            )

def get_page_ws_url(host: str = "127.0.0.1", port: int = 9222, notebook_pattern: str = "b3cd453a"):
    with urllib.request.urlopen(f"http://{host}:{port}/json") as r:
        tabs = json.loads(r.read())
    nb_tabs = [t for t in tabs if notebook_pattern in t.get("url", "") and t.get("type") == "page"]
    if not nb_tabs:
        raise RuntimeError(f"SDP-B001-EXTRACT tab ({notebook_pattern}) not found at http://{host}:{port}")
    return nb_tabs[0]["webSocketDebuggerUrl"]

async def send_cdp(ws, msg_id, method, params=None):
    payload = {"id": msg_id, "method": method}
    if params:
        payload["params"] = params
    await ws.send(json.dumps(payload))
    while True:
        raw = await ws.recv()
        data = json.loads(raw)
        if data.get("id") == msg_id:
            return data

async def evaluate(ws, msg_id, expr):
    res = await send_cdp(ws, msg_id, "Runtime.evaluate", {
        "expression": expr,
        "returnByValue": True,
        "awaitPromise": True
    })
    if "result" in res and "result" in res["result"]:
        return res["result"]["result"].get("value")
    return None

async def verify_tab_invariants(ws, expected_source: str = EXPECTED_DEFAULT_SOURCE):
    state = await evaluate(ws, 9000, """
    (() => {
        const titleInput = document.querySelector('input.title-input');
        const title = titleInput ? titleInput.value : document.title;
        const sources = Array.from(document.querySelectorAll('.source-panel .source-title, .source-title, [aria-label*="source"]'))
            .map(e => e.innerText.trim())
            .filter(t => t.endsWith('.pdf'));
        const unique = Array.from(new Set(sources));
        const abstractEl = document.querySelector('.source-panel .source-guide-container, .source-panel');
        return {
            title: title,
            sources: unique,
            abstract: abstractEl ? abstractEl.innerText : ""
        };
    })()
    """) or {}
    validate_notebook_state(state.get("title", ""), state.get("sources", []), expected_source=expected_source)
    return state.get("abstract", "")

async def run_prompt(prompt_text, max_wait=150, host="127.0.0.1", port=9222, expected_source: str = EXPECTED_DEFAULT_SOURCE):
    ws_url = get_page_ws_url(host=host, port=port)
    async with websockets.connect(ws_url, max_size=20*1024*1024) as ws:
        # Invariant 1: Verify notebook title and exact single source loaded
        abstract_text = await verify_tab_invariants(ws, expected_source=expected_source)

        # Get current count of model messages
        init_count = await evaluate(ws, 1, """
            document.querySelectorAll('.to-user-message-card-content').length
        """) or 0
        print(f"Initial model message count: {init_count}", flush=True)

        # Ensure interface is idle before submitting
        idle = False
        for _ in range(20):
            is_idle = await evaluate(ws, 1000, """
                (() => {
                    const stopBtn = document.querySelector('button[aria-label="Stop response"], button[aria-label*="Stop"]');
                    return !stopBtn;
                })()
            """)
            if is_idle:
                idle = True
                break
            await asyncio.sleep(2)
        if not idle:
            raise RuntimeError("Submission invariant violated: interface is busy (stop response active)")

        escaped_prompt = json.dumps(prompt_text)
        submit_js = f"""
        (() => {{
            const ta = document.querySelector('textarea[aria-label="Query box"], textarea[placeholder*="Ask"]');
            if (!ta) return "NO_TA";
            ta.focus();
            ta.value = {escaped_prompt};
            ta.dispatchEvent(new Event('input', {{ bubbles: true }}));
            ta.dispatchEvent(new Event('change', {{ bubbles: true }}));
            const btn = document.querySelector('button[aria-label="Submit"]');
            if (btn && !btn.disabled) {{
                btn.click();
                return "SUBMITTED_CLICK";
            }}
            return "BTN_DISABLED";
        }})()
        """
        submit_res = await evaluate(ws, 2, submit_js)
        print("Initial submit status:", submit_res, flush=True)

        # If button was disabled or not clicked, wait and retry click
        submitted = (submit_res == "SUBMITTED_CLICK")
        if not submitted:
            for retry in range(15):
                await asyncio.sleep(2)
                retry_res = await evaluate(ws, 20 + retry, """
                (() => {
                    const btn = document.querySelector('button[aria-label="Submit"]');
                    if (btn && !btn.disabled) {
                        btn.click();
                        return "CLICKED_RETRY";
                    }
                    return "STILL_DISABLED";
                })()
                """)
                print(f"Retry submit {retry}: {retry_res}", flush=True)
                if retry_res == "CLICKED_RETRY":
                    submitted = True
                    break

        if not submitted:
            raise RuntimeError("Submission invariant violated: Submit button remained disabled or unavailable")

        start_time = time.time()
        last_text = ""
        stable_count = 0
        stabilized = False
        cur_count = init_count

        # Invariant 2: Wait for new message to appear and stabilize
        while time.time() - start_time < max_wait:
            await asyncio.sleep(3)
            cur_count = await evaluate(ws, 3, """
                document.querySelectorAll('.to-user-message-card-content').length
            """) or 0

            if cur_count > init_count:
                cur_text = await evaluate(ws, 4, """
                    (() => {
                        const msgs = document.querySelectorAll('.to-user-message-card-content');
                        if (!msgs.length) return "";
                        return msgs[msgs.length - 1].innerText;
                    })()
                """) or ""

                # Check if still thinking / generating
                is_generating = await evaluate(ws, 5, """
                    (() => {
                        const stopBtn = document.querySelector('button[aria-label="Stop response"], button[aria-label*="Stop"]');
                        if (stopBtn && !stopBtn.disabled) return true;
                        const spinner = document.querySelector('.to-user-message-card-content:last-child mat-progress-spinner, .to-user-message-card-content:last-child .loading-indicator');
                        if (spinner) return true;
                        return false;
                    })()
                """)

                print(f"[{int(time.time() - start_time)}s] count={cur_count} (init={init_count}), text_len={len(cur_text)}, generating={is_generating}", flush=True)

                if not is_generating and len(cur_text) > 50:
                    if cur_text == last_text:
                        stable_count += 1
                        if stable_count >= 3:
                            print("Response completed and stable!", flush=True)
                            stabilized = True
                            break
                    else:
                        stable_count = 0
                        last_text = cur_text
                else:
                    stable_count = 0
                    last_text = cur_text
            else:
                print(f"[{int(time.time() - start_time)}s] waiting for new message... cur_count={cur_count}, init={init_count}", flush=True)

        if not stabilized:
            raise TimeoutError(
                f"Generation invariant violated: response did not stabilize within {max_wait}s "
                f"(init_count={init_count}, cur_count={cur_count}, stable_count={stable_count})"
            )

        # Handle collapsed markers if any exist
        await evaluate(ws, 99, """
        (() => {
            const msgs = document.querySelectorAll('.to-user-message-card-content');
            if (!msgs.length) return;
            const lastMsg = msgs[msgs.length - 1];
            const moreBtns = Array.from(lastMsg.querySelectorAll("button.citation-marker")).filter(
                b => b.querySelector('mat-icon')?.innerText.includes('more_horiz')
            );
            for (const b of moreBtns) {
                b.click();
            }
        })()
        """)
        await asyncio.sleep(0.5)

        # Extract message text and citation markers
        extract_info = await evaluate(ws, 10, """
        (() => {
            const msgs = document.querySelectorAll('.to-user-message-card-content');
            if (!msgs.length) return { text: "", markerCount: 0 };
            const lastMsg = msgs[msgs.length - 1];
            const text = lastMsg.innerText;
            const allBtns = Array.from(lastMsg.querySelectorAll("button.citation-marker"));
            const citationBtns = allBtns.filter(b => b.innerText.trim().match(/^\\d+$/));
            return {
                text: text,
                markerCount: citationBtns.length
            };
        })()
        """) or {}

        text = extract_info.get("text", "")
        marker_count = extract_info.get("markerCount", 0)
        print(f"Extracting {marker_count} citations...", flush=True)

        if marker_count == 0:
            raise RuntimeError("Extraction invariant violated: no citation markers found in message")

        # Focus page to receive hover input
        await send_cdp(ws, 999, "Page.bringToFront")

        citations = []
        prev_binding = None
        consecutive_duplicates = 0

        for idx in range(marker_count):
            # 1. Reset mouse away to (0, 0) and assert overlay is cleared
            await send_cdp(ws, 1000 + idx * 10, "Input.dispatchMouseEvent", {"type": "mouseMoved", "x": 0, "y": 0})

            cleared_js = """
            (() => {
                const container = document.querySelector('.cdk-overlay-container');
                if (!container) return { cleared: true, visibleCount: 0, lingeringIds: [] };
                const panes = Array.from(container.querySelectorAll('.cdk-overlay-pane'));
                const visible = panes.filter(p => {
                    const tt = p.querySelector('.citation-tooltip');
                    return tt && tt.innerText.trim().length > 0;
                });
                return {
                    cleared: visible.length === 0,
                    visibleCount: visible.length,
                    lingeringIds: visible.map(p => p.id)
                };
            })()
            """
            is_cleared = False
            clear_state = {}
            for _ in range(10):
                await asyncio.sleep(0.05)
                clear_state = await evaluate(ws, 1000 + idx * 10 + 1, cleared_js) or {}
                if clear_state.get("cleared", False):
                    is_cleared = True
                    break

            if not is_cleared:
                await send_cdp(ws, 1000 + idx * 10 + 2, "Input.dispatchKeyEvent", {"type": "rawKeyDown", "key": "Escape", "code": "Escape", "windowsVirtualKeyCode": 27})
                await send_cdp(ws, 1000 + idx * 10 + 3, "Input.dispatchKeyEvent", {"type": "keyUp", "key": "Escape", "code": "Escape", "windowsVirtualKeyCode": 27})
                await asyncio.sleep(0.15)
                clear_state = await evaluate(ws, 1000 + idx * 10 + 4, cleared_js) or {}
                is_cleared = clear_state.get("cleared", False)

            if not is_cleared:
                raise RuntimeError(
                    f"Fail-closed: CDK overlay container failed to dismiss prior to hovering marker {idx} "
                    f"(lingering overlay pane IDs: {clear_state.get('lingeringIds', [])}). Ineffective dismissal."
                )

            # 2. Scroll target marker into view and obtain its bounding rect
            js_rect = f"""
            (() => {{
                const msgs = document.querySelectorAll('.to-user-message-card-content');
                const lastMsg = msgs[msgs.length - 1];
                const allBtns = Array.from(lastMsg.querySelectorAll('button.citation-marker'));
                const citationBtns = allBtns.filter(b => b.innerText.trim().match(/^\\d+$/));
                const btn = citationBtns[{idx}];
                if (!btn) return null;
                btn.scrollIntoView({{ block: 'center', inline: 'center', behavior: 'instant' }});
                const r = btn.getBoundingClientRect();
                return {{
                    x: r.x + r.width / 2,
                    y: r.y + r.height / 2,
                    rect: {{ left: r.left, top: r.top, right: r.right, bottom: r.bottom, width: r.width, height: r.height }},
                    label: btn.innerText.trim()
                }};
            }})()
            """
            pos = await evaluate(ws, 1000 + idx * 10 + 5, js_rect)
            if not pos or not pos.get("rect") or pos["rect"].get("width", 0) <= 0:
                raise RuntimeError(f"Extraction invariant violated: marker {idx} rect could not be evaluated or has zero size")

            marker_rect = pos["rect"]
            x, y = pos["x"], pos["y"]
            m_label = pos["label"]

            # 3. Move mouse over marker to trigger tooltip
            await send_cdp(ws, 1000 + idx * 10 + 6, "Input.dispatchMouseEvent", {"type": "mouseMoved", "x": x, "y": y})

            # 4. Poll for the specific CDK overlay pane that is trigger-bound to this marker
            snippet = ""
            tooltip_rect = None
            active_pane_id = None
            v_dist = None
            h_overlap = None
            handshake_verified = False

            for attempt in range(8):
                await asyncio.sleep(0.12)
                query_bound_pane_js = f"""
                (() => {{
                    const container = document.querySelector('.cdk-overlay-container');
                    if (!container) return [];
                    const btnRect = {json.dumps(marker_rect)};
                    const panes = Array.from(container.querySelectorAll('.cdk-overlay-pane'));
                    
                    const matches = [];
                    for (const p of panes) {{
                        const tt = p.querySelector('.citation-tooltip');
                        if (!tt) continue;
                        const text = tt.innerText.trim();
                        if (text.length < 10) continue;
                        const r = tt.getBoundingClientRect();
                        
                        const vDist = Math.min(
                            Math.abs(r.top - btnRect.bottom),
                            Math.abs(btnRect.top - r.bottom)
                        );
                        const hOverlap = !(r.right < btnRect.left - 50 || r.left > btnRect.right + 50);
                        
                        if (vDist <= 100 && hOverlap) {{
                            matches.push({{
                                paneId: p.id,
                                text: tt.innerText,
                                rect: {{ left: r.left, top: r.top, width: r.width, height: r.height, x: r.x, y: r.y }},
                                vDist: vDist,
                                hOverlap: hOverlap
                            }});
                        }}
                    }}
                    return matches;
                }})()
                """
                bound_panes = await evaluate(ws, 1000 + idx * 10 + 7 + attempt, query_bound_pane_js) or []
                if len(bound_panes) == 1:
                    bp = bound_panes[0]
                    raw_text = bp.get("text", "")
                    clean = raw_text.replace(f"{expected_source}\n", "").replace("\nView source", "").replace("\n", " ").strip()
                    if "ABSTRACT" not in clean:
                        snippet = clean
                        tooltip_rect = bp.get("rect")
                        active_pane_id = bp.get("paneId")
                        v_dist = bp.get("vDist")
                        h_overlap = bp.get("hOverlap")
                        handshake_verified = True
                        break
                elif len(bound_panes) > 1:
                    raise RuntimeError(f"Fail-closed: Multiple conflicting trigger-bound overlays detected for marker {idx}")

            if not handshake_verified or not snippet or not tooltip_rect:
                raise RuntimeError(
                    f"Fail-closed: could not establish fresh, trigger-bound tooltip handshake for marker {idx} (label {m_label})."
                )

            # Invariant 4: Verify duplicate transition threshold BEFORE updating prev_binding
            old_snippet = prev_binding.get("snippet", "") if prev_binding else ""
            consecutive_duplicates = verify_tooltip_transition(
                old_snippet, snippet, idx, consecutive_duplicates, max_consecutive=15
            )

            # Invariant 5: Positive marker-to-tooltip binding and stale overlay detection
            prev_binding = verify_marker_tooltip_binding(
                idx, m_label, pos, tooltip_rect, snippet,
                handshake_verified=handshake_verified,
                active_pane_id=active_pane_id,
                prev_binding=prev_binding
            )

            citations.append({
                "index": idx,
                "label": m_label,
                "snippet": snippet,
                "audit": {
                    "pre_hover_cleared": True,
                    "overlay_pane_id": active_pane_id,
                    "marker_rect": marker_rect,
                    "tooltip_rect": tooltip_rect,
                    "vertical_dist": v_dist,
                    "trigger_bound": True,
                    "handshake_verified": True
                }
            })

        # Invariant 6: Validate extracted citations
        sample = "Early Palestinian Judaism" if "Early Palestinian Judaism" in abstract_text else ""
        validate_citations(citations, abstract_sample=sample)

        return {
            "text": text,
            "citations": citations
        }

if __name__ == "__main__":
    prompt = sys.argv[1] if len(sys.argv) > 1 else "Hello"
    output_file = sys.argv[2] if len(sys.argv) > 2 else "scripts/last_response.json"
    res = asyncio.run(run_prompt(prompt))
    print(f"=== RESPONSE SAVED TO {output_file} ===")
    print(f"Text length: {len(res['text'])}, Citations: {len(res['citations'])}")
    with open(output_file, "w") as f:
        json.dump(res, f, indent=2)
