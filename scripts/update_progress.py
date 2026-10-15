#!/usr/bin/env python3
"""Synchronize the segmented research roadmap with reviewed README milestones."""
from __future__ import annotations

import argparse
import re
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
CURRENT_BATCH = ROOT / "research-queue" / "CURRENT_BATCH.md"
SVG = ROOT / "assets" / "progress.svg"
PROGRESS_SECTION = re.compile(r"(?ms)^## Research progress\n.*?(?=^## |\Z)")
CHECKBOX = re.compile(r"(?m)^- \[([ xX])\] \*\*")
SUMMARY = re.compile(r"(?m)^<summary>Milestone gates \(\d+/\d+ accepted\)</summary>$")
IMAGE = "![Six-stage research roadmap](assets/progress.svg)"
STAGES = ("BASE", "TXT", "NAR", "CUL", "HIS", "BOOK")
COLORS = {
    "DONE": ("#86efac", "#14532d"),
    "ACTIVE": ("#fbbf24", "#78350f"),
    "PENDING": ("#e2e8f0", "#334155"),
}


def active_module() -> str | None:
    batch = CURRENT_BATCH.read_text(encoding="utf-8")
    match = re.search(r"(?m)^\*\*Module:\*\*\s+(TXT|NAR|CUL|HIS)\s*$", batch)
    return match.group(1) if match else None


def render_svg(completed: list[bool], active: str | None) -> str:
    count = sum(completed)
    total = len(completed)
    states = [
        "DONE" if done else "ACTIVE" if stage == active else "PENDING"
        for stage, done in zip(STAGES, completed)
    ]
    status = ", ".join(f"{name} {state.lower()}" for name, state in zip(STAGES, states))
    lines = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="740" height="122" viewBox="0 0 740 122" role="img" aria-labelledby="title description">',
        f'  <title id="title">Research roadmap: {count} of {total} gates accepted</title>',
        f'  <desc id="description">{escape(status)}. Green means accepted; amber means active research; gray means pending.</desc>',
        '  <rect x="1" y="1" width="738" height="120" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="2"/>',
        '  <text x="20" y="27" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="700" fill="#0f172a">Research roadmap</text>',
        f'  <text x="720" y="27" text-anchor="end" font-family="Arial, Helvetica, sans-serif" font-size="14" fill="#475569">{count} / {total} gates accepted</text>',
    ]
    for index, (stage, state) in enumerate(zip(STAGES, states)):
        x = 20 + index * 118
        background, foreground = COLORS[state]
        cx = x + 54
        weight = ' font-weight="700"' if state != "PENDING" else ""
        lines.append(f'  <rect x="{x}" y="42" width="108" height="34" rx="6" fill="{background}"/>')
        lines.append(
            f'  <text x="{cx}" y="64" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="11"{weight} fill="{foreground}">{stage} · {state}</text>'
        )
    lines.extend([
        '  <text x="20" y="103" font-family="Arial, Helvetica, sans-serif" font-size="13" fill="#475569">Green = accepted · Amber = active research</text>',
        '  <text x="720" y="103" text-anchor="end" font-family="Arial, Helvetica, sans-serif" font-size="13" fill="#475569">Gray = pending</text>',
        '</svg>',
    ])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if README or SVG is out of sync")
    args = parser.parse_args()

    readme = README.read_text(encoding="utf-8")
    match = PROGRESS_SECTION.search(readme)
    if match is None:
        parser.error("README.md must have a Research progress section")
    section = match.group()
    checkboxes = CHECKBOX.findall(section)
    if len(checkboxes) != len(STAGES):
        parser.error(f"expected {len(STAGES)} milestone checkboxes, found {len(checkboxes)}")
    if section.count(IMAGE) != 1 or len(SUMMARY.findall(section)) != 1:
        parser.error("README needs exactly one roadmap image and one milestone summary")

    completed = [mark.lower() == "x" for mark in checkboxes]
    active = active_module()
    if active is not None and completed[STAGES.index(active)]:
        parser.error(f"{active} is both accepted and active: reconcile CURRENT_BATCH.md")
    done, total = sum(completed), len(completed)
    new_section = SUMMARY.sub(f"<summary>Milestone gates ({done}/{total} accepted)</summary>", section)
    new_readme = readme[:match.start()] + new_section + readme[match.end():]
    new_svg = render_svg(completed, active)
    desired = [(README, new_readme), (SVG, new_svg)]
    stale = [path for path, content in desired
             if not path.exists() or path.read_text(encoding="utf-8") != content]

    if args.check:
        if stale:
            print("Out-of-sync progress files: " + ", ".join(str(p.relative_to(ROOT)) for p in stale))
            print("Run: python3 scripts/update_progress.py")
            return 1
        print(f"Progress verified: {done}/{total} accepted, active: {active or 'none'}")
        return 0

    for path, content in desired:
        if path in stale:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
    print(f"Progress synchronized: {done}/{total} accepted, active: {active or 'none'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
