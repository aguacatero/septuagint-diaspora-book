#!/usr/bin/env python3
"""Promote accepted source packet into cumulative synthesis notebook SDP-01 Paul."""

import asyncio
import hashlib
import json
import os
import sys
import time
import urllib.request
from pathlib import Path
import websockets

PDF_PATH = Path("/Users/chrisrodriguez/Downloads/sanday_headlam_1895_romans_icc.pdf")
EXPECTED_FILENAME = "sanday_headlam_1895_romans_icc.pdf"
SDP01_UUID = "65d4bea4-7939-4754-bb7b-09d420e8ff19"
TARGET_URL = f"https://notebook.google.com/notebook/{SDP01_UUID}"


class CDPClient:
    def __init__(self, ws):
        self.ws = ws
        self.msg_id = 0
        self.pending = {}  # id -> Future
        self.events = asyncio.Queue()
        self.reader_task = asyncio.create_task(self._reader())

    async def _reader(self):
        try:
            async for raw in self.ws:
                data = json.loads(raw)
                mid = data.get("id")
                if mid is not None and mid in self.pending:
                    fut = self.pending.pop(mid)
                    if not fut.done():
                        fut.set_result(data)
                elif "method" in data:
                    await self.events.put(data)
        except asyncio.CancelledError:
            pass
        except Exception as e:
            for fut in self.pending.values():
                if not fut.done():
                    fut.set_exception(e)

    async def call(self, method: str, params: dict | None = None) -> dict:
        self.msg_id += 1
        mid = self.msg_id
        fut = asyncio.get_running_loop().create_future()
        self.pending[mid] = fut
        payload = {"id": mid, "method": method}
        if params is not None:
            payload["params"] = params
        await self.ws.send(json.dumps(payload))
        return await fut

    async def evaluate(self, expr: str):
        res = await self.call("Runtime.evaluate", {
            "expression": expr,
            "returnByValue": True,
            "awaitPromise": True
        })
        if "result" in res and "result" in res["result"]:
            return res["result"]["result"].get("value")
        return None

    async def wait_for_event(self, method: str, timeout: float = 15.0):
        t0 = time.time()
        while time.time() - t0 < timeout:
            remaining = timeout - (time.time() - t0)
            try:
                evt = await asyncio.wait_for(self.events.get(), timeout=min(remaining, 1.0))
                if evt.get("method") == method:
                    return evt
            except asyncio.TimeoutError:
                pass
        return None

    async def close(self):
        self.reader_task.cancel()
        try:
            await self.reader_task
        except asyncio.CancelledError:
            pass


async def inspect_sdp01(client: CDPClient) -> dict:
    expr = """
    (() => {
        const titleInput = document.querySelector('input.title-input');
        const title = titleInput ? titleInput.value : document.title;
        const sources = Array.from(document.querySelectorAll('.source-title, .source-item-title, [data-source-title]'))
            .map(s => s.innerText.trim())
            .filter(t => t.endsWith('.pdf'));
        const uniqueSources = Array.from(new Set(sources));
        const errorEl = document.querySelector('.single-source-error-container, [aria-label*="Error info"]');
        const spinner = document.querySelector('mat-progress-bar, mat-spinner, [role=progressbar], .loading');
        const hasUploader = Boolean(
            document.querySelector('[xapscottyuploadertrigger]') ||
            Array.from(document.querySelectorAll('button')).some(b => b.innerText && b.innerText.includes('Upload files'))
        );
        return {
            title: title,
            sources: uniqueSources,
            source_count: uniqueSources.length,
            has_error: Boolean(errorEl),
            is_indexing: Boolean(spinner),
            dialog_open: hasUploader
        };
    })()
    """
    return await client.evaluate(expr) or {}


async def prove_retrieval(client: CDPClient, expected_source: str, timeout: float = 90.0) -> bool:
    print(f"Running source-grounded retrieval verification in SDP-01 Paul for '{expected_source}'...", flush=True)
    probe_query = "In Sanday and Headlam's commentary on Romans, what is their discussion in the Excursus on St. Paul's Use of the Old Testament regarding whether Paul quotes from memory or from a manuscript roll?"
    
    init_count = await client.evaluate("document.querySelectorAll('.to-user-message-card-content').length") or 0
    
    type_js = f"""
    (() => {{
        const ta = document.querySelector('textarea[aria-label="Query box"], textarea[placeholder*="Ask"]');
        if (!ta || ta.disabled) return false;
        ta.focus();
        ta.value = {json.dumps(probe_query)};
        ta.dispatchEvent(new Event('input', {{ bubbles: true }}));
        ta.dispatchEvent(new Event('change', {{ bubbles: true }}));
        return true;
    }})()
    """
    typed = await client.evaluate(type_js)
    if not typed:
        print("Could not find query textarea for probe", flush=True)
        return False
        
    await asyncio.sleep(0.5)
    
    submit_js = """
    (() => {
        const ta = document.querySelector('textarea[aria-label="Query box"], textarea[placeholder*="Ask"]');
        if (!ta) return false;
        const container = ta.closest('.query-box-container') || ta.parentElement.parentElement;
        const btn = container ? container.querySelector('button[aria-label="Submit"]') : document.querySelector('button[aria-label="Submit"]');
        if (btn && !btn.disabled) {
            btn.click();
            return true;
        }
        return false;
    })()
    """
    submitted = await client.evaluate(submit_js)
    if not submitted:
        print("Could not click submit button for probe", flush=True)
        return False
        
    t0 = time.time()
    while time.time() - t0 < timeout:
        await asyncio.sleep(4)
        check_js = f"""
        (() => {{
            const msgs = document.querySelectorAll('.to-user-message-card-content');
            if (msgs.length <= {init_count}) return {{ settled: false }};
            const latest = msgs[msgs.length - 1];
            const text = latest.innerText || '';
            const citationBtns = Array.from(latest.querySelectorAll('button.citation-marker, [class*="citation"]'));
            const isGenerating = Boolean(document.querySelector('.generating, mat-progress-bar, [aria-label="Stop generation"]'));
            return {{
                settled: !isGenerating && text.length > 50,
                text_len: text.length,
                markers: citationBtns.length
            }};
        }})()
        """
        status = await client.evaluate(check_js) or {}
        if status.get("settled"):
            print(f"Retrieval probe succeeded! Response length: {status.get('text_len')}, Citations: {status.get('markers')}", flush=True)
            return True
            
    print(f"Retrieval probe timed out after {timeout}s", flush=True)
    return False


async def promote():
    if not PDF_PATH.is_file():
        raise FileNotFoundError(f"Missing PDF: {PDF_PATH}")
    
    file_bytes = PDF_PATH.stat().st_size
    h = hashlib.sha256(PDF_PATH.read_bytes()).hexdigest()
    print(f"Validated local PDF: {EXPECTED_FILENAME} ({file_bytes:,} bytes, sha256={h})")
    
    # Connect to Chrome CDP and activate tab
    with urllib.request.urlopen("http://127.0.0.1:9222/json") as r:
        tabs = json.loads(r.read())
        
    sdp01_tabs = [
        t for t in tabs 
        if SDP01_UUID in t.get("url", "") and t.get("url", "").startswith("https://notebook.google.com")
    ]
    if not sdp01_tabs:
        sdp01_tabs = [t for t in tabs if SDP01_UUID in t.get("url", "")]
    if not sdp01_tabs:
        raise RuntimeError(f"SDP-01 Paul tab ({SDP01_UUID}) not found")
        
    tab = sdp01_tabs[0]
    tab_id = tab["id"]
    ws_url = tab["webSocketDebuggerUrl"]
    print(f"Activating tab {tab_id} in Chrome...")
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:9222/json/activate/{tab_id}") as r:
            pass
    except Exception as e:
        print(f"Activate warning: {e}")
        
    print(f"Connecting to CDP at {ws_url} (Tab ID: {tab_id})...")
    
    async with websockets.connect(ws_url, max_size=20*1024*1024) as ws:
        client = CDPClient(ws)
        try:
            state = await inspect_sdp01(client)
            print(f"Current SDP-01 Paul state: {state}")
            
            if EXPECTED_FILENAME in state.get("sources", []):
                print(f"SUCCESS: {EXPECTED_FILENAME} already present in SDP-01 Paul!")
                if not state.get("is_indexing") and not state.get("has_error"):
                    probe_ok = await prove_retrieval(client, EXPECTED_FILENAME, timeout=60.0)
                    print(f"Retrieval verified: {probe_ok}")
                return state
                
            print(f"Uploading {EXPECTED_FILENAME} into SDP-01 Paul...")
            
            # Open Add source dialog if not open
            if not state.get("dialog_open"):
                open_dlg_js = """
                (() => {
                    const addBtn = Array.from(document.querySelectorAll('button')).find(
                        b => b.innerText && b.innerText.includes('Sources') && b.innerText.includes('add')
                    ) || document.querySelector('button[aria-label*="Add source"]');
                    if (addBtn) { addBtn.click(); return true; }
                    return false;
                })()
                """
                opened = await client.evaluate(open_dlg_js)
                print(f"Add source clicked: {opened}")
                await asyncio.sleep(2)
                
            # Intercept file chooser
            await client.call("Page.enable")
            await client.call("Page.setInterceptFileChooserDialog", {"enabled": True})
            
            # Locate Upload files button
            find_btn_js = """
            (() => {
                const btn = document.querySelector('[xapscottyuploadertrigger]') || 
                            Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.includes('Upload files'));
                if (!btn) return null;
                const r = btn.getBoundingClientRect();
                return { x: r.x + r.width / 2, y: r.y + r.height / 2 };
            })()
            """
            btn_pos = await client.evaluate(find_btn_js)
            if not btn_pos:
                raise RuntimeError("Upload files button not found in Add source dialog")
                
            print(f"Clicking Upload files button at ({btn_pos['x']:.1f}, {btn_pos['y']:.1f})...")
            await client.call("Input.dispatchMouseEvent", {
                "type": "mousePressed", "x": btn_pos["x"], "y": btn_pos["y"], "button": "left", "clickCount": 1
            })
            await client.call("Input.dispatchMouseEvent", {
                "type": "mouseReleased", "x": btn_pos["x"], "y": btn_pos["y"], "button": "left", "clickCount": 1
            })
            
            # Wait for Page.fileChooserOpened
            print("Waiting for Page.fileChooserOpened event...")
            evt = await client.wait_for_event("Page.fileChooserOpened", timeout=15.0)
            if not evt:
                raise RuntimeError("Page.fileChooserOpened event not received within 15s")
                
            backend_node_id = evt["params"].get("backendNodeId")
            print(f"Page.fileChooserOpened received (backendNodeId={backend_node_id})!")
            
            # Set file input
            print(f"Setting file input to '{PDF_PATH}'...")
            res = await client.call("DOM.setFileInputFiles", {
                "files": [str(PDF_PATH)],
                "backendNodeId": backend_node_id
            })
            print(f"DOM.setFileInputFiles response: {res}")
            
            # Monitor ingestion progression
            print("Monitoring ingestion progression in SDP-01 Paul (deadline: 300s)...")
            t_start = time.time()
            saw_source = False
            
            while time.time() - t_start < 300.0:
                await asyncio.sleep(5)
                elapsed = int(time.time() - t_start)
                st = await inspect_sdp01(client)
                sources = st.get("sources", [])
                indexing = st.get("is_indexing")
                error = st.get("has_error")
                print(f"[{elapsed:3d}s heartbeat] sources={sources}, indexing={indexing}, error={error}")
                
                if error:
                    raise RuntimeError(f"Terminal error indicator detected in SDP-01 Paul: {st}")
                    
                if EXPECTED_FILENAME in sources:
                    saw_source = True
                    
                if saw_source and not indexing:
                    print(f"SUCCESS: {EXPECTED_FILENAME} ingested and settled in SDP-01 Paul after {elapsed}s!")
                    print(f"Cumulative sources in SDP-01 Paul ({len(sources)}): {sources}")
                    probe_ok = await prove_retrieval(client, EXPECTED_FILENAME, timeout=90.0)
                    print(f"Retrieval probe ok: {probe_ok}")
                    return st
                    
            raise TimeoutError("Monotonic deadline exceeded waiting for SDP-01 Paul ingestion")
        finally:
            await client.close()


if __name__ == "__main__":
    res = asyncio.run(promote())
    print("\nPROMOTION COMPLETED:", json.dumps(res, indent=2))
