import csv
import json
import re
from pathlib import Path
from typing import Optional, Dict, Any

def get_repo_root() -> Path:
    return Path(__file__).resolve().parent.parent

DEFAULT_SOURCE_FILENAMES = {
    "P01F": "sblgnt.pdf",
    "P02F": "swete_lxx_vol1_p02f_target.pdf",
    "P03F": "swete_lxx_vol3_p03f_target.pdf",
    "S01F": "aageson_1984_pauls_use_of_scripture.pdf",
    "S02F": "sanday_headlam_1895_romans_icc.pdf",
    "S03F": "robertson_plummer_1911_1corinthians_icc.pdf",
    "S04F": "lightfoot_1914_galatians.pdf",
    "S05": "wilk_1998_jesaja_paulus.pdf",
    "S06F": "ryskova_2019_isaiah_romans.pdf",
    "S07F": "baaij_2005_romans_4_3.pdf",
    "S08F": "tanner_2005_hosea_romans_9.pdf",
    "S09F": "oliver_2015_romans_10.pdf",
    "S10F": "hamer_2018_genesis_2_24.pdf",
    "S11F": "instone_brewer_1992_1cor_9_9.pdf",
    "S12F": "hwang_2011_exodus_32_6.pdf",
    "S13F": "steyn_2015_deuteronomy_21_23.pdf",
}

def get_source_context(
    source_id: Optional[str] = None,
    repo_root: Optional[Path] = None,
    state_file: str = "research-queue/B001_NOTEBOOKLM_STATE.json",
    queue_file: str = "research-queue/B001_NOTEBOOKLM_SOURCE_QUEUE.csv",
) -> Dict[str, Any]:
    """
    Derives the expected filename, source ID, output directory, and source metadata
    dynamically from the active queue record rather than hardcoding S01F.
    """
    if repo_root is None:
        repo_root = get_repo_root()
    else:
        repo_root = Path(repo_root)

    state_path = repo_root / state_file
    queue_path = repo_root / queue_file

    if not state_path.is_file():
        raise FileNotFoundError(f"State file not found: {state_path}")
    if not queue_path.is_file():
        raise FileNotFoundError(f"Queue file not found: {queue_path}")

    with open(state_path, "r", encoding="utf-8") as f:
        state_data = json.load(f)

    active_id = source_id or state_data.get("active_source_id")
    if not active_id:
        raise ValueError("No active_source_id found in state and no source_id provided")

    batch = state_data.get("batch", "B001-pauline-txt-pilot")
    extraction_nb = state_data.get("extraction_notebook", "SDP-B001-EXTRACT")
    synthesis_nb = state_data.get("synthesis_notebook", "SDP-01 Paul")

    with open(queue_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        matching_row = None
        for row in reader:
            if row.get("source_id") == active_id:
                matching_row = row
                break

    if not matching_row:
        raise KeyError(f"Source ID '{active_id}' not found in queue CSV ({queue_path})")

    expected_filename = matching_row.get("expected_filename")
    if not expected_filename or not expected_filename.strip():
        expected_filename = DEFAULT_SOURCE_FILENAMES.get(active_id)
        if not expected_filename:
            raise ValueError(f"Could not derive expected_filename for source ID '{active_id}'")

    output_dir = repo_root / "research" / "inbox" / batch / "sources" / active_id

    return {
        "source_id": active_id,
        "batch": batch,
        "source_class": matching_row.get("source_class"),
        "author_or_editor": matching_row.get("author_or_editor"),
        "title": matching_row.get("title"),
        "year": matching_row.get("year"),
        "notebook_label": matching_row.get("notebook_label"),
        "expected_filename": expected_filename.strip(),
        "output_dir": str(output_dir),
        "status": matching_row.get("status"),
        "review_status": matching_row.get("review_status"),
        "notes": matching_row.get("notes"),
        "extraction_notebook": extraction_nb,
        "synthesis_notebook": synthesis_nb,
        "raw_json_paths": {
            "prompt_1": str(output_dir / "prompt_1_raw.json"),
            "prompt_2": str(output_dir / "prompt_2_raw.json"),
            "prompt_3": str(output_dir / "prompt_3_raw.json"),
            "prompt_4": str(output_dir / "prompt_4_raw.json"),
            "prompt_5": str(output_dir / "prompt_5_raw.json"),
            "prompt_6": str(output_dir / "prompt_6_raw.json"),
        }
    }

def validate_output_path_isolation(output_path: str, active_source_id: str) -> None:
    """
    Fail-closed guard preventing an active source run (e.g. S02F) from writing into
    or overwriting another source's artifact directory (e.g. S01F).
    """
    norm_path = str(Path(output_path)).replace("\\", "/")
    m = re.search(r"/sources/([^/]+)/", norm_path)
    if m:
        target_source_id = m.group(1)
        if target_source_id != active_source_id:
            raise RuntimeError(
                f"Fail-closed: cross-source artifact overwrite blocked. Active source is '{active_source_id}', "
                f"but target output path points to source '{target_source_id}' ({output_path})."
            )
