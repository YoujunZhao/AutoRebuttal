# AutoRebuttal

[English README](README.md)

AutoRebuttal 是一个面向 coding agent 的 rebuttal workflow package。

## Installation

## Quick Install

直接告诉 Codex：

```text
Fetch and follow instructions from https://raw.githubusercontent.com/YoujunZhao/AutoRebuttal/refs/heads/main/.codex/INSTALL.md
```

### Codex

推荐路径是和 Superpowers 一样的原生 skill 发现方式：

1. clone 仓库
2. 建一个 skill junction / symlink
3. 重启 Codex

```bash
git clone https://github.com/YoujunZhao/AutoRebuttal.git ~/.codex/AutoRebuttal
```

```bash
mkdir -p ~/.agents/skills
ln -s ~/.codex/AutoRebuttal/skills/auto-rebuttal ~/.agents/skills/auto-rebuttal
```

Windows (PowerShell):

```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.agents\skills"
cmd /c mklink /J "$env:USERPROFILE\.agents\skills\auto-rebuttal" "$env:USERPROFILE\.codex\AutoRebuttal\skills\auto-rebuttal"
```

更新：

```bash
cd ~/.codex/AutoRebuttal && git pull
```

如果你还是想用 Python helper，也保留了 optional manager CLI：

```bash
python scripts/autorebuttal_manager.py codex install
python scripts/autorebuttal_manager.py codex update
python scripts/autorebuttal_manager.py codex remove
```

### Claude Code

```bash
python scripts/autorebuttal_manager.py claude install
python scripts/autorebuttal_manager.py claude update
python scripts/autorebuttal_manager.py claude remove
```

```text
/plugin marketplace add YoujunZhao/AutoRebuttal
/plugin install auto-rebuttal@auto-rebuttal-dev
```

## How To Use It

Examples：

```text
/rebuttal venue=ICML per_reviewer=5000
Input: paper PDF + review PDF
```

```text
/rebuttal venue=ICML per_reviewer=5000
Input: LaTeX paper + review text
```

```text
/rebuttal venue=ICML per_reviewer=5000
Input: paper PDF + review PDF + review text
```

```text
/rebuttal_revise venue=ICML per_reviewer=5000
Input: rebuttal PDF + optional paper PDF / LaTeX paper
```

## Parameters

| Parameter | 分类 | Optional | 作用 |
| --- | --- | --- | --- |
| `rebuttal` / `rebuttal_revise` | command parameter | no | 选择是从 paper + reviews 起草，还是对 existing rebuttal 做 revise。 |
| `venue` | venue parameter | yes | 应用 ICML / NeurIPS / AAAI / IEEE / CVPR / ICCV / ECCV 等默认格式。 |
| `per_reviewer` | per-reviewer parameter | yes | 指定每个 reviewer 的字符预算。IEEE 默认是 per-reviewer，但不预设字符上限。 |

## Notes

- `paper PDF`
- `paper text`
- `LaTeX paper`
- `review PDF`
- `review text`
- `rebuttal PDF`
- `rebuttal text`
- `revised_latex_paper`

AutoRebuttal 仍然会构建 reviewer outline、reviewer cards 和 global strategy。

Venue defaults 里当前包含：

- `AAAI`
- `IEEE`
- `CVPR`
- `ICCV`
- `ECCV`

point-to-point 结构继续支持：

- `W1`
- `Q1`
- `minor`

`Q1` 和 `minor` / `M1` 这类 point-to-point 结构仍然支持。

如果 reviewer 需要实验支持，仍然用 `XX` 或 experiment placeholder table。
