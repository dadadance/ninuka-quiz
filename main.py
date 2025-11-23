import pandas as pd
import os
import sys
from pathlib import Path
from typing import Dict, Any


def get_file_info(file_path: str) -> Dict[str, Any]:
    """Get basic file information."""
    path = Path(file_path)
    if not path.exists():
        return None
    
    stat = path.stat()
    return {
        "exists": True,
        "size_bytes": stat.st_size,
        "size_mb": stat.st_size / (1024 * 1024),
        "absolute_path": str(path.absolute())
    }


def read_excel_robust(file_path: str) -> Dict[str, pd.DataFrame]:
    """
    Robustly read Excel file, trying multiple methods if needed.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Excel file not found: {file_path}")
    
    try:
        # Try reading with openpyxl engine (default)
        excel_data = pd.read_excel(file_path, sheet_name=None, engine='openpyxl')
        return excel_data
    except Exception as e:
        print(f"Warning: Failed to read with openpyxl: {e}")
        try:
            # Try with xlrd engine (for older .xls files)
            excel_data = pd.read_excel(file_path, sheet_name=None, engine='xlrd')
            return excel_data
        except Exception as e2:
            raise RuntimeError(f"Failed to read Excel file with both engines. "
                             f"openpyxl error: {e}\nxlrd error: {e2}")


def analyze_dataframe(df: pd.DataFrame, sheet_name: str) -> None:
    """Comprehensive analysis of a DataFrame."""
    print(f"\n{'=' * 70}")
    print(f"SHEET: {sheet_name}")
    print(f"{'=' * 70}")
    
    # Basic info
    print(f"\n📊 BASIC INFORMATION")
    print(f"  Rows: {df.shape[0]:,}")
    print(f"  Columns: {df.shape[1]}")
    print(f"  Total cells: {df.size:,}")
    
    # Column information
    print(f"\n📋 COLUMNS ({len(df.columns)} total):")
    for i, col in enumerate(df.columns, 1):
        dtype = df[col].dtype
        non_null = df[col].notna().sum()
        null_count = df[col].isna().sum()
        print(f"  {i:2d}. {col}")
        print(f"      Type: {dtype} | Non-null: {non_null:,} | Null: {null_count:,}")
    
    # Data preview
    print(f"\n👀 DATA PREVIEW (first 10 rows):")
    print(df.head(10).to_string())
    
    if df.shape[0] > 10:
        print(f"\n... ({df.shape[0] - 10} more rows)")
    
    # Data types summary
    print(f"\n🔢 DATA TYPES SUMMARY:")
    dtype_counts = df.dtypes.value_counts()
    for dtype, count in dtype_counts.items():
        print(f"  {dtype}: {count} column(s)")
    
    # Missing values analysis
    print(f"\n⚠️  MISSING VALUES:")
    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(2)
    if missing.sum() > 0:
        print("  Columns with missing values:")
        for col in missing[missing > 0].index:
            print(f"    {col}: {missing[col]:,} ({missing_pct[col]}%)")
    else:
        print("  ✓ No missing values found")
    
    # Statistics for numeric columns
    numeric_cols = df.select_dtypes(include=['number']).columns
    if len(numeric_cols) > 0:
        print(f"\n📈 NUMERIC COLUMNS STATISTICS:")
        print(df[numeric_cols].describe().to_string())
    
    # Unique values for categorical columns
    object_cols = df.select_dtypes(include=['object']).columns
    if len(object_cols) > 0:
        print(f"\n🔤 TEXT/CATEGORICAL COLUMNS:")
        for col in object_cols[:10]:  # Limit to first 10 to avoid too much output
            unique_count = df[col].nunique()
            print(f"  {col}: {unique_count:,} unique values")
            if unique_count <= 20:
                print(f"    Values: {list(df[col].unique())}")
    
    # Memory usage
    memory_kb = df.memory_usage(deep=True).sum() / 1024
    memory_mb = memory_kb / 1024
    print(f"\n💾 MEMORY USAGE: {memory_kb:.2f} KB ({memory_mb:.2f} MB)")


def main():
    excel_file = "ninouk2.xlsx"
    
    print("=" * 70)
    print("EXCEL FILE READER - COMPREHENSIVE ANALYSIS")
    print("=" * 70)
    
    # File information
    print(f"\n📁 FILE INFORMATION:")
    file_info = get_file_info(excel_file)
    if not file_info:
        print(f"❌ Error: File '{excel_file}' not found!")
        print(f"   Current directory: {os.getcwd()}")
        sys.exit(1)
    
    print(f"  File: {excel_file}")
    print(f"  Size: {file_info['size_mb']:.2f} MB ({file_info['size_bytes']:,} bytes)")
    print(f"  Path: {file_info['absolute_path']}")
    
    # Read Excel file
    print(f"\n📖 Reading Excel file...")
    try:
        excel_data = read_excel_robust(excel_file)
    except Exception as e:
        print(f"❌ Error reading Excel file: {e}")
        sys.exit(1)
    
    # Summary
    print(f"\n✅ Successfully loaded Excel file!")
    print(f"  Number of sheets: {len(excel_data)}")
    print(f"  Sheet names: {list(excel_data.keys())}")
    
    # Analyze each sheet
    for sheet_name, df in excel_data.items():
        try:
            analyze_dataframe(df, sheet_name)
        except Exception as e:
            print(f"\n❌ Error analyzing sheet '{sheet_name}': {e}")
            continue
    
    print(f"\n{'=' * 70}")
    print("ANALYSIS COMPLETE")
    print(f"{'=' * 70}\n")


if __name__ == "__main__":
    main()
