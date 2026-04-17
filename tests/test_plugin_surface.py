import pathlib
import unittest
import json


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

    def test_rebuttal_revise_command_exists(self) -> None:
        self.assertTrue((ROOT / "commands" / "rebuttal_revise.md").exists())

    def test_experiment_bridge_command_exists(self) -> None:
        self.assertTrue((ROOT / "commands" / "experiment-bridge.md").exists())

    def test_codex_install_guide_uses_autorebuttal_manager_and_path(self) -> None:
        content = (ROOT / ".codex" / "INSTALL.md").read_text(encoding="utf-8")
        self.assertIn("python scripts/autorebuttal_manager.py codex install", content)
        self.assertIn("python scripts/autorebuttal_manager.py codex update", content)
        self.assertIn("python scripts/autorebuttal_manager.py codex remove", content)
        self.assertIn("~/.agents/skills/auto-rebuttal", content)

    def test_plugin_manifest_uses_auto_rebuttal_name(self) -> None:
        content = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(content["name"], "auto-rebuttal")
        self.assertIn("AutoRebuttal", content["description"])
        self.assertIn("AutoRebuttal", content["homepage"])
        self.assertIn("AutoRebuttal", content["repository"])

    def test_marketplace_manifest_uses_auto_rebuttal_name(self) -> None:
        content = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
        self.assertEqual(content["name"], "auto-rebuttal-dev")
        self.assertIn("AutoRebuttal", content["description"])
        self.assertEqual(content["plugins"][0]["name"], "auto-rebuttal")
        self.assertIn("AutoRebuttal", content["plugins"][0]["description"])

    def test_rebuttal_command_mentions_review_pdf_intake(self) -> None:
        content = (ROOT / "commands" / "rebuttal.md").read_text(encoding="utf-8").lower()
        self.assertIn("review pdf", content)
        self.assertIn("do not ask the user to paste review text", content)

    def test_rebuttal_command_mentions_reviewer_cards_and_strategy_memo(self) -> None:
        content = (ROOT / "commands" / "rebuttal.md").read_text(encoding="utf-8").lower()
        self.assertIn("reviewer cards", content)
        self.assertIn("strategy memo", content)
        self.assertIn("reviewer stance", content)

    def test_rebuttal_command_mentions_questions_and_minor_points(self) -> None:
        content = (ROOT / "commands" / "rebuttal.md").read_text(encoding="utf-8")
        self.assertIn("Q1", content)
        self.assertIn("minor", content.lower())

    def test_rebuttal_command_mentions_image_review_pdf_fallback_and_outline_step(self) -> None:
        content = (ROOT / "commands" / "rebuttal.md").read_text(encoding="utf-8").lower()
        self.assertIn("rendered page images", content)
        self.assertIn("build a reviewer outline", content)

    def test_rebuttal_command_mentions_latex_paper_and_dual_outputs(self) -> None:
        content = (ROOT / "commands" / "rebuttal.md").read_text(encoding="utf-8")
        self.assertIn("LaTeX", content)
        self.assertIn(".tex", content)
        self.assertIn("revised_latex_paper", content)


    def test_command_surfaces_document_output_parameter(self) -> None:
        draft = (ROOT / "commands" / "rebuttal.md").read_text(encoding="utf-8")
        revise = (ROOT / "commands" / "rebuttal_revise.md").read_text(encoding="utf-8")
        self.assertIn("output=text", draft)
        self.assertIn("output=md", draft)
        self.assertIn("output=text", revise)
        self.assertIn("output=md", revise)

    def test_command_surfaces_document_auto_experiment_parameter(self) -> None:
        draft = (ROOT / "commands" / "rebuttal.md").read_text(encoding="utf-8")
        revise = (ROOT / "commands" / "rebuttal_revise.md").read_text(encoding="utf-8")
        bridge = (ROOT / "commands" / "experiment-bridge.md").read_text(encoding="utf-8")
        self.assertIn("autoexperiment=true", draft)
        self.assertIn("autoexperiment=true", revise)
        self.assertIn("/experiment-bridge", draft)
        self.assertIn("/experiment-bridge", revise)
        self.assertIn("supplementary experiments", bridge.lower())
        self.assertIn("reviewers ask for new evidence", bridge.lower())

    def test_rebuttal_revise_command_mentions_polishing_existing_rebuttal(self) -> None:
        content = (ROOT / "commands" / "rebuttal_revise.md").read_text(encoding="utf-8").lower()
        self.assertIn("existing rebuttal", content)
        self.assertIn("revise", content)
        self.assertIn("do not invent", content)

    def test_rebuttal_revise_command_mentions_optional_latex_paper(self) -> None:
        content = (ROOT / "commands" / "rebuttal_revise.md").read_text(encoding="utf-8")
        self.assertIn("LaTeX", content)
        self.assertIn(".tex", content)
        self.assertIn("revised_latex_paper", content)

    def test_skill_and_reference_document_latex_dual_output_contract(self) -> None:
        skill = (ROOT / "skills" / "auto-rebuttal" / "SKILL.md").read_text(encoding="utf-8")
        reference = (
            ROOT / "skills" / "auto-rebuttal" / "references" / "input-contract.md"
        ).read_text(encoding="utf-8")
        self.assertIn("revised_latex_paper", skill)
        self.assertIn("entrypoint", skill)
        self.assertIn("revised_latex_paper", reference)
        self.assertIn("entrypoint", reference)


if __name__ == "__main__":
    unittest.main()
