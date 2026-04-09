import contextlib
import importlib.util
import io
import json
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


class ValidateBudgetTest(unittest.TestCase):
    def test_measure_budget_counts_characters(self) -> None:
        module = load_module(
            "validate_budget",
            ROOT / "skill" / "super-rebuttal" / "scripts" / "validate_budget.py",
        )

        result = module.measure_budget("Reviewer 1: Thanks!", limit=30, mode="chars")

        self.assertEqual(result["used"], 19)
        self.assertEqual(result["remaining"], 11)
        self.assertFalse(result["overflow"])
        self.assertEqual(result["mode"], "chars")

    def test_main_prints_budget_json(self) -> None:
        module = load_module(
            "validate_budget_cli",
            ROOT / "skill" / "super-rebuttal" / "scripts" / "validate_budget.py",
        )
        stdout = io.StringIO()

        with contextlib.redirect_stdout(stdout):
            exit_code = module.main(
                ["--text", "Reviewer 1: Thanks!", "--limit", "30", "--mode", "chars"]
            )

        payload = json.loads(stdout.getvalue())
        self.assertEqual(exit_code, 0)
        self.assertEqual(payload["used"], 19)
        self.assertEqual(payload["remaining"], 11)
        self.assertFalse(payload["overflow"])


if __name__ == "__main__":
    unittest.main()
