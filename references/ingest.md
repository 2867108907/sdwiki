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

| 分类 | 文件类型 | 处理方式 | 参考 |
| ---- | ---- | ---- | ---- |
| 文本类 | `.md` `.txt` 网页文章、博客 | 直接读取 | `ingest/text.md` |
| PDF | `.pdf` 论文/书籍 | **直接读取**（LLM 原生支持 PDF，可指定页码范围） | `ingest/text.md` |
| 图像/信息图 | `.png` `.jpg` `.jpeg` 信息图、流程图、思维导图、手绘笔记、扫描件 | **直接读取**（LLM 多模态视觉能力，无需 OCR） | `ingest/image.md` |
| Word（二进制） | `.docx` | 运行 `./scripts/extract-docx.py <文件>` 输出到 stdout 读取 | `ingest/text.md` |
| PPT（二进制） | `.pptx` | 运行 `./scripts/extract-pptx.py <文件>` 输出到 stdout 读取 | `ingest/text.md` |
| Excel/数据 | `.xlsx` `.xls` `.csv` | 运行 `./scripts/extract-excel.py <文件>` 输出到 stdout 读取 | `ingest/data.md` |
| 音频/视频 | `.mp3` `.wav` `.mp4` `.mov` | 运行 `./scripts/extract-audio.py <文件>` 输出到 stdout 读取 | `ingest/audio-video.md` |

**说明：**
- PDF 和图像由 LLM 直接读取
- Word/PPT/Excel/音视频需运行对应脚本将内容转为可读文本，LLM 读取后直接生成 wiki 页面

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
- 先搜索 index 找匹配目标文章，使用 [[目标文章标题]] 语法建立双向链接。
- 指向原始来源或相关文档时，同样使用 [[...]] 包裹。
- 对于相互关联的概念，应同时在本篇文章和对应文章中补充引用链接。


### 第5步：更新主索引和日志

#### 更新 `wiki/index.md`：

##### 确定文章所属主题，按主题分区添加条目
- **主题 = 内容所属领域**（如 "Obsidian"、"半导体 MES"、"知识库方法论"），由 LLM 根据文章内容自行识别
- **类型 ≠ 主题**：类型是页面的结构属性（concept/entity/data/note/comparison/synthesis/case），在表格的"类型"列中填写；主题决定文章归入哪个分区
- 在 index.md 的 `## <主题名>` 分区下添加条目：
   - 若该主题分区不存在，则在统计区之前新建一个 `## <主题名>` 二级标题，附一行简短描述
   - 在主题分区下维护表格，列头为：`| 页面 | 类型 | 标签 | 摘要 |`
   - 将新文章作为一行添加到表格中，填写：
     - 页面：`[[文章标题]]`
     - 类型：文章的 frontmatter 中 `type` 字段的值
     - 标签：文章的 `tags`（用 `#` 前缀，多个空格分隔）
     - 摘要：文章的简介，两三句话概括


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
