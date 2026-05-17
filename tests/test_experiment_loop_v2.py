import importlib.util
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "skills" / "auto-rebuttal"


def load_module(module_name: str, path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {module_name} from {path}")
    spec.loader.exec_module(module)
    return module


class ExperimentLoopV2SurfaceTest(unittest.TestCase):
    def test_v2_experiment_surface_exists(self) -> None:
        expected_files = [
            SKILL_ROOT / "schemas" / "experiment_request.schema.json",
            SKILL_ROOT / "schemas" / "experiment_packet.schema.json",
            SKILL_ROOT / "schemas" / "evidence_ledger.schema.json",
            SKILL_ROOT / "scripts" / "build_experiment_plan.py",
            SKILL_ROOT / "scripts" / "validate_experiment_plan.py",
            SKILL_ROOT / "scripts" / "run_experiment_packet.py",
            SKILL_ROOT / "scripts" / "parse_experiment_result.py",
            SKILL_ROOT / "scripts" / "update_evidence_ledger.py",
            SKILL_ROOT / "references" / "experiment-loop.md",
            SKILL_ROOT / "references" / "evidence-ledger.md",
            SKILL_ROOT / "examples" / "experiment_request.example.json",
            SKILL_ROOT / "examples" / "experiment_packet.example.json",
        ]

        for path in expected_files:
            with self.subTest(path=path):
                self.assertTrue(path.exists(), f"Expected v2 experiment asset to exist: {path}")

        adapters_dir = SKILL_ROOT / "adapters"
        self.assertTrue(adapters_dir.exists(), "Expected skills/auto-rebuttal/adapters to exist.")
        self.assertTrue(
            any(adapters_dir.glob("*.py")),
            "Expected at least one Python adapter in skills/auto-rebuttal/adapters.",
        )

    def test_examples_match_top_level_schema_requirements(self) -> None:
        request_schema = json.loads(
            (SKILL_ROOT / "schemas" / "experiment_request.schema.json").read_text(encoding="utf-8")
        )
        packet_schema = json.loads(
            (SKILL_ROOT / "schemas" / "experiment_packet.schema.json").read_text(encoding="utf-8")
        )
        ledger_schema = json.loads(
            (SKILL_ROOT / "schemas" / "evidence_ledger.schema.json").read_text(encoding="utf-8")
        )
        request_example = json.loads(
            (SKILL_ROOT / "examples" / "experiment_request.example.json").read_text(encoding="utf-8")
        )
        packet_example = json.loads(
            (SKILL_ROOT / "examples" / "experiment_packet.example.json").read_text(encoding="utf-8")
        )

        for name, schema in {
            "request": request_schema,
            "packet": packet_schema,
            "ledger": ledger_schema,
        }.items():
            with self.subTest(schema=name):
                self.assertEqual(schema.get("type"), "object")
                self.assertIn("$schema", schema)
                self.assertIsInstance(schema.get("properties"), dict)

        self.assertIsInstance(request_example, dict)
        self.assertIsInstance(packet_example, dict)

        for required_key in request_schema.get("required", []):
            with self.subTest(example="request", required_key=required_key):
                self.assertIn(required_key, request_example)

        for required_key in packet_schema.get("required", []):
            with self.subTest(example="packet", required_key=required_key):
                self.assertIn(required_key, packet_example)

    def test_build_experiment_plan_cli_accepts_single_request_example(self) -> None:
        script_path = SKILL_ROOT / "scripts" / "build_experiment_plan.py"
        example_path = SKILL_ROOT / "examples" / "experiment_request.example.json"
        completed = subprocess.run(
            [
                sys.executable,
                str(script_path),
                "--requests",
                str(example_path),
                "--command",
                "python run_eval.py",
                "--working-dir",
                "./project",
            ],
            capture_output=True,
            cwd=ROOT,
            text=True,
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertEqual(payload["schema_version"], "0.1")
        self.assertEqual(len(payload["packets"]), 1)
        self.assertEqual(payload["packets"][0]["request_id"], "R2-W3")
        self.assertEqual(payload["packets"][0]["command"], "python run_eval.py")

    def test_new_experiment_scripts_expose_help(self) -> None:
        expectations = {
            SKILL_ROOT / "scripts" / "build_experiment_plan.py": "experiment",
            SKILL_ROOT / "scripts" / "validate_experiment_plan.py": "validate",
            SKILL_ROOT / "scripts" / "run_experiment_packet.py": "experiment",
            SKILL_ROOT / "scripts" / "parse_experiment_result.py": "parse",
            SKILL_ROOT / "scripts" / "update_evidence_ledger.py": "ledger",
        }

        for script_path, token in expectations.items():
            with self.subTest(script=script_path.name):
                completed = subprocess.run(
                    [sys.executable, str(script_path), "--help"],
                    capture_output=True,
                    cwd=ROOT,
                    text=True,
                )
                output = (completed.stdout + completed.stderr).lower()
                self.assertEqual(completed.returncode, 0, output)
                self.assertIn(token, output)

    def test_run_experiment_packet_smoke_updates_results_and_ledger(self) -> None:
        module = load_module(
            "run_experiment_packet",
            SKILL_ROOT / "scripts" / "run_experiment_packet.py",
        )
        packet = json.loads(
            (SKILL_ROOT / "examples" / "experiment_packet.example.json").read_text(encoding="utf-8")
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = pathlib.Path(tmpdir)
            packet["working_dir"] = str(tmp)
            if packet["command"].startswith("python "):
                packet["command"] = "python3 " + packet["command"][7:]
            result = module.run_experiment_packet(
                packet,
                results_path="results.tsv",
                ledger_path="evidence_ledger.json",
                logs_root="logs/experiments",
            )

            self.assertEqual(result["decision"], "keep")
            self.assertTrue((tmp / "results.tsv").exists())
            self.assertTrue((tmp / "evidence_ledger.json").exists())

            ledger = json.loads((tmp / "evidence_ledger.json").read_text(encoding="utf-8"))
            self.assertEqual(len(ledger["claims"]), 1)
            self.assertEqual(ledger["claims"][0]["status"], "verified")
            self.assertTrue(ledger["claims"][0]["do_not_overclaim"])


if __name__ == "__main__":
    unittest.main()
