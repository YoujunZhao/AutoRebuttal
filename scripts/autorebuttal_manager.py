from __future__ import annotations

import argparse
import os
import pathlib
import shutil
import subprocess


PACKAGE_NAME = "auto-rebuttal"
CLAUDE_MARKETPLACE = "auto-rebuttal-dev"
CLAUDE_REPOSITORY = "YoujunZhao/AutoRebuttal"


def repo_root() -> pathlib.Path:
    return pathlib.Path(__file__).resolve().parents[1]


def codex_source_path(root: pathlib.Path | None = None) -> pathlib.Path:
    base = repo_root() if root is None else pathlib.Path(root)
    return base / "skills" / PACKAGE_NAME


def resolve_home_path(home: str | pathlib.Path | None = None) -> pathlib.Path:
    if home is not None:
        return pathlib.Path(home).expanduser()

    override = os.environ.get("AUTOREBUTTAL_HOME") or os.environ.get("SUPERREBUTTAL_HOME")
    if override:
        return pathlib.Path(override).expanduser()

    return pathlib.Path.home()


def codex_destination_path(home: pathlib.Path) -> pathlib.Path:
    return home / ".agents" / "skills" / PACKAGE_NAME


def remove_path(path: pathlib.Path) -> bool:
    if not path.exists() and not path.is_symlink():
        return False

    if path.is_symlink() or path.is_file():
        path.unlink()
        return True

    file_attributes = getattr(path.stat(), "st_file_attributes", 0)
    if file_attributes & 0x400:
        path.rmdir()
        return True

    if os.name == "nt":
        subprocess.run(["cmd", "/c", "rmdir", "/S", "/Q", str(path)], check=False)
    else:
        shutil.rmtree(path, ignore_errors=True)
    if path.exists():
        raise OSError(f"Failed to remove path cleanly: {path}")
    return True


def copy_skill_tree(source: pathlib.Path, destination: pathlib.Path) -> pathlib.Path:
    if not source.exists():
        raise FileNotFoundError(f"Skill source does not exist: {source}")

    destination.parent.mkdir(parents=True, exist_ok=True)
    remove_path(destination)
    shutil.copytree(source, destination)
    return destination


def codex_install(home: str | pathlib.Path | None = None) -> pathlib.Path:
    resolved_home = resolve_home_path(home)
    return copy_skill_tree(
        source=codex_source_path(),
        destination=codex_destination_path(resolved_home),
    )


def codex_update(home: str | pathlib.Path | None = None) -> pathlib.Path:
    return codex_install(home=home)


def codex_remove(home: str | pathlib.Path | None = None) -> pathlib.Path:
    resolved_home = resolve_home_path(home)
    destination = codex_destination_path(resolved_home)
    remove_path(destination)
    return destination


def claude_commands(action: str) -> list[str]:
    if action == "install":
        return [
            f"/plugin marketplace add {CLAUDE_REPOSITORY}",
            f"/plugin install {PACKAGE_NAME}@{CLAUDE_MARKETPLACE}",
        ]
    if action == "update":
        return [f"/plugin update {PACKAGE_NAME}"]
    if action == "remove":
        return [f"/plugin uninstall {PACKAGE_NAME}@{CLAUDE_MARKETPLACE}"]
    raise ValueError(f"Unsupported Claude action: {action}")


def run_codex_action(args: argparse.Namespace) -> int:
    action = args.action
    if action == "install":
        destination = codex_install(home=args.home)
        print(f"Installed AutoRebuttal for Codex at {destination}")
        return 0
    if action == "update":
        destination = codex_update(home=args.home)
        print(f"Updated AutoRebuttal for Codex at {destination}")
        return 0
    if action == "remove":
        destination = codex_remove(home=args.home)
        print(f"Removed AutoRebuttal for Codex from {destination}")
        return 0
    raise ValueError(f"Unsupported Codex action: {action}")


def run_claude_action(args: argparse.Namespace) -> int:
    print("Claude Code actions are print-only. Run the following official plugin commands:")
    for command in claude_commands(args.action):
        print(command)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Manage AutoRebuttal installation surfaces for Codex and Claude Code."
    )
    host_parsers = parser.add_subparsers(dest="host", required=True)

    codex_parser = host_parsers.add_parser(
        "codex",
        help="Manage the Codex install/update/remove workflow.",
        description="Codex manager commands for install, update, and remove.",
    )
    codex_actions = codex_parser.add_subparsers(dest="action", required=True)
    for action, help_text in (
        ("install", "Install AutoRebuttal into the Codex user-home skill path."),
        ("update", "Update AutoRebuttal in the Codex user-home skill path."),
        ("remove", "Remove AutoRebuttal from the Codex user-home skill path."),
    ):
        action_parser = codex_actions.add_parser(
            action,
            help=help_text,
            description=f"Codex {action} command for AutoRebuttal.",
        )
        action_parser.add_argument(
            "--home",
            help="Override the user home used for Codex filesystem operations.",
        )
        action_parser.set_defaults(handler=run_codex_action)

    claude_parser = host_parsers.add_parser(
        "claude",
        help="Render Claude Code plugin install/update/remove commands.",
        description="Claude Code manager commands for install, update, and remove.",
    )
    claude_actions = claude_parser.add_subparsers(dest="action", required=True)
    for action, help_text in (
        ("install", "Print the Claude Code plugin install commands."),
        ("update", "Print the Claude Code plugin update command."),
        ("remove", "Print the Claude Code plugin remove command."),
    ):
        action_parser = claude_actions.add_parser(
            action,
            help=help_text,
            description=f"Claude Code {action} command renderer for AutoRebuttal.",
        )
        action_parser.add_argument(
            "--print-only",
            action="store_true",
            help="Accepted for clarity; Claude manager actions only render commands.",
        )
        action_parser.set_defaults(handler=run_claude_action)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
