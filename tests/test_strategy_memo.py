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


class StrategyMemoTest(unittest.TestCase):
    def test_strategy_memo_builder_groups_shared_issues(self) -> None:
        module_path = ROOT / "skills" / "super-rebuttal" / "scripts" / "build_strategy_memo.py"
        self.assertTrue(module_path.exists(), "Expected build_strategy_memo.py to exist.")
        module = load_module("build_strategy_memo", module_path)
        memo = module.build_strategy_memo(
            reviewer_cards=[
                {
                    "reviewer_id": "R1",
                    "sentiment": "negative",
                    "movability": "swing",
                    "attitude": "skeptical",
                    "primary_concerns": ["novelty", "empirical_support"],
                },
                {
                    "reviewer_id": "R2",
                    "sentiment": "mixed",
                    "movability": "swing",
                    "attitude": "mixed",
                    "primary_concerns": ["empirical_support", "clarity"],
                },
            ]
        )
        self.assertIn("shared_issues", memo)
        self.assertIn("empirical_support", memo["shared_issues"])
        self.assertIn("global_strategy", memo)
        self.assertTrue(memo["priority_reviewers"])
