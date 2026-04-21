#!/usr/bin/env python3
"""
Extract Excel/CSV sheets to CSV files for SDWiki ingestion
Supports: .xlsx, .xls, .csv
Usage: ./scripts/extract-excel.py input.[xlsx|xls|csv] output_dir/
"""

import sys
import os
import pandas as pd

def main():
    if len(sys.argv) != 3:
        print("Usage: ./extract-excel.py <input.[xlsx|xls|csv]> <output_dir>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_dir = sys.argv[2]
    ext = os.path.splitext(input_file)[1].lower()

    # Check input
    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} not found")
        sys.exit(1)

    # Check extension
    if ext not in ['.xlsx', '.xls', '.csv']:
        print(f"Error: Unsupported file type {ext}")
        print("Supported: .xlsx, .xls, .csv")
        sys.exit(1)

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    if ext == '.csv':
        # Already CSV, just copy summary
        df = pd.read_csv(input_file)
        output_file = os.path.join(output_dir, os.path.basename(input_file))
        df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"✓ Copied {input_file} → {output_file} ({len(df)} rows)")
    else:
        # Excel file - read all sheets
        xl = pd.ExcelFile(input_file)
        print(f"✓ Found {len(xl.sheet_names)} sheet(s):")
        for sheet_name in xl.sheet_names:
            df = pd.read_excel(xl, sheet_name=sheet_name)
            output_file = os.path.join(output_dir, f"{sheet_name}.csv")
            df.to_csv(output_file, index=False, encoding='utf-8')
            print(f"  → {sheet_name} → {output_file} ({len(df)} rows)")

    print(f"\n✓ All data extracted to {output_dir}/")
    print("Now you can ingest the extracted CSV into SDWiki")

if __name__ == "__main__":
    main()
