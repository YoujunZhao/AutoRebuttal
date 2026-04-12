import importlib.util
import pathlib
import tempfile
import unittest

from PIL import Image, ImageDraw


ROOT = pathlib.Path(__file__).resolve().parents[1]


def load_module(module_name: str, path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {module_name} from {path}")
    spec.loader.exec_module(module)
    return module


class OcrRenderedPagesTest(unittest.TestCase):
    def test_ocr_reads_text_from_rendered_page_images(self) -> None:
        module_path = ROOT / "skills" / "auto-rebuttal" / "scripts" / "ocr_rendered_pages.py"
        self.assertTrue(module_path.exists(), "Expected ocr_rendered_pages.py to exist.")
        module = load_module("ocr_rendered_pages", module_path)

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = pathlib.Path(tmpdir)
            image = Image.new("RGB", (1400, 800), "white")
            draw = ImageDraw.Draw(image)
            draw.text((40, 40), "Key Questions For Authors", fill="black")
            draw.text((40, 120), "1. Why this baseline?", fill="black")
            image_path = tmp / "ocr.png"
            image.save(image_path)

            text = module.ocr_rendered_pages([image_path])

        self.assertIn("Key Questions", text)
        self.assertIn("Why this baseline", text)


if __name__ == "__main__":
    unittest.main()
