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


class ReviewerOutlineTest(unittest.TestCase):
    def test_outline_builder_splits_weaknesses_questions_and_minor_points(self) -> None:
        module_path = ROOT / "skills" / "auto-rebuttal" / "scripts" / "build_reviewer_outline.py"
        self.assertTrue(module_path.exists(), "Expected build_reviewer_outline.py to exist.")
        module = load_module("build_reviewer_outline", module_path)
        outline = module.build_reviewer_outline(
            reviewer_id="R1",
            review_text=(
                "Weaknesses:\n"
                "1. The novelty is unclear.\n"
                "2. The experiments are weak.\n"
                "Questions:\n"
                "1. Why was this baseline chosen?\n"
                "2. How sensitive is the method to thresholding?\n"
                "Minor Weaknesses:\n"
                "1. Typos in the method section.\n"
                "2. Figure labels are hard to read.\n"
            ),
        )
        self.assertEqual(outline["reviewer_id"], "R1")
        self.assertEqual(len(outline["weaknesses"]), 2)
        self.assertEqual(len(outline["questions"]), 2)
        self.assertEqual(len(outline["minor_points"]), 2)
        self.assertEqual(outline["weaknesses"][0]["label"], "W1")
        self.assertEqual(outline["questions"][0]["label"], "Q1")
        self.assertEqual(outline["minor_points"][0]["label"], "M1")

    def test_outline_builder_handles_openreview_style_headers_without_promoting_strengths(self) -> None:
        module_path = ROOT / "skills" / "auto-rebuttal" / "scripts" / "build_reviewer_outline.py"
        module = load_module("build_reviewer_outline", module_path)
        outline = module.build_reviewer_outline(
            reviewer_id="Qc8x",
            review_text=(
                "Strengths And Weaknesses:\n"
                "Strengths:\n"
                "1. Good empirical gains.\n"
                "2. Clear presentation.\n"
                "Main Weaknesses\n"
                "1. The novelty is limited.\n"
                "2. Prompt robustness is unclear.\n"
                "Key Questions For Authors:\n"
                "1. What prompts were used?\n"
                "2. Can baseline methods also benefit from external knowledge?\n"
                "Minor Weaknesses:\n"
                "1. Clarify Figure 2.\n"
                "2. Fix minor typos.\n"
            ),
        )

        self.assertEqual([item["text"] for item in outline["weaknesses"]], [
            "The novelty is limited.",
            "Prompt robustness is unclear.",
        ])
        self.assertEqual([item["label"] for item in outline["questions"]], ["Q1", "Q2"])
        self.assertEqual(
            [item["text"] for item in outline["questions"]],
            [
                "What prompts were used?",
                "Can baseline methods also benefit from external knowledge?",
            ],
        )
        self.assertEqual([item["label"] for item in outline["minor_points"]], ["M1", "M2"])
        weakness_blob = " ".join(item["text"] for item in outline["weaknesses"])
        self.assertNotIn("Good empirical gains", weakness_blob)

    def test_outline_builder_handles_inline_header_content(self) -> None:
        module_path = ROOT / "skills" / "auto-rebuttal" / "scripts" / "build_reviewer_outline.py"
        module = load_module("build_reviewer_outline", module_path)
        outline = module.build_reviewer_outline(
            reviewer_id="R2",
            review_text=(
                "Weaknesses: The novelty is limited.\n"
                "Key Questions For Authors: What prompts were used?\n"
                "Minor comments: Clarify Figure 2.\n"
            ),
        )

        self.assertEqual(outline["weaknesses"][0]["text"], "The novelty is limited.")
        self.assertEqual(outline["questions"][0]["text"], "What prompts were used?")
        self.assertEqual(outline["minor_points"][0]["text"], "Clarify Figure 2.")

    def test_outline_builder_ignores_openreview_preamble_until_real_sections(self) -> None:
        module_path = ROOT / "skills" / "auto-rebuttal" / "scripts" / "build_reviewer_outline.py"
        module = load_module("build_reviewer_outline", module_path)
        outline = module.build_reviewer_outline(
            reviewer_id="Qc8x",
            review_text=(
                "Official Review of Submission32408 by Reviewer Qc8x\n"
                "Summary:\n"
                "This paper studies generalized open-vocabulary 3D segmentation.\n"
                "Main Weaknesses\n"
                "1. The novelty is limited.\n"
            ),
        )

        self.assertEqual([item["text"] for item in outline["weaknesses"]], ["The novelty is limited."])

    def test_outline_builder_handles_questions_for_authors_header_without_partial_match(self) -> None:
        module_path = ROOT / "skills" / "auto-rebuttal" / "scripts" / "build_reviewer_outline.py"
        module = load_module("build_reviewer_outline", module_path)
        outline = module.build_reviewer_outline(
            reviewer_id="R3",
            review_text="Questions For Authors: What prompts were used?\n",
        )

        self.assertEqual(outline["questions"][0]["text"], "What prompts were used?")

    def test_outline_builder_handles_question_number_and_lettered_item_prefixes(self) -> None:
        module_path = ROOT / "skills" / "auto-rebuttal" / "scripts" / "build_reviewer_outline.py"
        module = load_module("build_reviewer_outline", module_path)
        outline = module.build_reviewer_outline(
            reviewer_id="R4",
            review_text=(
                "Weaknesses:\n"
                "a) The novelty is limited.\n"
                "b) The experiments are weak.\n"
                "Questions:\n"
                "Question 1: Why this baseline?\n"
                "Question 2: How sensitive is the threshold?\n"
            ),
        )

        self.assertEqual(
            [item["text"] for item in outline["weaknesses"]],
            ["The novelty is limited.", "The experiments are weak."],
        )
        self.assertEqual(
            [item["text"] for item in outline["questions"]],
            ["Why this baseline?", "How sensitive is the threshold?"],
        )
