"""Load and parse gap analysis results."""

import pandas as pd
import json
from pathlib import Path
from typing import Dict, List, Any
import re


def load_gap_analysis_report(report_path: str = "outputs/gap_analysis_report.md") -> Dict[str, Any]:
    """
    Load and parse the gap analysis report.
    
    Args:
        report_path: Path to gap analysis report markdown file
        
    Returns:
        Dictionary with parsed gap information
    """
    if not Path(report_path).exists():
        return {
            'missing_themes': [],
            'missing_entities': [],
            'underrepresented_fields': [],
            'format_recommendations': []
        }
    
    with open(report_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    gaps = {
        'missing_themes': [],
        'missing_entities': {'countries': [], 'artists': [], 'movies': [], 'brands': []},
        'underrepresented_fields': [],
        'format_recommendations': []
    }
    
    # Extract missing themes
    theme_section = re.search(r'## 1\. Missing Themes.*?## 2\.', content, re.DOTALL)
    if theme_section:
        theme_text = theme_section.group(0)
        theme_matches = re.findall(r'### \d+\. (.+?)\n', theme_text)
        gaps['missing_themes'] = [t.strip() for t in theme_matches]
    
    # Extract missing entities
    entity_section = re.search(r'## 2\. Missing Entities.*?## 3\.', content, re.DOTALL)
    if entity_section:
        entity_text = entity_section.group(0)
        for category in ['countries', 'artists', 'movies', 'brands']:
            cat_section = re.search(rf'### {category.capitalize()}\n.*?- \*\*Missing\*\*: (.+?)\n', entity_text, re.DOTALL)
            if cat_section:
                missing_list = cat_section.group(1).split(', ')
                gaps['missing_entities'][category] = [e.strip() for e in missing_list if e.strip()]
    
    # Extract underrepresented fields
    field_section = re.search(r'## 3\. Underrepresented Social Fields.*?## 4\.', content, re.DOTALL)
    if field_section:
        field_text = field_section.group(0)
        field_matches = re.findall(r'### (.+?)\n', field_text)
        gaps['underrepresented_fields'] = [f.strip() for f in field_matches if f.strip()]
    
    return gaps


def load_entity_coverage(csv_path: str = "outputs/entity_coverage.csv") -> Dict[str, List[str]]:
    """
    Load entity coverage CSV to find missing entities.
    
    Args:
        csv_path: Path to entity coverage CSV
        
    Returns:
        Dictionary mapping category to list of missing entities
    """
    if not Path(csv_path).exists():
        return {'countries': [], 'artists': [], 'movies': [], 'brands': []}
    
    df = pd.read_csv(csv_path)
    missing = {'countries': [], 'artists': [], 'movies': [], 'brands': []}
    
    # Filter for missing entities (category == 'missing')
    missing_df = df[df['category'] == 'missing']
    
    for _, row in missing_df.iterrows():
        entity_type = row.get('entity_type', '').lower()
        entity = row.get('entity', '')
        if entity_type in missing and entity:
            missing[entity_type].append(entity)
    
    return missing


def load_taxonomy_coverage(csv_path: str = "outputs/taxonomy_coverage.csv") -> List[Dict[str, Any]]:
    """
    Load taxonomy coverage to find underrepresented fields.
    
    Args:
        csv_path: Path to taxonomy coverage CSV
        
    Returns:
        List of underrepresented fields with coverage data
    """
    if not Path(csv_path).exists():
        return []
    
    df = pd.read_csv(csv_path)
    # Filter for underrepresented fields (< 5% coverage)
    underrepresented = df[df['coverage_percentage'] < 5.0].to_dict('records')
    return underrepresented


def load_reference_lists() -> Dict[str, List[str]]:
    """
    Load reference lists for entity generation.
    
    Returns:
        Dictionary mapping category to list of entities
    """
    ref_dir = Path("data/reference_lists")
    reference_lists = {}
    
    for category in ['countries', 'artists', 'movies', 'brands']:
        file_path = ref_dir / f"top_{category}.json"
        if file_path.exists():
            with open(file_path, 'r') as f:
                reference_lists[category] = json.load(f)
        else:
            reference_lists[category] = []
    
    return reference_lists


def get_prioritized_gaps() -> Dict[str, Any]:
    """
    Get prioritized gaps from all sources.
    
    Returns:
        Dictionary with prioritized gaps ready for question generation
    """
    # Load from multiple sources
    report_gaps = load_gap_analysis_report()
    entity_gaps = load_entity_coverage()
    taxonomy_gaps = load_taxonomy_coverage()
    reference_lists = load_reference_lists()
    
    # Combine and prioritize
    prioritized = {
        'themes': report_gaps.get('missing_themes', [])[:20],  # Top 20
        'entities': {
            'countries': entity_gaps.get('countries', [])[:10],
            'artists': entity_gaps.get('artists', [])[:20],
            'movies': entity_gaps.get('movies', [])[:15],
            'brands': entity_gaps.get('brands', [])[:15]
        },
        'fields': [f['field'] for f in taxonomy_gaps[:10]],  # Top 10 underrepresented
        'reference_lists': reference_lists
    }
    
    return prioritized

