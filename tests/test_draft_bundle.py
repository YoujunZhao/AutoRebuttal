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


class DraftBundleTest(unittest.TestCase):
    def test_draft_bundle_auto_detects_pdf_and_text_review_inputs(self) -> None:
        module_path = ROOT / "skills" / "auto-rebuttal" / "scripts" / "build_draft_bundle.py"
        self.assertTrue(module_path.exists(), "Expected build_draft_bundle.py to exist.")
        module = load_module("build_draft_bundle", module_path)

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = pathlib.Path(tmpdir)
            paper_pdf = tmp / "paper.pdf"
            review_pdf = tmp / "review.pdf"
            write_text_pdf(paper_pdf, "Paper summary: AutoRebuttal test paper.")
            write_text_pdf(review_pdf, "Review PDF: clarify baseline fairness.")

            bundle = module.build_draft_bundle(
                paper_pdf=paper_pdf,
                review_inputs=[
                    review_pdf,
                    "Review text: please explain prompt sensitivity.",
                ],
            )

        self.assertEqual(bundle["paper"]["source_type"], "pdf")
        self.assertEqual(len(bundle["reviews"]), 2)
        self.assertEqual(bundle["reviews"][0]["source_type"], "pdf")
        self.assertEqual(bundle["reviews"][1]["source_type"], "text")
        self.assertIn("clarify baseline fairness", bundle["reviews"][0]["text"])
        self.assertIn("prompt sensitivity", bundle["reviews"][1]["text"])

    def test_draft_bundle_ocrs_image_only_review_pdf(self) -> None:
        module_path = ROOT / "skills" / "auto-rebuttal" / "scripts" / "build_draft_bundle.py"
        module = load_module("build_draft_bundle", module_path)

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = pathlib.Path(tmpdir)
            paper_pdf = tmp / "paper.pdf"
            review_pdf = tmp / "review-image.pdf"
            write_text_pdf(paper_pdf, "Paper summary: AutoRebuttal OCR paper.")

            image = Image.new("RGB", (1400, 800), "white")
            draw = ImageDraw.Draw(image)
            draw.text((40, 40), "Key Questions For Authors", fill="black")
            draw.text((40, 120), "1. Why this baseline?", fill="black")
            png_path = tmp / "review.png"
            image.save(png_path)

            document = fitz.open()
            page = document.new_page(width=700, height=400)
            page.insert_image(fitz.Rect(0, 0, 700, 400), filename=str(png_path))
            document.save(review_pdf)
            document.close()

            bundle = module.build_draft_bundle(
                paper_pdf=paper_pdf,
                review_inputs=[review_pdf],
            )

        self.assertEqual(bundle["reviews"][0]["source_type"], "pdf")
        self.assertEqual(bundle["reviews"][0]["extraction_mode"], "ocr")
        self.assertIn("Key Questions", bundle["reviews"][0]["text"])
        self.assertIn("Why this baseline", bundle["reviews"][0]["text"])

    def test_draft_bundle_accepts_single_tex_paper(self) -> None:
        module_path = ROOT / "skills" / "auto-rebuttal" / "scripts" / "build_draft_bundle.py"
        module = load_module("build_draft_bundle", module_path)

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = pathlib.Path(tmpdir)
            paper_tex = tmp / "paper.tex"
            paper_tex.write_text(
                "\\section{Introduction}\nWe present a latex-paper workflow.\n",
                encoding="utf-8",
            )

            bundle = module.build_draft_bundle(
                paper_input=paper_tex,
                review_inputs=["Review text: please clarify the latex paper assumptions."],
            )

        self.assertEqual(bundle["paper"]["source_type"], "latex")
        self.assertIn("latex-paper workflow", bundle["paper"]["text"])
        self.assertIn("rebuttal_text", bundle["paper"]["expected_outputs"])
        self.assertIn("revised_latex_paper", bundle["paper"]["expected_outputs"])

    def test_draft_bundle_accepts_latex_project_directory(self) -> None:
        module_path = ROOT / "skills" / "auto-rebuttal" / "scripts" / "build_draft_bundle.py"
        module = load_module("build_draft_bundle", module_path)

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = pathlib.Path(tmpdir)
            latex_dir = tmp / "paper"
            latex_dir.mkdir()
            (latex_dir / "main.tex").write_text(
                "\\input{sections/method}\n\\section{Intro}\n",
                encoding="utf-8",
            )
            (latex_dir / "sections").mkdir()
            (latex_dir / "sections" / "method.tex").write_text(
                "\\section{Method}\nDetailed latex method.\n",
                encoding="utf-8",
            )

            bundle = module.build_draft_bundle(
                paper_input=latex_dir,
                review_inputs=[],
            )

        self.assertEqual(bundle["paper"]["source_type"], "latex")
        self.assertTrue(bundle["paper"]["entrypoint"].endswith("main.tex"))
        self.assertIn("Detailed latex method", bundle["paper"]["text"])
        self.assertTrue(bundle["paper"]["latex_sources"])

    def test_draft_bundle_rejects_missing_tex_path(self) -> None:
        module_path = ROOT / "skills" / "auto-rebuttal" / "scripts" / "build_draft_bundle.py"
        module = load_module("build_draft_bundle", module_path)
        with self.assertRaises(FileNotFoundError):
            module.build_draft_bundle(
                paper_input=pathlib.Path("missing-paper.tex"),
                review_inputs=[],
            )


if __name__ == "__main__":
    unittest.main()
