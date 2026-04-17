import importlib.util
import pathlib
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


def load_module(module_name: str, path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {module_name} from {path}")
    spec.loader.exec_module(module)
    return module


class ExperimentRequestBundleTest(unittest.TestCase):
    def test_bundle_keeps_blockers_empty_when_auto_experiment_is_off(self) -> None:
        module = load_module(
            "build_experiment_request_bundle",
            ROOT / "skills" / "auto-rebuttal" / "scripts" / "build_experiment_request_bundle.py",
        )
        bundle = module.build_experiment_request_bundle(
            reviews=[{"text": "Reviewer Qc8x\nQuestions For Authors: please run more experiments."}],
            auto_experiment=False,
            code=None,
        )
        self.assertFalse(bundle["auto_experiment"])
        self.assertFalse(bundle["workspace_ready"])
        self.assertEqual(bundle["blockers"], [])

    def test_bundle_requires_code_path_before_auto_experiment_can_run(self) -> None:
        module = load_module(
            "build_experiment_request_bundle",
            ROOT / "skills" / "auto-rebuttal" / "scripts" / "build_experiment_request_bundle.py",
        )
        bundle = module.build_experiment_request_bundle(
            reviews=[{"text": "Reviewer Qc8x\nQuestions For Authors: please run more experiments."}],
            auto_experiment=True,
            code=None,
        )
        self.assertTrue(bundle["auto_experiment"])
        self.assertIsNone(bundle["code"])
        self.assertFalse(bundle["workspace_ready"])
        self.assertTrue(bundle["blockers"])

    def test_bundle_extracts_baseline_and_ablation_requests(self) -> None:
        module = load_module(
            "build_experiment_request_bundle",
            ROOT / "skills" / "auto-rebuttal" / "scripts" / "build_experiment_request_bundle.py",
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            code_dir = pathlib.Path(tmpdir) / "project"
            code_dir.mkdir()
            (code_dir / "train.py").write_text("print('ok')\n", encoding="utf-8")
            bundle = module.build_experiment_request_bundle(
                reviews=[
                    {
                        "text": (
                            "Reviewer Qc8x\n"
                            "Main Weaknesses: Please compare against a stronger baseline.\n"
                            "Questions For Authors: Can you add an ablation on the filtering threshold?"
                        )
                    }
                ],
                auto_experiment=True,
                code=str(code_dir),
            )
        self.assertTrue(bundle["auto_experiment"])
        self.assertGreaterEqual(len(bundle["requests"]), 2)
        request_types = {request["request_type"] for request in bundle["requests"]}
        self.assertIn("comparison", request_types)
        self.assertIn("ablation", request_types)
        self.assertTrue(bundle["workspace_ready"])

    def test_bundle_reports_blocker_without_runnable_workspace(self) -> None:
        module = load_module(
            "build_experiment_request_bundle",
            ROOT / "skills" / "auto-rebuttal" / "scripts" / "build_experiment_request_bundle.py",
        )
        bundle = module.build_experiment_request_bundle(
            reviews=[{"text": "Reviewer Qc8x\nQuestions For Authors: please run more experiments."}],
            auto_experiment=True,
            code=None,
        )
        self.assertTrue(bundle["auto_experiment"])
        self.assertFalse(bundle["workspace_ready"])
        self.assertTrue(bundle["blockers"])


if __name__ == "__main__":
    unittest.main()
