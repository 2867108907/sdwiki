---
name: sdwiki
description: 结构化知识库（Obsidian + Karpathy）操作工具，基于三层架构（raw + wiki + schema）。支持知识库内容摄取、查询、检查。触发方式：CLI 输入 `/sdwiki` 或对话以 `知识库：` 开头。
---

# SDWiki - 结构化知识库操作技能

## 架构背景

SDWiki 遵循 Andrej Karpathy 的 LLM wiki 理念，采用 Obsidian 作为编辑器，三层架构：
- **raw 层**：作为知识库的输入源，存放各种格式的原始文档，不可编辑
- **wiki 层**：知识层，全为 Markdown 格式，包含 index.md 目录索引和 log.md 操作日志，由 LLM 维护
- **schema 层**：定义各种功能的格式规范和工作流程，本skill将此层内置

## 触发方式与执行规则

> **⚠️ 强制规则：必须先读取对应参考文件，严格按流程执行，禁止不读文件直接回答！**

触发方式：
- CLI: `/sdwiki <command>`
- 对话: `知识库：<需求描述>`

按命令类型加载对应参考文件并执行：
- **摄取**：`/sdwiki ingest <文档>` 或 `知识库：摄取 <文档描述>`  
  → 必须先读取 `references/ingest.md`，然后按工作流执行
  → 根据文档类型自动加载 `references/ingest/{text|data|image|audio-video}.md` 进一步处理

- **查询**：`/sdwiki query <问题>` 或 `知识库：查询 <查询内容>`  
  → 按`ingest.md`的工作流执行
  → **强制**：必须先读 `wiki/index.md` 找相关文章，再逐个读取文章内容，才能回答
  → **禁止**：禁止不读文件直接凭记忆/全局搜索回答

- **检查**：`/sdwiki check <范围>` 或 `知识库：检查 <检查内容>`  
  → 必须先读取 `references/check.md`，然后按工作流执行

- **初始化**：`/sdwiki init` 或 `知识库：初始化`  
  → 必须先读取 `references/init.md`，然后按工作流执行
  → 检查当前目录，如果已有知识库结构直接告知；如果缺失，询问用户确认后再创建

**关键约束：**
- 知识库存储在当前工作目录下，`wiki/` 是知识层，`raw/` 是原始资料层
- 所有操作必须基于实际读取的文件内容，不得虚构文章或内容
- 查询必须走 `读取index → 找到相关文章 → 读取文章 → 整理回答 → 询问用户` 流程，不得跳过任何一步

## 功能模块

本技能内置完整的 schema 规范作为参考，使用时加载对应的参考文件：

| 功能   | 参考文件                                         | 说明                  |
| ---- | -------------------------------------------- | ------------------- |
| 初始化  | [references/init.md](references/init.md)     | 在当前目录初始化知识库结构       |
| 体系结构 | [references/schema.md](references/schema.md) | 整体知识库结构定义           |
| 内容摄取 | [references/ingest.md](references/ingest.md) | 从 raw 层摄取转换到 wiki 层 |
| 知识查询 | [references/query.md](references/query.md)   | 查询知识库内容             |
| 检查整理 | [references/check.md](references/check.md)   | 检查知识完整性和连接          |

## 脚本目录

`scripts/` 存放二进制文件预处理抽取脚本：

- `extract-docx.py` - 提取 Word 文本
- `extract-pptx.py` - 提取 PowerPoint 文本
- `extract-excel.py` - 提取 Excel/CSV 表格数据
- `extract-audio.py` - 音频/视频语音转文字提取

详见 [scripts/README.md](scripts/README.md)。若后续出现新格式需求，可以继续添加。

## 使用流程

- 根据用户需求，加载对应 schema 参考文件了解规范
- 按照 schema 定义的工作流程执行操作
- 遵循格式要求输出结果，写入对应目录
- 向用户展示结果，并提供后续操作建议
