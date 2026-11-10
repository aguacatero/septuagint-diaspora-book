#!/usr/bin/env python3
"""Execute deterministic extraction prompts for S09F (Oliver 2015 Romans 10:5–13 Revisited)."""

import asyncio
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.queue_context import get_source_context, validate_output_path_isolation
from scripts.run_secondary_prompt import run_prompt

PROMPTS = {
    0: (
        "Work only from the currently loaded source. Do not use outside knowledge. First identify the source's "
        "author/editor, exact title, publication year, journal name, volume, issue, article number/pages, and the page-numbering system. "
        "State whether printed page numbers are visible and whether your citations can be mapped to them. "
        "If any bibliographic detail is not visible in the source, write UNKNOWN rather than guessing. "
        "End with: SOURCE-BOUND MODE CONFIRMED.",
        "prompt_0_raw.json",
        "metadata.md",
        False  # require_citations
    ),
    1: (
        "Work only from this source. Search the entire source for substantive discussion relevant to any of these B001 comparisons:\n\n"
        "1. Romans 4:3 / Genesis 15:6\n"
        "2. Romans 9:25 / Hosea 2:23\n"
        "3. Romans 9:26 / Hosea 1:10\n"
        "4. Romans 10:6–8 / Deuteronomy 30:12–14 (and Romans 10:11 / Isaiah 28:16, Romans 10:5 / Leviticus 18:5)\n"
        "5. Romans 10:13 / Joel 2:32 (LXX Joel 3:5)\n"
        "6. Romans 11:34 / Isaiah 40:13\n"
        "7. Romans 15:12 / Isaiah 11:10\n"
        "8. 1 Corinthians 1:19 / Isaiah 29:14\n"
        "9. 1 Corinthians 6:16 / Genesis 2:24\n"
        "10. 1 Corinthians 9:9 / Deuteronomy 25:4\n"
        "11. 1 Corinthians 10:7 / Exodus 32:6\n"
        "12. Galatians 3:13 / Deuteronomy 21:23\n\n"
        "Return a table with: B001 ID, discussed YES/NO, page/locator, depth (passing/substantive/extended), "
        "and a one-sentence description of what the author addresses. Do not infer relevance from the article's topic alone. "
        "If the passage is not actually discussed, write NOT DISCUSSED.",
        "prompt_1_raw.json",
        "relevance_scan.md",
        False  # require_citations
    ),
    2: (
        "Work only from this source. For B001-4 (Romans 10:6–8 / Deuteronomy 30:12–14 and Rom 10:11 / Isa 28:16, including Lev 18:5) "
        "and B001-5 (Romans 10:13 / Joel 2:32), extract Willem Oliver's explicit claims. Support each claim with inline citations.\n\n"
        "For each claim provide:\n"
        "- proposed evidence ID: S09F-E###;\n"
        "- B001 passage ID;\n"
        "- author's claim in neutral language;\n"
        "- exact short quotation (<=25 words);\n"
        "- printed page number (pp. 1–12);\n"
        "- citation marker;\n"
        "- textual evidence invoked (MT vs LXX vs Romans);\n"
        "- claim type (textual-critical, exegetical, structural/chiastic);\n"
        "- qualifications stated by the author;\n"
        "- extraction confidence HIGH/MEDIUM/LOW.\n\n"
        "Do not merge separate claims. Do not silently supply premises that the author does not state. "
        "If you cannot find direct support, omit the claim.",
        "prompt_2_raw.json",
        "extraction.md",
        True  # require_citations
    ),
    3: (
        "Work only from this source. For each substantive B001 discussion (especially Romans 10:5–13, Deuteronomy 30:12–14, and Joel 2:32), "
        "map the author's reasoning as:\n\n"
        "QUESTION -> EVIDENCE -> INFERENCE -> CONCLUSION\n\n"
        "Then list:\n"
        "- assumptions the author explicitly acknowledges (e.g. regarding the nature of chiasm, Paul's hermeneutic, oral culture, rhetoric);\n"
        "- alternative explanations the author considers (e.g. traditional antithetical view contrasting Moses and Christ/Faith, chronological vs theological readings of telos nomou);\n"
        "- alternative explanations the author does not address but that are visible from the author's own presentation;\n"
        "- what evidence would weaken or falsify the author's conclusion, if the source states this.\n\n"
        "Distinguish what the source explicitly says from your structural paraphrase.",
        "prompt_3_raw.json",
        "argument_map.md",
        False  # require_citations
    ),
    4: (
        "Work only from this source. Extract every place where the author:\n"
        "- expresses uncertainty;\n"
        "- discusses a competing textual form (e.g. Hebrew MT vs Septuagint LXX vs Romans Greek text, alterations in Deuteronomy 30:12–14, additions in Isaiah 28:16 pas, omission/inclusion of Lord in Joel 2:32);\n"
        "- notes translation nuances or interpretive challenges in Paul's handling of the Law and Faith in Romans 10:5–13;\n"
        "- allows authorial adaptation, midrashic pesher technique, rhetorical modification, or differing Vorlage;\n"
        "- disagrees with another scholar (e.g. Käsemann, Cranfield, Dunn, Moo, Wright, Badenas, Sanders, Toews, etc.);\n"
        "- acknowledges evidence that weakens the preferred chiastic/literary interpretation.\n\n"
        "Give page/locator and citation for each item. If none are present for a B001 passage, "
        "write NONE FOUND IN THIS SOURCE, not NONE EXISTS.",
        "prompt_4_raw.json",
        "counterevidence.md",
        False  # require_citations
    ),
    5: (
        "Work only from this source. For each substantive B001 discussion, list the sources in footnotes/bibliography "
        "that the author relies on or disputes and that look directly relevant to the textual problem of Romans 10:5–13 and its Old Testament citations. "
        "Give the cited author, title or abbreviated title, year if visible, pages if visible, and why it matters. "
        "Do not invent full bibliographic details that are not visible.",
        "prompt_5_raw.json",
        "bibliography_leads.md",
        False  # require_citations
    ),
    6: (
        "Audit your own extraction against this source only.\n\n"
        "Check:\n"
        "1. Did you attribute any claim to the author without direct source support?\n"
        "2. Did any quotation omit nearby words that materially change its meaning?\n"
        "3. Did you infer a printed page number rather than observe it?\n"
        "4. Did you convert an author's possibility into a probability or certainty?\n"
        "5. Did you confuse the author's description of another scholar with the author's own view?\n"
        "6. Did you miss a qualification, objection, textual variant, or counterexample near any extracted passage?\n"
        "7. Did you rely on general model knowledge?\n\n"
        "Return CORRECTIONS REQUIRED or NO CORRECTIONS FOUND, followed by itemized corrections with citations.",
        "prompt_6_raw.json",
        "notebooklm_self_audit.md",
        False  # require_citations
    ),
    7: (
        "Work only from this source. Extract Willem Oliver's explicit analysis of:\n"
        "1. Romans 10:5–13: The overarching chiastic structure and how Deuteronomy 30:12–14 (Rom 10:6–8), Leviticus 18:5 (Rom 10:5), Isaiah 28:16 (Rom 10:11), and Joel 2:32 (Rom 10:13) form the structural and thematic framework.\n"
        "2. The textual and hermeneutical relationship between Paul's quotation of Deuteronomy 30:12–14 and the Old Testament text (MT and LXX), including Paul's explicit changes and personification ('the righteousness of faith speaks').\n"
        "3. The relationship between 'mouth' and 'heart' in Deuteronomy 30:14 and Paul's chiastic inversion and elaboration in Romans 10:9–10.\n"
        "4. The theological debate over whether Paul presents a contrast between Moses (Law) and Faith or whether Paul reads Deuteronomy as prophetic testimony of faith in Christ.\n\n"
        "Provide direct short quotations and exact printed page numbers (pp. 1–12) for each point.",
        "prompt_7_raw.json",
        "oliver_romans_10_chiasm_synthesis.md",
        False  # require_citations
    )
}

async def execute_prompt_step(p_num: int, skip_submission: bool = False, source_id: str = "S09F"):
    ctx = get_source_context(source_id=source_id)
    out_dir = Path(ctx["output_dir"])
    validate_output_path_isolation(str(out_dir), ctx["source_id"])
    out_dir.mkdir(parents=True, exist_ok=True)

    text_prompt, raw_name, md_name, req_cit = PROMPTS[p_num]
    raw_path = out_dir / raw_name
    md_path = out_dir / md_name

    print(f"\n=======================================================", flush=True)
    print(f"Executing Prompt {p_num} for {ctx['source_id']} -> {md_name} (skip_submission={skip_submission})", flush=True)
    print(f"=======================================================", flush=True)

    res = await run_prompt(
        text_prompt,
        expected_source=ctx["expected_filename"],
        source_id=ctx["source_id"],
        output_file=str(raw_path),
        require_citations=req_cit,
        max_wait=180,
        skip_submission=skip_submission
    )

    # Save raw JSON
    with open(raw_path, "w", encoding="utf-8") as f:
        json.dump(res, f, indent=2, ensure_ascii=False)
    print(f"Saved raw response to {raw_path} ({len(res['text'])} chars, {len(res['citations'])} citations)", flush=True)

    # Save markdown prose
    header = f"# {ctx['source_id']} — {md_name.replace('.md', '').replace('_', ' ').title()}\n\n"
    if p_num == 0:
        header += f"**Source ID:** {ctx['source_id']}  \n"
        header += f"**Source Class:** {ctx['source_class']}  \n"
        header += f"**Notebook Container:** `SDP-B001-EXTRACT` (Sole loaded source)  \n"
        header += f"**Expected File:** `{ctx['expected_filename']}`  \n"
        header += f"**Ingestion Mode:** Isolated 1-Source Extraction  \n\n---\n\n"

    content = header + res["text"].strip() + "\n"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Saved markdown to {md_path}", flush=True)

    return res

async def main():
    skip_sub = "--skip-submit" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]

    if not args or args[0] == "all":
        steps = [0, 1, 2, 3, 4, 5, 6, 7]
    else:
        steps = [int(x) for x in args]

    for s in steps:
        await execute_prompt_step(s, skip_submission=skip_sub and (s == steps[0]))
        # Small delay between prompts
        await asyncio.sleep(2)

if __name__ == "__main__":
    asyncio.run(main())
