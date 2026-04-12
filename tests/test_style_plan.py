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


class StylePlanTest(unittest.TestCase):
    def test_style_plan_builder_exists_and_prioritizes_shared_issues(self) -> None:
        module_path = ROOT / "skills" / "auto-rebuttal" / "scripts" / "build_style_plan.py"
        self.assertTrue(module_path.exists(), "Expected build_style_plan.py to exist.")
        module = load_module("build_style_plan", module_path)
        plan = module.build_style_plan(
            phase="initial",
            mode="per-reviewer",
            strategy_memo={
                "shared_issues": ["empirical_support"],
                "priority_reviewers": ["R1"],
                "global_strategy": ["Lead with shared issues."],
            },
        )
        self.assertEqual(plan["phase"], "initial")
        self.assertIn("lead-with-shared-issues", plan["emphasis"])
        self.assertIn("prioritize-swing-reviewers", plan["emphasis"])


if __name__ == "__main__":
    unittest.main()
