# SDWiki 预处理脚本

这些脚本用于将二进制文件提取为文本格式，方便 Agent 读取和处理。

## 可用脚本

### 1. extract-pdf.sh (PDF提取)

提取文本从 PDF 文件。

依赖：`poppler-utils` (提供 `pdftotext`)

**安装依赖：**
```bash
# macOS
brew install poppler

# Ubuntu/Debian
sudo apt install poppler-utils
```

**使用：**
```bash
./scripts/extract-pdf.sh raw/your-paper.pdf raw/extracted/your-paper.txt
```

---

### 2. extract-excel.py (Excel/CSV提取)

提取表格数据从 Excel/CSV 文件。输出每个 sheet 为单独 CSV。

依赖：`pandas` (Python)

**安装依赖：**
```bash
pip install pandas openpyxl xlrd
```

**支持格式：** `.xlsx`, `.xls`, `.csv`

**使用：**
```bash
./scripts/extract-excel.py raw/your-data.xlsx raw/extracted/
```

输出会把每个sheet单独保存为 `output_dir/sheet_name.csv`

---

### 3. extract-docx.py (Word 提取)

提取文本从 Word `.docx` 文件。

依赖：`python-docx` (Python)

**安装依赖：**
```bash
pip install python-docx
```

**使用：**
```bash
./scripts/extract-docx.py raw/your-doc.docx raw/extracted/your-doc.txt
```

---

### 4. extract-pptx.py (PowerPoint 提取)

提取文本从 PowerPoint `.pptx` 文件。

依赖：`python-pptx` (Python)

**安装依赖：**
```bash
pip install python-pptx
```

**使用：**
```bash
./scripts/extract-pptx.py raw/your-slides.pptx raw/extracted/your-slides.txt
```

---

### 5. extract-audio.py (音频/视频 语音转文字提取)

提取文字转录从音频/视频文件，使用 OpenAI Whisper。

依赖：`openai-whisper` + `ffmpeg`

**使用：**
```bash
./scripts/extract-audio.py raw/your-podcast.mp3 raw/extracted/your-podcast.txt
./scripts/extract-audio.py raw/your-talk.mp4 raw/extracted/your-talk.txt
```

---

## 工作流程

1. 用户运行脚本预处理二进制文件 → 提取为文本/CSV
2. Agent 读取提取后的文本 → 按 SDWiki 规范生成 wiki 页
3. 这样避免 Agent 因为无法读取二进制文件而失败
