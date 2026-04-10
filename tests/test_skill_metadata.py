import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "super-rebuttal"


class SkillMetadataTest(unittest.TestCase):
    def test_required_files_exist(self) -> None:
        self.assertTrue((SKILL_DIR / "SKILL.md").exists())
        self.assertTrue((SKILL_DIR / "agents" / "openai.yaml").exists())
        self.assertTrue((SKILL_DIR / "references" / "input-contract.md").exists())
        self.assertTrue((SKILL_DIR / "references" / "rebuttal-playbook.md").exists())
        self.assertTrue((SKILL_DIR / "references" / "venue-policies.md").exists())
        self.assertTrue((SKILL_DIR / "references" / "source-notes.md").exists())
        self.assertTrue((SKILL_DIR / "examples" / "sample-input.md").exists())

    def test_skill_frontmatter_declares_name(self) -> None:
        self.assertTrue((SKILL_DIR / "SKILL.md").exists())
        content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(content.startswith("---\n"))
        self.assertIn("name: super-rebuttal", content)
        self.assertIn("description:", content)

    def test_skill_prefers_review_pdf_extraction_before_reasking(self) -> None:
        content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8").lower()
        self.assertIn("build_input_bundle.py", content)
        self.assertIn("review pdf", content)
        self.assertIn("do not ask the user to paste review text", content)

    def test_skill_mentions_reviewer_cards_and_strategy_memo(self) -> None:
        content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8").lower()
        self.assertIn("reviewer card", content)
        self.assertIn("reviewer stance", content)
        self.assertIn("strategy memo", content)
        self.assertIn("attitude", content)

    def test_openai_metadata_keys_exist(self) -> None:
        self.assertTrue((SKILL_DIR / "agents" / "openai.yaml").exists())
        content = (SKILL_DIR / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertIn("display_name:", content)
        self.assertIn("short_description:", content)
        self.assertIn("default_prompt:", content)


if __name__ == "__main__":
    unittest.main()
