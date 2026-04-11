# SuperRebuttal

[English README](README.md)

SuperRebuttal 是一个面向 coding agent 的 rebuttal 工作流包。仓库采用 `plugin-first` 组织方式，把安装入口、`super-rebuttal` skill、命令入口、说明文档和测试一起放在同一个可安装包里。

它的目标很窄也很明确：帮助作者把论文、reviews 和明确的 rebuttal 约束整理成结构化、证据优先、不会伪造实验结果或引用的回应草稿。

当前包也支持把 review PDF 作为输入材料，因此 paper PDF 和 review PDF 都可以直接进入工作流。

## 它是什么

SuperRebuttal 不是一个单独复制出去的 skill 文件夹，而是一个可以安装、再按工作流调用的 rebuttal package。

设计原则保持保守：

- 先整理 reviewer concerns，再写 prose
- 未验证的 venue 不假装“内置支持”
- 缺失证据用 `XX` 或 `[RESULT-TO-FILL]` 这样的占位符，而不是编造数字
- 安装声明和能力声明都只写仓库已经证明的范围
- 在写最终 draft 之前先做 reviewer stance / attitude analysis
- 在 reviewer-by-reviewer prose 之前先形成全局 strategy memo

## How It Works

当作者把论文和 reviews 交给 agent 时，SuperRebuttal 不会直接跳到最终文案，而是先判断回复格式、整理 reviewer concerns、分析 reviewer stance / attitude、形成全局策略，再生成草稿。

实际流程通常是：

1. 在宿主工具中安装这个包
2. 提供论文上下文、paper PDF，以及可选的 review PDF
3. 明确回复模式和预算
4. 生成 reviewer cards，分析 reviewer stance / attitude
5. 归并共享 reviewer concerns
6. 先形成 global strategy memo
7. 先分配字符预算
8. 再生成最终 rebuttal 文本
9. 对缺失证据保留显式占位符

这层 reviewer cards / reviewer stance / global strategy memo 的加入，就是这次“更像人写的 rebuttal”升级的核心。

## Installation

仓库现在提供统一的 manager CLI，按宿主工具划分安装方式。

### Codex

Codex 子命令会对用户主目录下的 skill 路径执行真实的 install/update/remove 文件系统操作：

```bash
python scripts/superrebuttal_manager.py codex install
python scripts/superrebuttal_manager.py codex update
python scripts/superrebuttal_manager.py codex remove
```

默认目标路径是 `~/.agents/skills/super-rebuttal`。更详细的说明见 [`.codex/INSTALL.md`](.codex/INSTALL.md)。

### Claude Code

仓库仍然提供 Claude 风格的 plugin shell：

- [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json)
- [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json)

Claude 侧的 manager CLI 采用 print-only 方式，按照 Claude plugin command model 输出需要手动执行的官方命令：

```bash
python scripts/superrebuttal_manager.py claude install
python scripts/superrebuttal_manager.py claude update
python scripts/superrebuttal_manager.py claude remove
```

安装时会打印：

```text
/plugin marketplace add YoujunZhao/SuperRebuttal
/plugin install super-rebuttal@super-rebuttal-dev
```

项目目前 **不** 声称已经发布到公开官方 marketplace。仓库已经验证的是插件元数据结构和本地 marketplace 形态，而不是公开上架状态。

## How To Use It

安装完成后，常见的调用方式有两种：

- **Use the `rebuttal` command**
- **Use the `super-rebuttal` skill**

不同宿主工具的 UI 会有差异，但核心意图相同：先让 agent 进入 SuperRebuttal 工作流，再提供论文、reviews 和预算约束。

### What is the difference between `rebuttal` and `super-rebuttal`?

- **`rebuttal`**
  这是更直接的命令式入口，适合快速开始。

- **`super-rebuttal`**
  这是底层的 skill / workflow engine，适合显式要求 agent 使用完整流程。

简而言之，`rebuttal` 是前门，`super-rebuttal` 是真正驱动流程的引擎。

### Invocation Examples

Use the `rebuttal` command:

```text
Use the `rebuttal` command. I will paste the abstract, the main claims, and three reviewer comments. This is per-reviewer mode with 5000 characters each.
```

Use the `super-rebuttal` skill:

```text
Use the `super-rebuttal` skill. This is a shared-global mode rebuttal with a total limit of 6000 characters. First cluster shared concerns, then draft the final response.
```

如果 venue 规则不清楚，就直接给明确预算：

```text
Use the `super-rebuttal` skill. Ignore venue defaults and use per-reviewer mode with 4000 characters per reviewer.
```

## The Basic Workflow

1. **Install SuperRebuttal** 到 Codex 或 Claude 风格的插件环境。
2. **Provide inputs**：paper PDF、review PDF、正文文本或可靠摘要，以及 reviews。
3. **Choose a budgeting mode**：
   - `per-reviewer mode`
   - `shared-global mode`
4. **Generate the issue map**，再要求最终 prose。
5. **Draft the rebuttal**，保持 evidence-first。
6. **Mark missing evidence explicitly**，不要编造。

### The Two Tested Budgeting Modes

- **`per-reviewer mode`**
  适合每位 reviewer 都有单独回复预算的情况，例如“每位 reviewer 5000 字符”。

- **`shared-global mode`**
  适合所有 reviewer 共享一个总预算的情况，例如“总共 6000 字符”。

## Verified Support Today

今天仓库只应把以下内容表述为“已验证支持”：

- Repo-level manager CLI via [`scripts/superrebuttal_manager.py`](scripts/superrebuttal_manager.py)
- Codex installation via [`.codex/INSTALL.md`](.codex/INSTALL.md)
- Claude plugin shell metadata via [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json)
- Local Claude marketplace metadata via [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json)
- A command entrypoint via [`commands/rebuttal.md`](commands/rebuttal.md)
- `per-reviewer mode`
- `shared-global mode`

## What's Inside

### Package Shell

- [`scripts/superrebuttal_manager.py`](scripts/superrebuttal_manager.py)
- [`.codex/INSTALL.md`](.codex/INSTALL.md)
- [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json)
- [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json)
- [`commands/rebuttal.md`](commands/rebuttal.md)

### Canonical Rebuttal Engine

- [`skills/super-rebuttal/SKILL.md`](skills/super-rebuttal/SKILL.md)
- [`skills/super-rebuttal/scripts/response_modes.py`](skills/super-rebuttal/scripts/response_modes.py)
- [`skills/super-rebuttal/scripts/install_skill.py`](skills/super-rebuttal/scripts/install_skill.py)
- [`skills/super-rebuttal/scripts/package_skill.py`](skills/super-rebuttal/scripts/package_skill.py)
- [`skills/super-rebuttal/scripts/validate_budget.py`](skills/super-rebuttal/scripts/validate_budget.py)

### Reference Material

- [`skills/super-rebuttal/references/input-contract.md`](skills/super-rebuttal/references/input-contract.md)
- [`skills/super-rebuttal/references/rebuttal-playbook.md`](skills/super-rebuttal/references/rebuttal-playbook.md)
- [`skills/super-rebuttal/references/venue-policies.md`](skills/super-rebuttal/references/venue-policies.md)
- [`skills/super-rebuttal/references/source-notes.md`](skills/super-rebuttal/references/source-notes.md)

## Limitations

- 不会运行实验
- 不会抓取投稿系统里的私有 reviews
- 不会声称支持所有会议 rebuttal 格式
- 不会把参考说明写成自动化能力
- 不会声称已发布到 Claude 官方 marketplace
- 不保证提分
