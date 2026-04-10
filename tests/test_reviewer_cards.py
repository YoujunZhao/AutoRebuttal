import importlib.util
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


def load_module(module_name: str, path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {module_name} from {path}")
    spec.loader.exec_module(module)
    return module


class ReviewerCardsTest(unittest.TestCase):
    def test_reviewer_card_builder_exists_and_emits_core_fields(self) -> None:
        module_path = ROOT / "skills" / "super-rebuttal" / "scripts" / "build_reviewer_cards.py"
        self.assertTrue(module_path.exists(), "Expected build_reviewer_cards.py to exist.")
        module = load_module("build_reviewer_cards", module_path)
        cards = module.build_reviewer_cards(
            [
                {
                    "path": "R1.pdf",
                    "text": "Reviewer 1: The novelty is unclear and the experiments are weak.",
                }
            ]
        )
        self.assertEqual(len(cards), 1)
        card = cards[0]
        self.assertIn("reviewer_id", card)
        self.assertIn("sentiment", card)
        self.assertIn("movability", card)
        self.assertIn("primary_concerns", card)


if __name__ == "__main__":
    unittest.main()
