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


class RebuttalBlockFormatTest(unittest.TestCase):
    def test_formatter_moves_inline_w_q_m_labels_onto_new_lines(self) -> None:
        module_path = (
            ROOT / "skills" / "super-rebuttal" / "scripts" / "format_rebuttal_blocks.py"
        )
        self.assertTrue(module_path.exists(), "Expected format_rebuttal_blocks.py to exist.")
        module = load_module("format_rebuttal_blocks", module_path)

        formatted = module.format_rebuttal_blocks(
            "We thank the reviewer. W1. Novelty is limited. Q1. Why this baseline? M1. Fix typos."
        )

        self.assertIn("We thank the reviewer.\nW1.", formatted)
        self.assertIn("\nQ1.", formatted)
        self.assertIn("\nM1.", formatted)

    def test_formatter_preserves_existing_line_starts(self) -> None:
        module_path = (
            ROOT / "skills" / "super-rebuttal" / "scripts" / "format_rebuttal_blocks.py"
        )
        module = load_module("format_rebuttal_blocks", module_path)

        source = "Reviewer Qc8x\nW1. Novelty is limited.\nQ1. Why this baseline?"
        formatted = module.format_rebuttal_blocks(source)

        self.assertEqual(formatted, source)


if __name__ == "__main__":
    unittest.main()
