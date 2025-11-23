"""Export generated questions to Excel format matching original structure."""

import pandas as pd
from pathlib import Path
from typing import Optional
import json


def assign_ids(df: pd.DataFrame, start_id: int = 30131) -> pd.DataFrame:
    """
    Assign IDs to questions (QID, ACID, AWID1, AWID2).
    
    Args:
        df: DataFrame with questions
        start_id: Starting ID for questions
        
    Returns:
        DataFrame with IDs assigned
    """
    df = df.copy()
    
    # Assign QID
    df['QID'] = range(start_id, start_id + len(df))
    
    # Assign answer IDs (sequential)
    answer_start = start_id * 100  # Use a different range for answers
    df['ACID'] = range(answer_start, answer_start + len(df))
    df['AWID1'] = range(answer_start + len(df), answer_start + 2 * len(df))
    df['AWID2'] = range(answer_start + 2 * len(df), answer_start + 3 * len(df))
    
    return df


def assign_category_id(df: pd.DataFrame, category_mapping: Optional[Dict[str, int]] = None) -> pd.DataFrame:
    """
    Assign category_id based on question category.
    
    Args:
        df: DataFrame with questions
        category_mapping: Optional mapping of category names to IDs
        
    Returns:
        DataFrame with category_id assigned
    """
    df = df.copy()
    
    # Default category mapping (based on original data structure)
    if category_mapping is None:
        category_mapping = {
            'countries': 4,  # Technology (using available category)
            'artists': 2,    # Entertainment
            'movies': 2,     # Entertainment
            'brands': 4,     # Technology
            'theme': 2,      # Entertainment
            'field': 1,     # Education
        }
    
    # Map categories
    if 'category' in df.columns:
        df['category_id'] = df['category'].map(category_mapping).fillna(1)
    else:
        df['category_id'] = 1  # Default to Education
    
    return df


def assign_tags(df: pd.DataFrame, tag_mapping: Optional[Dict[str, str]] = None) -> pd.DataFrame:
    """
    Assign tags based on question category.
    
    Args:
        df: DataFrame with questions
        tag_mapping: Optional mapping of categories to tag IDs
        
    Returns:
        DataFrame with tags assigned
    """
    df = df.copy()
    
    # Default tag mapping (based on original tag structure)
    if tag_mapping is None:
        tag_mapping = {
            'countries': '4',      # :COUNTRY
            'artists': '50',        # EN:MUSIC
            'movies': '51',         # EN:MOVIE
            'brands': '7',          # :COMPANY
            'theme': '54',          # EN:Facts
            'field': '10',          # ED:HISTORY (generic)
        }
    
    # Map categories to tags
    if 'category' in df.columns:
        df['tags'] = df['category'].map(tag_mapping).fillna('10')
    else:
        df['tags'] = '10'  # Default tag
    
    return df


def format_for_excel(df: pd.DataFrame) -> pd.DataFrame:
    """
    Format DataFrame to match original Excel structure.
    
    Args:
        df: DataFrame with generated questions
        
    Returns:
        Formatted DataFrame matching original structure
    """
    df = df.copy()
    
    # Ensure required columns exist
    required_columns = ['QTYPE', 'QID', 'category_id', 'QEN', 'ACEN', 'AW1EN', 'AW2EN', 'ACID', 'AWID1', 'AWID2', 'tags']
    
    # Add missing columns with defaults
    if 'QTYPE' not in df.columns:
        df['QTYPE'] = 'text'
    
    # Assign IDs if not present
    if 'QID' not in df.columns:
        df = assign_ids(df)
    
    if 'category_id' not in df.columns:
        df = assign_category_id(df)
    
    if 'tags' not in df.columns:
        df = assign_tags(df)
    
    # Select and order columns to match original format
    excel_columns = ['QTYPE', 'QID', 'category_id', 'QEN', 'ACEN', 'AW1EN', 'AW2EN', 'ACID', 'AWID1', 'AWID2', 'tags']
    
    # Only include columns that exist
    available_columns = [col for col in excel_columns if col in df.columns]
    df = df[available_columns]
    
    # Reorder to match original
    df = df.reindex(columns=excel_columns, fill_value='')
    
    return df


def export_to_excel(df: pd.DataFrame, output_path: str = "outputs/generated_questions.xlsx", sheet_name: str = "data") -> None:
    """
    Export questions to Excel file matching original format.
    
    Args:
        df: DataFrame with questions
        output_path: Output file path
        sheet_name: Sheet name
    """
    # Format for Excel
    df_formatted = format_for_excel(df)
    
    # Create Excel file
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        df_formatted.to_excel(writer, sheet_name=sheet_name, index=False)
    
    print(f"Exported {len(df_formatted)} questions to {output_path}")


def export_to_csv(df: pd.DataFrame, output_path: str = "outputs/generated_questions.csv") -> None:
    """Export questions to CSV file."""
    df_formatted = format_for_excel(df)
    df_formatted.to_csv(output_path, index=False)
    print(f"Exported {len(df_formatted)} questions to {output_path}")


def export_to_json(df: pd.DataFrame, output_path: str = "outputs/generated_questions.json") -> None:
    """Export questions to JSON file."""
    df_formatted = format_for_excel(df)
    df_formatted.to_json(output_path, orient='records', indent=2)
    print(f"Exported {len(df_formatted)} questions to {output_path}")

