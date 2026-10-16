# NotebookLM Browser Pre-flight — macOS

## Why this exists

The first B001 smoke test correctly failed because the Antigravity Chrome DevTools transport tried to attach to the normal Chrome profile and could not find `DevToolsActivePort`.

For current Chrome, do **not** solve this by adding only `--remote-debugging-port=9222` to the normal/default Chrome profile.

Chrome 136+ requires flag-based remote debugging to use a **non-default user-data directory**. This project therefore uses a dedicated persistent research profile.

## Supported browser transport

Dedicated Chrome profile:

```text
~/.cache/sdp-notebooklm-chrome
```

DevTools endpoint:

```text
http://127.0.0.1:9222
```

Start it with:

```bash
bash scripts/start_notebooklm_debug_chrome.sh
```

This intentionally does **not** quit or reuse the owner's normal Chrome profile.

## One-time login

On the first launch, the dedicated Chrome profile may not be logged into Google/NotebookLM.

The owner may need to sign in once interactively in that dedicated profile.

After login, keep this profile dedicated to NotebookLM/research automation so cookies/session state can persist between Antigravity runs.

Do not use the debug profile for email, banking, admin consoles, or unrelated sensitive browsing.

## Antigravity / Chrome DevTools MCP connection

Before invoking NotebookLM automation, verify:

```bash
curl -fsS http://127.0.0.1:9222/json/version
```

A successful JSON response is the browser-ready gate.

The Chrome DevTools MCP connection must attach explicitly to that endpoint, equivalent to:

```text
chrome-devtools-mcp@latest --browser-url=http://127.0.0.1:9222
```

If Antigravity's built-in `mcp_chrome_devtools` still searches for:

```text
~/Library/Application Support/Google/Chrome/DevToolsActivePort
```

then it is still attempting the wrong/default-profile transport.

In that case Antigravity must reconfigure/use a Chrome DevTools MCP instance with `--browser-url=http://127.0.0.1:9222`, or use the BrowserMCP/Playwright fallback allowed by the serial-research skill.

Do not declare the browser pre-flight successful merely because Chrome is open.

## Smoke-test browser gate

The rerun may proceed only after all of these are true:

1. `scripts/start_notebooklm_debug_chrome.sh` exits 0.
2. `curl -fsS http://127.0.0.1:9222/json/version` succeeds.
3. Antigravity's browser tool can list/open a page through that exact debug browser.
4. NotebookLM is reachable in the dedicated profile.
5. The Google account is authenticated.

Then continue the existing ten-step NotebookLM/citation smoke test in `START_HERE_ANTIGRAVITY.md`.

## Security note

A DevTools-enabled browser can be controlled by local software with access to its debugging endpoint. That is why this project uses a separate profile bound to loopback and keeps the owner's normal Chrome profile out of the automation lane.
