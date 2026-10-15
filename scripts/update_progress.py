#!/usr/bin/env python3
"""Synchronize the public progress figure with reviewed README milestones.

The six README checkboxes are the source of truth. Do not check a box until
the corresponding milestone has passed review and has been accepted into main.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
SVG = ROOT / "assets" / "progress.svg"
PROGRESS_SECTION = re.compile(r"(?ms)^## Project progress\n.*?(?=^## |\Z)")
CHECKBOX = re.compile(r"(?m)^- \[([ xX])\] \*\*")
SUMMARY = re.compile(r"(?m)^\*\*Milestones complete: \d+ of \d+ \(\d+%\)\*\*$")
IMAGE = "![Project progress bar](assets/progress.svg)"


def render_svg(done: int, total: int, percent: int) -> str:
    fill_width = 732 * done // total
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="800" height="108" viewBox="0 0 800 108" role="img" aria-labelledby="progress-title progress-description">\n'
        f'  <title id="progress-title">Project progress: {percent}%</title>\n'
        f'  <desc id="progress-description">{done} of {total} research-to-book milestones complete</desc>\n'
        '  <rect x="0" y="0" width="800" height="108" rx="15" fill="#f6f8fa"/>\n'
        '  <text x="24" y="35" font-family="Arial, Helvetica, sans-serif" font-size="21" font-weight="bold" fill="#24292f">Research-to-book progress</text>\n'
        f'  <text x="776" y="35" text-anchor="end" font-family="Arial, Helvetica, sans-serif" font-size="19" font-weight="bold" fill="#24292f">{percent}%  ({done}/{total})</text>\n'
        '  <rect x="24" y="57" width="732" height="27" rx="13.5" fill="#d0d7de"/>\n'
        '  <clipPath id="progress-clip"><rect x="24" y="57" width="732" height="27" rx="13.5"/></clipPath>\n'
        f'  <rect x="24" y="57" width="{fill_width}" height="27" fill="#238636" clip-path="url(#progress-clip)"/>\n'
        '</svg>\n'
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if README or SVG is out of sync")
    args = parser.parse_args()

    readme = README.read_text(encoding="utf-8")
    match = PROGRESS_SECTION.search(readme)
    if match is None:
        parser.error("README.md must have a '## Project progress' section")
    section = match.group()
    checkboxes = CHECKBOX.findall(section)
    if len(checkboxes) != 6:
        parser.error(f"expected exactly six milestone checkboxes, found {len(checkboxes)}")
    if section.count(IMAGE) != 1:
        parser.error("README progress section must contain the local SVG image exactly once")
    if len(SUMMARY.findall(section)) != 1:
        parser.error("README progress section must contain exactly one milestone summary")

    done = sum(c.lower() == "x" for c in checkboxes)
    total = len(checkboxes)
    percent = (100 * done + total // 2) // total
    new_section = SUMMARY.sub(f"**Milestones complete: {done} of {total} ({percent}%)**", section)
    new_readme = readme[:match.start()] + new_section + readme[match.end():]
    new_svg = render_svg(done, total, percent)

    desired = [(README, new_readme), (SVG, new_svg)]
    stale = [path for path, text in desired if not path.exists() or path.read_text(encoding="utf-8") != text]
    if args.check:
        if stale:
            print("Out-of-sync progress files: " + ", ".join(str(path.relative_to(ROOT)) for path in stale))
            print("Run: python3 scripts/update_progress.py")
            return 1
        print(f"Progress verified: {done}/{total} ({percent}%)")
        return 0

    for path, text in desired:
        if path in stale:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
    print(f"Progress synchronized: {done}/{total} ({percent}%)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
