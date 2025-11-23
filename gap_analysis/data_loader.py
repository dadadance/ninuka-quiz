"""Load and prepare quiz data from Excel file."""

import pandas as pd
from pathlib import Path
from typing import Dict, Tuple
from .utils import clean_text, parse_tag_ids, get_character_count


def load_excel_data(excel_path: str = "ninouk2.xlsx") -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load both sheets from Excel file.
    
    Args:
        excel_path: Path to Excel file
        
    Returns:
        Tuple of (questions_df, tags_df)
    """
    if not Path(excel_path).exists():
        raise FileNotFoundError(f"Excel file not found: {excel_path}")
    
    excel_data = pd.read_excel(excel_path, sheet_name=None, engine='openpyxl')
    
    if 'data' not in excel_data:
        raise ValueError("Excel file must contain 'data' sheet")
    if 'cats_tags' not in excel_data:
        raise ValueError("Excel file must contain 'cats_tags' sheet")
    
    questions_df = excel_data['data']
    tags_df = excel_data['cats_tags']
    
    return questions_df, tags_df


def merge_tag_information(questions_df: pd.DataFrame, tags_df: pd.DataFrame) -> pd.DataFrame:
    """
    Merge tag information from cats_tags sheet into questions dataframe.
    
    Args:
        questions_df: Questions dataframe
        tags_df: Tags/categories dataframe
        
    Returns:
        Questions dataframe with merged tag information
    """
    df = questions_df.copy()
    
    # Create tag mapping dictionary
    tag_map = {}
    for _, row in tags_df.iterrows():
        tag_id = row['id']
        tag_name = row['tag']
        category = row.get('category', None)
        code = row.get('code', None)
        
        tag_map[tag_id] = {
            'tag_name': tag_name,
            'category': category,
            'code': code
        }
    
    # Parse tag IDs and create tag columns
    df['tag_ids'] = df['tags'].apply(parse_tag_ids)
    df['tag_names'] = df['tag_ids'].apply(
        lambda ids: [tag_map.get(id, {}).get('tag_name', f'Unknown_{id}') for id in ids]
    )
    df['tag_categories'] = df['tag_ids'].apply(
        lambda ids: [tag_map.get(id, {}).get('category', None) for id in ids if tag_map.get(id, {}).get('category')]
    )
    df['tag_codes'] = df['tag_ids'].apply(
        lambda ids: [tag_map.get(id, {}).get('code', None) for id in ids if tag_map.get(id, {}).get('code')]
    )
    
    # Get primary category from category_id
    category_map = {}
    for _, row in tags_df.iterrows():
        if pd.notna(row.get('id.1')):
            cat_id = int(row['id.1'])
            category_map[cat_id] = row.get('category', None)
    
    df['primary_category'] = df['category_id'].map(category_map)
    
    return df


def clean_question_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean question data: text cleaning, handle NaN values.
    
    Args:
        df: Questions dataframe
        
    Returns:
        Cleaned dataframe
    """
    df = df.copy()
    
    # Clean text columns
    text_columns = ['QEN', 'ACEN', 'AW1EN', 'AW2EN']
    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].apply(clean_text)
    
    # Fill NaN with empty string for text columns
    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].fillna('')
    
    return df


def add_character_lengths(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add character length columns for QEN, ACEN, AW1EN, AW2EN.
    
    Args:
        df: Questions dataframe
        
    Returns:
        Dataframe with character length columns
    """
    df = df.copy()
    
    text_columns = ['QEN', 'ACEN', 'AW1EN', 'AW2EN']
    for col in text_columns:
        if col in df.columns:
            df[f'{col}_length'] = df[col].apply(get_character_count)
    
    return df


def create_combined_text(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create combined text field (question + answers) for analysis.
    
    Args:
        df: Questions dataframe
        
    Returns:
        Dataframe with combined_text column
    """
    df = df.copy()
    
    def combine_text(row):
        parts = []
        if pd.notna(row.get('QEN')):
            parts.append(str(row['QEN']))
        if pd.notna(row.get('ACEN')):
            parts.append(str(row['ACEN']))
        if pd.notna(row.get('AW1EN')):
            parts.append(str(row['AW1EN']))
        if pd.notna(row.get('AW2EN')):
            parts.append(str(row['AW2EN']))
        return ' '.join(parts)
    
    df['combined_text'] = df.apply(combine_text, axis=1)
    
    return df


def load_and_prepare_data(excel_path: str = "ninouk2.xlsx") -> pd.DataFrame:
    """
    Complete data loading and preparation pipeline.
    
    Args:
        excel_path: Path to Excel file
        
    Returns:
        Fully prepared dataframe with all metadata
    """
    print(f"Loading data from {excel_path}...")
    questions_df, tags_df = load_excel_data(excel_path)
    
    print(f"Loaded {len(questions_df)} questions and {len(tags_df)} tags")
    
    print("Cleaning question data...")
    questions_df = clean_question_data(questions_df)
    
    print("Merging tag information...")
    questions_df = merge_tag_information(questions_df, tags_df)
    
    print("Adding character lengths...")
    questions_df = add_character_lengths(questions_df)
    
    print("Creating combined text field...")
    questions_df = create_combined_text(questions_df)
    
    print(f"Data preparation complete. Final dataset: {len(questions_df)} questions")
    
    return questions_df

