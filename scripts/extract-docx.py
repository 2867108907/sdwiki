#!/usr/bin/env python3
"""
Extract text from Word docx file for SDWiki ingestion
Usage: ./scripts/extract-docx.py input.docx output.txt
"""

import sys
import os

try:
    from docx import Document
except ImportError:
    print("Error: python-docx not installed")
    print("Install with: pip install python-docx")
    sys.exit(1)

def main():
    if len(sys.argv) != 3:
        print("Usage: ./extract-docx.py <input.docx> <output.txt>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} not found")
        sys.exit(1)

    ext = os.path.splitext(input_file)[1].lower()
    if ext != '.docx':
        print(f"Error: Only .docx files are supported, got {ext}")
        sys.exit(1)

    # Read docx
    doc = Document(input_file)
    full_text = '\n'.join([para.text for para in doc.paragraphs])

    # Also extract text from tables
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                full_text += '\n' + cell.text

    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_text)

    print(f"✓ Extracted {len(full_text)} characters to {output_file}")

if __name__ == "__main__":
    main()
