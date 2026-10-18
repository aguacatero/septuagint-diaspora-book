import asyncio
import json
import sys
import time
import urllib.request
import websockets

def validate_notebook_state(title: str, sources: list):
    """
    Validates that the connected notebook tab matches SDP-B001-EXTRACT
    and contains exactly one source loaded.
    """
    if not title or "SDP-B001-EXTRACT" not in title:
        raise RuntimeError(f"Connected notebook title '{title}' does not match expected 'SDP-B001-EXTRACT'")
    if len(sources) != 1:
        raise RuntimeError(f"Expected exactly 1 source in SDP-B001-EXTRACT, found {len(sources)}: {sources}")

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

async def verify_tab_invariants(ws):
    state = await evaluate(ws, 9000, """
    (() => {
        const titleInput = document.querySelector('input.title-input');
        const title = titleInput ? titleInput.value : document.title;
        const sources = Array.from(document.querySelectorAll('.source-panel .source-title')).map(e => e.innerText.trim()).filter(Boolean);
        const abstractEl = document.querySelector('.source-panel .source-guide-container, .source-panel');
        return {
            title: title,
            sources: sources,
            abstract: abstractEl ? abstractEl.innerText : ""
        };
    })()
    """) or {}
    validate_notebook_state(state.get("title", ""), state.get("sources", []))
    return state.get("abstract", "")

async def run_prompt(prompt_text, max_wait=150, host="127.0.0.1", port=9222):
    ws_url = get_page_ws_url(host=host, port=port)
    async with websockets.connect(ws_url, max_size=20*1024*1024) as ws:
        # Invariant 1: Verify notebook title and exactly one source loaded
        abstract_text = await verify_tab_invariants(ws)

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

        citations = []
        for idx in range(marker_count):
            click_js = f"""
            (() => {{
                const msgs = document.querySelectorAll('.to-user-message-card-content');
                const lastMsg = msgs[msgs.length - 1];
                const markers = Array.from(lastMsg.querySelectorAll("button.citation-marker"));
                if (markers[{idx}]) {{
                    markers[{idx}].scrollIntoView({{ block: 'center' }});
                    markers[{idx}].click();
                    return markers[{idx}].innerText.trim();
                }}
                return null;
            }})()
            """
            m_label = await evaluate(ws, 100 + idx * 2, click_js)
            await asyncio.sleep(0.6)

            # Query strictly the active CDK overlay pane containing citation tooltip
            # Exclude .source-panel, persistent sidebars, and unrelated dialogs
            snippet_js = """
            (() => {
                const panels = Array.from(document.querySelectorAll(
                    ".cdk-overlay-container .cdk-overlay-pane.citation-tooltip-panel, " +
                    ".cdk-overlay-container .cdk-overlay-pane:has(.citation-tooltip)"
                ));
                for (let i = panels.length - 1; i >= 0; i--) {
                    const p = panels[i];
                    const rect = p.getBoundingClientRect();
                    if (rect.width > 0 && rect.height > 0) {
                        const t = p.innerText.trim();
                        if (t.length > 10 && !t.includes("Recently used") && !t.includes("Search your sources")) {
                            return t;
                        }
                    }
                }
                return "";
            })()
            """
            snippet = await evaluate(ws, 100 + idx * 2 + 1, snippet_js)
            citations.append({
                "index": idx,
                "label": m_label,
                "snippet": snippet
            })

        # Invariant 3: Validate extracted citations
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
