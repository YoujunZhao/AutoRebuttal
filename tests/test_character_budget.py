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


class CharacterBudgetTest(unittest.TestCase):
    def test_budget_allocator_handles_per_reviewer_limit(self) -> None:
        module_path = ROOT / "skills" / "super-rebuttal" / "scripts" / "allocate_rebuttal_budget.py"
        self.assertTrue(module_path.exists(), "Expected allocate_rebuttal_budget.py to exist.")
        module = load_module("allocate_rebuttal_budget", module_path)
        allocation = module.allocate_budget(
            mode="per-reviewer",
            reviewer_count=3,
            per_reviewer_limit=5000,
            total_limit=None,
        )
        self.assertEqual(allocation["mode"], "per-reviewer")
        self.assertEqual(allocation["per_reviewer_limit"], 5000)
        self.assertIn("section_plan", allocation)
        self.assertLessEqual(allocation["section_plan"]["opener"], 1000)

    def test_budget_allocator_handles_shared_global_limit(self) -> None:
        module_path = ROOT / "skills" / "super-rebuttal" / "scripts" / "allocate_rebuttal_budget.py"
        module = load_module("allocate_rebuttal_budget", module_path)
        allocation = module.allocate_budget(
            mode="shared-global",
            reviewer_count=3,
            per_reviewer_limit=None,
            total_limit=6000,
        )
        self.assertEqual(allocation["mode"], "shared-global")
        self.assertEqual(allocation["total_limit"], 6000)
        self.assertEqual(sum(allocation["section_plan"].values()), 6000)
        self.assertIn("reviewer_sections", allocation)
        self.assertEqual(len(allocation["reviewer_sections"]), 3)
