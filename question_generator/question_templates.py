"""Question templates for different formats."""

from typing import Dict, List, Callable
import random


# Question templates by format
TEMPLATES = {
    'standard_what': [
        "What is {entity}?",
        "What is the capital of {entity}?",
        "What color is {entity}'s logo?",
        "What is {entity} known for?",
    ],
    'standard_which': [
        "Which country is {entity} in?",
        "Which artist sang '{song}'?",
        "Which brand uses this logo?",
        "Which movie featured {entity}?",
    ],
    'standard_who': [
        "Who sang '{song}'?",
        "Who is {entity}?",
        "Who starred in {movie}?",
    ],
    'standard_name': [
        "Name the {category} shown in this picture.",
        "Name the {entity} from this image.",
    ],
    'fill_blank': [
        "Complete: '{lyric_start} _____'",
        "Fill in the blank: '{quote_start} _____'",
    ],
    'true_false': [
        "True or False: {statement}",
        "{statement} - True or False?",
    ],
    'visual_description': [
        "What color is {entity}'s logo?",
        "What color combination is {entity}?",
        "Which app has this icon?",
    ],
    'odd_one_out': [
        "Which doesn't belong: {options}",
        "Find the odd one out: {options}",
    ]
}


def get_template(format_type: str) -> str:
    """
    Get a random template for a given format.
    
    Args:
        format_type: Type of question format
        
    Returns:
        Random template string
    """
    if format_type in TEMPLATES:
        return random.choice(TEMPLATES[format_type])
    return random.choice(TEMPLATES['standard_what'])


def format_question(template: str, **kwargs) -> str:
    """
    Format a question template with provided values.
    
    Args:
        template: Template string with placeholders
        **kwargs: Values to fill in placeholders
        
    Returns:
        Formatted question string
    """
    try:
        return template.format(**kwargs)
    except KeyError as e:
        # If a placeholder is missing, return a simpler version
        return template.replace(f'{{{e.args[0]}}}', 'this')


# Entity-specific question generators
def generate_country_question(country: str) -> str:
    """Generate a question about a country."""
    templates = [
        f"Which country is {country}?",
        f"What is the capital of {country}?",
        f"Which continent is {country} in?",
    ]
    return random.choice(templates)


def generate_artist_question(artist: str, song: str = None) -> str:
    """Generate a question about an artist."""
    if song:
        templates = [
            f"Who sang '{song}'?",
            f"Which artist released '{song}'?",
        ]
    else:
        templates = [
            f"Who is {artist}?",
            f"Which genre does {artist} perform?",
        ]
    return random.choice(templates)


def generate_movie_question(movie: str) -> str:
    """Generate a question about a movie."""
    templates = [
        f"Which movie is this scene from?",
        f"Name the movie: {movie}",
        f"Which year was {movie} released?",
    ]
    return random.choice(templates)


def generate_brand_question(brand: str) -> str:
    """Generate a question about a brand."""
    templates = [
        f"What color is {brand}'s logo?",
        f"Which company owns {brand}?",
        f"What does {brand} produce?",
    ]
    return random.choice(templates)


def generate_theme_question(theme: str, keywords: List[str]) -> str:
    """Generate a question about a theme."""
    # Use keywords from the theme
    if 'emoji' in theme.lower() or 'emoji' in ' '.join(keywords).lower():
        return "What does this emoji sequence mean: 🍕💔?"
    elif 'tiktok' in theme.lower() or 'tiktok' in ' '.join(keywords).lower():
        return "Complete this TikTok audio: 'Oh no, oh no, oh no no no...'"
    elif 'slang' in theme.lower() or 'gen z' in theme.lower():
        return f"What does '{keywords[0] if keywords else 'no cap'}' mean?"
    else:
        return f"Which topic relates to {keywords[0] if keywords else theme}?"


def generate_field_question(field: str) -> str:
    """Generate a question for a social field."""
    field_questions = {
        'Domestic Sphere': [
            "How often should you change your bed sheets?",
            "Which appliance requires descaling?",
            "What is the boiling point of water?",
        ],
        'Digital Life': [
            "What does this emoji mean: 🍕💔?",
            "Which app has this icon?",
            "What does 'no cap' mean?",
        ],
        'Nostalgia': [
            "What decade was the Walkman popular?",
            "Which toy was popular in the 90s?",
        ],
        'Visual Memory': [
            "What color is Spotify's logo?",
            "Which brand uses red and yellow?",
        ],
        'Common Sense': [
            "How many hours of sleep should adults get?",
            "What is the freezing point of water?",
        ]
    }
    
    if field in field_questions:
        return random.choice(field_questions[field])
    return f"Which topic relates to {field}?"

