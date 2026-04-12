from __future__ import annotations

import argparse
import json
import pathlib

import fitz


def render_review_pdf_pages(
    pdf_path: str | pathlib.Path,
    output_dir: str | pathlib.Path,
    *,
    max_pages: int = 3,
    zoom: float = 2.0,
) -> list[str]:
    pdf_path = pathlib.Path(pdf_path).resolve()
    output_dir = pathlib.Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    document = fitz.open(pdf_path)
    try:
        outputs: list[str] = []
        for index in range(min(max_pages, document.page_count)):
            page = document.load_page(index)
            pixmap = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
            output_path = output_dir / f"{pdf_path.stem}_p{index + 1}.png"
            pixmap.save(output_path)
            outputs.append(str(output_path))
        return outputs
    finally:
        document.close()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Render review PDF pages to PNG images.")
    parser.add_argument("pdf_path")
    parser.add_argument("output_dir")
    parser.add_argument("--max-pages", type=int, default=3)
    args = parser.parse_args(argv)
    print(
        json.dumps(
            render_review_pdf_pages(
                pdf_path=args.pdf_path,
                output_dir=args.output_dir,
                max_pages=args.max_pages,
            ),
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
