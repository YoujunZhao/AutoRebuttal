# SuperRebuttal Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a cross-tool rebuttal skill package that installs into Codex, Claude Code, and OpenClaw, ships venue-aware rebuttal guidance, and includes standard-library helper scripts for install, packaging, and budget validation.

**Architecture:** Keep one canonical skill at `skill/super-rebuttal/`, then wrap it with thin cross-platform installers under `install/`. Use Python standard-library helpers for copying, packaging, and text-budget validation. Protect the helpers with `unittest` so the skill repo stays dependency-light and portable.

**Tech Stack:** Markdown, YAML, Python 3 standard library, PowerShell, POSIX shell, git

---

### Task 1: Bootstrap the repository and test harness

**Files:**
- Create: `D:\rebuttalskill\.gitignore`
- Create: `D:\rebuttalskill\LICENSE`
- Create: `D:\rebuttalskill\README.md`
- Create: `D:\rebuttalskill\skill\super-rebuttal\scripts\__init__.py`
- Create: `D:\rebuttalskill\tests\__init__.py`
- Create: `D:\rebuttalskill\tests\test_skill_metadata.py`

- [ ] **Step 1: Write the failing metadata test**

```python
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skill" / "super-rebuttal"


class SkillMetadataTest(unittest.TestCase):
    def test_required_files_exist(self) -> None:
        self.assertTrue((SKILL_DIR / "SKILL.md").exists())
        self.assertTrue((SKILL_DIR / "agents" / "openai.yaml").exists())
        self.assertTrue((SKILL_DIR / "references" / "venue-policies.md").exists())
        self.assertTrue((SKILL_DIR / "references" / "rebuttal-playbook.md").exists())
        self.assertTrue((SKILL_DIR / "references" / "input-contract.md").exists())
        self.assertTrue((SKILL_DIR / "references" / "source-notes.md").exists())


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m unittest tests.test_skill_metadata -v`
Expected: `FAIL` because the skill directory and required files do not exist yet.

- [ ] **Step 3: Create the minimal bootstrap files**

```text
.gitignore
LICENSE
README.md
skill/super-rebuttal/scripts/__init__.py
tests/__init__.py
```

Use this `.gitignore` content:

```gitignore
__pycache__/
*.pyc
.pytest_cache/
dist/
build/
.DS_Store
Thumbs.db
```

Use MIT license text in `LICENSE`.

- [ ] **Step 4: Re-run the metadata test**

Run: `python -m unittest tests.test_skill_metadata -v`
Expected: `FAIL` again, but now only because the actual skill files still do not exist.

- [ ] **Step 5: Commit the bootstrap**

```bash
git add .gitignore LICENSE README.md skill/super-rebuttal/scripts/__init__.py tests/__init__.py tests/test_skill_metadata.py
git commit -m "Prepare a clean scaffold for the SuperRebuttal skill

Constraint: Repository must stay dependency-light and cross-platform
Rejected: Start with a prompt-only repo | insufficient for cross-tool installability
Confidence: high
Scope-risk: narrow
Directive: Keep the canonical skill under skill/super-rebuttal and add wrappers around it
Tested: python -m unittest tests.test_skill_metadata -v
Not-tested: installer scripts and packaging helpers"
```

### Task 2: Implement the Python helper scripts with tests first

**Files:**
- Create: `D:\rebuttalskill\skill\super-rebuttal\scripts\install_skill.py`
- Create: `D:\rebuttalskill\skill\super-rebuttal\scripts\validate_budget.py`
- Create: `D:\rebuttalskill\skill\super-rebuttal\scripts\package_skill.py`
- Create: `D:\rebuttalskill\tests\test_install_skill.py`
- Create: `D:\rebuttalskill\tests\test_validate_budget.py`
- Create: `D:\rebuttalskill\tests\test_package_skill.py`

- [ ] **Step 1: Write the failing install helper test**

```python
import importlib.util
import pathlib
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]

def load_module(module_name: str, path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    spec.loader.exec_module(module)
    return module


class InstallSkillTest(unittest.TestCase):
    def test_install_skill_copies_required_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            source = pathlib.Path(tmpdir) / "source"
            target = pathlib.Path(tmpdir) / "target"
            (source / "agents").mkdir(parents=True)
            (source / "references").mkdir(parents=True)
            (source / "SKILL.md").write_text("---\nname: super-rebuttal\ndescription: Use when drafting rebuttals\n---\n", encoding="utf-8")
            (source / "agents" / "openai.yaml").write_text("interface:\n  display_name: SuperRebuttal\n", encoding="utf-8")
            module = load_module(
                "install_skill",
                ROOT / "skill" / "super-rebuttal" / "scripts" / "install_skill.py",
            )
            module.install_skill(source=source, destination=target)
            self.assertTrue((target / "SKILL.md").exists())
            self.assertTrue((target / "agents" / "openai.yaml").exists())


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Write the failing budget validator test**

```python
import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]

def load_module(module_name: str, path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    spec.loader.exec_module(module)
    return module


class ValidateBudgetTest(unittest.TestCase):
    def test_measure_budget_counts_characters(self) -> None:
        module = load_module(
            "validate_budget",
            ROOT / "skill" / "super-rebuttal" / "scripts" / "validate_budget.py",
        )
        result = module.measure_budget("Reviewer 1: Thanks!", limit=30, mode="chars")
        self.assertEqual(result["used"], 19)
        self.assertEqual(result["remaining"], 11)
        self.assertFalse(result["overflow"])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 3: Write the failing packaging test**

```python
import importlib.util
import pathlib
import tempfile
import unittest
import zipfile

ROOT = pathlib.Path(__file__).resolve().parents[1]


def load_module(module_name: str, path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    spec.loader.exec_module(module)
    return module


class PackageSkillTest(unittest.TestCase):
    def test_build_archive_contains_skill_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = pathlib.Path(tmpdir)
            skill_dir = root / "skill" / "super-rebuttal"
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text("stub", encoding="utf-8")
            module = load_module(
                "package_skill",
                ROOT / "skill" / "super-rebuttal" / "scripts" / "package_skill.py",
            )
            archive = module.build_archive(skill_dir=skill_dir, dist_dir=root / "dist")
            with zipfile.ZipFile(archive) as zf:
                self.assertIn("super-rebuttal/SKILL.md", zf.namelist())


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 4: Run the helper tests to verify they fail**

Run: `python -m unittest tests.test_install_skill tests.test_validate_budget tests.test_package_skill -v`
Expected: `ERROR` because the helper modules do not exist yet.

- [ ] **Step 5: Implement the helper modules**

`install_skill.py`

```python
from __future__ import annotations

import argparse
import pathlib
import shutil


def install_skill(source: pathlib.Path, destination: pathlib.Path) -> pathlib.Path:
    if not source.exists():
        raise FileNotFoundError(f"Skill source does not exist: {source}")
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(source, destination)
    return destination


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--destination", required=True)
    args = parser.parse_args()
    install_skill(pathlib.Path(args.source), pathlib.Path(args.destination))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

`validate_budget.py`

```python
from __future__ import annotations

import argparse
import json


def measure_budget(text: str, limit: int, mode: str = "chars") -> dict[str, int | bool | str]:
    if mode not in {"chars", "words"}:
        raise ValueError(f"Unsupported mode: {mode}")
    used = len(text) if mode == "chars" else len(text.split())
    remaining = limit - used
    return {
        "mode": mode,
        "limit": limit,
        "used": used,
        "remaining": remaining,
        "overflow": remaining < 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", required=True)
    parser.add_argument("--limit", required=True, type=int)
    parser.add_argument("--mode", default="chars")
    args = parser.parse_args()
    print(json.dumps(measure_budget(args.text, args.limit, args.mode), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

`package_skill.py`

```python
from __future__ import annotations

import pathlib
import zipfile


def build_archive(skill_dir: pathlib.Path, dist_dir: pathlib.Path) -> pathlib.Path:
    dist_dir.mkdir(parents=True, exist_ok=True)
    archive_path = dist_dir / "super-rebuttal.zip"
    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in skill_dir.rglob("*"):
            if path.is_file():
                zf.write(path, pathlib.Path("super-rebuttal") / path.relative_to(skill_dir))
    return archive_path


def main() -> int:
    root = pathlib.Path(__file__).resolve().parents[1]
    build_archive(skill_dir=root, dist_dir=root.parents[1] / "dist")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 6: Re-run the helper tests**

Run: `python -m unittest tests.test_install_skill tests.test_validate_budget tests.test_package_skill -v`
Expected: `PASS`

- [ ] **Step 7: Commit the helper layer**

```bash
git add skill/super-rebuttal/scripts/install_skill.py skill/super-rebuttal/scripts/validate_budget.py skill/super-rebuttal/scripts/package_skill.py tests/test_install_skill.py tests/test_validate_budget.py tests/test_package_skill.py
git commit -m "Add portable helper scripts for installation, packaging, and budget checks

Constraint: Use only the Python standard library
Rejected: Depend on click or pytest | unnecessary runtime and setup burden
Confidence: high
Scope-risk: narrow
Directive: Keep helper behavior explicit and file-copy based so tool adapters stay thin
Tested: python -m unittest tests.test_install_skill tests.test_validate_budget tests.test_package_skill -v
Not-tested: end-to-end install wrappers on each shell"
```

### Task 3: Author the canonical skill package and research references

**Files:**
- Create: `D:\rebuttalskill\skill\super-rebuttal\SKILL.md`
- Create: `D:\rebuttalskill\skill\super-rebuttal\agents\openai.yaml`
- Create: `D:\rebuttalskill\skill\super-rebuttal\references\input-contract.md`
- Create: `D:\rebuttalskill\skill\super-rebuttal\references\rebuttal-playbook.md`
- Create: `D:\rebuttalskill\skill\super-rebuttal\references\venue-policies.md`
- Create: `D:\rebuttalskill\skill\super-rebuttal\references\source-notes.md`
- Create: `D:\rebuttalskill\skill\super-rebuttal\examples\sample-input.md`
- Create: `D:\rebuttalskill\skill\super-rebuttal\examples\sample-output.md`
- Modify: `D:\rebuttalskill\tests\test_skill_metadata.py`

- [ ] **Step 1: Expand the metadata test so it checks frontmatter and display metadata**

```python
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skill" / "super-rebuttal"


class SkillMetadataTest(unittest.TestCase):
    def test_skill_frontmatter_is_present(self) -> None:
        content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("name: super-rebuttal", content)
        self.assertIn("description:", content)

    def test_openai_yaml_has_display_metadata(self) -> None:
        content = (SKILL_DIR / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertIn("display_name:", content)
        self.assertIn("short_description:", content)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the metadata test to verify it fails**

Run: `python -m unittest tests.test_skill_metadata -v`
Expected: `ERROR` or `FAIL` because the canonical skill files are still missing.

- [ ] **Step 3: Write `SKILL.md` with the workflow contract**

The file must include:

```markdown
---
name: super-rebuttal
description: Use when drafting a conference or journal rebuttal from a paper, reviews, and venue constraints, especially when the response must stay polite, evidence-based, venue-aware, and free of fabricated experiments or numbers.
---

# Super Rebuttal

## Overview

Turn a paper, a review set, and venue constraints into a rebuttal plan and final response.

## Required behavior

- Read the paper or paper summary first.
- Convert each review into atomic concerns.
- Infer reviewer personas.
- Load venue rules from `references/venue-policies.md`.
- Never invent experimental numbers.
- Use placeholders like `XX` and `[RESULT-TO-FILL]` when results are missing.
```

- [ ] **Step 4: Write `agents/openai.yaml`**

```yaml
interface:
  display_name: "SuperRebuttal"
  short_description: "Draft venue-aware academic rebuttals without fabricating evidence"
  default_prompt: "Use this skill to analyze a paper, reviews, and venue constraints, then produce a rebuttal strategy and final rebuttal text while avoiding fabricated experiments or numbers."
```

- [ ] **Step 5: Write the reference files**

`references/input-contract.md` should define accepted inputs, fallback modes, and output variants.

`references/rebuttal-playbook.md` should define:

- concern extraction
- reviewer persona mapping
- shared-issue consolidation
- response-strategy selection
- tone and evidence rules
- placeholder policy

`references/venue-policies.md` should contain dated sections for:

- ICLR 2025 and 2026
- NeurIPS 2025
- ICML 2025 and 2026
- ARR / ACL / EMNLP
- Generic OpenReview defaults

`references/source-notes.md` should cite the research and project references gathered during brainstorming.

- [ ] **Step 6: Add realistic examples**

`examples/sample-input.md`

```markdown
# Sample Input

- Venue: ICML 2026
- Constraint: 5000 characters per response
- Reviewer 1: "The novelty over prior graph transformers is unclear..."
- Reviewer 2: "Ablations on XX are missing..."
- Author note: "Do not promise new experiments beyond placeholders."
```

`examples/sample-output.md`

```markdown
# Sample Output

## Constraint Summary
- Venue rule: ICML 2026, 5000 characters per response

## Reviewer 2
We thank the reviewer for highlighting the missing ablation. We agree that this analysis would strengthen the paper. In the rebuttal, we will add a concise clarification of the current evidence and, if space permits, include a placeholder summary such as `XX` for the planned result rather than inventing numbers.
```

- [ ] **Step 7: Re-run the metadata test**

Run: `python -m unittest tests.test_skill_metadata -v`
Expected: `PASS`

- [ ] **Step 8: Commit the canonical skill content**

```bash
git add skill/super-rebuttal/SKILL.md skill/super-rebuttal/agents/openai.yaml skill/super-rebuttal/references/input-contract.md skill/super-rebuttal/references/rebuttal-playbook.md skill/super-rebuttal/references/venue-policies.md skill/super-rebuttal/references/source-notes.md skill/super-rebuttal/examples/sample-input.md skill/super-rebuttal/examples/sample-output.md tests/test_skill_metadata.py
git commit -m "Encode the SuperRebuttal workflow and venue-aware reference base

Constraint: Skill must stay usable across Codex, Claude Code, and OpenClaw
Rejected: Hard-code one conference template | too brittle for real rebuttal workflows
Confidence: high
Scope-risk: moderate
Directive: Keep policy notes dated and let explicit user constraints override built-in defaults
Tested: python -m unittest tests.test_skill_metadata -v
Not-tested: live invocation inside each host tool"
```

### Task 4: Add shell installers and complete the bilingual documentation

**Files:**
- Create: `D:\rebuttalskill\install\install-codex.ps1`
- Create: `D:\rebuttalskill\install\install-codex.sh`
- Create: `D:\rebuttalskill\install\install-claude-code.ps1`
- Create: `D:\rebuttalskill\install\install-claude-code.sh`
- Create: `D:\rebuttalskill\install\install-openclaw.ps1`
- Create: `D:\rebuttalskill\install\install-openclaw.sh`
- Modify: `D:\rebuttalskill\README.md`
- Modify: `D:\rebuttalskill\tests\test_install_skill.py`

- [ ] **Step 1: Extend the install test to verify the shell adapters call the Python helper with the expected target layout**

```python
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


class InstallWrapperTest(unittest.TestCase):
    def test_codex_installer_mentions_default_user_path(self) -> None:
        content = (ROOT / "install" / "install-codex.ps1").read_text(encoding="utf-8")
        self.assertIn(".codex", content)
        self.assertIn("super-rebuttal", content)

    def test_claude_installer_mentions_default_user_path(self) -> None:
        content = (ROOT / "install" / "install-claude-code.sh").read_text(encoding="utf-8")
        self.assertIn(".claude/skills", content)

    def test_openclaw_installer_mentions_default_user_path(self) -> None:
        content = (ROOT / "install" / "install-openclaw.sh").read_text(encoding="utf-8")
        self.assertIn(".openclaw", content)
```

- [ ] **Step 2: Run the install test to verify it fails**

Run: `python -m unittest tests.test_install_skill -v`
Expected: `FAIL` because the wrapper scripts do not exist yet.

- [ ] **Step 3: Add the install wrapper scripts**

`install/install-codex.ps1`

```powershell
$root = Split-Path -Parent $PSScriptRoot
$source = Join-Path $root "skill/super-rebuttal"
$target = Join-Path $HOME ".codex/skills/super-rebuttal"
python (Join-Path $source "scripts/install_skill.py") --source $source --destination $target
Write-Host "Installed SuperRebuttal to $target"
```

`install/install-codex.sh`

```sh
#!/usr/bin/env sh
set -eu
root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
source_dir="$root/skill/super-rebuttal"
target_dir="${HOME}/.codex/skills/super-rebuttal"
python "$source_dir/scripts/install_skill.py" --source "$source_dir" --destination "$target_dir"
printf 'Installed SuperRebuttal to %s\n' "$target_dir"
```

Repeat the same pattern for:

- Claude Code target: `$HOME/.claude/skills/super-rebuttal`
- OpenClaw target: `$HOME/.openclaw/skills/super-rebuttal`

- [ ] **Step 4: Replace the placeholder README with the full bilingual guide**

The README must include:

- English / Chinese anchor links at the top
- project overview
- why the skill exists
- supported tools
- install commands for Codex, Claude Code, and OpenClaw
- example invocation prompts
- supported venues
- limitations
- research references

Use concrete install examples like:

```markdown
[English](#english) | [Chinese](#chinese)

## English

### Install for Codex

```powershell
./install/install-codex.ps1
```

### Install for Claude Code

```bash
./install/install-claude-code.sh
```
```

- [ ] **Step 5: Re-run the test suite**

Run: `python -m unittest discover -s tests -v`
Expected: `PASS`

- [ ] **Step 6: Build the distributable archive**

Run: `python skill/super-rebuttal/scripts/package_skill.py`
Expected: `dist/super-rebuttal.zip` is created.

- [ ] **Step 7: Commit the final product surface**

```bash
git add README.md install/install-codex.ps1 install/install-codex.sh install/install-claude-code.ps1 install/install-claude-code.sh install/install-openclaw.ps1 install/install-openclaw.sh
git commit -m "Make SuperRebuttal easy to install and use across three agent ecosystems

Constraint: The same canonical skill must drive all tool adapters
Rejected: Separate divergent copies per tool | higher drift and maintenance cost
Confidence: medium
Scope-risk: moderate
Directive: Keep README examples in sync with the install wrappers and canonical skill path
Tested: python -m unittest discover -s tests -v; python skill/super-rebuttal/scripts/package_skill.py
Not-tested: real host-tool UI discovery after manual installation"
```

### Task 5: Verify, initialize git hosting, and publish privately

**Files:**
- Modify: `D:\rebuttalskill\README.md`
- Modify: `D:\rebuttalskill\skill\super-rebuttal\references\source-notes.md`

- [ ] **Step 1: Run a final repository check**

Run: `python -m unittest discover -s tests -v`
Expected: all tests pass.

- [ ] **Step 2: Run quick skill validation**

Run: `python C:\Users\A\.codex\skills\.system\skill-creator\scripts\quick_validate.py D:\rebuttalskill\skill\super-rebuttal`
Expected: validation passes.

- [ ] **Step 3: Initialize git and create the default branch**

Run:

```bash
git init
git checkout -b codex/super-rebuttal
git add .
git commit -m "Ship the first installable SuperRebuttal skill

Constraint: Initial release must stay private while the workflow stabilizes
Rejected: Publish publicly before cross-tool validation | too risky for early iteration
Confidence: medium
Scope-risk: broad
Directive: Re-verify venue policy notes before each public release because rebuttal rules drift by year
Tested: python -m unittest discover -s tests -v; quick_validate.py D:\\rebuttalskill\\skill\\super-rebuttal
Not-tested: live invocation against a real rebuttal packet in each host tool"
```

- [ ] **Step 4: Create the private GitHub repository and push**

Run:

```bash
git remote add origin https://github.com/<username>/SuperRebuttal.git
git push -u origin codex/super-rebuttal
```

Expected: repository exists as private and the branch is pushed successfully.
