<a id="top"></a>

# SuperRebuttal

[English](#english) | [中文](#chinese)

SuperRebuttal is a private-first, plugin-shaped rebuttal workflow package. The repository is the product: it contains the installation surfaces, the internal `super-rebuttal` skill, the prompt entrypoint, the reference notes, and the tests that define what we can honestly claim today.

The goal is not to market a magical "supports every conference" assistant. The goal is to provide a truthful, evidence-first rebuttal workflow that:

- installs like a small superpower package instead of a lone copied skill
- helps authors map reviewer concerns before drafting prose
- supports two tested budgeting modes
- refuses to fabricate experiments, numbers, or citations

<a id="english"></a>

## English

### What This Project Is

SuperRebuttal is a plugin-first workflow package for rebuttal drafting. Internally it still uses a skill, but the user-facing model is:

1. install the package
2. provide manuscript context and reviews
3. choose a rebuttal budgeting mode
4. generate a strategy-first issue map
5. draft the final rebuttal text

That shape is intentionally closer to `superpowers` than to a standalone "copy this skill folder" repo.

### Workflow

The expected flow is:

1. Install SuperRebuttal into your host tool.
2. Give the agent the paper PDF, manuscript text, or a faithful manuscript summary.
3. Paste the reviews.
4. Decide how the response is budgeted:
   - `per-reviewer mode`
   - `shared-global mode`
5. Let the workflow cluster reviewer concerns and shared issues.
6. Review the strategy-first output.
7. Ask for final prose.
8. Keep unresolved evidence as placeholders such as `XX` or `[RESULT-TO-FILL]`.

### Verified Support Today

These are the only things the repository should present as verified support today:

- Codex installation via [` .codex/INSTALL.md `](D:/rebuttalskill/.worktrees/plugin-first-redesign/.codex/INSTALL.md)
- Claude plugin shell metadata via [` .claude-plugin/plugin.json `](D:/rebuttalskill/.worktrees/plugin-first-redesign/.claude-plugin/plugin.json)
- Local Claude marketplace metadata via [` .claude-plugin/marketplace.json `](D:/rebuttalskill/.worktrees/plugin-first-redesign/.claude-plugin/marketplace.json)
- A command entrypoint via [` commands/rebuttal.md `](D:/rebuttalskill/.worktrees/plugin-first-redesign/commands/rebuttal.md)
- `per-reviewer mode`
- `shared-global mode`

### Checked Reference Notes, Not Full Venue Guarantees

The repository includes checked reference notes for:

- ICLR
- NeurIPS
- ICML
- ARR-style author responses

Those notes live under [`venue-policies.md`](D:/rebuttalskill/.worktrees/plugin-first-redesign/skills/super-rebuttal/references/venue-policies.md). They are reference material, not a promise that every venue-specific rebuttal format is fully automated or fully tested.

### Generic Fallback

If your venue is not explicitly covered, or if you do not trust the bundled venue notes for your current cycle, use explicit budgeting:

- `per-reviewer mode`
  Example: "Reply to each reviewer with 5000 characters."
- `shared-global mode`
  Example: "Reply to all reviewers together within 6000 characters."

The shared-global path is the right fallback for CV-style or forum-style rebuttals where all reviewers are answered in one combined response.

### Installation

#### Codex

The intended Codex entrypoint is [` .codex/INSTALL.md `](D:/rebuttalskill/.worktrees/plugin-first-redesign/.codex/INSTALL.md).

The "Superpowers-style" install instruction is:

```text
Fetch and follow instructions from https://raw.githubusercontent.com/YoujunZhao/SuperRebuttal/refs/heads/codex/plugin-first-redesign/.codex/INSTALL.md
```

Manual install remains documented in that file for clone + symlink / junction setups.

#### Claude Code

This repository now includes the plugin shell expected by Claude-style plugin packaging:

- [` .claude-plugin/plugin.json `](D:/rebuttalskill/.worktrees/plugin-first-redesign/.claude-plugin/plugin.json)
- [` .claude-plugin/marketplace.json `](D:/rebuttalskill/.worktrees/plugin-first-redesign/.claude-plugin/marketplace.json)

Important: the repository is still private and is **not** claiming public official marketplace publication. What is verified today is the plugin-shaped metadata and local marketplace layout, not a public marketplace listing.

### How To Use It

After installation, invoke the internal `super-rebuttal` workflow or the [`rebuttal` command](D:/rebuttalskill/.worktrees/plugin-first-redesign/commands/rebuttal.md), then provide:

- manuscript context
- reviews
- venue name and year, if known
- one explicit budget mode if the venue format is not already clear
- any hard constraints such as "do not promise new experiments"

### Sample Prompts

- `Use super-rebuttal. I have a shared-global mode rebuttal with a total budget of 6000 characters. First cluster the shared concerns, then draft the response.`
- `Use super-rebuttal. This is per-reviewer mode with 5000 characters for each reviewer. Do not invent any new experiment results.`
- `Use super-rebuttal. The venue notes are uncertain, so ignore built-in venue assumptions and use the explicit budget I provide.`

### What The Internal Skill Does

The canonical skill now lives at [`skills/super-rebuttal`](D:/rebuttalskill/.worktrees/plugin-first-redesign/skills/super-rebuttal).

It is responsible for:

- issue extraction
- reviewer persona reasoning
- shared-issue consolidation
- response drafting
- placeholder-based handling for missing evidence

The tested mode-selection logic lives in [`response_modes.py`](D:/rebuttalskill/.worktrees/plugin-first-redesign/skills/super-rebuttal/scripts/response_modes.py).

### What This Project Does Not Claim

- It does not claim official public Claude marketplace publication.
- It does not claim support for every conference rebuttal format.
- It does not claim automatic experiment execution.
- It does not claim that reference notes alone equal tested venue support.
- It does not claim guaranteed score improvement.

### Research Basis

The workflow is grounded in:

- public venue instructions
- public rebuttal studies and datasets
- explicit non-fabrication rules

See:

- [`source-notes.md`](D:/rebuttalskill/.worktrees/plugin-first-redesign/skills/super-rebuttal/references/source-notes.md)
- [`rebuttal-playbook.md`](D:/rebuttalskill/.worktrees/plugin-first-redesign/skills/super-rebuttal/references/rebuttal-playbook.md)
- [`input-contract.md`](D:/rebuttalskill/.worktrees/plugin-first-redesign/skills/super-rebuttal/references/input-contract.md)

### Repository Status

- private-first
- plugin-first
- truthful about verified vs fallback support

[Back to top](#top)

<a id="chinese"></a>

## 中文

### 这个项目现在是什么

SuperRebuttal 现在被重构成一个 **plugin-first / superpower 风格** 的 rebuttal 工作流包，而不是“单独拷贝一个 skill 目录”的仓库。

对用户来说，它的使用方式应该是：

1. 先安装这个包
2. 提供论文和 reviews
3. 选择回复预算模式
4. 先得到 strategy-first 的问题图谱
5. 再生成最终 rebuttal 文本

### 工作流

推荐流程如下：

1. 安装 SuperRebuttal
2. 提供论文 PDF、正文文本，或者可信的论文摘要
3. 粘贴 reviews
4. 选择预算模式：
   - `per-reviewer mode`
   - `shared-global mode`
5. 让工作流先做 reviewer concern 归并
6. 检查 strategy-first 输出
7. 再要求生成最终 rebuttal
8. 对缺失证据使用 `XX`、`[RESULT-TO-FILL]` 之类的占位符

### 今天真正验证过的支持范围

目前这个仓库只应该宣称下面这些“已验证支持”：

- 通过 [` .codex/INSTALL.md `](D:/rebuttalskill/.worktrees/plugin-first-redesign/.codex/INSTALL.md) 进行 Codex 安装
- 具备 Claude plugin 形态的 [` .claude-plugin/plugin.json `](D:/rebuttalskill/.worktrees/plugin-first-redesign/.claude-plugin/plugin.json)
- 具备本地 Claude marketplace 形态的 [` .claude-plugin/marketplace.json `](D:/rebuttalskill/.worktrees/plugin-first-redesign/.claude-plugin/marketplace.json)
- 具备命令入口 [` commands/rebuttal.md `](D:/rebuttalskill/.worktrees/plugin-first-redesign/commands/rebuttal.md)
- `per-reviewer mode`
- `shared-global mode`

### 已核对的 venue 参考，不等于“完整自动支持”

仓库里现在带有核对过的公开参考说明，覆盖：

- ICLR
- NeurIPS
- ICML
- ARR 风格 author response

这些内容位于 [`venue-policies.md`](D:/rebuttalskill/.worktrees/plugin-first-redesign/skills/super-rebuttal/references/venue-policies.md)。它们是 **参考说明**，不是“这个 venue 已被完整自动化支持”的保证。

### 通用降级方案

如果你的 venue 不在已核对范围内，或者你不想依赖内置 venue notes，就直接手动给预算：

- `per-reviewer mode`
  例如：“每个 reviewer 回复 5000 字符”
- `shared-global mode`
  例如：“所有 reviewer 合起来总共 6000 字符”

对于很多 CV 风格、统一回复框风格的 rebuttal，这种 `shared-global mode` 就是更稳妥的通用路径。

### 安装方式

#### Codex

Codex 的入口现在是 [` .codex/INSTALL.md `](D:/rebuttalskill/.worktrees/plugin-first-redesign/.codex/INSTALL.md)。

推荐直接告诉 Codex：

```text
Fetch and follow instructions from https://raw.githubusercontent.com/YoujunZhao/SuperRebuttal/refs/heads/codex/plugin-first-redesign/.codex/INSTALL.md
```

#### Claude Code

这个仓库现在已经具备 Claude plugin 风格的外壳：

- [` .claude-plugin/plugin.json `](D:/rebuttalskill/.worktrees/plugin-first-redesign/.claude-plugin/plugin.json)
- [` .claude-plugin/marketplace.json `](D:/rebuttalskill/.worktrees/plugin-first-redesign/.claude-plugin/marketplace.json)

但这里要说清楚：当前仓库仍然是 private，并且 **没有** 宣称已经上架到公开官方 marketplace。现在已验证的是“插件结构”和“本地 marketplace 形态”，不是公开上架状态。

### 如何使用

安装后，可以调用内部的 `super-rebuttal` workflow，或者使用 [`rebuttal` 命令入口](D:/rebuttalskill/.worktrees/plugin-first-redesign/commands/rebuttal.md)，然后提供：

- 论文上下文
- reviews
- venue 和年份（如果知道）
- 如果 venue 规则不明确，就直接给预算模式
- 额外硬约束，例如“不要承诺新实验”

### 示例提示词

- `Use super-rebuttal. I have a shared-global mode rebuttal with a total budget of 6000 characters. First cluster the shared concerns, then draft the response.`
- `Use super-rebuttal. This is per-reviewer mode with 5000 characters for each reviewer. Do not invent any new experiment results.`
- `Use super-rebuttal. The venue notes are uncertain, so ignore built-in venue assumptions and use the explicit budget I provide.`

### 这个项目不再宣称什么

- 不再宣称支持 OpenClaw
- 不再宣称“支持所有会议 rebuttal 格式”
- 不再把 venue 参考说明写成“完整支持”
- 不再暗示已经公开上架到 Claude 官方 marketplace
- 不会替作者跑实验

### 研究与规则依据

核心依据仍然是：

- 公开 venue 规则
- 公开 rebuttal 研究和数据集
- 明确的 non-fabrication 规则

可参考：

- [`source-notes.md`](D:/rebuttalskill/.worktrees/plugin-first-redesign/skills/super-rebuttal/references/source-notes.md)
- [`rebuttal-playbook.md`](D:/rebuttalskill/.worktrees/plugin-first-redesign/skills/super-rebuttal/references/rebuttal-playbook.md)
- [`input-contract.md`](D:/rebuttalskill/.worktrees/plugin-first-redesign/skills/super-rebuttal/references/input-contract.md)

### 当前状态

- private-first
- plugin-first
- 只宣传已验证支持，未验证部分统一走显式 budget fallback

[返回顶部](#top)
