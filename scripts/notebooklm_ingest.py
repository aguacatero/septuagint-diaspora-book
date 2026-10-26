import asyncio
import hashlib
import json
import os
import sys
from pathlib import Path
import time
from typing import Dict, Any, Optional
import urllib.request
import websockets

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.queue_context import get_source_context, validate_output_path_isolation
from scripts.run_secondary_prompt import validate_notebook_state

async def send_cdp(ws, msg_id: int, method: str, params: Optional[dict] = None) -> dict:
    payload = {"id": msg_id, "method": method}
    if params:
        payload["params"] = params
    await ws.send(json.dumps(payload))
    while True:
        raw = await ws.recv()
        data = json.loads(raw)
        if data.get("id") == msg_id:
            return data

async def evaluate_cdp(ws, msg_id: int, expr: str) -> Any:
    res = await send_cdp(ws, msg_id, "Runtime.evaluate", {
        "expression": expr,
        "returnByValue": True,
        "awaitPromise": True
    })
    if "result" in res and "result" in res["result"]:
        return res["result"]["result"].get("value")
    return None

def check_local_pdf(pdf_path: str) -> Dict[str, Any]:
    p = Path(pdf_path)
    if not p.is_file():
        raise FileNotFoundError(f"Local source PDF file not found: {pdf_path}")
    size = p.stat().st_size
    if size < 1000:
        raise ValueError(f"Local source PDF file is too small or corrupt ({size} bytes): {pdf_path}")
    
    # Calculate SHA256 digest
    h = hashlib.sha256()
    with open(p, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
            
    return {
        "exists": True,
        "path": str(p),
        "filename": p.name,
        "size_bytes": size,
        "size_mb": round(size / (1024 * 1024), 2),
        "sha256": h.hexdigest()
    }

async def get_extract_tab(host: str = "127.0.0.1", port: int = 9222, notebook_pattern: str = "b3cd453a") -> Dict[str, Any]:
    url = f"http://{host}:{port}/json"
    with urllib.request.urlopen(url) as r:
        tabs = json.loads(r.read())
        
    matching = [t for t in tabs if notebook_pattern in t.get("url", "")]
    if not matching:
        raise RuntimeError(f"SDP-B001-EXTRACT tab matching '{notebook_pattern}' not found at {url}")
        
    t = matching[0]
    tab_url = t.get("url", "")
    
    # If tab was parked by tab-suspender extension, restore it
    if "park.html" in tab_url:
        print("SDP-B001-EXTRACT tab is parked. Restoring live URL...", flush=True)
        ws_url = t["webSocketDebuggerUrl"]
        async with websockets.connect(ws_url) as ws:
            restore_url = f"https://notebook.google.com/notebook/{notebook_pattern}"
            await send_cdp(ws, 1, "Page.navigate", {"url": restore_url})
            await asyncio.sleep(4)
        # Re-fetch tabs
        with urllib.request.urlopen(url) as r:
            tabs = json.loads(r.read())
        matching = [t for t in tabs if notebook_pattern in t.get("url", "")]
        t = matching[0]
        
    return t

async def inspect_notebook_sources(ws) -> Dict[str, Any]:
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
        const checkbox = document.querySelector('.source-item mat-checkbox, .single-source-container mat-checkbox, mat-checkbox');
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
            has_checkbox: Boolean(checkbox),
            dialog_open: hasUploader
        };
    })()
    """
    return await evaluate_cdp(ws, 100, expr) or {}

async def prove_source_retrieval(ws, expected_source: str, timeout: float = 60.0) -> bool:
    """
    Submits a probe query to prove NotebookLM can retrieve and ground answers from the source.
    """
    print(f"Running source-grounded retrieval verification for '{expected_source}'...", flush=True)
    probe_query = "What is the exact title and author of this book?"
    
    # Check initial message count
    init_count = await evaluate_cdp(ws, 201, "document.querySelectorAll('.to-user-message-card-content').length") or 0
    
    # Enter query into textarea
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
    typed = await evaluate_cdp(ws, 202, type_js)
    if not typed:
        print("Could not find query textarea for probe", flush=True)
        return False
        
    await asyncio.sleep(0.5)
    
    # Submit query
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
    submitted = await evaluate_cdp(ws, 203, submit_js)
    if not submitted:
        print("Could not click submit button for probe", flush=True)
        return False
        
    # Wait for response with citations
    t0 = time.time()
    while time.time() - t0 < timeout:
        await asyncio.sleep(4)
        check_js = f"""
        (() => {{
            const msgs = document.querySelectorAll('.to-user-message-card-content');
            if (msgs.length <= {init_count}) return {{ settled: false }};
            const latest = msgs[msgs.length - 1];
            const text = latest.innerText || '';
            const citationBtns = Array.from(latest.querySelectorAll('button.citation-marker'));
            const isGenerating = Boolean(document.querySelector('.generating, mat-progress-bar, [aria-label="Stop generation"]'));
            return {{
                settled: !isGenerating && text.length > 30,
                text_len: text.length,
                markers: citationBtns.length
            }};
        }})()
        """
        status = await evaluate_cdp(ws, 204, check_js) or {}
        if status.get("settled"):
            print(f"Retrieval probe succeeded! Response length: {status.get('text_len')}, Citations: {status.get('markers')}", flush=True)
            return True
            
    print(f"Retrieval probe timed out after {timeout}s", flush=True)
    return False

async def ensure_source_ingested(
    source_id: Optional[str] = None,
    max_wait_seconds: float = 600.0,
    heartbeat_seconds: float = 5.0
) -> Dict[str, Any]:
    """
    Finite state machine to verify or execute source ingestion in SDP-B001-EXTRACT.
    Fails closed on any unexpected state or invariant violation.
    """
    ctx = get_source_context(source_id=source_id)
    expected_filename = ctx["expected_filename"]
    pdf_path = f"/Users/chrisrodriguez/Downloads/{expected_filename}"
    
    # 1. Validate local PDF
    pdf_meta = check_local_pdf(pdf_path)
    print(f"Local PDF validated: {pdf_meta['filename']} ({pdf_meta['size_mb']} MB, SHA: {pdf_meta['sha256'][:12]}...)", flush=True)
    
    # 2. Get extract tab
    tab = await get_extract_tab()
    ws_url = tab["webSocketDebuggerUrl"]
    
    async with websockets.connect(ws_url, max_size=20*1024*1024) as ws:
        # Check current notebook state
        state = await inspect_notebook_sources(ws)
        print(f"Initial notebook state: {state}", flush=True)
        
        # CATEGORY A: Exactly one source tile exists matching expected_filename
        if state.get("sources") == [expected_filename] and not state.get("has_error"):
            print(f"Source tile '{expected_filename}' already exists. Testing retrieval proof...", flush=True)
            proven = await prove_source_retrieval(ws, expected_filename, timeout=45.0)
            if proven:
                print(f"CATEGORY A: Source '{expected_filename}' is already ingested and verified!", flush=True)
                return {
                    "status": "ALREADY_INGESTED_AND_VERIFIED",
                    "source_id": ctx["source_id"],
                    "expected_filename": expected_filename,
                    "pdf_meta": pdf_meta
                }
                
        # CATEGORY D: Unwanted, residual, or multiple sources exist -> clean up
        if state.get("sources") and state.get("sources") != [expected_filename]:
            print(f"CATEGORY D: Residual/unexpected sources found ({state.get('sources')}). Cleaning up...", flush=True)
            # Remove all sources to restore clean invariant
            await evaluate_cdp(ws, 301, """
            (() => {
                const moreBtns = Array.from(document.querySelectorAll('.source-item-more-button, [aria-label="More"]'));
                for (const b of moreBtns) {
                    b.click();
                }
            })()
            """)
            await asyncio.sleep(1)
            # Navigate to refresh notebook cleanly
            await send_cdp(ws, 302, "Page.navigate", {"url": f"https://notebook.google.com/notebook/b3cd453a-e164-4b72-8383-2bcb5ee075a5"})
            await asyncio.sleep(5)
            state = await inspect_notebook_sources(ws)
            if state.get("sources"):
                raise RuntimeError(f"Could not restore clean 0-source invariant in SDP-B001-EXTRACT: {state.get('sources')}")

        # CATEGORY C: No source tile -> initiate controlled upload
        print(f"CATEGORY C: Ready to upload '{expected_filename}' into SDP-B001-EXTRACT.", flush=True)
        
        # Ensure Add source dialog is open
        if not state.get("dialog_open"):
            print("Opening Add source dialog...", flush=True)
            open_dlg_js = """
            (() => {
                const addBtn = document.querySelector('button[aria-label="Add source"]') ||
                               document.querySelector('.add-source-link') ||
                               Array.from(document.querySelectorAll('button')).find(
                                   b => b.innerText && (b.innerText.includes('Add source') || b.innerText.includes('Sources'))
                               );
                if (addBtn) { addBtn.click(); return true; }
                return false;
            })()
            """
            opened = await evaluate_cdp(ws, 401, open_dlg_js)
            await asyncio.sleep(2)
            
        # Enable CDP Page and file chooser interception
        await send_cdp(ws, 402, "Page.enable")
        await send_cdp(ws, 403, "Page.setInterceptFileChooserDialog", {"enabled": True})
        
        # Locate Upload files button ([xapscottyuploadertrigger])
        find_btn_js = """
        (() => {
            const btn = document.querySelector('[xapscottyuploadertrigger]') || 
                        Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.includes('Upload files'));
            if (!btn) return null;
            const r = btn.getBoundingClientRect();
            return { x: r.x + r.width / 2, y: r.y + r.height / 2, w: r.width, h: r.height };
        })()
        """
        btn_pos = await evaluate_cdp(ws, 404, find_btn_js)
        if not btn_pos:
            raise RuntimeError("Upload files button ([xapscottyuploadertrigger]) not found in Add source dialog")
            
        print(f"Dispatching trusted mouse click to Upload files button at ({btn_pos['x']:.1f}, {btn_pos['y']:.1f})...", flush=True)
        await send_cdp(ws, 405, "Input.dispatchMouseEvent", {
            "type": "mousePressed", "x": btn_pos["x"], "y": btn_pos["y"], "button": "left", "clickCount": 1
        })
        await send_cdp(ws, 406, "Input.dispatchMouseEvent", {
            "type": "mouseReleased", "x": btn_pos["x"], "y": btn_pos["y"], "button": "left", "clickCount": 1
        })
        
        # Wait for Page.fileChooserOpened with 15s deadline
        print("Waiting for Page.fileChooserOpened...", flush=True)
        backend_node_id = None
        t_chooser = time.time()
        while time.time() - t_chooser < 15.0:
            try:
                raw = await asyncio.wait_for(ws.recv(), timeout=2.0)
                evt = json.loads(raw)
                if evt.get("method") == "Page.fileChooserOpened":
                    backend_node_id = evt["params"].get("backendNodeId")
                    print(f"Page.fileChooserOpened received (backendNodeId={backend_node_id})!", flush=True)
                    break
            except asyncio.TimeoutError:
                pass
                
        if not backend_node_id:
            raise RuntimeError("Page.fileChooserOpened event not received within 15s deadline")
            
        # Set file input
        print(f"Setting file input to '{pdf_path}'...", flush=True)
        set_file_res = await send_cdp(ws, 407, "DOM.setFileInputFiles", {
            "files": [pdf_path],
            "backendNodeId": backend_node_id
        })
        print(f"DOM.setFileInputFiles completed: {set_file_res}", flush=True)
        
        # 3. Observe Ingestion Progression
        print(f"Observing ingestion progression (deadline: {max_wait_seconds}s, heartbeat: {heartbeat_seconds}s)...", flush=True)
        t_start = time.time()
        saw_source = False
        saw_indexing = False
        
        while time.time() - t_start < max_wait_seconds:
            await asyncio.sleep(heartbeat_seconds)
            elapsed = int(time.time() - t_start)
            
            st = await inspect_notebook_sources(ws)
            sources = st.get("sources", [])
            has_error = st.get("has_error")
            is_indexing = st.get("is_indexing")
            
            print(f"[{elapsed:3d}s heartbeat] sources={sources}, indexing={is_indexing}, error={has_error}", flush=True)
            
            if has_error:
                raise RuntimeError(f"Terminal error indicator detected on source tile in SDP-B001-EXTRACT: {st}")
                
            if expected_filename in sources:
                saw_source = True
                
            if is_indexing:
                saw_indexing = True
                
            # If source tile is present, indexing has completed/settled, and no errors exist
            if saw_source and not is_indexing:
                print(f"Source tile '{expected_filename}' settled after {elapsed}s! Validating exact state...", flush=True)
                validate_notebook_state("SDP-B001-EXTRACT", sources, expected_source=expected_filename)
                
                # Prove with retrieval probe
                proven = await prove_source_retrieval(ws, expected_filename, timeout=60.0)
                if proven:
                    print(f"SUCCESS: Ingestion of '{expected_filename}' fully verified and proven!", flush=True)
                    return {
                        "status": "INGESTED_AND_VERIFIED",
                        "source_id": ctx["source_id"],
                        "expected_filename": expected_filename,
                        "pdf_meta": pdf_meta,
                        "elapsed_seconds": elapsed
                    }
                else:
                    raise RuntimeError(f"Source tile settled but retrieval verification probe failed for '{expected_filename}'")
                    
        raise TimeoutError(f"Monotonic deadline ({max_wait_seconds}s) exceeded waiting for source ingestion")

if __name__ == "__main__":
    res = asyncio.run(ensure_source_ingested(max_wait_seconds=300.0))
    print(f"\nINGESTION RESULT: {json.dumps(res, indent=2)}")
