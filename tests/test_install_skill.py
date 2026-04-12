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


class InstallSkillTest(unittest.TestCase):
    def test_install_skill_copies_required_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            source = pathlib.Path(tmpdir) / "source"
            target = pathlib.Path(tmpdir) / "target"
            (source / "agents").mkdir(parents=True)
            (source / "references").mkdir(parents=True)
            (source / "SKILL.md").write_text(
                "---\nname: auto-rebuttal\ndescription: Use when drafting rebuttals\n---\n",
                encoding="utf-8",
            )
            (source / "agents" / "openai.yaml").write_text(
                "interface:\n  display_name: AutoRebuttal\n",
                encoding="utf-8",
            )
            (source / "references" / "guide.md").write_text(
                "# Guide\n",
                encoding="utf-8",
            )

            module = load_module(
                "install_skill",
                ROOT / "skills" / "auto-rebuttal" / "scripts" / "install_skill.py",
            )

            installed = module.install_skill(source=source, destination=target)

            self.assertEqual(installed, target)
            self.assertTrue((target / "SKILL.md").exists())
            self.assertTrue((target / "agents" / "openai.yaml").exists())
            self.assertTrue((target / "references" / "guide.md").exists())


if __name__ == "__main__":
    unittest.main()
