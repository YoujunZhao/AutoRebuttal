import importlib.util
import pathlib
import tempfile
import unittest

import fitz
from PIL import Image, ImageDraw


ROOT = pathlib.Path(__file__).resolve().parents[1]


def load_module(module_name: str, path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {module_name} from {path}")
    spec.loader.exec_module(module)
    return module


def write_text_pdf(path: pathlib.Path, text: str) -> None:
    escaped = text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
    stream = f"BT /F1 12 Tf 72 720 Td ({escaped}) Tj ET".encode("latin-1")
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>",
        b"<< /Length %d >>\nstream\n%b\nendstream" % (len(stream), stream),
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]

    pdf = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for index, obj in enumerate(objects, start=1):
        offsets.append(len(pdf))
        pdf.extend(f"{index} 0 obj\n".encode("ascii"))
        pdf.extend(obj)
        pdf.extend(b"\nendobj\n")

    xref_start = len(pdf)
    pdf.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    pdf.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        pdf.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    pdf.extend(
        (
            f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
            f"startxref\n{xref_start}\n%%EOF\n"
        ).encode("ascii")
    )
    path.write_bytes(pdf)


class RevisionBundleTest(unittest.TestCase):
    def test_revision_bundle_defaults_output_format_to_text(self) -> None:
        module_path = ROOT / "skills" / "auto-rebuttal" / "scripts" / "build_revision_bundle.py"
        module = load_module("build_revision_bundle", module_path)

        bundle = module.build_revision_bundle(
            rebuttal_input="Reviewer Qc8x\nW1. Existing rebuttal text.",
        )

        self.assertEqual(bundle["output_format"], "text")

    def test_revision_bundle_accepts_markdown_output_format(self) -> None:
        module_path = ROOT / "skills" / "auto-rebuttal" / "scripts" / "build_revision_bundle.py"
        module = load_module("build_revision_bundle", module_path)

        bundle = module.build_revision_bundle(
            rebuttal_input="Reviewer Qc8x\nW1. Existing rebuttal text.",
            output="md",
        )

        self.assertEqual(bundle["output_format"], "md")

    def test_revision_bundle_rejects_unknown_output_format(self) -> None:
        module_path = ROOT / "skills" / "auto-rebuttal" / "scripts" / "build_revision_bundle.py"
        module = load_module("build_revision_bundle", module_path)

        with self.assertRaises(ValueError):
            module.build_revision_bundle(
                rebuttal_input="Reviewer Qc8x\nW1. Existing rebuttal text.",
                output="html",
            )

    def test_revision_bundle_auto_detects_pdf_rebuttal_and_optional_paper(self) -> None:
        module_path = ROOT / "skills" / "auto-rebuttal" / "scripts" / "build_revision_bundle.py"
        self.assertTrue(module_path.exists(), "Expected build_revision_bundle.py to exist.")
        module = load_module("build_revision_bundle", module_path)

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = pathlib.Path(tmpdir)
            rebuttal_pdf = tmp / "rebuttal.pdf"
            paper_pdf = tmp / "paper.pdf"
            write_text_pdf(rebuttal_pdf, "Reviewer Qc8x W1. Existing rebuttal content.")
            write_text_pdf(paper_pdf, "Paper summary: AutoRebuttal revision paper.")

            bundle = module.build_revision_bundle(
                rebuttal_input=rebuttal_pdf,
                paper_pdf=paper_pdf,
            )

        self.assertEqual(bundle["rebuttal"]["source_type"], "pdf")
        self.assertIn("Existing rebuttal content", bundle["rebuttal"]["text"])
        self.assertEqual(bundle["paper"]["source_type"], "pdf")

    def test_revision_bundle_auto_detects_text_rebuttal(self) -> None:
        module_path = ROOT / "skills" / "auto-rebuttal" / "scripts" / "build_revision_bundle.py"
        module = load_module("build_revision_bundle", module_path)

        bundle = module.build_revision_bundle(
            rebuttal_input="Reviewer Qc8x\nW1. Existing rebuttal text.",
            paper_pdf=None,
        )

        self.assertEqual(bundle["rebuttal"]["source_type"], "text")
        self.assertIn("Existing rebuttal text", bundle["rebuttal"]["text"])
        self.assertIsNone(bundle["paper"])

    def test_revision_bundle_ocrs_image_only_rebuttal_pdf(self) -> None:
        module_path = ROOT / "skills" / "auto-rebuttal" / "scripts" / "build_revision_bundle.py"
        module = load_module("build_revision_bundle", module_path)

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = pathlib.Path(tmpdir)
            rebuttal_pdf = tmp / "rebuttal-image.pdf"

            image = Image.new("RGB", (1400, 800), "white")
            draw = ImageDraw.Draw(image)
            draw.text((40, 40), "Reviewer Qc8x", fill="black")
            draw.text((40, 120), "W1. Existing rebuttal OCR content.", fill="black")
            png_path = tmp / "rebuttal.png"
            image.save(png_path)

            document = fitz.open()
            page = document.new_page(width=700, height=400)
            page.insert_image(fitz.Rect(0, 0, 700, 400), filename=str(png_path))
            document.save(rebuttal_pdf)
            document.close()

            bundle = module.build_revision_bundle(
                rebuttal_input=rebuttal_pdf,
                paper_pdf=None,
            )

        self.assertEqual(bundle["rebuttal"]["source_type"], "pdf")
        self.assertEqual(bundle["rebuttal"]["extraction_mode"], "ocr")
        self.assertIn("Reviewer", bundle["rebuttal"]["text"])
        normalized = bundle["rebuttal"]["text"].replace(" ", "")
        self.assertIn("ExistingrebuttalOCRcontent", normalized)

    def test_revision_bundle_accepts_optional_latex_paper(self) -> None:
        module_path = ROOT / "skills" / "auto-rebuttal" / "scripts" / "build_revision_bundle.py"
        module = load_module("build_revision_bundle", module_path)

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = pathlib.Path(tmpdir)
            paper_tex = tmp / "paper.tex"
            paper_tex.write_text(
                "\\section{Conclusion}\nLatex revision paper.\n",
                encoding="utf-8",
            )

            bundle = module.build_revision_bundle(
                rebuttal_input="Reviewer Qc8x\nW1. Existing rebuttal text.",
                paper_input=paper_tex,
            )

        self.assertEqual(bundle["paper"]["source_type"], "latex")
        self.assertIn("Latex revision paper", bundle["paper"]["text"])


if __name__ == "__main__":
    unittest.main()
