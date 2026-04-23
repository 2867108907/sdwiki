---
name: 摄取提示词
description: 结构化知识库（obsidian + karpathy）操作工具，作为摄取功能操作指南。
---

# 摄取提示词

我提供了一个源文档。请按以下方式处理：

---

## 第1步：检查知识库是否已有相关内容

读取 `wiki/index.md`，根据关键词搜索：

- 如果**找到相关主题已有页面**：
  - 列出所有找到的相关页面及其简要描述
  - 询问用户："已找到相关主题页面，是否要将新内容合并更新到现有页面？还是创建独立新页面？"
  - 等待用户回答后再继续操作

- 如果**未找到相关主题**：
  - 继续下一步创建新页面

---

### 第2步：识别源材料类型，根据文档类型调用对应处理规范

| 分类 | 包含文件/内容类型 | 预处理 | 参考 |
| ---- | ---- | ---- | ---- |
| 文本知识类 | `.md` `.txt` 网页文章、博客 | 直接读取 | `ingest/text.md` |
| 文本知识类（二进制） | `.pdf` 论文/书籍 | **自动运行预处理脚本**：执行 `./scripts/extract-pdf.sh input.pdf raw/extracted/name.txt` 然后读取 | `ingest/text.md` |
| 文本知识类（二进制） | `.docx` Word文档 | **自动运行预处理脚本**：执行 `./scripts/extract-docx.py input.docx raw/extracted/name.txt` 然后读取 | `ingest/text.md` |
| 文本知识类（二进制） | `.pptx` PowerPoint 幻灯片 | **自动运行预处理脚本**：执行 `./scripts/extract-pptx.py input.pptx raw/extracted/name.txt` 然后读取 | `ingest/text.md` |
| 数据表格类 | `.xlsx` `.xls` `.csv` Excel/CSV/数据集 | **自动运行预处理脚本**：执行 `./scripts/extract-excel.py input.xlsx raw/extracted/name/` 然后读取提取的 CSV | `ingest/data.md` |
| 图像/信息图类 | 信息图、流程图、思维导图、手绘笔记、照片扫描件 | 需要 OCR，请用户确认已提取文字后继续 | `ingest/image.md` |
| 音频/视频类（二进制） | `.mp3` `.wav` `.mp4` `.mov` 播客/讲座/访谈 | **自动运行预处理脚本**：执行 `./scripts/extract-audio.py input.mp3 raw/extracted/name.txt` 然后读取 | `ingest/audio-video.md` |

**脚本说明：**
- 预处理脚本放在 skill 的 `scripts/` 目录
- 提取结果自动输出到 `raw/extracted/` 目录，保留原始文件
- Agent 执行脚本后，读取提取出的文本/CSV，再进行结构化处理

---

## 第3步：页面开头YAML frontmatter格式规范

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

### 第4步：添加反向链接、添加Frontmatter

确保您创建或更新的每篇文章开头都有：
- frontmatter
- 使用 [[目标文章标题]] 语法建立双向链接。
- 指向原始来源或相关文档时，同样使用 [[...]] 包裹。
- 对于相互关联的概念，应同时在本篇文章和对应文章中补充引用链接。


### 第5步：更新主索引和日志

#### 更新 `wiki/index.md`：

##### 确定文章所属主题，按主题添加条目
- 在 `## 按主题分类` 下找到对应主题子节（如 `### 机器学习`）。
   - 若该主题子节不存在，则新建一个。
   - 在每个主题子节下维护一个表格，表格列头为：`| 页面 | 类型 | 标签 | 摘要 |`。
   - 将新文章作为一行添加到对应主题的表格中，填写：
     - 页面：`[[文章标题]]`
     - 类型：文章的 `type` 字段（如 `concept`、`entity`、`interface-spec` 等）
     - 标签：文章的 `tags`（用 `#` 前缀，多个空格分隔）
     - 摘要：文章的一句简介（可从文章首段提取或手动填写）

#### 更新 `wiki/log.md`：
- 操作
- 详情
- 影响页面
- 更新每次到页面开头

## 输出格式

处理后，在agent对话框里提供：

1. **更改摘要** —— 创建/更新了哪些文章
2. **每个新文件或修改文件的完整内容** —— 文件路径作为标题
3. **开放问题列表** —— 源中不清楚的事项，可以通过其他来源解决
