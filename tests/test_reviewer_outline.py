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
        module_path = ROOT / "skills" / "super-rebuttal" / "scripts" / "build_reviewer_outline.py"
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
