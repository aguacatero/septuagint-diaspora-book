import asyncio
import base64
import json
from pathlib import Path
import urllib.request
import websockets

async def diagnose():
    url = 'http://127.0.0.1:9222/json'
    with urllib.request.urlopen(url) as r:
        tabs = json.loads(r.read())
    matching = [tab for tab in tabs if 'b3cd453a' in tab.get('url', '')]
    if not matching:
        print("SDP-B001-EXTRACT tab not found!")
        return
    t = matching[0]
    tab_id = t.get('id')
    tab_url = t.get('url')
    ws_url = t.get('webSocketDebuggerUrl')
    print(f"Tab ID: {tab_id}, URL: {tab_url}")
    
    async with websockets.connect(ws_url, max_size=25*1024*1024) as ws:
        async def send(method, params=None):
            msg_id = 1
            payload = {'id': msg_id, 'method': method}
            if params:
                payload['params'] = params
            await ws.send(json.dumps(payload))
            while True:
                msg = json.loads(await ws.recv())
                if msg.get('id') == msg_id:
                    return msg
                    
        async def evaluate(expr):
            res = await send('Runtime.evaluate', {'expression': expr, 'returnByValue': True})
            return res.get('result', {}).get('result', {}).get('value')

        dom_info = await evaluate("""(() => {
            const titleInput = document.querySelector('input.title-input');
            const title = titleInput ? titleInput.value : document.title;
            const sources = Array.from(document.querySelectorAll('.source-title, .source-item-title, [data-source-title]'))
                .map(s => s.innerText.trim());
            const errorContainers = Array.from(document.querySelectorAll('.single-source-error-container, [aria-label*="Error info"]'))
                .map(e => e.innerText.trim());
            const spinners = document.querySelectorAll('mat-progress-bar, mat-spinner, [role=progressbar], .loading').length;
            const dialog = document.querySelector('mat-dialog-container, [role=dialog]');
            const authEl = document.querySelector('[aria-label*="Google Account"], [aria-label*="Google-Konto"]');
            const authAccount = authEl ? authEl.getAttribute('aria-label') : null;
            const userMessages = document.querySelectorAll('.to-user-message-card-content').length;
            
            return {
                title: title,
                sources: sources,
                errorContainers: errorContainers,
                spinners: spinners,
                dialogOpen: Boolean(dialog),
                authAccount: authAccount,
                userMessagesCount: userMessages
            };
        })()""")
        print("DOM State:\n", json.dumps(dom_info, indent=2))
        
        # Capture screenshot for diagnostic artifact
        shot = await send('Page.captureScreenshot', {'format': 'png'})
        if 'result' in shot and 'data' in shot['result']:
            out_img = Path('research/inbox/B001-pauline-txt-pilot/sources/S02F/diagnostic_extract_tab.png')
            out_img.parent.mkdir(parents=True, exist_ok=True)
            out_img.write_bytes(base64.b64decode(shot['result']['data']))
            print(f"Diagnostic screenshot saved to: {out_img}")

if __name__ == '__main__':
    asyncio.run(diagnose())
