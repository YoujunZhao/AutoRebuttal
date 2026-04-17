import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


class ReadmeTruthTest(unittest.TestCase):
    def test_readmes_use_autorebuttal_product_name(self) -> None:
        english = (ROOT / "README.md").read_text(encoding="utf-8")
        chinese = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
        self.assertIn("# AutoRebuttal", english)
        self.assertIn("AutoRebuttal", chinese)
        self.assertNotIn("SuperRebuttal", english)

    def test_readme_uses_product_style_sections(self) -> None:
        content = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("## AutoRebuttal Outputs", content)
        self.assertIn("## Quick Install", content)
        self.assertIn("## How To Use It", content)
        self.assertIn("## Parameters", content)
        self.assertLess(content.index("## AutoRebuttal Outputs"), content.index("## Quick Install"))
        self.assertLess(content.index("## Quick Install"), content.index("## How To Use It"))
        self.assertLess(content.index("## How To Use It"), content.index("## Parameters"))

    def test_readme_includes_workflow_diagram(self) -> None:
        content = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("```mermaid", content)
        self.assertIn("Build Draft Bundle", content)

    def test_readme_includes_parameter_table(self) -> None:
        content = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("| Parameter |", content)
        self.assertIn("| `rebuttal` / `rebuttal_revise` |", content)
        self.assertIn("| `venue` |", content)
        self.assertIn("| `per_reviewer` |", content)
        self.assertIn("| `output` |", content)

    def test_readmes_document_latex_paper_contract(self) -> None:
        english = (ROOT / "README.md").read_text(encoding="utf-8")
        chinese = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
        self.assertIn("LaTeX paper", english)
        self.assertIn("revised_latex_paper", english)
        self.assertIn("build_latex_output_package.py", english)
        self.assertIn("LaTeX", chinese)
        self.assertIn("revised_latex_paper", chinese)

    def test_readme_mentions_codex_install_doc(self) -> None:
        content = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn(".codex/INSTALL.md", content)
        self.assertIn("README.zh-CN.md", content)
        self.assertNotIn("scripts/superrebuttal_manager.py", content)

    def test_readme_includes_quick_install_for_codex(self) -> None:
        content = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("Quick Install", content)
        self.assertIn("Fetch and follow instructions", content)
        self.assertIn(".codex/INSTALL.md", content)

    def test_codex_install_doc_prefers_clone_and_skill_junction(self) -> None:
        content = (ROOT / ".codex" / "INSTALL.md").read_text(encoding="utf-8")
        self.assertIn("git clone", content)
        self.assertIn("~/.agents/skills/auto-rebuttal", content)
        self.assertTrue("mklink" in content or "ln -s" in content)

    def test_codex_install_doc_mentions_manager_as_optional(self) -> None:
        content = (ROOT / ".codex" / "INSTALL.md").read_text(encoding="utf-8").lower()
        self.assertIn("optional", content)
        self.assertIn("autorebuttal_manager.py", content)

    def test_readme_includes_quick_install_line_for_codex(self) -> None:
        content = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("Quick Install", content)
        self.assertIn("Fetch and follow instructions", content)
        self.assertIn(".codex/INSTALL.md", content)

    def test_codex_install_doc_prefers_clone_and_skill_junction(self) -> None:
        content = (ROOT / ".codex" / "INSTALL.md").read_text(encoding="utf-8")
        self.assertIn("git clone", content)
        self.assertIn("~/.agents/skills/auto-rebuttal", content)
        self.assertTrue("mklink" in content or "ln -s" in content)

    def test_codex_install_doc_mentions_manager_as_optional_path(self) -> None:
        content = (ROOT / ".codex" / "INSTALL.md").read_text(encoding="utf-8").lower()
        self.assertIn("optional", content)
        self.assertIn("autorebuttal_manager.py", content)

    def test_readme_mentions_per_reviewer_mode(self) -> None:
        content = (ROOT / "README.md").read_text(encoding="utf-8").lower()
        self.assertIn("per-reviewer mode", content)

    def test_readme_mentions_shared_global_mode(self) -> None:
        content = (ROOT / "README.md").read_text(encoding="utf-8").lower()
        self.assertIn("shared-global mode", content)

    def test_readmes_mention_review_pdf_support(self) -> None:
        english = (ROOT / "README.md").read_text(encoding="utf-8").lower()
        chinese = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8").lower()
        self.assertIn("review pdf", english)
        self.assertIn("review pdf", chinese)

    def test_readmes_document_codex_update_and_remove_cli_commands(self) -> None:
        english = (ROOT / "README.md").read_text(encoding="utf-8")
        chinese = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
        self.assertIn("python scripts/autorebuttal_manager.py codex update", english)
        self.assertIn("python scripts/autorebuttal_manager.py codex remove", english)
        self.assertIn("python scripts/autorebuttal_manager.py codex update", chinese)
        self.assertIn("python scripts/autorebuttal_manager.py codex remove", chinese)

    def test_readmes_document_claude_update_and_remove_cli_commands(self) -> None:
        english = (ROOT / "README.md").read_text(encoding="utf-8")
        chinese = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
        self.assertIn("python scripts/autorebuttal_manager.py claude update", english)
        self.assertIn("python scripts/autorebuttal_manager.py claude remove", english)
        self.assertIn("python scripts/autorebuttal_manager.py claude update", chinese)
        self.assertIn("python scripts/autorebuttal_manager.py claude remove", chinese)

    def test_readmes_mention_reviewer_stance_and_global_strategy(self) -> None:
        english = (ROOT / "README.md").read_text(encoding="utf-8").lower()
        chinese = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8").lower()
        self.assertIn("reviewer stance", english)
        self.assertIn("global strategy", english)
        self.assertIn("reviewer", chinese)
        self.assertIn("strategy", chinese)

    def test_readmes_mention_venue_aware_defaults_and_w_format(self) -> None:
        english = (ROOT / "README.md").read_text(encoding="utf-8")
        chinese = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
        self.assertIn("AAAI", english)
        self.assertIn("IEEE", english)
        self.assertIn("CVPR", english)
        self.assertIn("ICCV", english)
        self.assertIn("ECCV", english)
        self.assertIn("W1", english)
        self.assertIn("W2", english)
        self.assertIn("AAAI", chinese)
        self.assertIn("IEEE", chinese)
        self.assertIn("CVPR", chinese)
        self.assertIn("W1", chinese)

    def test_readmes_mention_q_and_minor_point_handling(self) -> None:
        english = (ROOT / "README.md").read_text(encoding="utf-8")
        chinese = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
        self.assertIn("Q1", english)
        self.assertIn("minor", english.lower())
        self.assertIn("Q1", chinese)
        self.assertIn("minor", chinese.lower())

    def test_readmes_mention_experiment_placeholder_tables(self) -> None:
        english = (ROOT / "README.md").read_text(encoding="utf-8").lower()
        chinese = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8").lower()
        self.assertIn("experiment placeholder", english)
        self.assertIn("xx", english)
        self.assertIn("xx", chinese)

    def test_readme_includes_usage_and_invocation_examples(self) -> None:
        content = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("## How To Use It", content)
        self.assertIn("/rebuttal venue=ICML per_reviewer=5000", content)
        self.assertIn("/rebuttal_revise venue=ICML per_reviewer=5000", content)
        self.assertIn("output=md", content)
        self.assertIn("paper PDF", content)
        self.assertIn("review PDF", content)
        self.assertIn("LaTeX paper", content)
        self.assertIn("review text", content)
        self.assertIn("/plugin marketplace add", content)
        self.assertIn("/plugin install", content)

    def test_readmes_mention_rebuttal_revise_polish_mode(self) -> None:
        english = (ROOT / "README.md").read_text(encoding="utf-8")
        chinese = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
        self.assertIn("/rebuttal_revise", english)
        self.assertIn("existing rebuttal", english)
        self.assertIn("/rebuttal_revise", chinese)
        self.assertNotIn("/rebuttal_revies", english)

    def test_readmes_mention_line_breaks_before_w_q_m_labels(self) -> None:
        english = (ROOT / "README.md").read_text(encoding="utf-8").lower()
        chinese = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8").lower()
        self.assertIn("own line", english)
        self.assertIn("w1", english)
        self.assertIn("q1", english)
        self.assertIn("m1", english)
        self.assertIn("w1", chinese)
        self.assertIn("q1", chinese)

    def test_readme_does_not_mention_openclaw(self) -> None:
        content = (ROOT / "README.md").read_text(encoding="utf-8").lower()
        self.assertNotIn("- openclaw\n", content)

    def test_english_readme_no_longer_embeds_chinese_section(self) -> None:
        content = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertNotIn("## 中文", content)
        self.assertNotIn('<a id="chinese"></a>', content)

    def test_chinese_readme_exists(self) -> None:
        chinese_readme = ROOT / "README.zh-CN.md"
        self.assertTrue(chinese_readme.exists())


if __name__ == "__main__":
    unittest.main()
