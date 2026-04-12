import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


class ReadmeTruthTest(unittest.TestCase):
    def test_readme_uses_product_style_sections(self) -> None:
        content = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("## How It Works", content)
        self.assertIn("## Installation", content)
        self.assertIn("## The Basic Workflow", content)
        self.assertIn("## What's Inside", content)

    def test_readme_mentions_codex_install_doc(self) -> None:
        content = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn(".codex/INSTALL.md", content)
        self.assertIn("README.zh-CN.md", content)

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
        self.assertIn("python scripts/superrebuttal_manager.py codex update", english)
        self.assertIn("python scripts/superrebuttal_manager.py codex remove", english)
        self.assertIn("python scripts/superrebuttal_manager.py codex update", chinese)
        self.assertIn("python scripts/superrebuttal_manager.py codex remove", chinese)

    def test_readmes_document_claude_update_and_remove_cli_commands(self) -> None:
        english = (ROOT / "README.md").read_text(encoding="utf-8")
        chinese = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
        self.assertIn("python scripts/superrebuttal_manager.py claude update", english)
        self.assertIn("python scripts/superrebuttal_manager.py claude remove", english)
        self.assertIn("python scripts/superrebuttal_manager.py claude update", chinese)
        self.assertIn("python scripts/superrebuttal_manager.py claude remove", chinese)

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
        self.assertIn("CVPR", english)
        self.assertIn("ICCV", english)
        self.assertIn("ECCV", english)
        self.assertIn("W1", english)
        self.assertIn("W2", english)
        self.assertIn("AAAI", chinese)
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
        self.assertIn("Use the `rebuttal` command", content)
        self.assertIn("Use the `super-rebuttal` skill", content)
        self.assertIn("/plugin marketplace add", content)
        self.assertIn("/plugin install", content)
        self.assertIn("What is the difference between `rebuttal` and `super-rebuttal`?", content)

    def test_readmes_mention_rebuttal_revies_polish_mode(self) -> None:
        english = (ROOT / "README.md").read_text(encoding="utf-8")
        chinese = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
        self.assertIn("/rebuttal_revies", english)
        self.assertIn("existing rebuttal", english)
        self.assertIn("/rebuttal_revies", chinese)

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
