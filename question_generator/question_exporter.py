"""Export generated questions to Excel format matching original structure."""

import pandas as pd
from pathlib import Path
from typing import Optional, Dict, List
import json
import random


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


def get_tag_definitions() -> pd.DataFrame:
    """
    Get definitions of all available tags.
    
    Returns:
        DataFrame with tag definitions
    """
    tags_data = [
        {'TAG_ID': '4', 'TAG_NAME': ':COUNTRY', 'CATEGORY': 'Geography'},
        {'TAG_ID': '7', 'TAG_NAME': ':COMPANY', 'CATEGORY': 'Business'},
        {'TAG_ID': '10', 'TAG_NAME': 'ED:HISTORY', 'CATEGORY': 'Education'},
        {'TAG_ID': '50', 'TAG_NAME': 'EN:MUSIC', 'CATEGORY': 'Entertainment'},
        {'TAG_ID': '51', 'TAG_NAME': 'EN:MOVIE', 'CATEGORY': 'Entertainment'},
        {'TAG_ID': '54', 'TAG_NAME': 'EN:Facts', 'CATEGORY': 'General'},
        {'TAG_ID': '99', 'TAG_NAME': 'NEW:Viral', 'CATEGORY': 'Trends'},
        {'TAG_ID': '100', 'TAG_NAME': 'NEW:Tech', 'CATEGORY': 'Technology'},
        {'TAG_ID': '101', 'TAG_NAME': 'NEW:Nostalgia', 'CATEGORY': 'Lifestyle'},
    ]
    return pd.DataFrame(tags_data)


def assign_tags(df: pd.DataFrame, min_tags: int = 2, max_tags: int = 5) -> pd.DataFrame:
    """
    Assign multiple tags to questions.
    
    Args:
        df: DataFrame with questions
        min_tags: Minimum number of tags per question
        max_tags: Maximum number of tags per question
        
    Returns:
        DataFrame with tags assigned (comma separated IDs)
    """
    df = df.copy()
    
    # Base mapping for primary tag
    primary_tag_mapping = {
        'countries': '4',      # :COUNTRY
        'artists': '50',        # EN:MUSIC
        'movies': '51',         # EN:MOVIE
        'brands': '7',          # :COMPANY
        'theme': '54',          # EN:Facts
        'field': '10',          # ED:HISTORY (generic)
    }
    
    # Additional tags pool
    additional_tags = ['99', '100', '101', '54', '10']
    
    def generate_tags(row):
        # Start with primary tag based on category
        category = row.get('category', 'theme')
        primary_tag = primary_tag_mapping.get(category, '54')
        
        current_tags = {primary_tag}
        
        # Determine how many tags to add
        num_total = random.randint(min_tags, max_tags)
        
        # Add random additional tags until we reach count
        available = [t for t in additional_tags if t != primary_tag]
        
        while len(current_tags) < num_total and available:
            tag = random.choice(available)
            current_tags.add(tag)
            available.remove(tag)
            
        return ','.join(sorted(list(current_tags)))

    df['tags'] = df.apply(generate_tags, axis=1)
    return df


def format_for_excel(df: pd.DataFrame, min_tags: int = 2, max_tags: int = 5) -> pd.DataFrame:
    """
    Format DataFrame to match original Excel structure.
    
    Args:
        df: DataFrame with generated questions
        min_tags: Minimum tags
        max_tags: Maximum tags
        
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
    
    # Always re-assign tags to ensure multi-tag requirement is met
    # (Unless tags are already pre-calculated correctly, but here we enforce the new rule)
    df = assign_tags(df, min_tags, max_tags)
    
    # Select and order columns to match original format
    excel_columns = ['QTYPE', 'QID', 'category_id', 'QEN', 'ACEN', 'AW1EN', 'AW2EN', 'ACID', 'AWID1', 'AWID2', 'tags']
    
    # Only include columns that exist
    available_columns = [col for col in excel_columns if col in df.columns]
    df = df[available_columns]
    
    # Reorder to match original
    df = df.reindex(columns=excel_columns, fill_value='')
    
    return df


def export_to_excel(df: pd.DataFrame, output_path: str = "outputs/generated_questions.xlsx", 
                   sheet_name: str = "data", min_tags: int = 2, max_tags: int = 5) -> None:
    """
    Export questions to Excel file matching original format with tag sheet.
    
    Args:
        df: DataFrame with questions
        output_path: Output file path
        sheet_name: Sheet name for data
        min_tags: Min tags per question
        max_tags: Max tags per question
    """
    # Format for Excel
    df_formatted = format_for_excel(df, min_tags, max_tags)
    
    # Get tag definitions
    df_tags = get_tag_definitions()
    
    # Create Excel file with multiple sheets
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        df_formatted.to_excel(writer, sheet_name=sheet_name, index=False)
        df_tags.to_excel(writer, sheet_name="tags", index=False)
    
    print(f"Exported {len(df_formatted)} questions to {output_path} (with {len(df_tags)} tags)")


def export_to_csv(df: pd.DataFrame, output_path: str = "outputs/generated_questions.csv",
                 min_tags: int = 2, max_tags: int = 5) -> None:
    """Export questions to CSV file."""
    df_formatted = format_for_excel(df, min_tags, max_tags)
    df_formatted.to_csv(output_path, index=False)
    print(f"Exported {len(df_formatted)} questions to {output_path}")


def export_to_json(df: pd.DataFrame, output_path: str = "outputs/generated_questions.json",
                  min_tags: int = 2, max_tags: int = 5) -> None:
    """Export questions to JSON file."""
    df_formatted = format_for_excel(df, min_tags, max_tags)
    df_formatted.to_json(output_path, orient='records', indent=2)
    print(f"Exported {len(df_formatted)} questions to {output_path}")
