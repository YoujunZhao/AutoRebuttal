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


if __name__ == "__main__":
    unittest.main()
