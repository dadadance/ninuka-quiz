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
from .semantic_checker import validate_semantics


def generate_question_from_entity(entity: str, category: str, reference_lists: Dict[str, List[str]]) -> Optional[Dict[str, Any]]:
    """
    Generate a question from an entity.
    """
    try:
        # Generate question
        answers = None
        qen = None
        
        if category == 'countries':
            answers = generate_answers_for_country(entity, reference_lists)
            if 'QEN' in answers:
                qen = answers['QEN']
            else:
                qen = generate_country_question(entity)
        elif category == 'artists':
            answers = generate_answers_for_artist(entity, reference_lists)
            if 'QEN' in answers:
                qen = answers['QEN']
            else:
                qen = generate_artist_question(entity)
        elif category == 'movies':
            answers = generate_answers_for_movie(entity, reference_lists)
            if 'QEN' in answers:
                qen = answers['QEN']
            else:
                qen = generate_movie_question(entity)
        elif category == 'brands':
            answers = generate_answers_for_brand(entity, reference_lists)
            if 'QEN' in answers:
                qen = answers['QEN']
            else:
                qen = generate_brand_question(entity)
        else:
            return None
        
        question_data = {
            'QEN': qen,
            'ACEN': answers['ACEN'],
            'AW1EN': answers['AW1EN'],
            'AW2EN': answers['AW2EN'],
            'QTYPE': 'text',
            'category': category,
            'source_entity': entity
        }
        
        # Semantic Validation
        is_valid, errors = validate_semantics(question_data)
        if not is_valid:
            # print(f"Skipping question for {entity}: {errors[0]}") # Optional logging
            return None
            
        return question_data
        
    except Exception as e:
        print(f"Error generating question for {entity}: {e}")
        return None


def generate_question_from_theme(theme: str, keywords: List[str], reference_lists: Dict[str, List[str]]) -> Optional[Dict[str, Any]]:
    """
    Generate a question from a theme.
    """
    try:
        answers = generate_answers_for_theme(theme, keywords, reference_lists)
        
        if 'QEN' in answers:
            qen = answers['QEN']
        else:
            qen = generate_theme_question(theme, keywords)
        
        question_data = {
            'QEN': qen,
            'ACEN': answers['ACEN'],
            'AW1EN': answers['AW1EN'],
            'AW2EN': answers['AW2EN'],
            'QTYPE': 'text',
            'category': 'theme',
            'source_theme': theme
        }
        
        # Semantic Validation
        is_valid, errors = validate_semantics(question_data)
        if not is_valid:
            return None
            
        return question_data
        
    except Exception as e:
        print(f"Error generating question for theme {theme}: {e}")
        return None


def generate_question_from_field(field: str, reference_lists: Dict[str, List[str]]) -> Optional[Dict[str, Any]]:
    """
    Generate a question from an underrepresented field.
    """
    try:
        answers = generate_answers_for_field(field, reference_lists)
        
        if 'QEN' in answers:
            qen = answers['QEN']
        else:
            qen = generate_field_question(field)
        
        question_data = {
            'QEN': qen,
            'ACEN': answers['ACEN'],
            'AW1EN': answers['AW1EN'],
            'AW2EN': answers['AW2EN'],
            'QTYPE': 'text',
            'category': 'field',
            'source_field': field
        }
        
        # Semantic Validation
        is_valid, errors = validate_semantics(question_data)
        if not is_valid:
            return None
            
        return question_data
        
    except Exception as e:
        print(f"Error generating question for field {field}: {e}")
        return None


def generate_questions_from_gaps(num_questions: int = 100) -> pd.DataFrame:
    """
    Generate questions from gap analysis results.
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
        target_count = int(num_questions * proportion)
        current_cat_count = 0
        
        # Use ALL entities available, not just slice, to handle rejections
        for entity in entities:
            if current_cat_count >= target_count:
                break
                
            question = generate_question_from_entity(entity, category, reference_lists)
            if question:
                generated_questions.append(question)
                current_cat_count += 1
                
            if len(generated_questions) >= num_questions:
                break
        if len(generated_questions) >= num_questions:
            break
    
    # Generate from themes (if we need more)
    if len(generated_questions) < num_questions:
        print("Generating questions from missing themes...")
        remaining = num_questions - len(generated_questions)
        
        for theme in gaps['themes']:
            if len(generated_questions) >= num_questions:
                break
                
            # Extract keywords from theme (simplified)
            keywords = theme.split()[:3]
            question = generate_question_from_theme(theme, keywords, reference_lists)
            if question:
                generated_questions.append(question)
    
    # Generate from fields (if we need more)
    if len(generated_questions) < num_questions:
        print("Generating questions from underrepresented fields...")
        remaining = num_questions - len(generated_questions)
        
        # Cycle through fields if we run out
        fields = gaps['fields']
        if not fields:
            fields = ['Common Sense', 'Domestic Sphere', 'Digital Life'] # Fallback
            
        import itertools
        field_cycle = itertools.cycle(fields)
        
        count = 0
        max_attempts = remaining * 3
        
        for field in field_cycle:
            if len(generated_questions) >= num_questions or count > max_attempts:
                break
            
            question = generate_question_from_field(field, reference_lists)
            if question:
                generated_questions.append(question)
            
            count += 1
    
    print(f"Generated {len(generated_questions)} questions")
    
    # Convert to DataFrame
    if generated_questions:
        df = pd.DataFrame(generated_questions)
        return df
    else:
        return pd.DataFrame(columns=['QEN', 'ACEN', 'AW1EN', 'AW2EN', 'QTYPE'])
