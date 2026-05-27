#!/usr/bin/env python3
"""
Extract Excel/CSV sheets to text for SDWiki ingestion
Supports: .xlsx, .xls, .csv
Usage: ./scripts/extract-excel.py input.[xlsx|xls|csv]
"""

import sys
import os
import pandas as pd

def main():
    if len(sys.argv) != 2:
        print("Usage: ./extract-excel.py <input.[xlsx|xls|csv]>", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    ext = os.path.splitext(input_file)[1].lower()

    # Check input
    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} not found", file=sys.stderr)
        sys.exit(1)

    # Check extension
    if ext not in ['.xlsx', '.xls', '.csv']:
        print(f"Error: Unsupported file type {ext}", file=sys.stderr)
        print("Supported: .xlsx, .xls, .csv", file=sys.stderr)
        sys.exit(1)

    if ext == '.csv':
        df = pd.read_csv(input_file)
        print(f"=== Sheet: {os.path.basename(input_file)} ({len(df)} rows) ===", file=sys.stderr)
        print(df.to_csv(index=False))
    else:
        xl = pd.ExcelFile(input_file)
        print(f"=== Found {len(xl.sheet_names)} sheet(s) ===", file=sys.stderr)
        for sheet_name in xl.sheet_names:
            df = pd.read_excel(xl, sheet_name=sheet_name)
            print(f"--- Sheet: {sheet_name} ({len(df)} rows) ---", file=sys.stderr)
            print(df.to_csv(index=False))

if __name__ == "__main__":
    main()
