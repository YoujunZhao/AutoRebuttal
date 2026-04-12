from __future__ import annotations

import argparse
import pathlib
import shutil


def install_skill(source: pathlib.Path, destination: pathlib.Path) -> pathlib.Path:
    """Copy a skill directory into the requested destination path."""
    source = pathlib.Path(source)
    destination = pathlib.Path(destination)

    if not source.exists():
        raise FileNotFoundError(f"Skill source does not exist: {source}")
    if destination.exists():
        shutil.rmtree(destination)

    shutil.copytree(source, destination)
    return destination


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Install the AutoRebuttal skill.")
    parser.add_argument("--source", required=True)
    parser.add_argument("--destination", required=True)
    args = parser.parse_args(argv)
    install_skill(pathlib.Path(args.source), pathlib.Path(args.destination))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
