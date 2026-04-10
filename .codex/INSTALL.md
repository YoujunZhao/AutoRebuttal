# Installing SuperRebuttal for Codex

The preferred Codex path now goes through the repo-level manager CLI:

```bash
python scripts/superrebuttal_manager.py codex install
python scripts/superrebuttal_manager.py codex update
python scripts/superrebuttal_manager.py codex remove
```

These commands perform real filesystem operations against the Codex user-home skill path and manage:

```text
~/.agents/skills/super-rebuttal
```

If you need to target a different home directory, pass `--home`:

```bash
python scripts/superrebuttal_manager.py codex install --home /tmp/superrebuttal-home
```

## What Each Command Does

- `codex install` copies this repository's `skills/super-rebuttal` tree into the Codex user-home skill path.
- `codex update` replaces the existing installed tree with the current repository copy.
- `codex remove` deletes the installed tree from the Codex user-home skill path.

## Verify

```bash
python scripts/superrebuttal_manager.py codex install
ls -la ~/.agents/skills/super-rebuttal
```

You should see an installed copy of this repository's `skills/super-rebuttal` directory.
