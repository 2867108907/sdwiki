# SDWiki 预处理脚本

这些脚本将二进制文件输出到标准输出（stdout），方便 Agent 直接读取内容并生成 wiki 页面。

## 可用脚本

### 1. extract-excel.py (Excel/CSV 提取)

将表格数据输出为 CSV 格式。每个 sheet 单独输出。

依赖：`pandas` (Python)

**安装依赖：**
```bash
pip install pandas openpyxl xlrd
```

**支持格式：** `.xlsx`, `.xls`, `.csv`

**使用：**
```bash
./scripts/extract-excel.py raw/your-data.xlsx
```

---

### 2. extract-docx.py (Word 提取)

提取文本从 Word `.docx` 文件（段落 + 表格）。

依赖：`python-docx` (Python)

**安装依赖：**
```bash
pip install python-docx
```

**使用：**
```bash
./scripts/extract-docx.py raw/your-doc.docx
```

---

### 3. extract-pptx.py (PowerPoint 提取)

提取文本从 PowerPoint `.pptx` 文件，按幻灯片分页。

依赖：`python-pptx` (Python)

**安装依赖：**
```bash
pip install python-pptx
```

**使用：**
```bash
./scripts/extract-pptx.py raw/your-slides.pptx
```

---

### 4. extract-audio.py (音频/视频 语音转文字)

使用 OpenAI Whisper 将音频/视频转为带时间戳的转录文本。

依赖：`openai-whisper` + `ffmpeg`

**使用：**
```bash
./scripts/extract-audio.py raw/your-podcast.mp3
./scripts/extract-audio.py raw/your-talk.mp4
./scripts/extract-audio.py raw/your-talk.mp4 --language zh --model base
```

---

## 工作流程

1. Agent 运行脚本，内容直接输出到 stdout
2. Agent 读取内容，按 SDWiki 规范生成 wiki 页面
3. 无需中间文件，不污染 raw/ 目录
