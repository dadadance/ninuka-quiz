"""Named Entity Recognition analysis using spaCy."""

import pandas as pd
import json
from pathlib import Path
from collections import Counter, defaultdict
from typing import Dict, List, Any, Set
import spacy


def load_spacy_model():
    """Load spaCy English model."""
    try:
        nlp = spacy.load("en_core_web_sm")
        return nlp
    except OSError:
        print("spaCy model 'en_core_web_sm' not found. Please install it:")
        print("python -m spacy download en_core_web_sm")
        raise


def extract_entities(text: str, nlp) -> Dict[str, List[str]]:
    """
    Extract named entities from text.
    
    Args:
        text: Input text
        nlp: spaCy model
        
    Returns:
        Dictionary mapping entity type to list of entities
    """
    if pd.isna(text) or text == "":
        return defaultdict(list)
    
    doc = nlp(str(text))
    entities = defaultdict(list)
    
    for ent in doc.ents:
        entities[ent.label_].append(ent.text)
    
    return entities


def extract_all_entities(df: pd.DataFrame, nlp) -> Dict[str, Any]:
    """
    Extract entities from all questions and answers.
    
    Args:
        df: Questions dataframe
        nlp: spaCy model
        
    Returns:
        Dictionary with entity analysis
    """
    print("Extracting entities from questions and answers...")
    
    all_entities = defaultdict(lambda: Counter())
    question_entities = defaultdict(lambda: Counter())
    answer_entities = defaultdict(lambda: Counter())
    
    # Extract from questions
    for idx, row in df.iterrows():
        q_entities = extract_entities(row.get('QEN', ''), nlp)
        for ent_type, ent_list in q_entities.items():
            question_entities[ent_type].update(ent_list)
            all_entities[ent_type].update(ent_list)
        
        # Extract from answers
        for col in ['ACEN', 'AW1EN', 'AW2EN']:
            if col in row:
                a_entities = extract_entities(row[col], nlp)
                for ent_type, ent_list in a_entities.items():
                    answer_entities[ent_type].update(ent_list)
                    all_entities[ent_type].update(ent_list)
    
    return {
        'all_entities': dict(all_entities),
        'question_entities': dict(question_entities),
        'answer_entities': dict(answer_entities)
    }


def load_reference_list(file_path: str) -> List[str]:
    """Load reference list from JSON file."""
    with open(file_path, 'r') as f:
        return json.load(f)


def normalize_entity_name(name: str) -> str:
    """Normalize entity name for comparison."""
    return name.strip().lower()


def compare_entities_to_reference(extracted_entities: Dict[str, Counter],
                                  reference_list: List[str],
                                  entity_type: str = "GPE") -> Dict[str, Any]:
    """
    Compare extracted entities against reference list.
    
    Args:
        extracted_entities: Dictionary of entity type to Counter
        reference_list: List of reference entities
        entity_type: Entity type to compare (e.g., 'GPE' for countries)
        
    Returns:
        Dictionary with comparison results
    """
    if entity_type not in extracted_entities:
        return {
            'found': [],
            'missing': reference_list,
            'found_count': 0,
            'missing_count': len(reference_list),
            'coverage_pct': 0.0
        }
    
    extracted = set(normalize_entity_name(e) for e in extracted_entities[entity_type].keys())
    reference = set(normalize_entity_name(e) for e in reference_list)
    
    found = [e for e in reference_list if normalize_entity_name(e) in extracted]
    missing = [e for e in reference_list if normalize_entity_name(e) not in extracted]
    
    coverage_pct = (len(found) / len(reference_list)) * 100 if reference_list else 0.0
    
    return {
        'found': found,
        'missing': missing,
        'found_count': len(found),
        'missing_count': len(missing),
        'coverage_pct': coverage_pct
    }


def analyze_entity_coverage(df: pd.DataFrame, nlp) -> Dict[str, Any]:
    """
    Complete entity coverage analysis.
    
    Args:
        df: Questions dataframe
        nlp: spaCy model
        
    Returns:
        Dictionary with entity coverage analysis
    """
    # Extract entities
    entity_data = extract_all_entities(df, nlp)
    
    # Load reference lists
    ref_dir = Path("data/reference_lists")
    
    countries_ref = load_reference_list(ref_dir / "top_countries.json")
    artists_ref = load_reference_list(ref_dir / "top_artists.json")
    movies_ref = load_reference_list(ref_dir / "top_movies.json")
    brands_ref = load_reference_list(ref_dir / "top_brands.json")
    
    # Compare entities
    print("Comparing entities to reference lists...")
    
    # Countries (GPE - Geopolitical Entity)
    countries_comparison = compare_entities_to_reference(
        entity_data['all_entities'], countries_ref, 'GPE'
    )
    
    # Artists (PERSON or ORG)
    artists_comparison = compare_entities_to_reference(
        entity_data['all_entities'], artists_ref, 'PERSON'
    )
    
    # Movies (WORK_OF_ART or PRODUCT)
    movies_comparison = compare_entities_to_reference(
        entity_data['all_entities'], movies_ref, 'WORK_OF_ART'
    )
    
    # Brands (ORG or PRODUCT)
    brands_comparison = compare_entities_to_reference(
        entity_data['all_entities'], brands_ref, 'ORG'
    )
    
    return {
        'entity_data': entity_data,
        'countries': countries_comparison,
        'artists': artists_comparison,
        'movies': movies_comparison,
        'brands': brands_comparison
    }


def generate_entity_report(coverage_analysis: Dict[str, Any],
                           output_path: str = "outputs/entity_coverage.csv") -> pd.DataFrame:
    """
    Generate entity coverage report.
    
    Args:
        coverage_analysis: Entity coverage analysis results
        output_path: Output file path
        
    Returns:
        Report dataframe
    """
    rows = []
    
    # Entity type frequencies
    for ent_type, counter in coverage_analysis['entity_data']['all_entities'].items():
        top_entities = counter.most_common(20)
        for entity, count in top_entities:
            rows.append({
                'entity_type': ent_type,
                'entity': entity,
                'frequency': count,
                'category': 'extracted'
            })
    
    # Missing entities
    for category, comparison in [
        ('countries', coverage_analysis['countries']),
        ('artists', coverage_analysis['artists']),
        ('movies', coverage_analysis['movies']),
        ('brands', coverage_analysis['brands'])
    ]:
        for missing_entity in comparison['missing'][:20]:  # Top 20 missing
            rows.append({
                'entity_type': category,
                'entity': missing_entity,
                'frequency': 0,
                'category': 'missing'
            })
    
    df = pd.DataFrame(rows)
    df.to_csv(output_path, index=False)
    
    print(f"Entity coverage report saved to {output_path}")
    print(f"Countries coverage: {coverage_analysis['countries']['coverage_pct']:.1f}%")
    print(f"Artists coverage: {coverage_analysis['artists']['coverage_pct']:.1f}%")
    print(f"Movies coverage: {coverage_analysis['movies']['coverage_pct']:.1f}%")
    print(f"Brands coverage: {coverage_analysis['brands']['coverage_pct']:.1f}%")
    
    return df


def analyze_entities(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Complete entity recognition pipeline.
    
    Args:
        df: Questions dataframe
        
    Returns:
        Dictionary with all entity analysis results
    """
    print("Loading spaCy model...")
    nlp = load_spacy_model()
    
    coverage_analysis = analyze_entity_coverage(df, nlp)
    
    print("Generating entity report...")
    report_df = generate_entity_report(coverage_analysis)
    
    return {
        'coverage_analysis': coverage_analysis,
        'report_df': report_df
    }

