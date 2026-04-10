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


class PdfExtractTest(unittest.TestCase):
    def test_extract_pdf_text_reads_review_sentence_from_text_pdf(self) -> None:
        module_path = (
            ROOT / "skills" / "super-rebuttal" / "scripts" / "extract_pdf_text.py"
        )
        self.assertTrue(
            module_path.exists(),
            "Expected skills/super-rebuttal/scripts/extract_pdf_text.py to exist.",
        )

        module = load_module("extract_pdf_text", module_path)

        with tempfile.TemporaryDirectory() as tmpdir:
            pdf_path = pathlib.Path(tmpdir) / "review.pdf"
            review_sentence = "Reviewer 2 requested a stronger ablation discussion."
            write_text_pdf(pdf_path, review_sentence)

            extracted = module.extract_pdf_text(pdf_path)

        self.assertIn(review_sentence, extracted)

    def test_extract_pdf_text_ignores_non_rendered_strings(self) -> None:
        module_path = (
            ROOT / "skills" / "super-rebuttal" / "scripts" / "extract_pdf_text.py"
        )
        module = load_module("extract_pdf_text", module_path)

        with tempfile.TemporaryDirectory() as tmpdir:
            pdf_path = pathlib.Path(tmpdir) / "hidden.pdf"
            stream = b"q (HIDDEN) BT /F1 12 Tf 72 720 Td (VISIBLE) Tj ET Q"
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
            pdf_path.write_bytes(pdf)
            extracted = module.extract_pdf_text(pdf_path)

        self.assertIn("VISIBLE", extracted)
        self.assertNotIn("HIDDEN", extracted)

    def test_extract_pdf_text_raises_when_no_text_is_recovered(self) -> None:
        module_path = (
            ROOT / "skills" / "super-rebuttal" / "scripts" / "extract_pdf_text.py"
        )
        module = load_module("extract_pdf_text", module_path)

        with tempfile.TemporaryDirectory() as tmpdir:
            pdf_path = pathlib.Path(tmpdir) / "empty.pdf"
            pdf_path.write_bytes(b"%PDF-1.4\n1 0 obj\n<<>>\nendobj\n%%EOF\n")
            with self.assertRaises(ValueError):
                module.extract_pdf_text(pdf_path)


if __name__ == "__main__":
    unittest.main()
