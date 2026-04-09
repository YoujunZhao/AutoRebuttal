from __future__ import annotations

import argparse
import pathlib
import zipfile


def build_archive(skill_dir: pathlib.Path, dist_dir: pathlib.Path) -> pathlib.Path:
    """Build a zip archive that preserves the canonical skill root directory."""
    skill_dir = pathlib.Path(skill_dir)
    dist_dir = pathlib.Path(dist_dir)
    dist_dir.mkdir(parents=True, exist_ok=True)

    archive_path = dist_dir / "super-rebuttal.zip"
    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in skill_dir.rglob("*"):
            if path.is_file():
                archive.write(
                    path,
                    pathlib.Path("super-rebuttal") / path.relative_to(skill_dir),
                )

    return archive_path


def main(argv: list[str] | None = None) -> int:
    default_skill_dir = pathlib.Path(__file__).resolve().parents[1]
    default_dist_dir = default_skill_dir.parents[1] / "dist"

    parser = argparse.ArgumentParser(description="Package the SuperRebuttal skill.")
    parser.add_argument("--skill-dir", default=str(default_skill_dir))
    parser.add_argument("--dist-dir", default=str(default_dist_dir))
    args = parser.parse_args(argv)

    build_archive(pathlib.Path(args.skill_dir), pathlib.Path(args.dist_dir))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
