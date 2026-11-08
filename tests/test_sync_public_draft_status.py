"""Adversarial checks: public source progress cannot promote a research gate."""
from __future__ import annotations

import copy
import unittest

from scripts.sync_public_draft_status import (
    BEGIN, END, replace_public_block, reviews_from_comments, validate_and_render,
)

HEAD = "a" * 40
ORDER = ["P01F", "P02F", "P03F", "S01F", "S02F", "S03F", "S04F", "S05", "S06F", "S07F",
         "S08F", "S09F", "S10F", "S11F", "S12F", "S13F"]


def fixtures():
    pr = {"number": 2, "state": "open", "draft": True, "merged_at": None,
          "base": {"ref": "main"},
          "head": {"ref": "research/B001-notebooklm-serial", "sha": HEAD,
                   "repo": {"full_name": "aguacatero/septuagint-diaspora-book"}}}
    state = {"draft_pr": 2, "branch": "research/B001-notebooklm-serial",
             "active_source_id": "S07F", "last_accepted_source_id": "S06F",
             "active_phase": "AWAITING_REVIEW", "updated_at": "2026-11-08"}
    queue = [{"order": str(i + 1), "source_id": source,
              "status": "DONE" if i < 9 else ("SUBMITTED" if i == 9 else "PENDING"),
              "review_status": "ACCEPTED" if i < 9 else ("AWAITING_REVIEW" if i == 9 else "NOT_STARTED")}
             for i, source in enumerate(ORDER)]
    reviews = [{"source": sid, "sha": str(i + 1) * 40, "verdict": "ACCEPT",
                "url": f"https://github.com/aguacatero/septuagint-diaspora-book/pull/2#issuecomment-{i + 1}"}
               for i, sid in enumerate(ORDER[:9])]
    reviews.append({"source": "S07F", "sha": HEAD, "verdict": "REVISE",
                    "url": "https://github.com/aguacatero/septuagint-diaspora-book/pull/2#issuecomment-42"})
    return pr, state, queue, reviews


class PublicDraftStatusTests(unittest.TestCase):

    def test_renders_live_review_and_source_count_without_promoting_milestones(self):
        result = validate_and_render(*fixtures())
        self.assertIn("9/16 source packets independently accepted", result)
        self.assertIn("9/16 promoted", result)
        self.assertIn("**S07F** (source 10/16)", result)
        self.assertIn("**REVISE**", result)
        self.assertIn("DRAFT / UNMERGED", result)
        self.assertIn("Project milestone gates remain 1/6 accepted", result)
        self.assertNotIn("2/6 accepted", result)

    def test_new_head_cannot_inherit_previous_exact_sha_review(self):
        pr, state, queue, reviews = fixtures()
        pr["head"]["sha"] = "b" * 40
        text = validate_and_render(pr, state, queue, reviews)
        self.assertIn("**AWAITING_REVIEW** for the current commit", text)
        self.assertIn("last verdict was **REVISE**", text)

    def test_source_queue_must_be_reviewed_not_self_accepted(self):
        pr, state, queue, reviews = fixtures()
        reviews = [r for r in reviews if r["source"] != "S06F"]
        with self.assertRaisesRegex(ValueError, "lack independent exact-SHA review"):
            validate_and_render(pr, state, queue, reviews)

    def test_rejects_forged_acceptance_and_premature_source_advance(self):
        pr, state, queue, reviews = fixtures()
        queue[9]["status"] = "DONE"
        queue[9]["review_status"] = "ACCEPTED"
        state["active_source_id"] = "S08F"
        state["last_accepted_source_id"] = "S07F"
        with self.assertRaisesRegex(ValueError, "lack independent exact-SHA review"):
            validate_and_render(pr, state, queue, reviews)

    def test_rejects_nonserial_promotions(self):
        pr, state, queue, reviews = fixtures()
        queue[8]["status"] = "SUBMITTED"
        queue[7]["status"] = "DONE"
        with self.assertRaisesRegex(ValueError, "Promoted sources are not a serial prefix|Active source"):
            validate_and_render(pr, state, queue, reviews)

    def test_rejects_non_draft_or_merged_pr(self):
        pr, state, queue, reviews = fixtures()
        pr["draft"] = False
        with self.assertRaisesRegex(ValueError, "not the expected open"):
            validate_and_render(pr, state, queue, reviews)

    def test_comment_parser_requires_owner_sha_and_source_header(self):
        good = {"id": 10, "user": {"login": "aguacatero"},
                "body": "REVIEWED_SHA: " + HEAD +
                        "\nSOURCE_ID: S07F\n**SOURCE_PACKET: REVISE**\n"}
        bad = copy.deepcopy(good)
        bad["user"]["login"] = "someone_else"
        verdicts = reviews_from_comments([good, bad])
        self.assertEqual(len(verdicts), 1)
        self.assertEqual(verdicts[0]["source"], "S07F")
        self.assertEqual(verdicts[0]["verdict"], "REVISE")

    def test_replace_only_marked_readme_section_idempotently(self):
        original = ("# Book\n\n## Research progress\n"
                    "- [x] **Foundation**\n- [ ] **TXT**\n"
                    + BEGIN + "\nold\n" + END
                    + "\n\n## Conclusion\nDo not touch this.\n")
        updated = replace_public_block(original, "9/16 DRAFT")
        self.assertIn("- [x] **Foundation**\n- [ ] **TXT**", updated)
        self.assertIn("## Conclusion\nDo not touch this.", updated)
        self.assertEqual(updated, replace_public_block(updated, "9/16 DRAFT"))
        with self.assertRaisesRegex(ValueError, "exactly one"):
            replace_public_block("# No marker", "10/16")


if __name__ == "__main__":
    unittest.main()
