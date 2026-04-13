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


class LatexOutputPackageTest(unittest.TestCase):
    def test_latex_output_package_contains_rebuttal_and_revised_paper(self) -> None:
        module_path = ROOT / "skills" / "auto-rebuttal" / "scripts" / "build_latex_output_package.py"
        self.assertTrue(module_path.exists(), "Expected build_latex_output_package.py to exist.")
        module = load_module("build_latex_output_package", module_path)

        package = module.build_latex_output_package(
            rebuttal_text="Reviewer Qc8x\nW1. Clarified in the revision.",
            revised_latex_paper="\\section{Method}\nUpdated latex paper.\n",
            entrypoint="main.tex",
        )

        self.assertEqual(package["output_mode"], "latex-dual")
        self.assertIn("Reviewer Qc8x", package["rebuttal_text"])
        self.assertIn("Updated latex paper", package["revised_latex_paper"])
        self.assertEqual(package["entrypoint"], "main.tex")
