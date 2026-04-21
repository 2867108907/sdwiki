#!/bin/bash
# Extract text from PDF file for SDWiki ingestion
# Usage: ./scripts/extract-pdf.sh input.pdf output.txt

set -e

if [ $# -ne 2 ]; then
    echo "Usage: $0 <input.pdf> <output.txt>"
    exit 1
fi

INPUT="$1"
OUTPUT="$2"

# Check if input exists
if [ ! -f "$INPUT" ]; then
    echo "Error: Input file $INPUT not found"
    exit 1
fi

# Check if pdftotext is available
if ! command -v pdftotext &> /dev/null; then
    echo "Error: pdftotext not found"
    echo "Install it with:"
    echo "  macOS: brew install poppler"
    echo "  Ubuntu/Debian: sudo apt install poppler-utils"
    exit 1
fi

# Extract text
pdftotext -layout "$INPUT" "$OUTPUT"

echo "✓ Extracted text to $OUTPUT"
echo "Size: $(wc -l < "$OUTPUT") lines"
