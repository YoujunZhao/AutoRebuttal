from __future__ import annotations

import hashlib
import pathlib
import tempfile

from extract_pdf_text import extract_pdf_text
from ocr_rendered_pages import ocr_rendered_pages
from render_review_pdf_pages import render_review_pdf_pages


def _render_bucket(root: pathlib.Path, path: pathlib.Path, index: int) -> pathlib.Path:
    digest = hashlib.sha1(str(path).encode("utf-8")).hexdigest()[:10]
    return root / f"{index + 1:02d}_{path.stem}_{digest}"


def _maybe_path(input_value: str | pathlib.Path) -> pathlib.Path | None:
    if isinstance(input_value, pathlib.Path):
        return input_value.expanduser().resolve()
    try:
        candidate = pathlib.Path(str(input_value)).expanduser()
    except OSError:
        return None
    if candidate.exists():
        return candidate.resolve()
    return None


def detect_input_artifact(
    input_value: str | pathlib.Path,
    *,
    index: int = 0,
    allow_pdf_image_fallback: bool,
    temp_prefix: str,
) -> dict[str, object]:
    resolved_path = _maybe_path(input_value)
    if resolved_path is not None:
        if resolved_path.suffix.lower() == ".pdf":
            try:
                return {
                    "source_type": "pdf",
                    "path": str(resolved_path),
                    "text": extract_pdf_text(resolved_path),
                    "extraction_mode": "text",
                    "page_images": [],
                }
            except ValueError:
                tmp_root = pathlib.Path(tempfile.mkdtemp(prefix=temp_prefix))
                page_images = render_review_pdf_pages(
                    pdf_path=resolved_path,
                    output_dir=_render_bucket(tmp_root, resolved_path, index),
                )
                ocr_text = ocr_rendered_pages(page_images).strip()
                if ocr_text:
                    return {
                        "source_type": "pdf",
                        "path": str(resolved_path),
                        "text": ocr_text,
                        "extraction_mode": "ocr",
                        "page_images": page_images,
                    }
                if not allow_pdf_image_fallback:
                    raise ValueError(f"No OCR text recovered from PDF: {resolved_path}")
                return {
                    "source_type": "pdf",
                    "path": str(resolved_path),
                    "text": None,
                    "extraction_mode": "image_fallback",
                    "page_images": page_images,
                }

        return {
            "source_type": "text",
            "path": str(resolved_path),
            "text": resolved_path.read_text(encoding="utf-8"),
            "extraction_mode": "text",
            "page_images": [],
        }

    return {
        "source_type": "text",
        "path": None,
        "text": str(input_value),
        "extraction_mode": "text",
        "page_images": [],
    }
