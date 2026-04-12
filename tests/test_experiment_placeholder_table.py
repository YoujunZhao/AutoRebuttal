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


class ExperimentPlaceholderTableTest(unittest.TestCase):
    def test_placeholder_table_contains_xx_slots(self) -> None:
        module_path = ROOT / "skills" / "auto-rebuttal" / "scripts" / "build_experiment_placeholder_table.py"
        self.assertTrue(module_path.exists(), "Expected build_experiment_placeholder_table.py to exist.")
        module = load_module("build_experiment_placeholder_table", module_path)
        table = module.build_experiment_placeholder_table(
            title="Additional ablation",
            rows=["Setting A", "Setting B"],
        )
        self.assertIn("Setting A", table)
        self.assertIn("Setting B", table)
        self.assertIn("XX", table)
        self.assertIn("metric", table.lower())


if __name__ == "__main__":
    unittest.main()
