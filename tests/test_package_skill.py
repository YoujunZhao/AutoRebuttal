import importlib.util
import pathlib
import tempfile
import unittest
import zipfile

ROOT = pathlib.Path(__file__).resolve().parents[1]


def load_module(module_name: str, path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {module_name} from {path}")
    spec.loader.exec_module(module)
    return module


class PackageSkillTest(unittest.TestCase):
    def test_build_archive_contains_skill_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = pathlib.Path(tmpdir)
            skill_dir = root / "skill" / "super-rebuttal"
            dist_dir = root / "dist"
            (skill_dir / "references").mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text("stub", encoding="utf-8")
            (skill_dir / "references" / "guide.md").write_text("guide", encoding="utf-8")

            module = load_module(
                "package_skill",
                ROOT / "skills" / "super-rebuttal" / "scripts" / "package_skill.py",
            )

            archive = module.build_archive(skill_dir=skill_dir, dist_dir=dist_dir)

            self.assertEqual(archive, dist_dir / "super-rebuttal.zip")
            with zipfile.ZipFile(archive) as zf:
                self.assertIn("super-rebuttal/SKILL.md", zf.namelist())
                self.assertIn("super-rebuttal/references/guide.md", zf.namelist())

    def test_main_creates_archive_from_arguments(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = pathlib.Path(tmpdir)
            skill_dir = root / "skill" / "super-rebuttal"
            dist_dir = root / "dist"
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text("stub", encoding="utf-8")

            module = load_module(
                "package_skill_cli",
                ROOT / "skills" / "super-rebuttal" / "scripts" / "package_skill.py",
            )

            exit_code = module.main(
                ["--skill-dir", str(skill_dir), "--dist-dir", str(dist_dir)]
            )

            self.assertEqual(exit_code, 0)
            self.assertTrue((dist_dir / "super-rebuttal.zip").exists())


if __name__ == "__main__":
    unittest.main()
