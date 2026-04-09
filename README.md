<a id="top"></a>

# SuperRebuttal

[English](#english) | [中文](#chinese)

SuperRebuttal is a private-first skill package for drafting academic rebuttals and author responses across multiple agent ecosystems. The canonical skill lives in `skill/super-rebuttal`, and the thin installer wrappers in `install/` copy that one source of truth into Codex, Claude Code, or OpenClaw.

The project is intended to stay private during initial development and internal use. The repository layout is suitable for later publication, but the expected operating model for the first phase is a private repository with controlled distribution.

<a id="english"></a>

## English

### Purpose

SuperRebuttal exists to make rebuttal drafting more structured, venue-aware, and evidence-first. Instead of relying on one-off prompts, it packages a reusable workflow that helps an agent:

- read the manuscript or manuscript summary
- normalize reviewer comments into concrete issues
- map issues to likely reviewer concerns
- draft polite, specific responses without inventing experiments or numbers
- respect venue or user-provided response limits

### Key Features

- Canonical skill packaging under `skill/super-rebuttal` so all tools install the same artifact.
- Thin wrappers under `install/` that call `skill/super-rebuttal/scripts/install_skill.py`.
- Cross-tool default targets:
  - Codex: `$HOME/.codex/skills/super-rebuttal`
  - Claude Code: `$HOME/.claude/skills/super-rebuttal`
  - OpenClaw: `$HOME/.openclaw/skills/super-rebuttal`
- Evidence-first drafting stance that explicitly avoids fabricated experiments, fabricated gains, or unsupported citations.
- Venue-aware positioning for common ML/AI rebuttal settings such as ICLR, NeurIPS, ICML, and ARR / ACL / EMNLP style author responses.
- Support for reviewer-by-reviewer drafting, shared issue grouping, and budget-aware response shaping.

### Supported Tools

- Codex
- Claude Code
- OpenClaw

Each tool should consume the same canonical skill contents. The wrappers are intentionally thin so behavior stays aligned across ecosystems.

### Supported Venues

SuperRebuttal is designed for rebuttal workflows common in:

- ICLR
- NeurIPS
- ICML
- ARR / ACL / EMNLP-style author responses
- Generic OpenReview response forms
- Journal response letters when the user provides explicit constraints

Venue policies drift from year to year. Treat bundled policy guidance as a starting point, then verify the exact official rules for the target venue and cycle before submission.

### Installation

Prerequisites:

- Python 3 available as `python`, `python3`, or Windows `py -3`
- A complete checkout that includes the canonical skill at `skill/super-rebuttal`
- Permission to write to your user-level skills directory

#### Install for Codex

Default destination: `$HOME/.codex/skills/super-rebuttal`

PowerShell:

```powershell
./install/install-codex.ps1
```

POSIX shell:

```sh
./install/install-codex.sh
```

Optional custom destination:

```powershell
./install/install-codex.ps1 -Destination "$HOME/.codex/skills/super-rebuttal"
```

```sh
./install/install-codex.sh "$HOME/.codex/skills/super-rebuttal"
```

#### Install for Claude Code

Default destination: `$HOME/.claude/skills/super-rebuttal`

PowerShell:

```powershell
./install/install-claude-code.ps1
```

POSIX shell:

```sh
./install/install-claude-code.sh
```

Optional custom destination:

```powershell
./install/install-claude-code.ps1 -Destination "$HOME/.claude/skills/super-rebuttal"
```

```sh
./install/install-claude-code.sh "$HOME/.claude/skills/super-rebuttal"
```

#### Install for OpenClaw

Default destination: `$HOME/.openclaw/skills/super-rebuttal`

PowerShell:

```powershell
./install/install-openclaw.ps1
```

POSIX shell:

```sh
./install/install-openclaw.sh
```

Optional custom destination:

```powershell
./install/install-openclaw.ps1 -Destination "$HOME/.openclaw/skills/super-rebuttal"
```

```sh
./install/install-openclaw.sh "$HOME/.openclaw/skills/super-rebuttal"
```

### How the Install Wrappers Work

All six wrappers do the same three things:

1. Resolve the repository root relative to the wrapper location.
2. Point at the canonical skill source in `skill/super-rebuttal`.
3. Call `skill/super-rebuttal/scripts/install_skill.py` with `--source` and `--destination`.

That keeps the install surface simple and avoids maintaining divergent copies of the skill for different tools.

### How to Invoke the Skill

After installation, use your host tool's normal skill workflow and reference `super-rebuttal` by name. Exact UI wording varies by tool version, but the practical sequence is:

1. Open the tool where the skill was installed.
2. Select or invoke the `super-rebuttal` skill using that tool's native skill interface.
3. Provide manuscript context, reviewer comments, venue or journal constraints, and any response budget.
4. Ask for either a strategy-first outline or a final rebuttal draft.

Recommended input bundle:

- paper PDF or extracted manuscript text
- reviewer comments
- venue and year, if known
- global or per-review character / word budget
- any hard constraints such as "do not promise new experiments"

### Sample Prompts

- `Use super-rebuttal. I will paste the abstract, main claims, and three reviewer comments for ICLR 2026. First produce an issue map and response strategy, then draft the rebuttal.`
- `Use super-rebuttal to draft reviewer-by-reviewer responses for NeurIPS. Do not invent new experiments. If evidence is missing, use placeholders such as [RESULT-TO-FILL].`
- `Use super-rebuttal. The venue is unknown, but I have a limit of 5000 characters per reviewer. Help me cluster shared concerns before drafting prose.`
- `Use super-rebuttal for a journal revision letter. Keep the tone formal, acknowledge genuine limitations, and separate changes already completed from changes promised for the revision.`

### What the Skill Should Help Produce

- a constraint summary
- a reviewer issue map
- grouped shared concerns across reviewers
- response strategy notes
- final rebuttal text
- explicit placeholders for missing evidence rather than fabricated claims

### Limitations

- It does not run experiments.
- It does not fetch private reviews from conference systems.
- It should not invent gains, p-values, new baselines, or citations.
- Venue policies may change yearly, so users must verify the current official rules.
- Final submission formatting and compliance remain the author's responsibility.
- Tool-specific skill discovery UX may evolve, even though the canonical skill stays the same.

### Research Basis and Positioning

SuperRebuttal is positioned as an evidence-first writing aid, not an autonomous publication agent. Its design is grounded in two practical sources of guidance:

- public author-response and rebuttal instructions from major ML / NLP venues and journal workflows
- common rebuttal best practices such as answering reviewer concerns directly, acknowledging limitations plainly, and separating existing evidence from promised follow-up work

The intended reference base for the canonical skill includes venue-policy notes and source citations tracked alongside the skill content. Because policy language changes over time, the safe operating rule is: use the built-in guidance to structure the draft, then confirm the exact venue/year requirements against the official public source before submitting.

### Repository Status

- Private-first by design for the initial release cycle
- Meant to be shared selectively before any public publication
- Structured so a later public release does not require reworking the installation model

[Back to top](#top)

<a id="chinese"></a>

## 中文

### 项目目的

SuperRebuttal 用来把学术 rebuttal / author response 的起草流程做成可复用、可安装、可跨工具迁移的技能包。它不是一次性的提示词，而是一套更稳定的工作流，帮助代理：

- 阅读论文或论文摘要
- 将 reviewer comments 拆成可执行的问题项
- 识别问题背后的常见审稿关注点
- 在不虚构实验、不虚构数字的前提下起草礼貌且具体的回复
- 按照会议或用户提供的篇幅限制组织内容

### 核心特性

- 以 `skill/super-rebuttal` 作为唯一规范技能目录，避免多工具之间内容漂移。
- `install/` 下的薄封装脚本统一调用 `skill/super-rebuttal/scripts/install_skill.py`。
- 三个默认安装目标：
  - Codex：`$HOME/.codex/skills/super-rebuttal`
  - Claude Code：`$HOME/.claude/skills/super-rebuttal`
  - OpenClaw：`$HOME/.openclaw/skills/super-rebuttal`
- 强调 evidence-first：不捏造实验、不捏造提升、不补写并不存在的引用。
- 面向常见 ML / AI rebuttal 场景，适配 ICLR、NeurIPS、ICML、ARR / ACL / EMNLP 等常见 author response 工作流。
- 支持 reviewer-by-reviewer 回复、共享问题合并、以及预算约束下的篇幅控制。

### 支持的工具

- Codex
- Claude Code
- OpenClaw

三个工具都应安装同一个 canonical skill。安装脚本故意保持很薄，只负责把同一份技能复制到不同工具的技能目录。

### 支持的场景与 venue

SuperRebuttal 主要面向以下类型的回复场景：

- ICLR
- NeurIPS
- ICML
- ARR / ACL / EMNLP 风格的 author response
- 通用 OpenReview rebuttal / response 表单
- 用户已明确给出约束的期刊回复信

不同 venue、不同年份的规则会变化。内置 guidance 只能作为起点，真正提交前仍应核对目标 venue 和年份的官方最新规则。

### 安装说明

前置条件：

- 机器上可用 Python 3，命令形式可以是 `python`、`python3` 或 Windows 下的 `py -3`
- 仓库中包含 canonical skill 目录 `skill/super-rebuttal`
- 当前用户对目标技能目录有写权限

#### 安装到 Codex

默认目标：`$HOME/.codex/skills/super-rebuttal`

PowerShell：

```powershell
./install/install-codex.ps1
```

POSIX shell：

```sh
./install/install-codex.sh
```

自定义目标：

```powershell
./install/install-codex.ps1 -Destination "$HOME/.codex/skills/super-rebuttal"
```

```sh
./install/install-codex.sh "$HOME/.codex/skills/super-rebuttal"
```

#### 安装到 Claude Code

默认目标：`$HOME/.claude/skills/super-rebuttal`

PowerShell：

```powershell
./install/install-claude-code.ps1
```

POSIX shell：

```sh
./install/install-claude-code.sh
```

自定义目标：

```powershell
./install/install-claude-code.ps1 -Destination "$HOME/.claude/skills/super-rebuttal"
```

```sh
./install/install-claude-code.sh "$HOME/.claude/skills/super-rebuttal"
```

#### 安装到 OpenClaw

默认目标：`$HOME/.openclaw/skills/super-rebuttal`

PowerShell：

```powershell
./install/install-openclaw.ps1
```

POSIX shell：

```sh
./install/install-openclaw.sh
```

自定义目标：

```powershell
./install/install-openclaw.ps1 -Destination "$HOME/.openclaw/skills/super-rebuttal"
```

```sh
./install/install-openclaw.sh "$HOME/.openclaw/skills/super-rebuttal"
```

### 安装脚本的工作方式

六个 wrapper 的逻辑完全一致：

1. 根据脚本所在位置反推出仓库根目录。
2. 固定指向 `skill/super-rebuttal` 这一份 canonical source。
3. 调用 `skill/super-rebuttal/scripts/install_skill.py`，并传入 `--source` 与 `--destination`。

这样可以保证 Codex、Claude Code、OpenClaw 安装的都是同一份技能内容，而不是三套分叉副本。

### 如何调用技能

安装完成后，在对应工具里通过该工具自己的技能入口调用 `super-rebuttal`。不同版本的 UI 文案可能不同，但实际使用流程基本一致：

1. 打开已经安装该技能的工具。
2. 在该工具的原生技能入口中选择或调用 `super-rebuttal`。
3. 提供论文上下文、reviewer comments、venue 或期刊约束、以及字数 / 字符预算。
4. 先让它输出 strategy-first 大纲，或直接要求生成最终 rebuttal 草稿。

建议提供的输入材料：

- 论文 PDF 或提取后的正文文本
- reviewer comments
- venue 与年份（如果知道）
- 总体或按 reviewer 划分的字数 / 字符限制
- 明确约束，例如 “不要承诺新实验”

### 示例提示词

- `Use super-rebuttal. I will paste the abstract, main claims, and three reviewer comments for ICLR 2026. First produce an issue map and response strategy, then draft the rebuttal.`
- `Use super-rebuttal to draft reviewer-by-reviewer responses for NeurIPS. Do not invent new experiments. If evidence is missing, use placeholders such as [RESULT-TO-FILL].`
- `Use super-rebuttal. The venue is unknown, but I have a limit of 5000 characters per reviewer. Help me cluster shared concerns before drafting prose.`
- `Use super-rebuttal for a journal revision letter. Keep the tone formal, acknowledge genuine limitations, and separate changes already completed from changes promised for the revision.`

### 预期输出

- 约束摘要
- reviewer 问题地图
- 跨 reviewer 的共享问题归并
- 回复策略说明
- 最终 rebuttal 文本
- 对缺失证据使用显式占位符，而不是虚构内容

### 限制

- 不会替你运行实验。
- 不会从投稿系统抓取私有评论。
- 不应该虚构提升数字、统计显著性、新 baseline 或不存在的引用。
- venue 规则会逐年变化，最终仍需作者自己核对官方要求。
- 最终提交格式与合规责任仍在作者本人。
- 即使 canonical skill 不变，不同工具的技能发现 UI 也可能变化。

### 研究依据与定位

SuperRebuttal 的定位是 evidence-first 的写作辅助工具，而不是自动化投稿代理。它的设计依据主要来自两类公开且可解释的来源：

- 主要 ML / NLP venue 与期刊工作流中的公开 rebuttal / author response 说明
- 常见 rebuttal 写作实践，例如逐条回应 reviewer concern、明确承认限制、把已有证据与未来计划严格区分

canonical skill 预期会把 venue policy notes 与 source citations 跟随技能内容一起维护。由于这些政策文本会持续变化，最稳妥的做法是：先用技能组织结构化草稿，再对照目标 venue / 年份的官方公开规则做最终检查。

### 仓库状态

- 初始阶段按 private-first 使用方式设计
- 预期先做受控分发，再考虑公开发布
- 仓库结构已经为后续公开化预留了空间，不需要重新设计安装模型

[返回顶部](#top)
