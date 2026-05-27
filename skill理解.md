# SDWiki

SDWiki 是一个面向 Codex/Agent 的结构化知识库 skill。它把 Andrej Karpathy 提出的 LLM Wiki 思路落成一套可执行的工作流：用户负责收集原始资料和提出问题，LLM 负责按固定 schema 读取、整理、链接、查询和检查一个 Obsidian 友好的 Markdown 知识库。

这个项目不是另一个笔记模板，而是一个“让 Agent 可靠维护知识库”的操作层。它将知识库维护过程拆成明确命令、参考规范和预处理脚本，使每次摄取、查询、检查都有相同的入口和约束。

## 出处与判断

SDWiki 的来源是 Andrej Karpathy 的 [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 设计。Karpathy 在该 gist 中把 LLM Wiki 描述为一种用 LLM 构建个人知识库的模式：不要在每次提问时重新从原文检索和拼接答案，而是让 LLM 持续维护一个持久、互相链接的 Markdown wiki。

外部核对后，你对来源和问题的判断基本是对的，但需要一个更精确的表述：

- 对：SDWiki 确实是基于 Karpathy 的 LLM Wiki 模式设计的 skill。
- 对：Karpathy 原始设计强调把 raw source 编译进 wiki 层，摄取一个资料时可能更新 summary、entity page、concept page、comparison、overview、synthesis 等多个页面。
- 对：这种多页、图谱化写法在长期积累时很强，但对“我想高密度读完一个主题/一份材料”的场景，容易产生信息密度被分散到许多实体页和概念页中的问题。
- 需要修正：原始设计不只是“归纳总结不同的实体页”。实体页只是其中一类，它还包括来源摘要、概念页、比较页、综述页、索引和日志。信息分散不是原设计的错误，而是它为了可链接、可增量维护而付出的结构代价。

SDWiki 的核心改造是：保留 Karpathy 的 `raw + wiki + schema` 三层思想，但把 schema 固化为 skill 内置流程，并在摄取时更强调“单篇高密度知识文章 + 索引 + 反向链接”的组织方式。

## 设计目标

SDWiki 解决的是个人知识管理中的三个问题：

1. 资料会被反复重新理解：传统 RAG 或文件上传式问答通常在每次提问时重新检索、重新综合，知识不会自然沉淀。
2. wiki 容易越长越散：原始 LLM Wiki 的多页面增量更新适合构建知识图谱，但一个主题的关键解释、背景、机制、优劣和结论可能散落在多处。
3. Agent 容易凭印象回答：如果没有强制流程，LLM 会跳过索引、跳过原文、跳过日志，导致知识库维护不稳定。

因此 SDWiki 的目标是：

- 用 raw 层保存不可修改的原始资料。
- 用 wiki 层保存 LLM 维护的结构化 Markdown 知识。
- 用 skill 内置的 references 充当 schema 层，让 Agent 每次操作都有明确规则。
- 用 index 和 log 降低知识库维护成本。
- 用单篇高密度文章承载一次摄取的核心知识，同时用 Obsidian wiki-link 保留可连接性。

## 整体架构

Karpathy 原始模式包含三层：

```text
raw sources  ->  wiki  ->  schema
```

SDWiki 对这三层做了 skill 化改造：

```text
SDWiki skill/
├── SKILL.md                 # skill 入口、触发方式、强制执行规则
├── references/              # 内置 schema：结构、命令、流程和质量规范
│   ├── schema.md
│   ├── init.md
│   ├── ingest.md
│   ├── query.md
│   ├── check.md
│   └── ingest/
│       ├── text.md
│       ├── data.md
│       ├── image.md
│       └── audio-video.md
└── scripts/                 # 二进制/多媒体资料的预处理脚本
    ├── extract-docx.py
    ├── extract-pptx.py
    ├── extract-excel.py
    └── extract-audio.py
```

用户实际知识库只需要：

```text
Vault/
├── raw/                     # 原始资料层，只读
├── wiki/                    # LLM 维护的知识层
│   ├── index.md             # 内容索引
│   └── log.md               # 操作日志
└── output/                  # 可选：报告、PDF、PPT、可视化等输出物
```

也就是说，Karpathy 模式里的 schema 层不再要求用户在每个 vault 中手动维护一份 `CLAUDE.md` 或 `AGENTS.md`。SDWiki 将它内置在 skill 的 `references/` 目录中，Agent 被触发时按命令读取对应规范。

## 命令入口

SDWiki 支持两种触发方式：

```text
/sdwiki <command>
知识库：<需求描述>
```

当前设计包含四类操作：

| 命令 | 参考规范 | 作用 |
| --- | --- | --- |
| `init` | `references/init.md` | 初始化 `raw/`、`wiki/`、`wiki/index.md`、`wiki/log.md` |
| `ingest` | `references/ingest.md` | 从 raw 或指定文件摄取资料，生成或更新 wiki 文章 |
| `query` | `references/query.md` | 先读 index，再读相关文章，基于知识库回答问题 |
| `check` | `references/check.md` | 检查结构、链接、frontmatter、索引和内容质量 |

`SKILL.md` 中最重要的规则是：执行任何命令前必须先读取对应 reference 文件，不能凭记忆直接回答。

## 内容设计

### 1. 高密度摄取

Karpathy 原始设计中，一次 ingest 可能触碰 10 到 15 个 wiki 页面，这适合让 wiki 逐步变成知识图谱。SDWiki 选择了更适合个人深读和复盘的默认策略：优先创建或更新一篇单一、高密度的知识文章，然后用 index、frontmatter 和 wiki-link 维持结构。

一篇 SDWiki 文章通常包含：

- 来源信息：标题、作者、URL、文件类型、原始文档位置。
- 核心摘要：2 到 3 句话说明材料讲了什么。
- 深度知识讲解：定义、背景、机制、细节、案例、局限和 trade-offs。
- 结构化表达：表格、Mermaid、Excalidraw 或其他可编辑图示。
- 关联知识：通过 `[[wiki-link]]` 连接已有页面。
- YAML frontmatter：记录类型、创建时间、更新时间、来源和标签。

这种设计的取舍是：不追求把每个实体和概念立即拆成独立页面，而是先保证一份材料或一个主题在单篇文章中足够完整、可读、可复盘。后续当某个概念真正变成高频中心节点时，再通过检查和重构拆出独立页面。

### 2. 先 index 后内容

SDWiki 查询和摄取都要求先读取 `wiki/index.md`：

- 摄取时，先判断是否已有相关主题，避免重复造页。
- 查询时，先通过 index 找相关文章，再读取文章全文，最后组织答案。
- 更新时，把新文章按主题写回 index，而不是只按页面类型分类。

这里的主题是内容领域，例如“Obsidian”“知识库方法论”“半导体 MES”；类型只是页面结构属性，例如 `concept`、`entity`、`data`、`synthesis`。

### 3. 人在回路中

SDWiki 在遇到已有相关页面时不会直接覆盖，而是要求向用户确认：

- 合并更新到现有页面。
- 创建独立新页面。
- 或在新旧信息之间做对比补充。

这继承了 Karpathy 原始设计中“人负责方向、LLM 负责维护”的思想。LLM 处理重复劳动，但主题边界、强调重点和最终知识结构仍由用户把关。

### 4. 多格式资料统一摄取

SDWiki 按资料类型选择处理方式：

| 类型 | 文件格式 | 处理方式 |
| --- | --- | --- |
| 文本 | `.md`、`.txt`、网页文章、博客 | 直接读取 |
| PDF | `.pdf` | 直接读取，必要时指定页码范围 |
| 图像 | `.png`、`.jpg`、`.jpeg` | 直接使用多模态能力读取 |
| Word | `.docx` | `scripts/extract-docx.py` 输出文本 |
| PPT | `.pptx` | `scripts/extract-pptx.py` 按页输出文本 |
| 表格 | `.xlsx`、`.xls`、`.csv` | `scripts/extract-excel.py` 输出 CSV |
| 音视频 | `.mp3`、`.wav`、`.mp4`、`.mov` | `scripts/extract-audio.py` 使用 Whisper 转录 |

这些脚本都把结果输出到 stdout，Agent 读取后直接进入摄取流程，避免生成多余中间文件污染 raw 层。

## 页面规范

所有 wiki 页面都使用 Markdown，并带有 YAML frontmatter：

```yaml
---
title: 页面标题
type: concept|entity|data|note|comparison|synthesis|case|index|log
created: YYYY-MM-DD
updated: YYYY-MM-DD
source: 原始来源（可选）
tags:
  - tag1
  - tag2
---
```

当前支持的页面类型：

- `concept`：概念、技术、方法、原理。
- `entity`：人物、项目、公司、产品、工具、框架。
- `data`：数据集、统计数据、指标和报表解读。
- `note`：读书笔记、文章随记、个人思考、会议记录。
- `comparison`：多个方案或技术的对比。
- `synthesis`：跨来源主题综述。
- `case`：实战案例、项目案例、代码示例。
- `index`：索引页。
- `log`：日志页。

内部链接使用 Obsidian wiki-link：

```markdown
[[页面标题]]
[[页面标题|显示文本]]
```

## 工作流

### 初始化

`/sdwiki init` 会检查当前目录是否已经存在：

- `raw/`
- `wiki/`
- `wiki/index.md`
- `wiki/log.md`

如果结构完整，直接提示可用命令；如果结构缺失，列出缺失项并等待用户确认后创建。

### 摄取

`/sdwiki ingest <文档>` 的流程：

1. 读取 `references/ingest.md`。
2. 读取 `wiki/index.md`，判断是否已有相关主题。
3. 根据文件类型读取对应 `references/ingest/*.md`。
4. 读取或预处理原始资料。
5. 创建或更新一篇高密度知识文章。
6. 添加 frontmatter、来源、内部链接和反向链接。
7. 更新 `wiki/index.md`。
8. 更新 `wiki/log.md`。
9. 向用户汇报修改摘要、文件内容和开放问题。

### 查询

`/sdwiki query <问题>` 的流程：

1. 读取 `references/query.md`。
2. 先读 `wiki/index.md`。
3. 根据关键词找到相关文章。
4. 逐个读取相关文章全文。
5. 基于实际文章回答，并用 `[[页面标题]]` 形式引用来源。
6. 标出知识库没有覆盖的空白。
7. 询问是否需要继续查 raw 层或结合网络搜索。

### 检查

`/sdwiki check <范围>` 会按 `references/check.md` 做健康检查，覆盖：

- 损坏链接。
- 孤立文章。
- frontmatter 缺失。
- 空节和模板残留。
- 重复概念。
- 应该互链但未互链的文章。
- index 完整性和统计准确性。
- 文章过薄、缺来源、置信度不匹配等质量问题。

## 与 Karpathy 原始模式的区别

| 维度 | Karpathy LLM Wiki | SDWiki |
| --- | --- | --- |
| 形式 | 抽象 idea file，交给 Agent 和用户共同实例化 | 可安装、可触发的 skill |
| schema | 通常写在 `CLAUDE.md`、`AGENTS.md` 等项目文件中 | 内置在 `references/`，按命令加载 |
| 摄取结果 | 一次来源可能更新多个实体页、概念页和综述页 | 默认优先生成或更新单篇高密度知识文章 |
| 重点 | 持久、互链、可增量维护的 wiki 图谱 | 高密度理解、稳定流程、可审计操作 |
| 查询 | 读 index，再读相关页面并综合 | 强制读 index 和全文，禁止凭记忆回答 |
| 维护 | lint 检查矛盾、陈旧、孤立、缺链接 | check 细化为结构、内容、索引三类健康检查 |
| 多模态 | 原文中作为可选能力提到 | 明确拆分 text、data、image、audio-video 摄取规范 |

SDWiki 不是否定 Karpathy 的多页 wiki，而是在它的基础上做了一层面向个人高密度学习的约束：先把材料讲透，再建立连接；先保证可读性和复盘价值，再逐步演化知识图谱。

## 使用示例

```text
/sdwiki init
```

初始化当前目录的 `raw/` 和 `wiki/`。

```text
/sdwiki ingest raw/articles/llm-wiki.md
```

摄取一篇文章，生成或更新 wiki 知识文章。

```text
知识库：查询 Karpathy LLM Wiki 和 SDWiki 的差异是什么？
```

基于 `wiki/index.md` 和相关文章回答问题。

```text
/sdwiki check wiki/
```

检查知识库健康度。

## 设计原则

- 原始资料不可改：raw 层是事实来源，LLM 只读不写。
- 回答必须有依据：查询必须先读 index 和文章，不允许凭印象回答。
- 知识要能复利：摄取、查询和检查的结果都应回到 wiki，而不是停留在聊天窗口。
- 信息密度优先：默认把一次摄取整理成完整、可读、可复盘的高密度文章。
- 链接保持开放：即使采用单篇高密度文章，也要用 wiki-link 保持概念之间的可连接性。
- 低基础设施依赖：Markdown、文件系统、Obsidian 和少量脚本即可运行。
- 人在回路中：合并、拆分、重构、强调重点等判断由用户确认。

## 参考资料

- [Andrej Karpathy: LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [Karpathy gists listing](https://gist.github.com/karpathy)
