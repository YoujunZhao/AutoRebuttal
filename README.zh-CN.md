# SuperRebuttal

[English README](README.md)

SuperRebuttal 是一个面向 coding agent 的 rebuttal 工作流包。它现在采用 `plugin-first` 形态：仓库里同时包含安装入口、内部 `super-rebuttal` skill、命令入口、规则参考和测试，而不是只放一个可以被手工复制的 skill 目录。

这个项目的目标很简单：帮助作者把论文、reviews 和明确的 rebuttal 约束，转成一份结构化、证据优先、不会虚构实验结果的回复草稿。

## 它是什么

SuperRebuttal 不是一个“单独 skill 文件夹”，而是一个可以安装、再按工作流调用的 rebuttal package。

它围绕几个核心原则设计：

- rebuttal 应该先做问题整理，再写 prose
- 未验证的 venue 不假装“内置支持”
- 缺失证据用 `XX`、`[RESULT-TO-FILL]` 等占位符，而不是编数字
- 安装声明和 venue 声明必须比仓库真实能力更保守

## 它怎么工作

当作者把论文和 reviews 交给 agent 时，SuperRebuttal 不会直接跳到最终文本，而是先判断回复形式，再归并 reviewer concerns，最后才起草。

实际流程是：

1. 在宿主工具里安装这个包
2. 提供论文上下文和 reviews
3. 明确回复模式和预算
4. 归并 reviewer concerns
5. 产出 strategy-first 的回复地图
6. 生成最终 rebuttal 文本
7. 对缺失证据保留占位符

## 安装

目前仓库只把两个安装面当作“已验证”来写。

### Codex

直接告诉 Codex：

```text
Fetch and follow instructions from https://raw.githubusercontent.com/YoujunZhao/SuperRebuttal/refs/heads/codex/plugin-first-redesign/.codex/INSTALL.md
```

手工安装说明在 [`.codex/INSTALL.md`](.codex/INSTALL.md)。

### Claude Code

仓库提供了 Claude 风格的 plugin shell：

- [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json)
- [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json)

这表示仓库结构已经对齐 Claude plugin / local marketplace 的安装方式。

注意：项目目前 **不** 宣称已经公开上架官方 marketplace。现在能确认的是“插件结构正确”和“本地 marketplace 形态存在”。

## 怎么调用 / 怎么使用

安装完成之后，实际可用的调用方式有两种：

- **使用 `rebuttal` command**
- **使用 `super-rebuttal` skill**

不同宿主工具的 UI 会有差异，但核心意图是一致的：先让 agent 进入 SuperRebuttal 工作流，再提供论文、reviews 和预算。

### 调用示例

使用 `rebuttal` command：

```text
Use the `rebuttal` command. I will paste the abstract, the main claims, and three reviewer comments. This is per-reviewer mode with 5000 characters each.
```

使用 `super-rebuttal` skill：

```text
Use the `super-rebuttal` skill. This is a shared-global mode rebuttal with a total limit of 6000 characters. First cluster shared concerns, then draft the final response.
```

如果 venue 形式不明确，就直接显式给预算：

```text
Use the `super-rebuttal` skill. Ignore venue defaults and use per-reviewer mode with 4000 characters per reviewer.
```

## 基本工作流

1. 安装 SuperRebuttal
2. 提供论文 PDF、正文文本，或者可信的摘要
3. 选择预算模式：
   - `per-reviewer mode`
   - `shared-global mode`
4. 先生成 issue map，再要求最终 prose
5. 用 evidence-first 方式起草 rebuttal
6. 对缺失证据明确标注占位符

### 两种已测试的预算模式

- **`per-reviewer mode`**
  适用于每个 reviewer 有单独回复上限的场景，例如“每个 reviewer 5000 字符”。

- **`shared-global mode`**
  适用于所有 reviewer 共用一段回复的场景，例如“总共 6000 字符”。

很多 CV 风格或统一回复框风格的 rebuttal，都更适合 `shared-global mode`。

## 今天真正验证过的支持范围

目前项目只应该把下面这些写成“已验证支持”：

- Codex 安装入口 [`.codex/INSTALL.md`](.codex/INSTALL.md)
- Claude plugin shell [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json)
- Claude 本地 marketplace 形态 [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json)
- 命令入口 [`commands/rebuttal.md`](commands/rebuttal.md)
- `per-reviewer mode`
- `shared-global mode`

## 已核对的参考说明

仓库还附带了公开规则参考，覆盖：

- ICLR
- NeurIPS
- ICML
- ARR 风格 author response

这些内容位于 [`skills/super-rebuttal/references/venue-policies.md`](skills/super-rebuttal/references/venue-policies.md)。

这里要强调：这只是“已核对的公开参考”，不等于“所有年份、所有格式都已经完整支持”。

## 仓库里有什么

### Package 外壳

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

### 参考材料

- [`skills/super-rebuttal/references/input-contract.md`](skills/super-rebuttal/references/input-contract.md)
- [`skills/super-rebuttal/references/rebuttal-playbook.md`](skills/super-rebuttal/references/rebuttal-playbook.md)
- [`skills/super-rebuttal/references/venue-policies.md`](skills/super-rebuttal/references/venue-policies.md)
- [`skills/super-rebuttal/references/source-notes.md`](skills/super-rebuttal/references/source-notes.md)

## 对未验证 venue 的通用降级方案

如果 venue 不明确，或者当前年份规则不确定，就不要假装有现成模板，而是直接显式给预算，走通用模式：

- `per-reviewer mode`
- `shared-global mode`

这才是当前仓库对未验证场景的正确处理方式。

## 限制

- 不跑实验
- 不抓私有 reviews
- 不宣称支持所有会议 rebuttal 格式
- 不把参考说明写成自动化能力
- 不宣称已经上架到 Claude 官方 marketplace
- 不保证提分

## 研究依据

核心依据来自：

- 公开 venue 规则
- 公开 rebuttal 研究和数据集
- 明确的 non-fabrication 规则

可从下面开始看：

- [`skills/super-rebuttal/references/source-notes.md`](skills/super-rebuttal/references/source-notes.md)
- [`skills/super-rebuttal/references/rebuttal-playbook.md`](skills/super-rebuttal/references/rebuttal-playbook.md)
- [`skills/super-rebuttal/references/input-contract.md`](skills/super-rebuttal/references/input-contract.md)

## 当前状态

- private-first
- plugin-first
- 只宣传真正验证过的能力
- 更偏向工作流纪律，而不是 venue 自动化
