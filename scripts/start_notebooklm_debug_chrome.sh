#!/usr/bin/env bash
set -euo pipefail

PORT="${SDP_NOTEBOOKLM_CHROME_PORT:-9222}"
PROFILE_DIR="${SDP_NOTEBOOKLM_CHROME_PROFILE:-$HOME/.cache/sdp-notebooklm-chrome}"
START_URL="${1:-https://notebooklm.google.com/}"
CHROME_APP="/Applications/Google Chrome.app"

if [[ ! -d "$CHROME_APP" ]]; then
  echo "Google Chrome not found at $CHROME_APP" >&2
  exit 1
fi

endpoint="http://127.0.0.1:${PORT}/json/version"

if curl --silent --fail --max-time 2 "$endpoint" >/dev/null 2>&1; then
  echo "NotebookLM debug Chrome already available: $endpoint"
  echo "Profile: $PROFILE_DIR"
  exit 0
fi

mkdir -p "$PROFILE_DIR"

echo "Starting dedicated NotebookLM Chrome profile..."
echo "Profile: $PROFILE_DIR"
echo "DevTools: http://127.0.0.1:$PORT"
echo "IMPORTANT: use this profile only for NotebookLM/research automation."

open -na "Google Chrome" --args   --remote-debugging-address=127.0.0.1   --remote-debugging-port="$PORT"   --user-data-dir="$PROFILE_DIR"   --no-first-run   --no-default-browser-check   "$START_URL"

for _ in {1..30}; do
  if curl --silent --fail --max-time 2 "$endpoint" >/dev/null 2>&1; then
    echo "READY: $endpoint"
    exit 0
  fi
  sleep 1
done

echo "Chrome started but the DevTools endpoint did not become reachable." >&2
echo "Check: curl $endpoint" >&2
exit 2
