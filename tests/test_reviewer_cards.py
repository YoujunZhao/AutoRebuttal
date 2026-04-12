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
        module_path = ROOT / "skills" / "auto-rebuttal" / "scripts" / "build_reviewer_cards.py"
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

    def test_reviewer_card_classifies_novelty_and_empirical_weakness(self) -> None:
        module_path = ROOT / "skills" / "auto-rebuttal" / "scripts" / "build_reviewer_cards.py"
        module = load_module("build_reviewer_cards", module_path)
        cards = module.build_reviewer_cards(
            [
                {
                    "path": "R1.pdf",
                    "text": "Reviewer 1: The novelty is unclear and the experiments are weak.",
                }
            ]
        )
        card = cards[0]
        self.assertIn("novelty", card["primary_concerns"])
        self.assertIn("empirical_support", card["primary_concerns"])
        self.assertEqual(card["movability"], "swing")

    def test_reviewer_card_classifies_scope_and_evidence_shortfall(self) -> None:
        module_path = ROOT / "skills" / "auto-rebuttal" / "scripts" / "build_reviewer_cards.py"
        module = load_module("build_reviewer_cards", module_path)
        cards = module.build_reviewer_cards(
            [
                {
                    "path": "R2.pdf",
                    "text": "Reviewer 2: The scope is limited and the evidence is insufficient.",
                }
            ]
        )
        card = cards[0]
        self.assertIn("scope_mismatch", card["primary_concerns"])
        self.assertIn("empirical_support", card["primary_concerns"])
        self.assertEqual(card["movability"], "swing")

    def test_reviewer_cards_preserve_outline_questions_and_minor_points(self) -> None:
        module_path = ROOT / "skills" / "auto-rebuttal" / "scripts" / "build_reviewer_cards.py"
        module = load_module("build_reviewer_cards", module_path)
        cards = module.build_reviewer_cards(
            [
                {
                    "path": "Qc8x.pdf",
                    "text": (
                        "Official Review of Submission32408 by Reviewer Qc8x\n"
                        "Strengths And Weaknesses:\n"
                        "Strengths:\n"
                        "1. Good gains.\n"
                        "Main Weaknesses\n"
                        "1. The novelty is limited.\n"
                        "Key Questions For Authors:\n"
                        "1. What prompts were used?\n"
                        "Minor Weaknesses:\n"
                        "1. Clarify Figure 2.\n"
                    ),
                }
            ]
        )
        card = cards[0]
        self.assertIn("outline", card)
        self.assertEqual(card["outline"]["questions"][0]["label"], "Q1")
        self.assertEqual(card["question_count"], 1)
        self.assertEqual(card["minor_point_count"], 1)

    def test_reviewer_cards_reject_image_fallback_without_text_or_outline(self) -> None:
        module_path = ROOT / "skills" / "auto-rebuttal" / "scripts" / "build_reviewer_cards.py"
        module = load_module("build_reviewer_cards", module_path)
        with self.assertRaises(ValueError):
            module.build_reviewer_cards(
                [
                    {
                        "path": "review.pdf",
                        "text": None,
                        "page_images": ["review_p1.png"],
                        "extraction_mode": "image_fallback",
                    }
                ]
            )


if __name__ == "__main__":
    unittest.main()
