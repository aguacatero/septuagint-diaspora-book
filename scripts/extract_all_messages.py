import asyncio
import json
import time
import urllib.request
import websockets

from scripts.run_secondary_prompt import (
    validate_notebook_state,
    verify_marker_tooltip_binding,
    verify_tooltip_transition,
    EXPECTED_DEFAULT_SOURCE,
)

_msg_id = 0

async def call_cdp(ws, method, params=None, timeout=10.0):
    global _msg_id
    _msg_id += 1
    mid = _msg_id
    payload = {"id": mid, "method": method}
    if params:
        payload["params"] = params
    await ws.send(json.dumps(payload))
    t0 = time.time()
    while True:
        remaining = timeout - (time.time() - t0)
        if remaining <= 0:
            raise TimeoutError(f"CDP call {method} (id={mid}) timed out after {timeout}s")
        raw = await asyncio.wait_for(ws.recv(), timeout=remaining)
        data = json.loads(raw)
        if data.get("id") == mid:
            return data

async def evaluate(ws, expr):
    res = await call_cdp(ws, "Runtime.evaluate", {
        "expression": expr,
        "returnByValue": True
    })
    if "result" in res and "result" in res["result"]:
        return res["result"]["result"].get("value")
    return None

async def extract_message_citations(ws, msg_idx, output_path, expected_source=EXPECTED_DEFAULT_SOURCE):
    print(f"\n==========================================", flush=True)
    print(f"Extracting Message Index {msg_idx} -> {output_path}", flush=True)
    print(f"==========================================", flush=True)

    # Bring to front to ensure input events are dispatched immediately
    await call_cdp(ws, "Page.bringToFront")

    # Expand all collapsed citations first
    await evaluate(ws, f"""
    (() => {{
        const msgs = document.querySelectorAll('.to-user-message-card-content');
        if (!msgs[{msg_idx}]) return;
        const m = msgs[{msg_idx}];
        const moreBtns = Array.from(m.querySelectorAll('button.citation-marker')).filter(
            b => b.innerText.includes('more_horiz') || b.querySelector('mat-icon')?.innerText.includes('more_horiz')
        );
        for (const b of moreBtns) {{
            b.click();
        }}
    }})()
    """)
    await asyncio.sleep(0.4)

    # Get message info and numeric citation marker count
    msg_info = await evaluate(ws, f"""
    (() => {{
        const msgs = document.querySelectorAll('.to-user-message-card-content');
        if (!msgs[{msg_idx}]) return null;
        const m = msgs[{msg_idx}];
        const allBtns = Array.from(m.querySelectorAll('button.citation-marker'));
        const citationBtns = allBtns.filter(b => b.innerText.trim().match(/^\\d+$/));
        return {{
            text: m.innerText,
            markerCount: citationBtns.length
        }};
    }})()
    """)
    if not msg_info:
        raise RuntimeError(f"Message index {msg_idx} not found")

    text = msg_info["text"]
    marker_count = msg_info["markerCount"]
    print(f"Total numeric citation markers in message {msg_idx}: {marker_count}", flush=True)

    citations = []
    seen_snippets = set()
    prev_binding = None
    consecutive_duplicates = 0

    for idx in range(marker_count):
        # 1. Reset mouse away to 0,0 and assert overlay is cleared
        await call_cdp(ws, "Input.dispatchMouseEvent", {"type": "mouseMoved", "x": 0, "y": 0})
        await asyncio.sleep(0.08)

        # Assert clean/dismissed overlay state prior to hovering new marker
        is_cleared = await evaluate(ws, """
        (() => {
            const tt = document.querySelector('.cdk-overlay-container .citation-tooltip');
            return !tt || !tt.innerText.trim();
        })()
        """)
        if not is_cleared:
            # Attempt escape dismiss if overlay lingered
            await call_cdp(ws, "Input.dispatchKeyEvent", {"type": "rawKeyDown", "key": "Escape", "code": "Escape", "windowsVirtualKeyCode": 27})
            await call_cdp(ws, "Input.dispatchKeyEvent", {"type": "keyUp", "key": "Escape", "code": "Escape", "windowsVirtualKeyCode": 27})
            await asyncio.sleep(0.1)

        # 2. Scroll into view and get marker rect
        js_rect = f"""
        (() => {{
            const msgs = document.querySelectorAll('.to-user-message-card-content');
            const m = msgs[{msg_idx}];
            const allBtns = Array.from(m.querySelectorAll('button.citation-marker'));
            const citationBtns = allBtns.filter(b => b.innerText.trim().match(/^\\d+$/));
            const btn = citationBtns[{idx}];
            btn.scrollIntoView({{ block: 'center', inline: 'center', behavior: 'instant' }});
            const r = btn.getBoundingClientRect();
            return {{
                x: r.x + r.width/2,
                y: r.y + r.height/2,
                label: btn.innerText.trim()
            }};
        }})()
        """
        pos = await evaluate(ws, js_rect)
        if not pos:
            raise RuntimeError(f"Failed to find rect for marker {idx}")
        x, y = pos["x"], pos["y"]
        label = pos["label"]

        # 3. Move mouse over marker to trigger tooltip
        await call_cdp(ws, "Input.dispatchMouseEvent", {"type": "mouseMoved", "x": x, "y": y})

        # 4. Poll for tooltip and its bounding rect
        snip = ""
        tooltip_rect = None
        for attempt in range(8):
            await asyncio.sleep(0.12)
            js_snip = """
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
            tt_data = await evaluate(ws, js_snip) or {}
            raw_text = tt_data.get("text", "")
            if len(raw_text.strip()) > 10:
                clean = raw_text.replace(f"{expected_source}\n", "").replace("\nView source", "").replace("\n", " ").strip()
                if "ABSTRACT" not in clean:
                    snip = clean
                    tooltip_rect = tt_data.get("rect")
                    break

        if not snip:
            raise RuntimeError(f"Fail-closed: could not extract valid tooltip for marker {idx} (label {label})")

        # Invariant 4: Verify duplicate transition threshold BEFORE updating prev_binding
        old_snippet = prev_binding.get("snippet", "") if prev_binding else ""
        consecutive_duplicates = verify_tooltip_transition(
            old_snippet, snip, idx, consecutive_duplicates, max_consecutive=15
        )

        # Invariant 5: Positive marker-to-tooltip binding and stale overlay detection
        prev_binding = verify_marker_tooltip_binding(
            idx, label, pos, tooltip_rect, snip, handshake_verified=True, prev_binding=prev_binding
        )

        citations.append({
            "index": idx,
            "label": label,
            "snippet": snip
        })
        seen_snippets.add(snip)
        if idx % 10 == 0 or idx == marker_count - 1:
            print(f"  [{idx+1}/{marker_count}] Label {label}: {snip[:70]}...", flush=True)

    print(f"Extracted {len(citations)} citations. Unique snippets: {len(seen_snippets)}", flush=True)
    if marker_count > 1 and len(seen_snippets) <= 1:
        raise RuntimeError(f"Fail-closed: All citations were identical ({len(seen_snippets)} unique)")

    out_data = {
        "text": text,
        "citations": citations
    }
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(out_data, f, indent=2, ensure_ascii=False)
    print(f"Saved: {output_path}\n", flush=True)
    return out_data

async def main():
    tabs = json.loads(urllib.request.urlopen("http://127.0.0.1:9222/json").read())
    t = [x for x in tabs if "b3cd453a" in x.get("url", "")][0]
    async with websockets.connect(t["webSocketDebuggerUrl"], max_size=20*1024*1024) as ws:
        # Validate exact single active source
        state = await evaluate(ws, """
        (() => {
            const titleInput = document.querySelector('input.title-input');
            const title = titleInput ? titleInput.value : document.title;
            const sources = Array.from(document.querySelectorAll('.source-title, .source-title-container, [aria-label*="source"]'));
            const sourceTexts = sources.map(s => s.innerText.trim()).filter(t => t.endsWith('.pdf'));
            const unique = Array.from(new Set(sourceTexts));
            return { title: title, count: unique.length, sources: unique };
        })()
        """)
        print(f"Source validation state: {state}", flush=True)
        validate_notebook_state(
            state.get("title", ""),
            state.get("sources", []),
            expected_source=EXPECTED_DEFAULT_SOURCE
        )

        # Msg 5 -> Prompt 2
        await extract_message_citations(
            ws, 5,
            "research/inbox/B001-pauline-txt-pilot/sources/S01F/prompt_2_raw.json"
        )

        # Msg 6 -> Prompt 3
        await extract_message_citations(
            ws, 6,
            "research/inbox/B001-pauline-txt-pilot/sources/S01F/prompt_3_raw.json"
        )

        # Msg 8 -> Prompt 4
        await extract_message_citations(
            ws, 8,
            "research/inbox/B001-pauline-txt-pilot/sources/S01F/prompt_4_raw.json"
        )

        print("ALL PROMPTS EXTRACTED SUCCESSFULLY WITH AUTHENTIC SNIPPETS!", flush=True)

if __name__ == "__main__":
    asyncio.run(main())
