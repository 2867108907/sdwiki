---
name: 音频视频类处理
description: 结构化知识库（obsidian + karpathy）操作工具，作为摄取功能的音频视频类处理指南。
---

# 音频视频类知识摄取指南
## 前置处理

音频视频文件无法直接读取，必须先由用户通过外部工具转为文本。推荐使用 OpenAI Whisper 进行语音转文字：

**依赖安装：**
```bash
pip install openai-whisper
```

**转换示例：**
```bash
# 转换音频
whisper raw/your-podcast.mp3 --model base --language zh --output_format txt --output_dir raw/extracted/

# 提取音频后转换视频
ffmpeg -i raw/your-talk.mp4 -vn -acodec copy raw/extracted/audio.aac
whisper raw/extracted/audio.aac --model base --language zh --output_format txt --output_dir raw/extracted/
```

转换完成后，得到 `.txt` 文件，再按文本类流程摄取。

## 第1步：理解转录文本内容

仔细阅读转录文本。识别：
- 演讲主题和核心论点
- 嘉宾/讲者身份
- 关键观点和结论
- 值得记录的数据和案例
- 时间戳（如果保留）对应重要段落

## 第2步：创建或更新知识文章

在`index.md`中检查相关知识文章是否存在：

### 如果知识文章尚不存在

在`wiki/`下创建单一知识文章，结构如下：
- **来源信息**（页面顶部）
  - 原始标题、讲者、活动名称、日期/URL
  - 类型（播客/讲座/访谈/TED/课程）
  - 核心摘要（2-3句话概括主要内容）

- **内容整理**（主体部分）

  根据内容性质整理：
  - **观点整理**：按主题分点整理核心观点
  - **问答记录**：保留提问和回答完整脉络
  - **知识要点**：提取可复用的知识点

  **核心原则：**
  - 保留干货，去掉口语冗余
  - 维持讲者原有逻辑，不重构改写
  - 重要原话保留引用
  - 标注哪些是讲者观点，哪些是补充

### 如果知识文章已存在：
- 补充新的观点和信息到现有文章
- 将新来源添加到frontmatter字段
- 添加发现的任何新连接
- 保留现有内容 —— 添加到它，不要替换它
