"""Validate generated questions against constraints."""

import pandas as pd
from typing import Dict, List, Tuple, Any
import re


def validate_character_limit(text: str, limit: int = 100) -> bool:
    """Check if text is within character limit."""
    if pd.isna(text) or text == "":
        return False
    return len(str(text)) <= limit


def validate_question(question_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate a single question.
    
    Args:
        question_data: Dictionary with question data
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    
    # Check required fields
    required_fields = ['QEN', 'ACEN', 'AW1EN', 'AW2EN']
    for field in required_fields:
        if field not in question_data or pd.isna(question_data[field]) or question_data[field] == "":
            errors.append(f"Missing or empty {field}")
    
    if errors:
        return False, errors
    
    # Check character limits
    if not validate_character_limit(question_data['QEN'], 100):
        errors.append(f"Question too long: {len(str(question_data['QEN']))} chars")
    
    if not validate_character_limit(question_data['ACEN'], 100):
        errors.append(f"Correct answer too long: {len(str(question_data['ACEN']))} chars")
    
    if not validate_character_limit(question_data['AW1EN'], 100):
        errors.append(f"Wrong answer 1 too long: {len(str(question_data['AW1EN']))} chars")
    
    if not validate_character_limit(question_data['AW2EN'], 100):
        errors.append(f"Wrong answer 2 too long: {len(str(question_data['AW2EN']))} chars")
    
    # Check for duplicate answers
    answers = [
        str(question_data['ACEN']).strip().lower(),
        str(question_data['AW1EN']).strip().lower(),
        str(question_data['AW2EN']).strip().lower()
    ]
    if len(answers) != len(set(answers)):
        errors.append("Duplicate answers found")
    
    # Check question format (should not be empty or just whitespace)
    qen = str(question_data['QEN']).strip()
    if len(qen) < 10:  # Minimum reasonable question length
        errors.append("Question too short")
    
    # Check for question mark (optional but preferred)
    if not qen.endswith('?'):
        # Not an error, just a note
        pass
    
    is_valid = len(errors) == 0
    return is_valid, errors


def validate_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validate all questions in a DataFrame.
    
    Args:
        df: DataFrame with questions
        
    Returns:
        DataFrame with validation results added
    """
    df = df.copy()
    
    validation_results = []
    for idx, row in df.iterrows():
        is_valid, errors = validate_question(row.to_dict())
        validation_results.append({
            'is_valid': is_valid,
            'errors': '; '.join(errors) if errors else '',
            'error_count': len(errors)
        })
    
    validation_df = pd.DataFrame(validation_results)
    df = pd.concat([df, validation_df], axis=1)
    
    valid_count = validation_df['is_valid'].sum()
    total_count = len(df)
    
    print(f"Validation complete: {valid_count}/{total_count} questions are valid ({valid_count/total_count*100:.1f}%)")
    
    if valid_count < total_count:
        invalid = df[~df['is_valid']]
        print(f"\nInvalid questions ({len(invalid)}):")
        for idx, row in invalid.head(10).iterrows():
            print(f"  - {row.get('QEN', 'N/A')[:50]}... Errors: {row.get('errors', 'N/A')}")
    
    return df


def filter_valid_questions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filter DataFrame to only include valid questions.
    
    Args:
        df: DataFrame with questions and validation columns
        
    Returns:
        DataFrame with only valid questions
    """
    if 'is_valid' in df.columns:
        return df[df['is_valid'] == True].copy()
    else:
        # If no validation column, validate first
        validated_df = validate_dataframe(df)
        return validated_df[validated_df['is_valid'] == True].copy()

