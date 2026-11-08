#!/usr/bin/env python3
"""Publish *provisional* B001 source-queue progress on main without promoting research.

Run on trusted main only. Remote PR #2 data are treated as untrusted input: all
counts are validated against serial queue invariants and exact-SHA review
comments. This program edits only the marked README section; never the roadmap,
registry, six milestone checkboxes, or the research branch.
"""
from __future__ import annotations

import argparse
import base64
import csv
import io
import json
import os
import re
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

REPO = "aguacatero/septuagint-diaspora-book"
PR_NUMBER = 2
SOURCE_COUNT = 16
STATE_PATH = "research-queue/B001_NOTEBOOKLM_STATE.json"
QUEUE_PATH = "research-queue/B001_NOTEBOOKLM_SOURCE_QUEUE.csv"
ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
BEGIN = "<!-- BEGIN PUBLIC-B001-DRAFT-STATUS: automated, provisional; do not edit -->"
END = "<!-- END PUBLIC-B001-DRAFT-STATUS -->"
SOURCE_ID = re.compile(r"^[PS]\d{2}F?$")
SHA = re.compile(r"^[a-f0-9]{40}$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SAFE_STATE = re.compile(r"^[A-Z][A-Z0-9_]*$")
VERDICT = re.compile(r"(?m)^[ \t]*(?:\*\*)?SOURCE_PACKET:[ \t]*(ACCEPT|REVISE|REJECT)\b")
REVIEW_SHA = re.compile(r"(?m)^REVIEWED_SHA:[ \t]*([a-f0-9]{40})[ \t]*$")
REVIEW_SOURCE = re.compile(r"(?m)^SOURCE_ID:[ \t]*([PS]\d{2}F?)[ \t]*$")


def api_json(path: str):
    """Read public repository metadata with the Actions token (no PR code runs)."""
    token = os.getenv("GH_TOKEN", "")
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "public-b001-draft-readme-sync",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = "Bearer " + token
    with urlopen(Request("https://api.github.com/repos/" + REPO + "/" + path,
                         headers=headers), timeout=25) as response:
        return json.load(response)


def branch_file(path: str, sha: str) -> str:
    payload = api_json("contents/" + path + "?ref=" + quote(sha))
    if payload.get("type") != "file" or payload.get("encoding") != "base64":
        raise ValueError("Unexpected GitHub Contents response for " + path)
    return base64.b64decode(payload["content"], validate=False).decode("utf-8")


def reviews_from_comments(comments: list[dict]) -> list[dict]:
    """Accept only clearly marked owner-posted exact-SHA source verdicts."""
    records = []
    for comment in comments:
        if comment.get("user", {}).get("login") != "aguacatero":
            continue
        body = comment.get("body") or ""
        verdicts = VERDICT.findall(body)
        shas = REVIEW_SHA.findall(body)
        sources = REVIEW_SOURCE.findall(body)
        if not (verdicts and len(shas) == 1 and len(sources) == 1):
            continue
        records.append({
            "source": sources[0],
            "sha": shas[0],
            "verdict": verdicts[-1],
            "url": "https://github.com/" + REPO + "/pull/2#issuecomment-" + str(comment["id"]),
        })
    return records


def issue_comments() -> list[dict]:
    comments = []
    for page in range(1, 21):
        part = api_json(f"issues/{PR_NUMBER}/comments?per_page=100&page={page}")
        if not isinstance(part, list):
            raise ValueError("GitHub comments response is not a list")
        comments.extend(part)
        if len(part) < 100:
            return comments
    raise ValueError("Review comment pagination exceeds safety cap")


def validate_and_render(pr: dict, state: dict, queue: list[dict], reviews: list[dict]) -> str:
    """Fail closed on inconsistent draft facts rather than publishing an inflated count."""
    head = pr.get("head", {})
    if (pr.get("number") != PR_NUMBER or pr.get("state") != "open"
            or pr.get("draft") is not True or pr.get("merged_at") is not None
            or pr.get("base", {}).get("ref") != "main"
            or head.get("ref") != "research/B001-notebooklm-serial"
            or head.get("repo", {}).get("full_name") != REPO
            or not SHA.fullmatch(head.get("sha", ""))):
        raise ValueError("B001 PR #2 is not the expected open, draft, unmerged research PR")
    if (state.get("draft_pr") != PR_NUMBER
            or state.get("branch") != head["ref"]
            or state.get("active_source_id") is None
            or not DATE.fullmatch(str(state.get("updated_at", "")))):
        raise ValueError("B001 state does not match live research PR")
    if len(queue) != SOURCE_COUNT or any(set(["order", "source_id", "status", "review_status"]) - set(r) for r in queue):
        raise ValueError("B001 source queue must contain 16 complete records")
    ids = [row["source_id"] for row in queue]
    if (len(ids) != len(set(ids)) or any(not SOURCE_ID.fullmatch(i) for i in ids)
            or [int(r["order"]) for r in queue] != list(range(1, SOURCE_COUNT + 1))):
        raise ValueError("B001 queue has duplicate, malformed, or unordered sources")
    active_id = state["active_source_id"]
    if active_id not in ids:
        raise ValueError("Active source missing from B001 queue")
    active_index = ids.index(active_id)
    phase = state.get("active_phase", "")
    if not SAFE_STATE.fullmatch(phase):
        raise ValueError("Unsafe active phase")
    for row in queue:
        if not SAFE_STATE.fullmatch(row["status"]) or not SAFE_STATE.fullmatch(row["review_status"]):
            raise ValueError("Unsafe queue status")
        if row["status"] == "DONE" and row["review_status"] != "ACCEPTED":
            raise ValueError("DONE source lacks accepted review")
    accepted = [row for row in queue if row["review_status"] == "ACCEPTED"]
    promoted = [row for row in accepted if row["status"] == "DONE"]
    if [row["source_id"] for row in accepted] != ids[:len(accepted)]:
        raise ValueError("Source acceptance is not a serial prefix")
    if [row["source_id"] for row in promoted] != ids[:len(promoted)]:
        raise ValueError("Promoted sources are not a serial prefix")
    if active_index != len(promoted):
        raise ValueError("Active source is not the next after promoted serial prefix")
    last = state.get("last_accepted_source_id")
    if last != (accepted[-1]["source_id"] if accepted else None):
        raise ValueError("State last accepted source disagrees with queue")
    # A queue label is not its own proof of source acceptance.
    accepted_ids = {r["source"] for r in reviews if r["verdict"] == "ACCEPT"}
    if not {row["source_id"] for row in accepted}.issubset(accepted_ids):
        raise ValueError("One or more accepted sources lack independent exact-SHA review comments")
    active_reviews = [r for r in reviews if r["source"] == active_id]
    last_review = active_reviews[-1] if active_reviews else None
    if last_review is not None and last_review["sha"] == head["sha"]:
        decision = f'**{last_review["verdict"]}** ([independent exact-SHA review]({last_review["url"]}))'
    elif last_review is not None:
        decision = (f'**AWAITING_REVIEW** for the current commit; last verdict was '
                    f'**{last_review["verdict"]}** ([previous review]({last_review["url"]}))')
    else:
        decision = "**AWAITING_REVIEW** (no recorded source verdict yet)"
    return (
        f'**Provisional B001 progress — DRAFT / UNMERGED** '
        f'(research ledger {state["updated_at"]}; [live PR #{PR_NUMBER}]'
        f'(https://github.com/{REPO}/pull/{PR_NUMBER}), '
        f'HEAD `{head["sha"][:12]}`): '
        f'**{len(accepted)}/{SOURCE_COUNT} source packets independently accepted**, '
        f'**{len(promoted)}/{SOURCE_COUNT} promoted to the draft `SDP-01 Paul` synthesis. '
        f'Active: **{active_id}** (source {active_index + 1}/{SOURCE_COUNT}), '
        f'phase `{phase}`, queue `{queue[active_index]["status"]}`. '
        f'Latest independent review: {decision}. '
        f'This is **not accepted evidence on `main`** and does **not** complete '
        f'B001 or TXT. **Project milestone gates remain 1/6 accepted** '
        f'(the separately reviewed Foundation gate only).'
    )


def replace_public_block(readme: str, rendered: str) -> str:
    if readme.count(BEGIN) != 1 or readme.count(END) != 1:
        raise ValueError("README must contain exactly one marked public draft checkpoint")
    first = readme.index(BEGIN)
    last = readme.index(END) + len(END)
    if first >= last or not readme.startswith("## Research progress", readme.rfind("## ", 0, first)):
        raise ValueError("Draft checkpoint must be in README Research progress section")
    return readme[:first] + BEGIN + "\n" + rendered + "\n" + END + readme[last:]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    pr = api_json(f"pulls/{PR_NUMBER}")
    head_sha = pr["head"]["sha"]
    state = json.loads(branch_file(STATE_PATH, head_sha))
    queue = list(csv.DictReader(io.StringIO(branch_file(QUEUE_PATH, head_sha))))
    rendered = validate_and_render(pr, state, queue, reviews_from_comments(issue_comments()))
    before = README.read_text(encoding="utf-8")
    after = replace_public_block(before, rendered)
    if args.check and before != after:
        print("Public B001 draft checkpoint is stale")
        return 1
    if not args.check and before != after:
        README.write_text(after, encoding="utf-8")
        print("Updated provisional public B001 checkpoint (no research promotion)")
    else:
        print("Public B001 draft checkpoint checked and unchanged")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
