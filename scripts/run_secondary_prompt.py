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
    prev_binding: dict = None
) -> dict:
    """
    Enforces a positive, fail-closed binding between a hovered/clicked marker
    and the captured tooltip overlay:
    1. Non-empty, valid snippet.
    2. Positive geometric anchor association: tooltip must be anchored near the marker.
    3. Rejects single-marker and multi-marker stale retained overlays where the overlay
       was not updated or belongs to a prior marker at a different position.
    4. Permits legitimate identical snippets only when the anchor ownership is verified.
    """
    if not snippet or len(snippet.strip()) < 10:
        raise RuntimeError(f"Tooltip binding invariant violated at marker {marker_idx}: snippet is empty or too short")

    # Positive geometric anchor association
    if marker_pos and tooltip_rect:
        my = marker_pos.get("y", 0)
        ty = tooltip_rect.get("y", tooltip_rect.get("top", 0))
        th = tooltip_rect.get("height", 0)

        # Vertical proximity check: tooltip is anchored near trigger
        v_dist = min(abs(ty - my), abs(ty + th - my))
        if v_dist > 300:
            raise RuntimeError(
                f"Positive anchor binding failed at marker {marker_idx}: tooltip vertical distance "
                f"({v_dist:.1f}px) exceeds attachment threshold. Suspected retained stale overlay."
            )

    # Stale retention check across consecutive markers
    if prev_binding:
        prev_snip = prev_binding.get("snippet", "")
        prev_pos = prev_binding.get("marker_pos", {})
        prev_rect = prev_binding.get("tooltip_rect", {})

        if snippet == prev_snip:
            # If snippet is identical to previous, check if the overlay is a retained duplicate from a different marker location
            if marker_pos and prev_pos:
                m_dist_y = abs(marker_pos.get("y", 0) - prev_pos.get("y", 0))
                m_dist_x = abs(marker_pos.get("x", 0) - prev_pos.get("x", 0))
                # If markers are at different locations on screen, the tooltip MUST have repositioned
                if (m_dist_y > 20 or m_dist_x > 50) and tooltip_rect and prev_rect:
                    t_dist_y = abs(tooltip_rect.get("top", tooltip_rect.get("y", 0)) - prev_rect.get("top", prev_rect.get("y", 0)))
                    t_dist_x = abs(tooltip_rect.get("left", tooltip_rect.get("x", 0)) - prev_rect.get("left", prev_rect.get("x", 0)))
                    if t_dist_y < 2 and t_dist_x < 2:
                        raise RuntimeError(
                            f"Stale retained overlay detected at marker {marker_idx}: marker moved from "
                            f"({prev_pos.get('x')}, {prev_pos.get('y')}) to ({marker_pos.get('x')}, {marker_pos.get('y')}), "
                            f"but tooltip overlay position remained completely static at ({tooltip_rect.get('left')}, {tooltip_rect.get('top')})."
                        )

    return {
        "marker_idx": marker_idx,
        "marker_label": marker_label,
        "marker_pos": marker_pos,
        "tooltip_rect": tooltip_rect,
        "snippet": snippet
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
            const markers = Array.from(lastMsg.querySelectorAll("button.citation-marker"));
            return {
                text: text,
                markerCount: markers.length
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
            # 1. Reset mouse away to 0,0
            await send_cdp(ws, 1000 + idx * 10, "Input.dispatchMouseEvent", {"type": "mouseMoved", "x": 0, "y": 0})
            await asyncio.sleep(0.05)

            # 2. Scroll into view and get marker rect
            js_rect = f"""
            (() => {{
                const msgs = document.querySelectorAll('.to-user-message-card-content');
                const lastMsg = msgs[msgs.length - 1];
                const markers = Array.from(lastMsg.querySelectorAll('button.citation-marker'));
                const btn = markers[{idx}];
                btn.scrollIntoView({{ block: 'center', inline: 'center', behavior: 'instant' }});
                const r = btn.getBoundingClientRect();
                return {{
                    x: r.x + r.width/2,
                    y: r.y + r.height/2,
                    label: btn.innerText.trim()
                }};
            }})()
            """
            pos = await evaluate(ws, 1000 + idx * 10 + 1, js_rect)
            if not pos:
                raise RuntimeError(f"Extraction invariant violated: marker {idx} rect could not be evaluated")
            x, y = pos["x"], pos["y"]
            m_label = pos["label"]

            # 3. Move mouse over marker to trigger tooltip
            await send_cdp(ws, 1000 + idx * 10 + 2, "Input.dispatchMouseEvent", {"type": "mouseMoved", "x": x, "y": y})

            # 4. Poll active CDK overlay tooltip text and rect
            snippet = ""
            tooltip_rect = None
            for attempt in range(8):
                await asyncio.sleep(0.12)
                snippet_js = """
                (() => {
                    const tt = document.querySelector('.cdk-overlay-container .citation-tooltip');
                    if (!tt) return null;
                    const r = tt.getBoundingClientRect();
                    return {
                        text: tt.innerText,
                        rect: { left: r.left, top: r.top, width: r.width, height: r.height, x: r.x, y: r.y }
                    };
                })()
                """
                tt_data = await evaluate(ws, 1000 + idx * 10 + 3 + attempt, snippet_js) or {}
                raw_text = tt_data.get("text", "")
                if len(raw_text.strip()) > 10:
                    clean = raw_text.replace(f"{expected_source}\n", "").replace("\nView source", "").replace("\n", " ").strip()
                    if "ABSTRACT" not in clean:
                        snippet = clean
                        tooltip_rect = tt_data.get("rect")
                        break

            if not snippet:
                raise RuntimeError(f"Fail-closed: could not extract valid tooltip for marker {idx} (label {m_label})")

            # Invariant 4: Positive marker-to-tooltip binding and stale overlay detection
            prev_binding = verify_marker_tooltip_binding(
                idx, m_label, pos, tooltip_rect, snippet, prev_binding=prev_binding
            )

            # Invariant 5: Verify duplicate transition threshold
            consecutive_duplicates = verify_tooltip_transition(
                prev_binding.get("snippet", ""), snippet, idx, consecutive_duplicates, max_consecutive=15
            )

            citations.append({
                "index": idx,
                "label": m_label,
                "snippet": snippet
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
