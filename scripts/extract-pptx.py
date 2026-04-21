#!/usr/bin/env python3
"""
Extract text from PowerPoint pptx file for SDWiki ingestion
Usage: ./scripts/extract-pptx.py input.pptx output.txt
"""

import sys
import os

try:
    from pptx import Presentation
except ImportError:
    print("Error: python-pptx not installed")
    print("Install with: pip install python-pptx")
    sys.exit(1)

def main():
    if len(sys.argv) != 3:
        print("Usage: ./extract-pptx.py <input.pptx> <output.txt>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} not found")
        sys.exit(1)

    ext = os.path.splitext(input_file)[1].lower()
    if ext != '.pptx':
        print(f"Error: Only .pptx files are supported, got {ext}")
        sys.exit(1)

    # Read pptx
    prs = Presentation(input_file)
    full_text = []

    for slide in prs.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                full_text.append(shape.text)

    full_text = '\n\n'.join(full_text)

    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_text)

    print(f"✓ Extracted {len(full_text)} characters to {output_file}")
    print(f"  {len(prs.slides)} slides")

if __name__ == "__main__":
    main()
