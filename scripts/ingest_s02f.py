import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.notebooklm_ingest import ensure_source_ingested

async def main():
    source_id = sys.argv[1] if len(sys.argv) > 1 else "S02F"
    res = await ensure_source_ingested(source_id=source_id, max_wait_seconds=600.0, heartbeat_seconds=5.0)
    print(f"\nINGESTION COMPLETED: {json.dumps(res, indent=2)}")

if __name__ == "__main__":
    asyncio.run(main())
