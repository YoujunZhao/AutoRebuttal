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


class ResponseModesSurfaceTest(unittest.TestCase):
    def test_explicit_per_reviewer_budget_resolves_per_reviewer(self) -> None:
        module = load_module(
            "response_modes",
            ROOT / "skills" / "super-rebuttal" / "scripts" / "response_modes.py",
        )
        mode = module.resolve_response_mode(
            venue=None,
            per_reviewer_limit=5000,
            total_limit=None,
            shared_response=False,
        )
        self.assertEqual(mode["mode"], "per-reviewer")

    def test_shared_budget_resolves_shared_global(self) -> None:
        module = load_module(
            "response_modes",
            ROOT / "skills" / "super-rebuttal" / "scripts" / "response_modes.py",
        )
        mode = module.resolve_response_mode(
            venue=None,
            per_reviewer_limit=None,
            total_limit=6000,
            shared_response=True,
        )
        self.assertEqual(mode["mode"], "shared-global")


if __name__ == "__main__":
    unittest.main()
