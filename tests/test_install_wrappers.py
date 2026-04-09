import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


class InstallWrapperTest(unittest.TestCase):
    def test_codex_wrapper_targets_codex_skill_directory(self) -> None:
        content = (ROOT / "install" / "install-codex.ps1").read_text(encoding="utf-8")
        self.assertIn(".codex/skills/super-rebuttal", content)
        self.assertIn("install_skill.py", content)

    def test_claude_wrapper_targets_claude_skill_directory(self) -> None:
        content = (ROOT / "install" / "install-claude-code.sh").read_text(
            encoding="utf-8"
        )
        self.assertIn(".claude/skills/super-rebuttal", content)
        self.assertIn("install_skill.py", content)

    def test_openclaw_wrapper_targets_openclaw_skill_directory(self) -> None:
        content = (ROOT / "install" / "install-openclaw.sh").read_text(
            encoding="utf-8"
        )
        self.assertIn(".openclaw/skills/super-rebuttal", content)
        self.assertIn("install_skill.py", content)


if __name__ == "__main__":
    unittest.main()
