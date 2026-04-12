import importlib.util
import pathlib
import tempfile
import unittest

import fitz


ROOT = pathlib.Path(__file__).resolve().parents[1]


def load_module(module_name: str, path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {module_name} from {path}")
    spec.loader.exec_module(module)
    return module


def write_graphics_only_pdf(path: pathlib.Path) -> None:
    document = fitz.open()
    page = document.new_page()
    page.draw_rect(fitz.Rect(72, 72, 420, 240), color=(0, 0, 0), fill=(0.9, 0.9, 0.9))
    page.draw_rect(fitz.Rect(72, 280, 420, 420), color=(0, 0, 1), fill=(0.8, 0.9, 1.0))
    document.save(path)
    document.close()


class RenderReviewPdfPagesTest(unittest.TestCase):
    def test_renderer_creates_pngs_for_graphics_only_review_pdf(self) -> None:
        module_path = (
            ROOT / "skills" / "auto-rebuttal" / "scripts" / "render_review_pdf_pages.py"
        )
        self.assertTrue(
            module_path.exists(),
            "Expected render_review_pdf_pages.py to exist.",
        )
        module = load_module("render_review_pdf_pages", module_path)

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = pathlib.Path(tmpdir)
            pdf_path = tmp / "review.pdf"
            output_dir = tmp / "rendered"
            write_graphics_only_pdf(pdf_path)

            image_paths = module.render_review_pdf_pages(
                pdf_path=pdf_path,
                output_dir=output_dir,
                max_pages=2,
            )

            self.assertEqual(len(image_paths), 1)
            rendered_path = pathlib.Path(image_paths[0])
            self.assertTrue(rendered_path.exists())
            self.assertEqual(rendered_path.suffix.lower(), ".png")


if __name__ == "__main__":
    unittest.main()
