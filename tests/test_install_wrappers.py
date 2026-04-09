import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


class ReadmeTruthTest(unittest.TestCase):
    def test_readme_mentions_per_reviewer_mode(self) -> None:
        content = (ROOT / "README.md").read_text(encoding="utf-8").lower()
        self.assertIn("per-reviewer mode", content)

    def test_readme_mentions_shared_global_mode(self) -> None:
        content = (ROOT / "README.md").read_text(encoding="utf-8").lower()
        self.assertIn("shared-global mode", content)

    def test_readme_does_not_mention_openclaw(self) -> None:
        content = (ROOT / "README.md").read_text(encoding="utf-8").lower()
        self.assertNotIn("openclaw", content)


if __name__ == "__main__":
    unittest.main()
