"""Main question generator that creates questions from gap analysis."""

import pandas as pd
from typing import Dict, List, Any, Optional
from .gap_loader import get_prioritized_gaps
from .question_templates import (
    generate_country_question,
    generate_artist_question,
    generate_movie_question,
    generate_brand_question,
    generate_theme_question,
    generate_field_question
)
from .answer_generator import (
    generate_answers_for_country,
    generate_answers_for_artist,
    generate_answers_for_movie,
    generate_answers_for_brand,
    generate_answers_for_theme,
    generate_answers_for_field
)


def generate_question_from_entity(entity: str, category: str, reference_lists: Dict[str, List[str]]) -> Optional[Dict[str, Any]]:
    """
    Generate a question from an entity.
    
    Args:
        entity: Entity name (country, artist, movie, brand)
        category: Category type
        reference_lists: Reference lists for wrong answers
        
    Returns:
        Dictionary with question data or None if generation fails
    """
    try:
        # Generate question
        if category == 'countries':
            qen = generate_country_question(entity)
            answers = generate_answers_for_country(entity, reference_lists)
        elif category == 'artists':
            qen = generate_artist_question(entity)
            answers = generate_answers_for_artist(entity, reference_lists)
        elif category == 'movies':
            qen = generate_movie_question(entity)
            answers = generate_answers_for_movie(entity, reference_lists)
        elif category == 'brands':
            qen = generate_brand_question(entity)
            answers = generate_answers_for_brand(entity, reference_lists)
        else:
            return None
        
        return {
            'QEN': qen,
            'ACEN': answers['ACEN'],
            'AW1EN': answers['AW1EN'],
            'AW2EN': answers['AW2EN'],
            'QTYPE': 'text',
            'category': category,
            'source_entity': entity
        }
    except Exception as e:
        print(f"Error generating question for {entity}: {e}")
        return None


def generate_question_from_theme(theme: str, keywords: List[str], reference_lists: Dict[str, List[str]]) -> Optional[Dict[str, Any]]:
    """
    Generate a question from a theme.
    
    Args:
        theme: Theme name
        keywords: Keywords associated with theme
        reference_lists: Reference lists
        
    Returns:
        Dictionary with question data or None
    """
    try:
        qen = generate_theme_question(theme, keywords)
        answers = generate_answers_for_theme(theme, keywords, reference_lists)
        
        return {
            'QEN': qen,
            'ACEN': answers['ACEN'],
            'AW1EN': answers['AW1EN'],
            'AW2EN': answers['AW2EN'],
            'QTYPE': 'text',
            'category': 'theme',
            'source_theme': theme
        }
    except Exception as e:
        print(f"Error generating question for theme {theme}: {e}")
        return None


def generate_question_from_field(field: str, reference_lists: Dict[str, List[str]]) -> Optional[Dict[str, Any]]:
    """
    Generate a question from an underrepresented field.
    
    Args:
        field: Field name
        reference_lists: Reference lists
        
    Returns:
        Dictionary with question data or None
    """
    try:
        qen = generate_field_question(field)
        answers = generate_answers_for_field(field, reference_lists)
        
        return {
            'QEN': qen,
            'ACEN': answers['ACEN'],
            'AW1EN': answers['AW1EN'],
            'AW2EN': answers['AW2EN'],
            'QTYPE': 'text',
            'category': 'field',
            'source_field': field
        }
    except Exception as e:
        print(f"Error generating question for field {field}: {e}")
        return None


def generate_questions_from_gaps(num_questions: int = 100) -> pd.DataFrame:
    """
    Generate questions from gap analysis results.
    
    Args:
        num_questions: Number of questions to generate
        
    Returns:
        DataFrame with generated questions
    """
    print(f"Loading gap analysis results...")
    gaps = get_prioritized_gaps()
    reference_lists = gaps.get('reference_lists', {})
    
    generated_questions = []
    
    # Generate from missing entities (highest priority)
    print("Generating questions from missing entities...")
    entity_priorities = [
        ('artists', gaps['entities']['artists'], 0.4),  # 40% from artists
        ('countries', gaps['entities']['countries'], 0.2),  # 20% from countries
        ('movies', gaps['entities']['movies'], 0.2),  # 20% from movies
        ('brands', gaps['entities']['brands'], 0.1),  # 10% from brands
    ]
    
    for category, entities, proportion in entity_priorities:
        num_to_generate = int(num_questions * proportion)
        for entity in entities[:num_to_generate]:
            question = generate_question_from_entity(entity, category, reference_lists)
            if question:
                generated_questions.append(question)
            if len(generated_questions) >= num_questions:
                break
        if len(generated_questions) >= num_questions:
            break
    
    # Generate from themes (if we need more)
    if len(generated_questions) < num_questions:
        print("Generating questions from missing themes...")
        remaining = num_questions - len(generated_questions)
        for theme in gaps['themes'][:remaining]:
            # Extract keywords from theme (simplified)
            keywords = theme.split()[:3]
            question = generate_question_from_theme(theme, keywords, reference_lists)
            if question:
                generated_questions.append(question)
            if len(generated_questions) >= num_questions:
                break
    
    # Generate from fields (if we need more)
    if len(generated_questions) < num_questions:
        print("Generating questions from underrepresented fields...")
        remaining = num_questions - len(generated_questions)
        for field in gaps['fields'][:remaining]:
            question = generate_question_from_field(field, reference_lists)
            if question:
                generated_questions.append(question)
            if len(generated_questions) >= num_questions:
                break
    
    print(f"Generated {len(generated_questions)} questions")
    
    # Convert to DataFrame
    if generated_questions:
        df = pd.DataFrame(generated_questions)
        return df
    else:
        return pd.DataFrame(columns=['QEN', 'ACEN', 'AW1EN', 'AW2EN', 'QTYPE'])

