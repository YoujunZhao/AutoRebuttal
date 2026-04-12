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


if __name__ == "__main__":
    unittest.main()
