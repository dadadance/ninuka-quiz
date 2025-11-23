"""Sociological taxonomy analysis: keyword-based field coverage."""

import pandas as pd
import re
from typing import Dict, List, Any
from collections import defaultdict


def create_keyword_dictionaries() -> Dict[str, List[str]]:
    """
    Create keyword dictionaries for social fields.
    
    Returns:
        Dictionary mapping field name to list of keywords
    """
    return {
        'Domestic Sphere': [
            'cooking', 'recipe', 'kitchen', 'baking', 'cook', 'chef',
            'cleaning', 'clean', 'laundry', 'wash', 'tidy', 'organize',
            'pets', 'dog', 'cat', 'pet', 'animal', 'puppy', 'kitten',
            'gardening', 'garden', 'plant', 'flower', 'vegetable', 'herb',
            'home', 'house', 'decor', 'furniture', 'interior', 'room',
            'household', 'domestic', 'chore', 'maintenance'
        ],
        'Digital Life': [
            'emoji', 'emoticon', 'app', 'application', 'software',
            'social media', 'facebook', 'instagram', 'twitter', 'tiktok',
            'meme', 'viral', 'trend', 'hashtag', 'post', 'share',
            'slang', 'internet', 'online', 'digital', 'tech', 'device',
            'smartphone', 'phone', 'computer', 'laptop', 'tablet',
            'website', 'browser', 'search', 'google', 'youtube',
            'streaming', 'netflix', 'spotify', 'podcast', 'blog'
        ],
        'Nostalgia': [
            '90s', 'nineties', '2000s', 'millennium', 'retro', 'vintage',
            'old school', 'classic', 'throwback', 'nostalgic',
            'childhood', 'kid', 'toy', 'game', 'cartoon', 'tv show',
            'snack', 'candy', 'treat', 'memory', 'remember',
            'decade', 'era', 'generation', 'millennial', 'gen z'
        ],
        'Somatic/Body': [
            'sleep', 'rest', 'nap', 'bed', 'dream',
            'health', 'wellness', 'fitness', 'exercise', 'workout',
            'anatomy', 'body', 'organ', 'muscle', 'bone', 'skin',
            'diet', 'nutrition', 'vitamin', 'calorie', 'protein',
            'medical', 'doctor', 'hospital', 'medicine', 'treatment',
            'pain', 'ache', 'illness', 'disease', 'symptom'
        ],
        'Visual Memory': [
            'logo', 'brand', 'color', 'colour', 'icon', 'symbol',
            'visual', 'appearance', 'look', 'design', 'style',
            'shape', 'form', 'pattern', 'image', 'picture',
            'recognize', 'identify', 'appearance', 'aesthetic'
        ],
        'Common Sense': [
            'how to', 'how do', 'what is', 'what are',
            'basic', 'common', 'everyday', 'simple', 'easy',
            'practical', 'useful', 'tip', 'trick', 'hack',
            'should', 'must', 'need', 'require', 'important',
            'adulting', 'life skill', 'survival', 'essential'
        ]
    }


def search_keywords_in_text(text: str, keywords: List[str]) -> List[str]:
    """
    Search for keywords in text (case-insensitive, partial match).
    
    Args:
        text: Text to search
        keywords: List of keywords to find
        
    Returns:
        List of matched keywords
    """
    if pd.isna(text) or text == "":
        return []
    
    text_lower = str(text).lower()
    matched = []
    
    for keyword in keywords:
        # Check for exact word match or partial match
        pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
        if re.search(pattern, text_lower, re.IGNORECASE):
            matched.append(keyword)
    
    return matched


def analyze_field_coverage(df: pd.DataFrame, keyword_dict: Dict[str, List[str]]) -> Dict[str, Any]:
    """
    Analyze coverage of each social field.
    
    Args:
        df: Questions dataframe
        keyword_dict: Dictionary of field names to keywords
        
    Returns:
        Dictionary with coverage analysis
    """
    print("Analyzing sociological taxonomy coverage...")
    
    field_matches = defaultdict(lambda: {'questions': [], 'count': 0})
    total_questions = len(df)
    
    # Search in questions
    for idx, row in df.iterrows():
        question_text = str(row.get('QEN', '')).lower()
        combined_text = str(row.get('combined_text', '')).lower()
        
        for field_name, keywords in keyword_dict.items():
            matches = search_keywords_in_text(combined_text, keywords)
            if matches:
                field_matches[field_name]['questions'].append({
                    'QID': row.get('QID'),
                    'QEN': row.get('QEN'),
                    'matched_keywords': matches
                })
                field_matches[field_name]['count'] += 1
    
    # Calculate percentages
    coverage_results = {}
    for field_name, data in field_matches.items():
        count = data['count']
        percentage = (count / total_questions) * 100 if total_questions > 0 else 0
        coverage_results[field_name] = {
            'count': count,
            'percentage': percentage,
            'sample_questions': data['questions'][:10]  # Sample questions
        }
    
    return coverage_results


def identify_underrepresented_fields(coverage_results: Dict[str, Any],
                                     threshold: float = 5.0) -> List[str]:
    """
    Identify fields with coverage below threshold.
    
    Args:
        coverage_results: Field coverage analysis
        threshold: Percentage threshold (default 5%)
        
    Returns:
        List of underrepresented field names
    """
    underrepresented = []
    
    for field_name, data in coverage_results.items():
        if data['percentage'] < threshold:
            underrepresented.append(field_name)
    
    return underrepresented


def generate_taxonomy_report(coverage_results: Dict[str, Any],
                            output_path: str = "outputs/taxonomy_coverage.csv") -> pd.DataFrame:
    """
    Generate taxonomy coverage report.
    
    Args:
        coverage_results: Field coverage analysis
        output_path: Output file path
        
    Returns:
        Report dataframe
    """
    rows = []
    
    for field_name, data in coverage_results.items():
        rows.append({
            'field': field_name,
            'question_count': data['count'],
            'coverage_percentage': data['percentage'],
            'status': 'underrepresented' if data['percentage'] < 5.0 else 'adequate'
        })
    
    df = pd.DataFrame(rows)
    df = df.sort_values('coverage_percentage', ascending=True)
    df.to_csv(output_path, index=False)
    
    print(f"Taxonomy coverage report saved to {output_path}")
    
    underrepresented = identify_underrepresented_fields(coverage_results)
    if underrepresented:
        print(f"Underrepresented fields (<5%): {', '.join(underrepresented)}")
    else:
        print("All fields have adequate coverage (>=5%)")
    
    return df


def analyze_sociological_taxonomy(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Complete sociological taxonomy analysis pipeline.
    
    Args:
        df: Questions dataframe
        
    Returns:
        Dictionary with all taxonomy analysis results
    """
    keyword_dict = create_keyword_dictionaries()
    
    coverage_results = analyze_field_coverage(df, keyword_dict)
    
    underrepresented = identify_underrepresented_fields(coverage_results)
    
    print("Generating taxonomy report...")
    report_df = generate_taxonomy_report(coverage_results)
    
    return {
        'keyword_dict': keyword_dict,
        'coverage_results': coverage_results,
        'underrepresented_fields': underrepresented,
        'report_df': report_df
    }

