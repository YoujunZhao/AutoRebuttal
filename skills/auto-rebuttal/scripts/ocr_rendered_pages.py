from __future__ import annotations

import argparse
import pathlib
import sys
from typing import Any


_OCR_ENGINE: Any | None = None


def _engine() -> Any:
    global _OCR_ENGINE
    if _OCR_ENGINE is None:
        try:
            from rapidocr_onnxruntime import RapidOCR
        except ModuleNotFoundError as exc:
            raise RuntimeError(
                "OCR support requires rapidocr_onnxruntime. Install it or provide a PDF with a text layer."
            ) from exc
        _OCR_ENGINE = RapidOCR()
    return _OCR_ENGINE


def ocr_rendered_pages(image_paths: list[str | pathlib.Path]) -> str:
    try:
        from PIL import Image
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "OCR support requires Pillow. Install it or provide a PDF with a text layer."
        ) from exc

    lines: list[str] = []
    engine = _engine()
    for image_path in image_paths:
        image = Image.open(image_path).convert("RGB")
        result, _ = engine(image)
        if not result:
            continue
        for item in result:
            if len(item) < 2:
                continue
            text = str(item[1]).strip()
            if text:
                lines.append(text)
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="OCR rendered page images into plain text.")
    parser.add_argument("image_paths", nargs="+")
    args = parser.parse_args(argv)
    sys.stdout.write(ocr_rendered_pages(args.image_paths))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
