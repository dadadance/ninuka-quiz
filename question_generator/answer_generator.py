"""Generate correct and wrong answers for questions."""

import random
from typing import List, Dict, Any
from .gap_loader import load_reference_lists


def generate_wrong_answers(correct_answer: str, category: str, reference_lists: Dict[str, List[str]] = None) -> List[str]:
    """
    Generate plausible wrong answers for a question.
    
    Args:
        correct_answer: The correct answer
        category: Category of the question (countries, artists, movies, brands)
        reference_lists: Reference lists for similar entities
        
    Returns:
        List of 2 wrong answers
    """
    if reference_lists is None:
        reference_lists = load_reference_lists()
    
    wrong_answers = []
    
    # Get similar entities from same category
    if category in reference_lists:
        similar_entities = [e for e in reference_lists[category] if e != correct_answer]
        if len(similar_entities) >= 2:
            wrong_answers = random.sample(similar_entities, 2)
        elif len(similar_entities) == 1:
            wrong_answers = [similar_entities[0]]
            # Add a generic wrong answer
            wrong_answers.append(_get_generic_wrong_answer(category))
        else:
            wrong_answers = [_get_generic_wrong_answer(category) for _ in range(2)]
    else:
        wrong_answers = [_get_generic_wrong_answer(category) for _ in range(2)]
    
    # Ensure we have exactly 2 wrong answers
    while len(wrong_answers) < 2:
        wrong_answers.append(_get_generic_wrong_answer(category))
    
    return wrong_answers[:2]


def _get_generic_wrong_answer(category: str) -> str:
    """Get a generic wrong answer based on category."""
    generic_answers = {
        'countries': ['Unknown', 'Not Listed', 'Other'],
        'artists': ['Unknown Artist', 'Other Artist', 'Various Artists'],
        'movies': ['Unknown Movie', 'Other Film', 'Various'],
        'brands': ['Unknown Brand', 'Other Company', 'Various'],
        'themes': ['Other', 'Not Listed', 'Various'],
        'fields': ['Other', 'Not Listed', 'Various'],
    }
    
    if category in generic_answers:
        return random.choice(generic_answers[category])
    return 'Other'


def generate_answers_for_country(country: str, reference_lists: Dict[str, List[str]]) -> Dict[str, str]:
    """
    Generate answers for a country question.
    
    Args:
        country: Country name
        reference_lists: Reference lists
        
    Returns:
        Dictionary with ACEN, AW1EN, AW2EN
    """
    wrong = generate_wrong_answers(country, 'countries', reference_lists)
    return {
        'ACEN': country,
        'AW1EN': wrong[0] if len(wrong) > 0 else 'Unknown',
        'AW2EN': wrong[1] if len(wrong) > 1 else 'Unknown'
    }


def generate_answers_for_artist(artist: str, reference_lists: Dict[str, List[str]]) -> Dict[str, str]:
    """Generate answers for an artist question."""
    wrong = generate_wrong_answers(artist, 'artists', reference_lists)
    return {
        'ACEN': artist,
        'AW1EN': wrong[0] if len(wrong) > 0 else 'Unknown Artist',
        'AW2EN': wrong[1] if len(wrong) > 1 else 'Unknown Artist'
    }


def generate_answers_for_movie(movie: str, reference_lists: Dict[str, List[str]]) -> Dict[str, str]:
    """Generate answers for a movie question."""
    wrong = generate_wrong_answers(movie, 'movies', reference_lists)
    return {
        'ACEN': movie,
        'AW1EN': wrong[0] if len(wrong) > 0 else 'Unknown Movie',
        'AW2EN': wrong[1] if len(wrong) > 1 else 'Unknown Movie'
    }


def generate_answers_for_brand(brand: str, reference_lists: Dict[str, List[str]]) -> Dict[str, str]:
    """Generate answers for a brand question."""
    wrong = generate_wrong_answers(brand, 'brands', reference_lists)
    return {
        'ACEN': brand,
        'AW1EN': wrong[0] if len(wrong) > 0 else 'Unknown Brand',
        'AW2EN': wrong[1] if len(wrong) > 1 else 'Unknown Brand'
    }


def generate_answers_for_theme(theme: str, keywords: List[str], reference_lists: Dict[str, List[str]] = None) -> Dict[str, str]:
    """Generate answers for a theme question."""
    # For themes, use keywords or theme name as answer
    correct = keywords[0] if keywords else theme.split()[0] if theme else 'Unknown'
    
    # Generate wrong answers from other themes or generic
    wrong = generate_wrong_answers(correct, 'themes', reference_lists)
    
    return {
        'ACEN': correct,
        'AW1EN': wrong[0] if len(wrong) > 0 else 'Other',
        'AW2EN': wrong[1] if len(wrong) > 1 else 'Various'
    }


def generate_answers_for_field(field: str, reference_lists: Dict[str, List[str]] = None) -> Dict[str, str]:
    """Generate answers for a field question."""
    # Field-specific answers
    field_answers = {
        'Domestic Sphere': {
            'ACEN': 'Weekly',
            'AW1EN': 'Monthly',
            'AW2EN': 'Daily'
        },
        'Digital Life': {
            'ACEN': 'No exaggeration',
            'AW1EN': 'Yes, definitely',
            'AW2EN': 'Maybe'
        },
        'Nostalgia': {
            'ACEN': '1990s',
            'AW1EN': '1980s',
            'AW2EN': '2000s'
        },
        'Visual Memory': {
            'ACEN': 'Red and Yellow',
            'AW1EN': 'Blue and Green',
            'AW2EN': 'Black and White'
        },
        'Common Sense': {
            'ACEN': '7-9 hours',
            'AW1EN': '5-6 hours',
            'AW2EN': '10+ hours'
        }
    }
    
    if field in field_answers:
        return field_answers[field]
    
    # Generic fallback
    return {
        'ACEN': 'Answer A',
        'AW1EN': 'Answer B',
        'AW2EN': 'Answer C'
    }

