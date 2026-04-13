from __future__ import annotations

import pathlib
import sys


if __package__ in {None, ""}:
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from detect_input_artifact import detect_input_artifact


LATEX_ENTRYPOINT_CANDIDATES = ("main.tex", "paper.tex", "ms.tex", "manuscript.tex")


def _collect_latex_project(path: pathlib.Path) -> dict[str, object]:
    if path.is_file():
        latex_files = [path]
        project_root = path.parent
    else:
        latex_files = sorted(path.rglob("*.tex"))
        project_root = path

    if not latex_files:
        raise FileNotFoundError(f"No .tex files found in LaTeX input: {path}")

    entrypoint = next(
        (candidate for candidate in latex_files if candidate.name in LATEX_ENTRYPOINT_CANDIDATES),
        latex_files[0],
    )

    latex_sources = {
        str(file.relative_to(project_root)).replace("\\", "/"): file.read_text(encoding="utf-8")
        for file in latex_files
    }
    combined = "\n\n".join(
        f"%% FILE: {relative_path}\n{content}"
        for relative_path, content in latex_sources.items()
    )
    return {
        "source_type": "latex",
        "path": str(path.resolve()),
        "project_root": str(project_root.resolve()),
        "entrypoint": str(entrypoint.resolve()),
        "text": combined,
        "latex_sources": latex_sources,
        "expected_outputs": ["rebuttal_text", "revised_latex_paper"],
    }


def detect_paper_artifact(paper_input: str | pathlib.Path) -> dict[str, object]:
    if isinstance(paper_input, pathlib.Path):
        candidate = paper_input.expanduser()
    else:
        candidate = pathlib.Path(str(paper_input)).expanduser()

    if candidate.exists():
        resolved = candidate.resolve()
        if resolved.suffix.lower() == ".pdf":
            artifact = detect_input_artifact(
                resolved,
                index=0,
                allow_pdf_image_fallback=True,
                temp_prefix="autorebuttal_paper_pages_",
            )
            artifact["expected_outputs"] = ["rebuttal_text"]
            return artifact
        if resolved.suffix.lower() == ".tex" or resolved.is_dir():
            return _collect_latex_project(resolved)
        return {
            "source_type": "text",
            "path": str(resolved),
            "text": resolved.read_text(encoding="utf-8"),
            "expected_outputs": ["rebuttal_text"],
        }

    return {
        "source_type": "text",
        "path": None,
        "text": str(paper_input),
        "expected_outputs": ["rebuttal_text"],
    }
