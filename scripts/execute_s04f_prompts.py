#!/usr/bin/env python3
"""Execute deterministic extraction prompts for S04F (Lightfoot 1914 Galatians)."""

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
        "author/editor, exact title, publication year, edition/volume if visible, and the page-numbering system. "
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
        "4. Romans 10:11 / Isaiah 28:16\n"
        "5. Romans 10:13 / Joel 2:32\n"
        "6. Romans 11:34 / Isaiah 40:13\n"
        "7. Romans 15:12 / Isaiah 11:10\n"
        "8. 1 Corinthians 1:19 / Isaiah 29:14\n"
        "9. 1 Corinthians 6:16 / Genesis 2:24\n"
        "10. 1 Corinthians 9:9 / Deuteronomy 25:4\n"
        "11. 1 Corinthians 10:7 / Exodus 32:6\n"
        "12. Galatians 3:13 / Deuteronomy 21:23\n\n"
        "Return a table with: B001 ID, discussed YES/NO, page/locator, depth (passing/substantive/extended), "
        "and a one-sentence description of what the author addresses. Do not infer relevance from the book's topic alone. "
        "If the passage is not actually discussed, write NOT DISCUSSED.",
        "prompt_1_raw.json",
        "relevance_scan.md",
        False  # require_citations
    ),
    2: (
        "Work only from this source. For every B001 item marked substantive or extended (particularly B001-12 Galatians 3:13 / Deuteronomy 21:23 "
        "and any substantive cross-epistle treatments such as B001-1 Genesis 15:6 / Romans 4:3 on Galatians 3:6 and the Faith of Abraham excursus), "
        "extract the author's actual position.\n\n"
        "For each distinct claim provide:\n"
        "- proposed evidence ID: S04F-E###;\n"
        "- B001 passage ID;\n"
        "- the author's claim in neutral language;\n"
        "- one short exact quotation that directly supports the claim, preferably <=25 words;\n"
        "- printed page number if visible, otherwise the best source locator;\n"
        "- your NotebookLM citation;\n"
        "- textual evidence the author invokes;\n"
        "- whether the author is making a textual-critical, exegetical, literary, historical, or methodological claim;\n"
        "- qualifications or conditions stated by the author;\n"
        "- extraction confidence HIGH/MEDIUM/LOW.\n\n"
        "Do not merge separate claims. Do not silently supply premises that the author does not state. "
        "If you cannot find direct support, omit the claim.",
        "prompt_2_raw.json",
        "extraction.md",
        True  # require_citations
    ),
    3: (
        "Work only from this source. For each substantive B001 discussion (especially Galatians 3:13 / Deuteronomy 21:23 "
        "and Galatians 3:6 / Genesis 15:6), map the author's reasoning as:\n\n"
        "QUESTION -> EVIDENCE -> INFERENCE -> CONCLUSION\n\n"
        "Then list:\n"
        "- assumptions the author explicitly acknowledges;\n"
        "- alternative explanations the author considers;\n"
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
        "- discusses a competing textual form (e.g. Hebrew vs LXX vs other Greek versions like Aquila, Symmachus, Theodotion, or Targums/Peshitta);\n"
        "- notes a Hebrew/Greek ambiguity (such as qilalath elohim in Deut 21:23);\n"
        "- allows authorial adaptation, intentional omission (such as hypo Theou in Gal 3:13), oral transmission, liturgical transmission, or an unknown textual form;\n"
        "- disagrees with another scholar (ancient or modern);\n"
        "- acknowledges evidence that weakens the preferred interpretation.\n\n"
        "Give page/locator and citation for each item. If none are present for a B001 passage, "
        "write NONE FOUND IN THIS SOURCE, not NONE EXISTS.",
        "prompt_4_raw.json",
        "counterevidence.md",
        False  # require_citations
    ),
    5: (
        "Work only from this source. For each substantive B001 discussion, list the sources in footnotes/bibliography "
        "that the author relies on or disputes and that look directly relevant to the textual problem "
        "(e.g. Patristic authors like Justin Martyr, Tertullian, Jerome; Jewish commentators like Philo, Targums; "
        "textual versions like Aquila, Symmachus; modern scholars like Winer, Bleek, Schöttgen, Carpzov). "
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
        "Work only from this source. From the dedicated Excursus 'The interpretation of Deut. xxi. 23' (printed pages 152–154) "
        "and the commentary on Galatians 3:13 (pp. 139–140), extract Lightfoot's explicit analysis and findings regarding:\n"
        "1. The Hebrew wording and grammatical ambiguity of Deut 21:23 (subjective genitive 'cursed by God' vs objective genitive 'a reproach/insult against God').\n"
        "2. How the passage was translated in ancient versions: LXX, Aquila, Symmachus, Theodotion, the Targums (Onkelos, Pseudo-Jonathan), and the Peshitta.\n"
        "3. The Patristic evidence and Jewish-Christian controversy (Justin Martyr Dialogue with Trypho, Tertullian Adv. Judaeos, Jerome on Galatians, the Dispute of Jason and Papiscus, Evagrius).\n"
        "4. Why Paul omitted 'by God' (hypo Theou) in his citation of Deut 21:23 in Galatians 3:13, and whether Christ was in any sense 'cursed by God'.\n"
        "5. Whether Deuteronomy originally referred to crucifixion or post-mortem impalement/exposure, and how Jewish and early Christian tradition applied it to crucifixion.\n\n"
        "Provide direct short quotations and exact printed page numbers for each point.",
        "prompt_7_raw.json",
        "deut_21_23_excursus_extraction.md",
        False  # require_citations
    )
}

async def execute_prompt_step(p_num: int, skip_submission: bool = False, source_id: str = "S04F"):
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
