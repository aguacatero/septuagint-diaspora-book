import asyncio
import json
import sys
import time
import urllib.request
import websockets

def get_page_ws_url():
    with urllib.request.urlopen("http://127.0.0.1:9222/json") as r:
        tabs = json.loads(r.read())
    nb_tabs = [t for t in tabs if "b3cd453a" in t.get("url", "") and t.get("type") == "page"]
    if not nb_tabs:
        raise RuntimeError("SDP-B001-EXTRACT tab not found at http://127.0.0.1:9222")
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

async def run_prompt(prompt_text, max_wait=150):
    ws_url = get_page_ws_url()
    async with websockets.connect(ws_url, max_size=20*1024*1024) as ws:
        # Get current count of model messages
        init_count = await evaluate(ws, 1, """
            document.querySelectorAll('.to-user-message-card-content').length
        """) or 0
        print(f"Initial model message count: {init_count}", flush=True)

        # Ensure interface is idle before submitting
        for _ in range(20):
            idle = await evaluate(ws, 1000, """
                (() => {
                    const stopBtn = document.querySelector('button[aria-label="Stop response"], button[aria-label*="Stop"]');
                    return !stopBtn;
                })()
            """)
            if idle:
                break
            await asyncio.sleep(2)

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
        if submit_res != "SUBMITTED_CLICK":
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
                    break

        start_time = time.time()
        last_text = ""
        stable_count = 0

        # Wait for new message to appear and stabilize
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
                            break
                    else:
                        stable_count = 0
                        last_text = cur_text
                else:
                    stable_count = 0
                    last_text = cur_text
            else:
                print(f"[{int(time.time() - start_time)}s] waiting for new message... cur_count={cur_count}, init={init_count}", flush=True)

        # Extract message text and citation markers
        extract_info = await evaluate(ws, 10, """
        (() => {
            const msgs = document.querySelectorAll('.to-user-message-card-content');
            if (!msgs.length) return { text: "", markerCount: 0 };
            const lastMsg = msgs[msgs.length - 1];
            
            // Clean text: if thoughts block exists, extract both thoughts and substantive response
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
                    return markers[{idx}].innerText;
                }}
                return null;
            }})()
            """
            m_label = await evaluate(ws, 100 + idx * 2, click_js)
            await asyncio.sleep(1.2)

            snippet_js = """
            (() => {
                const overlays = Array.from(document.querySelectorAll(".cdk-overlay-pane.citation-tooltip-panel, .citation-dialog, .citation-panel, .source-panel"));
                for (const o of overlays) {
                    const t = o.innerText.trim();
                    if (t.length > 20 && !t.includes("Recently used") && !t.includes("Search your sources")) {
                        return t;
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
