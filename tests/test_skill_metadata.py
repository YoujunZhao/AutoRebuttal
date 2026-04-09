import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skill" / "super-rebuttal"


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
        content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(content.startswith("---\n"))
        self.assertIn("name: super-rebuttal", content)
        self.assertIn("description:", content)

    def test_openai_metadata_keys_exist(self) -> None:
        content = (SKILL_DIR / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertIn("display_name:", content)
        self.assertIn("short_description:", content)
        self.assertIn("default_prompt:", content)


if __name__ == "__main__":
    unittest.main()
