# AutoRebuttal

[English README](README.md)

AutoRebuttal 是一个面向 coding agent 的 rebuttal workflow package。仓库采用 `plugin-first` 组织方式，把安装入口、`auto-rebuttal` skill、命令入口、参考资料和测试放在同一个可安装包里。

它的目标很直接：帮助作者把论文、reviews、review PDF、rebuttal PDF 和明确的 rebuttal 约束整理成结构化、证据优先、不会伪造实验结果或引用的回复草稿。

## 现在怎么调用

最直接的调用方式就是两条命令：

```text
/rebuttal venue=ICML per_reviewer=5000
```

```text
/rebuttal_revise venue=ICML per_reviewer=5000
```

含义是：

- `/rebuttal`
  从 paper + reviews 起草 rebuttal
- `/rebuttal_revise`
  对已经写好的 rebuttal 做润色、压缩和结构整理

也可以显式调用 skill：

```text
Use the `auto-rebuttal` skill. Per-reviewer mode with 5000 characters each. Do not invent any experiment results.
```

## 输入支持

### `/rebuttal`

支持这些输入：

- `paper PDF`
- `review PDF`
- `review text`

系统会自动检测 review 是 PDF 还是文本。

### `/rebuttal_revise`

支持这些输入：

- `rebuttal PDF`
- `rebuttal text`
- optional `paper PDF`

系统会自动检测 rebuttal 是 PDF 还是文本。

## PDF 识别

现在不是只会“看到 PDF 就报错”了。

AutoRebuttal 的 PDF 读取顺序是：

1. 先尝试读取 PDF 自带文本层
2. 如果没有文本层，就先把 PDF 渲染成页面图片
3. 再用本机已有的 OCR 路径自动识别图片文字
4. 只有 OCR 也失败时，review PDF 才会退回到 rendered-page-only fallback

也就是说：

- 图像型 `review PDF` 现在会先自动 OCR
- 图像型 `rebuttal PDF` 现在也会先自动 OCR

如果 reviewer 需要实验支持，仍然用 `XX` 或 experiment placeholder table，而不是编造数字。

## How It Works

默认流程是：

1. 安装到宿主工具
2. 提供 paper / review / rebuttal 输入
3. 自动检测是 PDF 还是文本
4. 如果 PDF 没有文本层，就先 OCR
5. 构建 reviewer outline，保留 `W1 / W2 / W3`、`Q1 / Q2 / Q3`、`M1 / M2 / M3`
6. 生成 reviewer cards
7. 归并 shared issues
8. 生成 global strategy memo
9. 分配字符预算
10. 起草或润色 rebuttal

## Human-Like Rebuttal Layer

当前版本包含：

- **reviewer outline**：保留 `W#`、`Q#`、`M# / minor`
- **reviewer cards**：分析 reviewer stance、movability、attitude、primary concerns
- **global strategy memo**：先组织共享问题，再写 reviewer-by-reviewer prose
- **character-budget planning**：先控预算，再生成文本
- **block formatter**：让 `W1`、`Q1`、`M1` 各自占一行

`W1`、`Q1`、`M1` 默认都应该单独占一行，不应该和上一句正文挤在同一段里。

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

## Installation

### Codex

```bash
python scripts/autorebuttal_manager.py codex install
python scripts/autorebuttal_manager.py codex update
python scripts/autorebuttal_manager.py codex remove
```

默认目标路径是：

```text
~/.agents/skills/auto-rebuttal
```

### Claude Code

```bash
python scripts/autorebuttal_manager.py claude install
python scripts/autorebuttal_manager.py claude update
python scripts/autorebuttal_manager.py claude remove
```

对应的本地 plugin 命令是：

```text
/plugin marketplace add YoujunZhao/AutoRebuttal
/plugin install auto-rebuttal@auto-rebuttal-dev
```

## Verified Support Today

当前可以诚实写进 README 的已验证能力包括：

- repo-level manager CLI：[`scripts/autorebuttal_manager.py`](scripts/autorebuttal_manager.py)
- Codex 安装说明：[`.codex/INSTALL.md`](.codex/INSTALL.md)
- Claude plugin metadata：[`.claude-plugin/plugin.json`](.claude-plugin/plugin.json)
- Claude marketplace metadata：[`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json)
- 命令入口：[`commands/rebuttal.md`](commands/rebuttal.md)
- 命令入口：[`commands/rebuttal_revise.md`](commands/rebuttal_revise.md)
- review/rebuttal PDF 与 text 自动检测
- OCR-backed PDF reading
- `per-reviewer mode`
- `shared-global mode`

## Limitations

- 不会运行实验
- 不会自动抓取投稿系统中的私有 reviews
- 不会为没有证据的结论编造数字
- OCR 是 best-effort，不保证所有扫描质量都能稳定识别
- 如果 rebuttal PDF 没有文本层且 OCR 也失败，`/rebuttal_revise` 会明确报错而不是假装成功
