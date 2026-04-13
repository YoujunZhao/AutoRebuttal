# AutoRebuttal

[English README](README.md)

AutoRebuttal 是一个面向 coding agent 的 rebuttal workflow package。仓库把安装入口、`auto-rebuttal` skill、命令入口、参考资料和测试放在同一个可安装包里，并且尽量只陈述仓库今天已经被代码和测试证明的能力。

它的目标很直接：帮助作者把论文、reviews 和明确的 rebuttal 约束整理成结构化、证据优先、不会伪造实验结果或引用的回复草稿。

当前仓库已经证明的论文输入路径有三种：

- `paper PDF`
- 提取后的 paper text 或手工提供的 paper text
- LaTeX 论文输入：单个 `.tex` 文件，或包含 `.tex` 文件的目录

review 输入仍然是 `review PDF` 或 review text。`/rebuttal_revise` 仍然从 existing rebuttal PDF 或 rebuttal text 开始。OCR 也只应被理解为仓库里已经实现的 rendered-page fallback 路径，而不是任意 PDF 都能稳定识别的泛化能力。

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
  对已经写好的 existing rebuttal 做润色、压缩和结构整理

也可以显式调用 skill：

```text
Use the `auto-rebuttal` skill. Per-reviewer mode with 5000 characters each. Do not invent any experiment results.
```

## 输入支持

### `/rebuttal`

支持这些输入：

- `paper PDF`
- `paper text`
- `paper_input` 指向的单个 `.tex`
- `paper_input` 指向的 LaTeX project directory
- `review PDF`
- `review text`

系统会自动检测每个 review 是 PDF 还是文本。对于 paper，PDF / text / LaTeX 是不同的检测路径。

### `/rebuttal_revise`

支持这些输入：

- `rebuttal PDF`
- `rebuttal text`
- optional `paper PDF`
- optional `paper text`
- optional LaTeX paper

系统会自动检测 rebuttal 是 PDF 还是文本；可选 paper 仍然可以是 PDF、text 或 LaTeX。

## PDF 识别

AutoRebuttal 当前实现的 PDF 读取顺序是：

1. 先尝试读取 PDF 自带文本层
2. 如果没有文本层，就先把 PDF 渲染成页面图片
3. 再用仓库里的 OCR 路径做 best-effort 识别
4. 如果 review PDF 的 OCR 仍然失败，就保留 rendered-page `image_fallback`
5. 如果 rebuttal PDF 的 OCR 仍然失败，`/rebuttal_revise` 会明确报错

也就是说：

- 图像型 `review PDF` 会先自动 OCR；如果还是没有可用文本，会保留 page images 而不是假装解析成功
- 图像型 `rebuttal PDF` 也会先 OCR；但 revise 模式下 OCR 失败会报错
- 如果 reviewer 需要实验支持，仍然用 `XX` 或 experiment placeholder table，而不是编造数字

## How It Works

默认流程是：

1. 安装到宿主工具
2. 提供 paper / review / rebuttal 输入
3. 自动检测是 PDF、text 还是 LaTeX
4. 如果 PDF 没有文本层，就先走 rendered-page OCR fallback
5. 构建 reviewer outline，保留 `W1 / W2 / W3`、`Q1 / Q2 / Q3`、`M1 / M2 / M3`
6. 生成 reviewer cards，分析 reviewer stance、movability、attitude、primary concerns
7. 归并 shared issues
8. 生成 global strategy memo
9. 分配字符预算
10. 起草或润色 `rebuttal_text`
11. 如果 paper 是 LaTeX，则把目标输出提升为 `rebuttal_text` + `revised_latex_paper`

## LaTeX Paper Contract

LaTeX 支持目前是输入/输出契约级别的能力，不应说得比代码更强：

- `detect_paper_artifact.py` 会把单个 `.tex` 或包含 `.tex` 的目录识别成 `source_type = "latex"`
- bundle 会保留 `entrypoint`、`latex_sources` 和合并后的论文文本
- LaTeX paper 的 `expected_outputs` 是 `rebuttal_text` 与 `revised_latex_paper`
- `build_latex_output_package.py` 会把这两个结果连同 `entrypoint` 打包成 `latex-dual` 结果

当前仓库**没有**证明：

- 自动编译 TeX
- 自动修改整套多文件工程并保证可编译
- 对 review PDF 或 rebuttal PDF 进行 LaTeX 化输入

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

`Q1` 用于 direct questions，`minor` 可拆成 `M1 / M2 / M3`，也可以在相似度很高时合并成一段。

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

更完整的说明在 [`.codex/INSTALL.md`](.codex/INSTALL.md)。

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
- `paper_input` 的 PDF / text / LaTeX 自动检测
- review/rebuttal PDF 与 text 自动检测
- rendered-page OCR fallback
- LaTeX dual output package：`rebuttal_text` + `revised_latex_paper`
- `per-reviewer mode`
- `shared-global mode`

## Limitations

- 不会运行实验
- 不会自动抓取投稿系统中的私有 reviews
- 不会为没有证据的结论编造数字
- OCR 是 best-effort，不保证所有扫描质量都能稳定识别
- 如果 rebuttal PDF 没有文本层且 OCR 也失败，`/rebuttal_revise` 会明确报错而不是假装成功
- LaTeX 支持目前只覆盖 paper 输入识别、`entrypoint` 保留和 `revised_latex_paper` 打包，不应宣称已经证明自动编译或多文件重写能力
