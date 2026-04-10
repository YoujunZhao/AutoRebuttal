# SuperRebuttal Plugin-First Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reshape SuperRebuttal from a standalone skill repo into a plugin-first superpower package with verified Codex and Claude installation surfaces, truthful README claims, and tested rebuttal mode resolution for per-reviewer and shared-global budgeting.

**Architecture:** Move the canonical rebuttal engine from `skill/` into `skills/` so the repository can act like a superpower/plugin package. Add `.codex/INSTALL.md`, `.claude-plugin/` metadata, and a command entrypoint. Replace oversold venue claims with a small tested support surface: per-reviewer mode, shared-global mode, and checked reference notes for public venues.

**Tech Stack:** Markdown, JSON, Python 3 standard library, PowerShell, POSIX shell, git

---

### Task 1: Add failing tests for the plugin shell and honest support surface

**Files:**
- Create: `D:\rebuttalskill\.worktrees\plugin-first-redesign\tests\test_plugin_surface.py`
- Create: `D:\rebuttalskill\.worktrees\plugin-first-redesign\tests\test_response_modes.py`
- Modify: `D:\rebuttalskill\.worktrees\plugin-first-redesign\tests\test_skill_metadata.py`
- Modify: `D:\rebuttalskill\.worktrees\plugin-first-redesign\tests\test_install_wrappers.py`

- [ ] **Step 1: Write the failing plugin-surface test**

```python
import json
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


class PluginSurfaceTest(unittest.TestCase):
    def test_codex_install_doc_exists(self) -> None:
        install_doc = ROOT / ".codex" / "INSTALL.md"
        self.assertTrue(install_doc.exists())
        self.assertIn(".agents/skills", install_doc.read_text(encoding="utf-8"))

    def test_claude_plugin_metadata_exists(self) -> None:
        plugin_json = ROOT / ".claude-plugin" / "plugin.json"
        self.assertTrue(plugin_json.exists())
        payload = json.loads(plugin_json.read_text(encoding="utf-8"))
        self.assertEqual(payload["name"], "super-rebuttal")

    def test_command_entrypoint_exists(self) -> None:
        command = ROOT / "commands" / "rebuttal.md"
        self.assertTrue(command.exists())
```

- [ ] **Step 2: Write the failing response-mode test**

```python
import importlib.util
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


def load_module(module_name: str, path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {module_name} from {path}")
    spec.loader.exec_module(module)
    return module


class ResponseModesTest(unittest.TestCase):
    def test_explicit_per_reviewer_budget_resolves_per_reviewer(self) -> None:
        module = load_module(
            "response_modes",
            ROOT / "skills" / "super-rebuttal" / "scripts" / "response_modes.py",
        )
        mode = module.resolve_response_mode(
            venue=None,
            per_reviewer_limit=5000,
            total_limit=None,
            shared_response=False,
        )
        self.assertEqual(mode["mode"], "per-reviewer")

    def test_shared_budget_resolves_shared_global(self) -> None:
        module = load_module(
            "response_modes",
            ROOT / "skills" / "super-rebuttal" / "scripts" / "response_modes.py",
        )
        mode = module.resolve_response_mode(
            venue=None,
            per_reviewer_limit=None,
            total_limit=6000,
            shared_response=True,
        )
        self.assertEqual(mode["mode"], "shared-global")
```

- [ ] **Step 3: Update the metadata test to point at the future `skills/` location**

```python
ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "super-rebuttal"
```

Keep the rest of the test shape the same, but make it assert the new path.

- [ ] **Step 4: Replace the wrapper test with README truthfulness checks**

```python
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


class ReadmeTruthfulnessTest(unittest.TestCase):
    def test_readme_mentions_per_reviewer_and_shared_global_modes(self) -> None:
        content = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("per-reviewer", content)
        self.assertIn("shared-global", content)

    def test_readme_does_not_advertise_openclaw(self) -> None:
        content = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertNotIn("OpenClaw", content)
```

- [ ] **Step 5: Run the tests to verify they fail**

Run: `python -m unittest tests.test_plugin_surface tests.test_response_modes tests.test_skill_metadata tests.test_install_wrappers -v`
Expected: `FAIL` or `ERROR` because `.codex/`, `.claude-plugin/`, `commands/`, `skills/`, and `response_modes.py` do not exist yet.

- [ ] **Step 6: Commit the failing-test checkpoint**

```bash
git add tests/test_plugin_surface.py tests/test_response_modes.py tests/test_skill_metadata.py tests/test_install_wrappers.py
git commit -m "Define the plugin-first support surface before reshaping the repository

Constraint: README claims must stay narrower than what the repository can actually prove
Rejected: Keep testing only install wrappers | insufficient for the plugin-first redesign
Confidence: high
Scope-risk: narrow
Directive: New support claims must land with tests first
Tested: python -m unittest tests.test_plugin_surface tests.test_response_modes tests.test_skill_metadata tests.test_install_wrappers -v
Not-tested: implementation that will satisfy these tests"
```

### Task 2: Implement the plugin shell and move the rebuttal engine under `skills/`

**Files:**
- Create: `D:\rebuttalskill\.worktrees\plugin-first-redesign\.codex\INSTALL.md`
- Create: `D:\rebuttalskill\.worktrees\plugin-first-redesign\.claude-plugin\plugin.json`
- Create: `D:\rebuttalskill\.worktrees\plugin-first-redesign\.claude-plugin\marketplace.json`
- Create: `D:\rebuttalskill\.worktrees\plugin-first-redesign\commands\rebuttal.md`
- Create: `D:\rebuttalskill\.worktrees\plugin-first-redesign\skills\super-rebuttal\SKILL.md`
- Create: `D:\rebuttalskill\.worktrees\plugin-first-redesign\skills\super-rebuttal\references\input-contract.md`
- Create: `D:\rebuttalskill\.worktrees\plugin-first-redesign\skills\super-rebuttal\references\rebuttal-playbook.md`
- Create: `D:\rebuttalskill\.worktrees\plugin-first-redesign\skills\super-rebuttal\references\venue-policies.md`
- Create: `D:\rebuttalskill\.worktrees\plugin-first-redesign\skills\super-rebuttal\references\source-notes.md`
- Create: `D:\rebuttalskill\.worktrees\plugin-first-redesign\skills\super-rebuttal\examples\sample-input.md`
- Create: `D:\rebuttalskill\.worktrees\plugin-first-redesign\skills\super-rebuttal\examples\sample-output.md`
- Create: `D:\rebuttalskill\.worktrees\plugin-first-redesign\skills\super-rebuttal\scripts\__init__.py`
- Create: `D:\rebuttalskill\.worktrees\plugin-first-redesign\skills\super-rebuttal\scripts\install_skill.py`
- Create: `D:\rebuttalskill\.worktrees\plugin-first-redesign\skills\super-rebuttal\scripts\package_skill.py`
- Create: `D:\rebuttalskill\.worktrees\plugin-first-redesign\skills\super-rebuttal\scripts\validate_budget.py`
- Create: `D:\rebuttalskill\.worktrees\plugin-first-redesign\skills\super-rebuttal\scripts\response_modes.py`
- Delete: `D:\rebuttalskill\.worktrees\plugin-first-redesign\skill\super-rebuttal\SKILL.md`
- Delete: `D:\rebuttalskill\.worktrees\plugin-first-redesign\skill\super-rebuttal\agents\openai.yaml`
- Delete: `D:\rebuttalskill\.worktrees\plugin-first-redesign\skill\super-rebuttal\examples\sample-input.md`
- Delete: `D:\rebuttalskill\.worktrees\plugin-first-redesign\skill\super-rebuttal\examples\sample-output.md`
- Delete: `D:\rebuttalskill\.worktrees\plugin-first-redesign\skill\super-rebuttal\references\input-contract.md`
- Delete: `D:\rebuttalskill\.worktrees\plugin-first-redesign\skill\super-rebuttal\references\rebuttal-playbook.md`
- Delete: `D:\rebuttalskill\.worktrees\plugin-first-redesign\skill\super-rebuttal\references\source-notes.md`
- Delete: `D:\rebuttalskill\.worktrees\plugin-first-redesign\skill\super-rebuttal\references\venue-policies.md`
- Delete: `D:\rebuttalskill\.worktrees\plugin-first-redesign\skill\super-rebuttal\scripts\__init__.py`
- Delete: `D:\rebuttalskill\.worktrees\plugin-first-redesign\skill\super-rebuttal\scripts\install_skill.py`
- Delete: `D:\rebuttalskill\.worktrees\plugin-first-redesign\skill\super-rebuttal\scripts\package_skill.py`
- Delete: `D:\rebuttalskill\.worktrees\plugin-first-redesign\skill\super-rebuttal\scripts\validate_budget.py`

- [ ] **Step 1: Create `.codex/INSTALL.md`**

Use this content:

```markdown
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

3. Restart Codex.
```

- [ ] **Step 2: Create the Claude plugin metadata**

`plugin.json`

```json
{
  "name": "super-rebuttal",
  "description": "Plugin-first rebuttal workflow for Codex and Claude Code with evidence-first drafting and explicit budget modes",
  "version": "0.2.0",
  "author": {
    "name": "Youjun Zhao"
  },
  "homepage": "https://github.com/YoujunZhao/SuperRebuttal",
  "repository": "https://github.com/YoujunZhao/SuperRebuttal",
  "license": "MIT",
  "keywords": [
    "rebuttal",
    "peer-review",
    "academic-writing",
    "claude-code",
    "codex"
  ]
}
```

`marketplace.json`

```json
{
  "name": "super-rebuttal-dev",
  "description": "Development marketplace for the SuperRebuttal plugin",
  "owner": {
    "name": "Youjun Zhao"
  },
  "plugins": [
    {
      "name": "super-rebuttal",
      "description": "Plugin-first rebuttal workflow with tested per-reviewer and shared-global budgeting modes",
      "version": "0.2.0",
      "source": "./"
    }
  ]
}
```

- [ ] **Step 3: Create the command entrypoint**

`commands/rebuttal.md`

```markdown
---
description: "Start the SuperRebuttal workflow for a paper, reviews, and response constraints"
---

Use the `super-rebuttal` skill. First identify whether the author needs:

1. a per-reviewer response budget
2. one shared global rebuttal budget

If the venue format is not explicitly verified by the repository, ask for an explicit character or word limit and continue in generic mode.
```

- [ ] **Step 4: Move the canonical skill into `skills/super-rebuttal/`**

Copy the existing rebuttal content from `skill/super-rebuttal/` into the new `skills/super-rebuttal/` tree, then delete the old `skill/` copy.

The new `skills/super-rebuttal/SKILL.md` must keep the current evidence-first rules but remove Codex-only metadata such as `agents/openai.yaml`.

- [ ] **Step 5: Add `response_modes.py`**

Use this implementation:

```python
from __future__ import annotations


def resolve_response_mode(
    *,
    venue: str | None,
    per_reviewer_limit: int | None,
    total_limit: int | None,
    shared_response: bool,
) -> dict[str, object]:
    if per_reviewer_limit is not None:
        return {
            "mode": "per-reviewer",
            "reason": "explicit per-reviewer limit",
            "limit": per_reviewer_limit,
        }
    if shared_response or total_limit is not None:
        return {
            "mode": "shared-global",
            "reason": "shared response or explicit total limit",
            "limit": total_limit,
        }
    return {
        "mode": "needs-user-budget",
        "reason": "no verified venue-specific format or explicit limit",
        "limit": None,
    }
```

- [ ] **Step 6: Re-run the focused tests**

Run: `python -m unittest tests.test_plugin_surface tests.test_response_modes tests.test_skill_metadata tests.test_install_wrappers -v`
Expected: `PASS`

- [ ] **Step 7: Commit the plugin shell**

```bash
git add .codex/INSTALL.md .claude-plugin/plugin.json .claude-plugin/marketplace.json commands/rebuttal.md skills tests
git rm -r skill
git commit -m "Promote SuperRebuttal into a plugin-first package with a canonical skills tree

Constraint: Codex and Claude Code are the only first-class installation surfaces we can honestly advertise today
Rejected: Keep repo layout centered on manual skill-copy wrappers | wrong shape for the product goal
Confidence: high
Scope-risk: moderate
Directive: Keep plugin metadata and Codex install docs aligned with the actual repository layout
Tested: python -m unittest tests.test_plugin_surface tests.test_response_modes tests.test_skill_metadata tests.test_install_wrappers -v
Not-tested: live plugin installation inside Claude Code UI"
```

### Task 3: Rewrite the README and trim unsupported claims

**Files:**
- Modify: `D:\rebuttalskill\.worktrees\plugin-first-redesign\README.md`
- Delete: `D:\rebuttalskill\.worktrees\plugin-first-redesign\install\install-codex.ps1`
- Delete: `D:\rebuttalskill\.worktrees\plugin-first-redesign\install\install-codex.sh`
- Delete: `D:\rebuttalskill\.worktrees\plugin-first-redesign\install\install-claude-code.ps1`
- Delete: `D:\rebuttalskill\.worktrees\plugin-first-redesign\install\install-claude-code.sh`
- Delete: `D:\rebuttalskill\.worktrees\plugin-first-redesign\install\install-openclaw.ps1`
- Delete: `D:\rebuttalskill\.worktrees\plugin-first-redesign\install\install-openclaw.sh`
- Modify: `D:\rebuttalskill\.worktrees\plugin-first-redesign\tests\test_install_wrappers.py`

- [ ] **Step 1: Replace the old wrapper test with README-content assertions**

Use this file content:

```python
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


class ReadmeTruthfulnessTest(unittest.TestCase):
    def test_readme_mentions_codex_install_doc(self) -> None:
        content = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn(".codex/INSTALL.md", content)

    def test_readme_mentions_two_verified_budgeting_modes(self) -> None:
        content = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("per-reviewer", content)
        self.assertIn("shared-global", content)

    def test_readme_does_not_claim_openclaw_support(self) -> None:
        content = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertNotIn("OpenClaw", content)
```

- [ ] **Step 2: Run the README test to verify it fails**

Run: `python -m unittest tests.test_install_wrappers -v`
Expected: `FAIL` because the current README still advertises the old skill-first and OpenClaw-first framing.

- [ ] **Step 3: Rewrite the README**

The new README must:

- start with English / Chinese anchors that render correctly
- describe the repository as a plugin-first superpower package
- explain the workflow:
  - install
  - provide paper + reviews
  - choose budget mode
  - map reviewer concerns
  - draft strategy
  - draft rebuttal
  - keep placeholders for missing evidence
- document Codex install through `.codex/INSTALL.md`
- document Claude plugin metadata and local marketplace shape truthfully
- avoid claiming official public marketplace availability unless already true
- distinguish:
  - checked venue reference notes
  - tested output modes
  - generic fallback mode

Use wording like this in the support section:

```markdown
## Verified Support Today

- Codex installation via `.codex/INSTALL.md`
- Claude Code plugin metadata via `.claude-plugin/plugin.json`
- Per-reviewer budgeting mode
- Shared-global budgeting mode

## Generic Fallback

If your venue is not explicitly covered, provide either:

- a per-reviewer limit, or
- one shared total limit
```

- [ ] **Step 4: Delete the old install wrappers**

Run:

```bash
git rm -r install
```

- [ ] **Step 5: Re-run the README and full test suite**

Run: `python -m unittest discover -s tests -v`
Expected: `PASS`

- [ ] **Step 6: Commit the documentation and cleanup**

```bash
git add README.md tests/test_install_wrappers.py
git commit -m "Rewrite SuperRebuttal around a truthful plugin workflow and verified support surface

Constraint: README should only promise installation surfaces and rebuttal modes we can demonstrate
Rejected: Keep broad venue and tool claims with caveats | still too misleading
Confidence: high
Scope-risk: moderate
Directive: Treat unsupported venues as manual-budget workflows unless a tested format lands
Tested: python -m unittest discover -s tests -v
Not-tested: real Codex fetch-from-URL install and private Claude marketplace distribution"
```

### Task 4: Final verification and review handoff

**Files:**
- Modify: `D:\rebuttalskill\.worktrees\plugin-first-redesign\docs\superpowers\plans\2026-04-10-super-rebuttal-plugin-redesign.md`

- [ ] **Step 1: Rebuild the distributable helper artifact**

Run: `python skills/super-rebuttal/scripts/package_skill.py`
Expected: `dist/super-rebuttal.zip` is created from the new `skills/` path.

- [ ] **Step 2: Run syntax and compile checks**

Run:

```bash
python -m py_compile skills/super-rebuttal/scripts/__init__.py skills/super-rebuttal/scripts/install_skill.py skills/super-rebuttal/scripts/package_skill.py skills/super-rebuttal/scripts/validate_budget.py skills/super-rebuttal/scripts/response_modes.py tests/test_plugin_surface.py tests/test_response_modes.py tests/test_install_wrappers.py
```

Expected: no output, exit code 0.

- [ ] **Step 3: Request code review**

Use superpowers:requesting-code-review against the full diff from `f1d4571` to `HEAD`.

- [ ] **Step 4: Apply any required fixes and re-run tests**

Run: `python -m unittest discover -s tests -v`
Expected: `PASS`

- [ ] **Step 5: Prepare branch completion**

Use superpowers:finishing-a-development-branch after tests and review are clean.
