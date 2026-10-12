# Antigravity Start — B001 NotebookLM Serial Research

Read and obey:

1. `.agents/skills/notebooklm-serial-research/SKILL.md`
2. `research-queue/CURRENT_BATCH.md`
3. `docs/workflow/NOTEBOOKLM_ANTIGRAVITY_SERIAL.md`
4. `docs/workflow/NOTEBOOKLM_EXTRACTION_PROMPTS.md`
5. `research-queue/B001_NOTEBOOKLM_SOURCE_QUEUE.csv`
6. `research-queue/B001_NOTEBOOKLM_STATE.json`

Goal: process the B001 corpus **one source at a time**, using NotebookLM for source-bounded extraction, verifying citations, committing the source packet to GitHub, and stopping at the independent ChatGPT review gate before advancing.

Use Google/Gemini models for Antigravity orchestration. Use the `aguacatero/chatgpt-relay` reusable review controller for exact-SHA review handoff. Do not use the legacy Claude/Haiku relay worker.

Do not begin the next source until the current source packet is independently accepted.
