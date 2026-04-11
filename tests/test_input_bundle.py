import json
import pathlib
import subprocess
import sys
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


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


class InputBundleCliTest(unittest.TestCase):
    def test_builder_accepts_paper_pdf_without_review_pdfs(self) -> None:
        script_path = (
            ROOT / "skills" / "super-rebuttal" / "scripts" / "build_input_bundle.py"
        )
        self.assertTrue(
            script_path.exists(),
            "Expected skills/super-rebuttal/scripts/build_input_bundle.py to exist.",
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = pathlib.Path(tmpdir)
            paper_pdf = tmp / "paper.pdf"
            write_text_pdf(paper_pdf, "Paper summary: our method improves robustness.")

            completed = subprocess.run(
                [
                    sys.executable,
                    str(script_path),
                    "--paper-pdf",
                    str(paper_pdf),
                ],
                capture_output=True,
                cwd=ROOT,
                text=True,
            )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        bundle = json.loads(completed.stdout)
        self.assertEqual(bundle["paper"]["path"], str(paper_pdf))
        self.assertIn("Paper summary", bundle["paper"]["text"])
        self.assertEqual(bundle["reviews"], [])
        self.assertEqual(bundle["source_files"]["review_pdfs"], [])

    def test_builder_accepts_paper_pdf_and_multiple_review_pdfs(self) -> None:
        script_path = (
            ROOT / "skills" / "super-rebuttal" / "scripts" / "build_input_bundle.py"
        )
        self.assertTrue(
            script_path.exists(),
            "Expected skills/super-rebuttal/scripts/build_input_bundle.py to exist.",
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = pathlib.Path(tmpdir)
            paper_pdf = tmp / "paper.pdf"
            review_one_pdf = tmp / "review-1.pdf"
            review_two_pdf = tmp / "review-2.pdf"
            write_text_pdf(paper_pdf, "Paper summary: our method improves robustness.")
            write_text_pdf(review_one_pdf, "Review 1: please clarify the training data.")
            write_text_pdf(review_two_pdf, "Review 2: add error bars to the main figure.")

            completed = subprocess.run(
                [
                    sys.executable,
                    str(script_path),
                    "--paper-pdf",
                    str(paper_pdf),
                    "--review-pdf",
                    str(review_one_pdf),
                    "--review-pdf",
                    str(review_two_pdf),
                ],
                capture_output=True,
                cwd=ROOT,
                text=True,
            )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        bundle = json.loads(completed.stdout)
        self.assertEqual(bundle["paper"]["path"], str(paper_pdf))
        self.assertIn("Paper summary", bundle["paper"]["text"])
        self.assertEqual(len(bundle["reviews"]), 2)
        self.assertEqual(
            [review["path"] for review in bundle["reviews"]],
            [str(review_one_pdf), str(review_two_pdf)],
        )
        self.assertIn("Review 1", bundle["reviews"][0]["text"])
        self.assertIn("Review 2", bundle["reviews"][1]["text"])
        self.assertEqual(
            bundle["source_files"]["review_pdfs"],
            [str(review_one_pdf), str(review_two_pdf)],
        )

    def test_builder_falls_back_to_rendered_page_images_for_graphics_only_review_pdf(self) -> None:
        script_path = (
            ROOT / "skills" / "super-rebuttal" / "scripts" / "build_input_bundle.py"
        )
        self.assertTrue(
            script_path.exists(),
            "Expected skills/super-rebuttal/scripts/build_input_bundle.py to exist.",
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = pathlib.Path(tmpdir)
            paper_pdf = tmp / "paper.pdf"
            review_pdf = tmp / "review.pdf"
            write_text_pdf(paper_pdf, "Paper summary: our method improves robustness.")

            import fitz

            document = fitz.open()
            page = document.new_page()
            page.draw_rect(fitz.Rect(72, 72, 420, 240), color=(0, 0, 0), fill=(0.9, 0.9, 0.9))
            document.save(review_pdf)
            document.close()

            completed = subprocess.run(
                [
                    sys.executable,
                    str(script_path),
                    "--paper-pdf",
                    str(paper_pdf),
                    "--review-pdf",
                    str(review_pdf),
                ],
                capture_output=True,
                cwd=ROOT,
                text=True,
            )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        bundle = json.loads(completed.stdout)
        self.assertEqual(len(bundle["reviews"]), 1)
        review = bundle["reviews"][0]
        self.assertEqual(review["path"], str(review_pdf))
        self.assertIsNone(review["text"])
        self.assertEqual(review["extraction_mode"], "image_fallback")
        self.assertTrue(review["page_images"])
        self.assertTrue(pathlib.Path(review["page_images"][0]).exists())


if __name__ == "__main__":
    unittest.main()
