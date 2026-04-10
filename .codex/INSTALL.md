# Installing SuperRebuttal for Codex

Tell Codex:

```text
Fetch and follow instructions from https://raw.githubusercontent.com/YoujunZhao/SuperRebuttal/refs/heads/codex/plugin-first-redesign/.codex/INSTALL.md
```

## Manual Install

1. Clone the repo:

```bash
git clone https://github.com/YoujunZhao/SuperRebuttal.git ~/.codex/super-rebuttal
```

2. Create the skill symlink:

```bash
mkdir -p ~/.agents/skills
ln -s ~/.codex/super-rebuttal/skills/super-rebuttal ~/.agents/skills/super-rebuttal
```

**Windows (PowerShell):**

```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.agents\skills"
cmd /c mklink /J "$env:USERPROFILE\.agents\skills\super-rebuttal" "$env:USERPROFILE\.codex\super-rebuttal\skills\super-rebuttal"
```

3. Restart Codex.

## Verify

```bash
ls -la ~/.agents/skills/super-rebuttal
```

You should see a symlink or junction pointing at this repository's `skills/super-rebuttal` directory.
