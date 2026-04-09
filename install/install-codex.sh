#!/usr/bin/env sh
set -eu

root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
source_dir="$root/skill/super-rebuttal"
installer="$source_dir/scripts/install_skill.py"
target_dir="${1:-${HOME}/.codex/skills/super-rebuttal}"

if [ ! -f "$installer" ]; then
    printf 'Missing install helper: %s\n' "$installer" >&2
    exit 1
fi

if command -v python3 >/dev/null 2>&1; then
    python_cmd=python3
elif command -v python >/dev/null 2>&1; then
    python_cmd=python
else
    printf 'Python 3 is required to install SuperRebuttal.\n' >&2
    exit 1
fi

"$python_cmd" "$installer" --source "$source_dir" --destination "$target_dir"
printf 'Installed SuperRebuttal to %s\n' "$target_dir"
