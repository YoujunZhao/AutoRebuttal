# SuperRebuttal

[English README](README.md)

SuperRebuttal 是一个面向 coding agent 的 rebuttal workflow package。仓库采用 `plugin-first` 组织方式，把安装入口、`super-rebuttal` skill、命令入口、参考资料和测试放在同一个可安装包里。

它的目标很直接：帮助作者把论文、reviews、review PDF 和明确的 rebuttal 约束整理成结构化、证据优先、不会伪造实验结果或引用的回复草稿。

当前版本已经支持把 review PDF 作为一等输入。如果 review PDF 是图像型而不是文本型，系统会先走 rendered page images 回退路径，而不是直接失败。

## 它是什么

SuperRebuttal 不是一个单独拷贝出去的 skill 文件夹，而是一个可安装、可调用、可测试的 rebuttal package。

设计原则是：

- 先做 issue extraction，再写 prose
- 用户参数优先于 venue 默认值
- 缺失证据时使用 `XX`、`[RESULT-TO-FILL]` 或 experiment placeholder table，而不是编造数字
- 先做 reviewer stance 和 global strategy，再写最终 draft
- 默认输出更像人类作者的点对点 rebuttal，而不是泛化模板

## How It Works

当作者把 paper 和 reviews 交给 agent 时，SuperRebuttal 不会直接跳到最终文字，而是先组织 review concerns，再决定格式和预算，最后才生成 rebuttal。

默认流程是：

1. 安装到宿主工具
2. 提供论文上下文、paper PDF、review PDF 或 review 文本
3. 判断 venue 规则和 budget mode
4. 构建 reviewer outline，保留 `W1 / W2 / W3`、`Q1 / Q2 / Q3` 和 `minor` 结构
5. 如果 review PDF 是 image_fallback，先检查 rendered page images，再进入 reviewer cards
6. 生成 reviewer cards，分析 reviewer stance、movability、attitude 和 primary concerns
7. 归并 shared issues
8. 生成 global strategy memo
9. 分配字符预算
10. 生成最终 rebuttal draft
11. 对无法证明的内容保留占位符

这意味着真正的 live path 不再只是“读 review text -> 直接写回复”，而是先保留 point-to-point outline，再进入后续分析。

## Human-Like Rebuttal Layer

当前版本包含：

- **reviewer outline**：保留 `W#`、`Q#`、`M# / minor`
- **reviewer cards**：分析 reviewer stance、movability、attitude、primary concerns
- **global strategy memo**：先组织共享问题，再写 reviewer-by-reviewer prose
- **character-budget planning**：先控预算，再生成文本

如果 reviewer 要求补实验，系统可以插入 experiment placeholder table，并把结果写成 `XX`，而不是伪造数字。

## Venue-Aware Formatting Defaults

- **ICLR**
  默认先给一小段 global summary，再进入 reviewer blocks
- **ICML**
  默认不加总述，直接 reviewer blocks，默认 `5000` 字符 / reviewer
- **NeurIPS**
  默认不加总述，直接 reviewer blocks，默认 `10000` 字符 / reviewer
- **AAAI**
  默认不加总述，直接 reviewer blocks，默认 `2500` 字符 / reviewer
- **CVPR / ICCV / ECCV**
  默认先给所有 reviewer 的 summary，再进入 reviewer blocks，并按一页 rebuttal PDF 左右的规模规划

在每个 reviewer block 里，默认格式应该是：

- `W1 / W2 / W3`
- `Q1 / Q2 / Q3`
- `M1 / M2 / M3`

如果 minor 很相似，也可以合并成一个 `Minor points` 段落。

对 OpenReview 风格的 review，parser 现在会识别：

- `Main Weaknesses`
- `Key Questions For Authors`
- `Questions For Authors`
- `Minor Weaknesses`
- `Minor comments`

并且会跳过 `Official Review of Submission...` 这类 preamble，不再把它误判成 `W1`。

## Installation

### Codex

Codex 侧通过 manager CLI 执行真实的 install / update / remove：

```bash
python scripts/superrebuttal_manager.py codex install
python scripts/superrebuttal_manager.py codex update
python scripts/superrebuttal_manager.py codex remove
```

默认目标路径是 `~/.agents/skills/super-rebuttal`。更多说明见 [`.codex/INSTALL.md`](.codex/INSTALL.md)。

### Claude Code

仓库包含 Claude 风格的 plugin shell：

- [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json)
- [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json)

manager CLI 会打印 Claude 侧应该运行的命令：

```bash
python scripts/superrebuttal_manager.py claude install
python scripts/superrebuttal_manager.py claude update
python scripts/superrebuttal_manager.py claude remove
```

本地安装命令是：

```text
/plugin marketplace add YoujunZhao/SuperRebuttal
/plugin install super-rebuttal@super-rebuttal-dev
```

## How To Use It

安装后，常见入口有两种：

- **Use the `rebuttal` command**
- **Use the `super-rebuttal` skill**

区别是：

- `rebuttal`
  更适合直接启动 workflow
- `super-rebuttal`
  是底层 skill / engine，适合显式调用完整流程

### Invocation Examples

```text
/rebuttal venue=ICML per_reviewer=5000
```

```text
Use the `super-rebuttal` skill. Per-reviewer mode with 5000 characters each. Do not invent any experiment results.
```

## The Basic Workflow

1. **Install SuperRebuttal**
2. **Provide inputs**
   可以是 paper PDF、review PDF、摘要、正文文本或 review 文本
3. **Choose a budgeting mode**
   - `per-reviewer mode`
   - `shared-global mode`
4. **Generate the issue map**
   先保留 reviewer outline，再生成 reviewer cards
5. **Draft the rebuttal**
6. **Mark missing evidence explicitly**

### The Two Tested Budgeting Modes

- **`per-reviewer mode`**
  适合每位 reviewer 各自有字符预算的场景
- **`shared-global mode`**
  适合所有 reviewer 共用一个总预算的场景

## Verified Support Today

当前可以诚实写进 README 的已验证能力包括：

- repo-level manager CLI：[`scripts/superrebuttal_manager.py`](scripts/superrebuttal_manager.py)
- Codex 安装说明：[`.codex/INSTALL.md`](.codex/INSTALL.md)
- Claude plugin metadata：[`.claude-plugin/plugin.json`](.claude-plugin/plugin.json)
- Claude marketplace metadata：[`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json)
- 命令入口：[`commands/rebuttal.md`](commands/rebuttal.md)
- `per-reviewer mode`
- `shared-global mode`
- review PDF support
- rendered page images fallback

## What's Inside

### Package Shell

- [`scripts/superrebuttal_manager.py`](scripts/superrebuttal_manager.py)
- [`.codex/INSTALL.md`](.codex/INSTALL.md)
- [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json)
- [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json)
- [`commands/rebuttal.md`](commands/rebuttal.md)

### Canonical Rebuttal Engine

- [`skills/super-rebuttal/SKILL.md`](skills/super-rebuttal/SKILL.md)
- [`skills/super-rebuttal/scripts/build_input_bundle.py`](skills/super-rebuttal/scripts/build_input_bundle.py)
- [`skills/super-rebuttal/scripts/render_review_pdf_pages.py`](skills/super-rebuttal/scripts/render_review_pdf_pages.py)
- [`skills/super-rebuttal/scripts/build_reviewer_outline.py`](skills/super-rebuttal/scripts/build_reviewer_outline.py)
- [`skills/super-rebuttal/scripts/build_reviewer_cards.py`](skills/super-rebuttal/scripts/build_reviewer_cards.py)
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
- 不会自动抓取投稿系统中的私有 reviews
- 不会为没有证据的结论编造数字
- 不会声称支持所有会议的 rebuttal 格式
- image_fallback 只能把 review 保留下来，后续仍需要图像检查来生成 outline
- 不保证提分
