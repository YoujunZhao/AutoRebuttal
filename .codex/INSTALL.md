# Installing AutoRebuttal for Codex

Enable AutoRebuttal in Codex via native skill discovery. The preferred path is the same shape as Superpowers:

1. clone the repo
2. create one skill symlink / junction
3. restart Codex

## Quick Install

Tell Codex:

```text
Fetch and follow instructions from https://raw.githubusercontent.com/YoujunZhao/AutoRebuttal/refs/heads/main/.codex/INSTALL.md
```

## Manual Installation

### Prerequisites

- Git

### Steps

1. Clone the repo:

```bash
git clone https://github.com/YoujunZhao/AutoRebuttal.git ~/.codex/AutoRebuttal
```

2. Create the skill symlink / junction:

```bash
mkdir -p ~/.agents/skills
ln -s ~/.codex/AutoRebuttal/skills/auto-rebuttal ~/.agents/skills/auto-rebuttal
```

Windows (PowerShell):

```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.agents\skills"
cmd /c mklink /J "$env:USERPROFILE\.agents\skills\auto-rebuttal" "$env:USERPROFILE\.codex\AutoRebuttal\skills\auto-rebuttal"
```

3. Restart Codex.

## Updating

```bash
cd ~/.codex/AutoRebuttal && git pull
```

Because Codex discovers the skill through the symlink / junction, updates flow through immediately after restart.

## Uninstalling

```bash
rm ~/.agents/skills/auto-rebuttal
```

Windows (PowerShell):

```powershell
Remove-Item "$env:USERPROFILE\.agents\skills\auto-rebuttal"
```

Optionally delete the clone:

```bash
rm -rf ~/.codex/AutoRebuttal
```

## Optional Manager CLI

If you prefer a Python-based helper instead of the native clone + junction path, the manager CLI is still available as an optional path:

```bash
python scripts/autorebuttal_manager.py codex install
python scripts/autorebuttal_manager.py codex update
python scripts/autorebuttal_manager.py codex remove
```

## Verify

```bash
ls -la ~/.agents/skills/auto-rebuttal
```

You should see a symlink (or a junction on Windows) pointing at your AutoRebuttal skill directory.
