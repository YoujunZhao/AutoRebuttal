import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


class PluginSurfaceTest(unittest.TestCase):
    def test_codex_install_guide_exists(self) -> None:
        self.assertTrue((ROOT / ".codex" / "INSTALL.md").exists())

    def test_claude_plugin_manifest_exists(self) -> None:
        self.assertTrue((ROOT / ".claude-plugin" / "plugin.json").exists())

    def test_claude_marketplace_manifest_exists(self) -> None:
        self.assertTrue((ROOT / ".claude-plugin" / "marketplace.json").exists())

    def test_rebuttal_command_exists(self) -> None:
        self.assertTrue((ROOT / "commands" / "rebuttal.md").exists())

    def test_rebuttal_command_mentions_review_pdf_intake(self) -> None:
        content = (ROOT / "commands" / "rebuttal.md").read_text(encoding="utf-8").lower()
        self.assertIn("review pdf", content)
        self.assertIn("do not ask the user to paste review text", content)

    def test_rebuttal_command_mentions_reviewer_cards_and_strategy_memo(self) -> None:
        content = (ROOT / "commands" / "rebuttal.md").read_text(encoding="utf-8").lower()
        self.assertIn("reviewer cards", content)
        self.assertIn("strategy memo", content)
        self.assertIn("reviewer stance", content)


if __name__ == "__main__":
    unittest.main()
