import pathlib
import subprocess
import sys
import tempfile
import unittest
import io
import contextlib
import importlib.util


ROOT = pathlib.Path(__file__).resolve().parents[1]


def load_module(module_name: str, path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {module_name} from {path}")
    spec.loader.exec_module(module)
    return module


class ManagerCliTest(unittest.TestCase):
    def test_manager_cli_exposes_host_install_update_and_remove_commands(self) -> None:
        script_path = ROOT / "scripts" / "superrebuttal_manager.py"
        self.assertTrue(
            script_path.exists(),
            "Expected repo-level scripts/superrebuttal_manager.py to exist.",
        )

        for host in ("codex", "claude"):
            for action in ("install", "update", "remove"):
                with self.subTest(host=host, action=action):
                    completed = subprocess.run(
                        [
                            sys.executable,
                            str(script_path),
                            host,
                            action,
                            "--help",
                        ],
                        capture_output=True,
                        cwd=ROOT,
                        text=True,
                    )

                    self.assertEqual(completed.returncode, 0, completed.stderr)
                    self.assertIn(host, completed.stdout.lower())
                    self.assertIn(action, completed.stdout.lower())

    def test_codex_default_cycle_install_update_remove(self) -> None:
        script_path = ROOT / "scripts" / "superrebuttal_manager.py"
        self.assertTrue(script_path.exists())

        with tempfile.TemporaryDirectory() as tmpdir:
            home = pathlib.Path(tmpdir)
            target = home / ".agents" / "skills" / "super-rebuttal"

            install = subprocess.run(
                [sys.executable, str(script_path), "codex", "install", "--home", str(home)],
                capture_output=True,
                cwd=ROOT,
                text=True,
            )
            self.assertEqual(install.returncode, 0, install.stderr)
            self.assertTrue(target.exists())

            update = subprocess.run(
                [sys.executable, str(script_path), "codex", "update", "--home", str(home)],
                capture_output=True,
                cwd=ROOT,
                text=True,
            )
            self.assertEqual(update.returncode, 0, update.stderr)
            self.assertTrue(target.exists())

            remove = subprocess.run(
                [sys.executable, str(script_path), "codex", "remove", "--home", str(home)],
                capture_output=True,
                cwd=ROOT,
                text=True,
            )
            self.assertEqual(remove.returncode, 0, remove.stderr)
            self.assertFalse(target.exists())

    def test_codex_install_overwrites_existing_partial_directory(self) -> None:
        script_path = ROOT / "scripts" / "superrebuttal_manager.py"
        self.assertTrue(script_path.exists())

        with tempfile.TemporaryDirectory() as tmpdir:
            home = pathlib.Path(tmpdir)
            target = home / ".agents" / "skills" / "super-rebuttal"
            (target / "examples").mkdir(parents=True)
            (target / "examples" / "stale.txt").write_text("old", encoding="utf-8")

            completed = subprocess.run(
                [
                    sys.executable,
                    str(script_path),
                    "codex",
                    "install",
                    "--home",
                    str(home),
                ],
                capture_output=True,
                cwd=ROOT,
                text=True,
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertTrue((target / "SKILL.md").exists())
            self.assertFalse((target / "examples" / "stale.txt").exists())

    def test_claude_remove_renders_uninstall_command(self) -> None:
        module = load_module(
            "superrebuttal_manager",
            ROOT / "scripts" / "superrebuttal_manager.py",
        )
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            exit_code = module.main(["claude", "remove", "--print-only"])
        self.assertEqual(exit_code, 0)
        self.assertIn("/plugin uninstall super-rebuttal@super-rebuttal-dev", stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
