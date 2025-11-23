"""Quality analysis: character limits, answer quality, format diversity."""

import pandas as pd
import re
from typing import Dict, List, Any
from .utils import validate_character_limit


def check_character_limits(df: pd.DataFrame, limit: int = 100) -> pd.DataFrame:
    """
    Check character limits for all text fields.
    
    Args:
        df: Questions dataframe
        limit: Character limit (default 100)
        
    Returns:
        Dataframe with violation flags
    """
    df = df.copy()
    
    text_columns = ['QEN', 'ACEN', 'AW1EN', 'AW2EN']
    for col in text_columns:
        if col in df.columns:
            df[f'{col}_violates_limit'] = ~df[col].apply(
                lambda x: validate_character_limit(x, limit)
            )
    
    # Overall violation flag
    violation_cols = [f'{col}_violates_limit' for col in text_columns if f'{col}_violates_limit' in df.columns]
    if violation_cols:
        df['has_violation'] = df[violation_cols].any(axis=1)
    
    return df


def analyze_answer_quality(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyze answer quality: completeness, uniqueness, etc.
    
    Args:
        df: Questions dataframe
        
    Returns:
        Dictionary with quality metrics
    """
    metrics = {}
    
    # Completeness
    total = len(df)
    metrics['total_questions'] = total
    
    metrics['qen_complete'] = df['QEN'].notna().sum()
    metrics['qen_complete_pct'] = (metrics['qen_complete'] / total) * 100
    
    metrics['acen_complete'] = df['ACEN'].notna().sum()
    metrics['acen_complete_pct'] = (metrics['acen_complete'] / total) * 100
    
    metrics['aw1en_complete'] = df['AW1EN'].notna().sum()
    metrics['aw1en_complete_pct'] = (metrics['aw1en_complete'] / total) * 100
    
    metrics['aw2en_complete'] = df['AW2EN'].notna().sum()
    metrics['aw2en_complete_pct'] = (metrics['aw2en_complete'] / total) * 100
    
    # Uniqueness of answers
    metrics['unique_acen'] = df['ACEN'].nunique()
    metrics['unique_aw1en'] = df['AW1EN'].nunique()
    metrics['unique_aw2en'] = df['AW2EN'].nunique()
    
    # Check for duplicate answers within same question
    def has_duplicate_answers(row):
        answers = [str(row.get('ACEN', '')), str(row.get('AW1EN', '')), str(row.get('AW2EN', ''))]
        answers = [a.strip().lower() for a in answers if a.strip()]
        return len(answers) != len(set(answers))
    
    df['has_duplicate_answers'] = df.apply(has_duplicate_answers, axis=1)
    metrics['duplicate_answers_count'] = df['has_duplicate_answers'].sum()
    metrics['duplicate_answers_pct'] = (metrics['duplicate_answers_count'] / total) * 100
    
    # Answer length analysis
    metrics['avg_qen_length'] = df['QEN_length'].mean()
    metrics['avg_acen_length'] = df['ACEN_length'].mean()
    metrics['avg_aw1en_length'] = df['AW1EN_length'].mean()
    metrics['avg_aw2en_length'] = df['AW2EN_length'].mean()
    
    return metrics


def identify_question_formats(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Identify question format patterns.
    
    Args:
        df: Questions dataframe
        
    Returns:
        Dictionary with format analysis
    """
    formats = {}
    
    # Common question patterns
    patterns = {
        'what_is': r'^what\s+(is|are)',
        'which': r'^which',
        'who': r'^who',
        'where': r'^where',
        'when': r'^when',
        'name': r'^name',
        'complete': r'complete|fill\s+in',
        'true_false': r'^(true|false)',
        'how_many': r'^how\s+many',
        'what_color': r'what\s+color',
        'what_country': r'what\s+country|which\s+country',
    }
    
    format_counts = {}
    format_questions = {}
    
    for pattern_name, pattern in patterns.items():
        mask = df['QEN'].str.contains(pattern, case=False, na=False, regex=True)
        count = mask.sum()
        format_counts[pattern_name] = count
        format_questions[pattern_name] = df[mask]['QID'].tolist()[:10]  # Sample QIDs
    
    formats['format_counts'] = format_counts
    formats['format_questions'] = format_questions
    formats['total_formatted'] = sum(format_counts.values())
    formats['unformatted_count'] = len(df) - formats['total_formatted']
    
    return formats


def generate_quality_report(df: pd.DataFrame, output_path: str = "outputs/quality_report.csv") -> pd.DataFrame:
    """
    Generate comprehensive quality report.
    
    Args:
        df: Questions dataframe with quality checks
        output_path: Path to save report
        
    Returns:
        Report dataframe
    """
    # Character limit violations
    violation_df = df[df['has_violation'] == True][
        ['QID', 'QTYPE', 'QEN', 'QEN_length', 'ACEN_length', 'AW1EN_length', 'AW2EN_length']
    ].copy()
    
    # Quality metrics
    metrics = analyze_answer_quality(df)
    formats = identify_question_formats(df)
    
    # Create summary report
    report_data = {
        'metric': [],
        'value': [],
        'percentage': []
    }
    
    # Add metrics to report
    for key, value in metrics.items():
        if 'pct' in key:
            continue
        report_data['metric'].append(key)
        report_data['value'].append(value)
        if f'{key}_pct' in metrics:
            report_data['percentage'].append(metrics[f'{key}_pct'])
        else:
            report_data['percentage'].append(None)
    
    report_df = pd.DataFrame(report_data)
    
    # Save violation details
    if len(violation_df) > 0:
        violation_df.to_csv(output_path.replace('.csv', '_violations.csv'), index=False)
    
    # Save report
    report_df.to_csv(output_path, index=False)
    
    print(f"Quality report saved to {output_path}")
    print(f"Total violations: {len(violation_df)}")
    print(f"Format diversity: {len(formats['format_counts'])} different patterns")
    
    return report_df


def analyze_quality(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Complete quality analysis pipeline.
    
    Args:
        df: Questions dataframe
        
    Returns:
        Dictionary with all quality metrics and reports
    """
    print("Checking character limits...")
    df = check_character_limits(df)
    
    print("Analyzing answer quality...")
    metrics = analyze_answer_quality(df)
    
    print("Identifying question formats...")
    formats = identify_question_formats(df)
    
    print("Generating quality report...")
    report_df = generate_quality_report(df)
    
    return {
        'dataframe': df,
        'metrics': metrics,
        'formats': formats,
        'report': report_df
    }

