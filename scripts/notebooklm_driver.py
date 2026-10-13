import asyncio
import json
import time
import urllib.request
import websockets

def get_page_ws_url():
    with urllib.request.urlopen("http://127.0.0.1:9222/json") as r:
        tabs = json.loads(r.read())
    nb_tabs = [t for t in tabs if "b3cd453a" in t.get("url", "") and t.get("type") == "page"]
    if not nb_tabs:
        nb_tabs = [t for t in tabs if "notebook" in t.get("url", "") and t.get("type") == "page"]
    if not nb_tabs:
        raise RuntimeError("No NotebookLM page found at http://127.0.0.1:9222")
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

async def run_prompt(prompt_text, max_wait=75):
    ws_url = get_page_ws_url()
    async with websockets.connect(ws_url, max_size=10*1024*1024) as ws:
        # Check initial message count
        init_count = await evaluate(ws, 1, """
            document.querySelectorAll(".chat-message-content, .message-content, [data-message-author='model'], .model-response-text, .response-text, .markdown-content").length
        """) or 0

        # Type prompt and submit
        escaped_prompt = json.dumps(prompt_text)
        submit_js = f"""
        (() => {{
            const ta = document.querySelector('textarea[aria-label="Query box"]');
            if (!ta) return "NO_TA";
            ta.value = {escaped_prompt};
            ta.dispatchEvent(new Event('input', {{ bubbles: true }}));
            ta.dispatchEvent(new Event('change', {{ bubbles: true }}));
            const btn = document.querySelector('button[aria-label="Submit"]');
            if (btn && !btn.disabled) {{
                btn.click();
                return "SUBMITTED_CLICK";
            }}
            const event = new KeyboardEvent('keydown', {{
                key: 'Enter',
                code: 'Enter',
                which: 13,
                keyCode: 13,
                bubbles: true
            }});
            ta.dispatchEvent(event);
            return "SUBMITTED_ENTER";
        }})()
        """
        submit_res = await evaluate(ws, 2, submit_js)
        print("Submit status:", submit_res)

        # Wait for new response
        start_time = time.time()
        last_text = ""
        stable_count = 0

        while time.time() - start_time < max_wait:
            await asyncio.sleep(2)
            cur_text = await evaluate(ws, 3, """
                (() => {
                    const msgs = document.querySelectorAll(".chat-message-content, .message-content, [data-message-author='model'], .model-response-text, .response-text, .markdown-content");
                    if (!msgs.length) return "";
                    return msgs[msgs.length - 1].innerText;
                })()
            """) or ""

            if cur_text and len(cur_text) > 30 and "Reviewing the References" not in cur_text and "Searched your sources" not in cur_text:
                if cur_text == last_text:
                    stable_count += 1
                    if stable_count >= 3: # stable for 6 seconds
                        print("Response stable!")
                        break
                else:
                    stable_count = 0
                    last_text = cur_text
            else:
                stable_count = 0

        # Extract full response and citations
        extract_js = """
        (() => {
            const msgs = document.querySelectorAll(".chat-message-content, .message-content, [data-message-author='model'], .model-response-text, .response-text, .markdown-content");
            if (!msgs.length) return { text: "", citations: [] };
            const lastMsg = msgs[msgs.length - 1];
            const text = lastMsg.innerText;
            const markers = Array.from(lastMsg.querySelectorAll("button.citation-marker"));
            return {
                text: text,
                markerCount: markers.length
            };
        })()
        """
        info = await evaluate(ws, 4, extract_js)
        text = info.get("text", "")
        marker_count = info.get("markerCount", 0)

        # Now click each marker and retrieve citation overlay text
        citations = []
        for idx in range(marker_count):
            click_js = f"""
            (() => {{
                const msgs = document.querySelectorAll(".chat-message-content, .message-content, [data-message-author='model'], .model-response-text, .response-text, .markdown-content");
                const lastMsg = msgs[msgs.length - 1];
                const markers = Array.from(lastMsg.querySelectorAll("button.citation-marker"));
                if (markers[{idx}]) {{
                    markers[{idx}].click();
                    return markers[{idx}].innerText;
                }}
                return null;
            }})()
            """
            m_label = await evaluate(ws, 100 + idx, click_js)
            await asyncio.sleep(1)
            overlay_js = """
            (() => {
                const overlays = Array.from(document.querySelectorAll(".citation-dialog, .citation-popover, .citation-panel, .source-viewer, xap-inline-dialog-container, [role='dialog'], .cdk-overlay-container"));
                for (const o of overlays) {
                    const t = o.innerText.trim();
                    if (t.includes("swete") || t.includes("sblgnt") || t.length > 20) {
                        return t;
                    }
                }
                return "";
            })()
            """
            snippet = await evaluate(ws, 200 + idx, overlay_js)
            citations.append({
                "index": idx,
                "label": m_label,
                "snippet": snippet
            })

        return {"text": text, "citations": citations}

if __name__ == "__main__":
    import sys
    prompt = sys.argv[1] if len(sys.argv) > 1 else "Hello"
    res = asyncio.run(run_prompt(prompt))
    print("=== EXTRACTED TEXT ===")
    print(res["text"])
    print("=== CITATIONS COUNT ===", len(res["citations"]))
