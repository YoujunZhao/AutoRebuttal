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
    def test_auto_experiment_defaults_to_false(self) -> None:
        module = load_module(
            "response_modes",
            ROOT / "skills" / "auto-rebuttal" / "scripts" / "response_modes.py",
        )
        self.assertFalse(module.resolve_auto_experiment(autoexperiment=None))

    def test_auto_experiment_accepts_true(self) -> None:
        module = load_module(
            "response_modes",
            ROOT / "skills" / "auto-rebuttal" / "scripts" / "response_modes.py",
        )
        self.assertTrue(module.resolve_auto_experiment(autoexperiment="true"))

    def test_auto_experiment_rejects_unknown_value(self) -> None:
        module = load_module(
            "response_modes",
            ROOT / "skills" / "auto-rebuttal" / "scripts" / "response_modes.py",
        )
        with self.assertRaises(ValueError):
            module.resolve_auto_experiment(autoexperiment="maybe")

    def test_output_format_defaults_to_text(self) -> None:
        module = load_module(
            "response_modes",
            ROOT / "skills" / "auto-rebuttal" / "scripts" / "response_modes.py",
        )
        output_format = module.resolve_output_format(output=None)
        self.assertEqual(output_format, "text")

    def test_output_format_accepts_markdown(self) -> None:
        module = load_module(
            "response_modes",
            ROOT / "skills" / "auto-rebuttal" / "scripts" / "response_modes.py",
        )
        output_format = module.resolve_output_format(output="md")
        self.assertEqual(output_format, "md")

    def test_output_format_rejects_unknown_value(self) -> None:
        module = load_module(
            "response_modes",
            ROOT / "skills" / "auto-rebuttal" / "scripts" / "response_modes.py",
        )
        with self.assertRaises(ValueError):
            module.resolve_output_format(output="html")

    def test_explicit_per_reviewer_budget_resolves_per_reviewer(self) -> None:
        module = load_module(
            "response_modes",
            ROOT / "skills" / "auto-rebuttal" / "scripts" / "response_modes.py",
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
            ROOT / "skills" / "auto-rebuttal" / "scripts" / "response_modes.py",
        )
        mode = module.resolve_response_mode(
            venue=None,
            per_reviewer_limit=None,
            total_limit=6000,
            shared_response=True,
        )
        self.assertEqual(mode["mode"], "shared-global")

    def test_existing_rebuttal_text_resolves_revise_existing_mode(self) -> None:
        module = load_module(
            "response_modes",
            ROOT / "skills" / "auto-rebuttal" / "scripts" / "response_modes.py",
        )
        mode = module.resolve_workflow_mode(
            existing_rebuttal_text="Reviewer Qc8x\nW1. Novelty is limited.",
            revise_command=True,
        )
        self.assertEqual(mode["workflow"], "revise-existing")


if __name__ == "__main__":
    unittest.main()
