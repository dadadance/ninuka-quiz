"""Generate correct and wrong answers for questions."""

import random
from typing import List, Dict, Any, Optional
from .gap_loader import load_reference_lists

# =============================================================================
# STATIC KNOWLEDGE BASE
# =============================================================================
# Rationale: The gap analysis dynamically identifies missing entities (e.g., "Drake").
# However, generating semantic facts (e.g., "Founded OVO Sound") requires external knowledge.
# Without an LLM/Web API, we use this static dictionary to provide high-quality 
# facts for the most common "gap" entities found in the analysis.
#
# For a production system with infinite variety, replace this with an LLM call.
# =============================================================================
KNOWLEDGE_BASE = {
    # Artists
    'Drake': {
        'questions': ["Which Canadian rapper released 'God's Plan'?", "Who founded OVO Sound?"],
        'ACEN': 'Drake',
        'wrong': ['The Weeknd', 'J. Cole', 'Kendrick Lamar', 'Travis Scott']
    },
    'The Weeknd': {
        'questions': ["Who performed at the 2021 Super Bowl Halftime Show?", "Which artist released 'Blinding Lights'?"],
        'ACEN': 'The Weeknd',
        'wrong': ['Bruno Mars', 'Drake', 'Post Malone', 'Justin Bieber']
    },
    'Bad Bunny': {
        'questions': ["Who was the most streamed artist on Spotify in 2020-2022?", "Which artist released 'Un Verano Sin Ti'?"],
        'ACEN': 'Bad Bunny',
        'wrong': ['J Balvin', 'Maluma', 'Daddy Yankee', 'Ozuna']
    },
    'Ariana Grande': {
        'questions': ["Who sings 'thank u, next'?", "Which artist started on Nickelodeon's 'Victorious'?"],
        'ACEN': 'Ariana Grande',
        'wrong': ['Selena Gomez', 'Demi Lovato', 'Miley Cyrus', 'Taylor Swift']
    },
    'Taylor Swift': {
        'questions': ["Who re-recorded their albums as 'Taylor's Version'?", "Who sings 'Anti-Hero'?"],
        'ACEN': 'Taylor Swift',
        'wrong': ['Katy Perry', 'Adele', 'Lady Gaga', 'Rihanna']
    },
    'Post Malone': {
        'questions': ["Who sings 'Circles' and 'Rockstar'?", "Which artist has face tattoos and sings 'Sunflower'?"],
        'ACEN': 'Post Malone',
        'wrong': ['Travis Scott', 'Lil Uzi Vert', 'Drake', 'Marshmello']
    },
    'Billie Eilish': {
        'questions': ["Who sings 'Bad Guy'?", "Which artist won 5 Grammys at age 18?"],
        'ACEN': 'Billie Eilish',
        'wrong': ['Lorde', 'Olivia Rodrigo', 'Halsey', 'Dua Lipa']
    },

    # Movies
    'Avatar': {
        'questions': ["Which movie features blue aliens called Na'vi?", "Highest grossing movie of all time (as of 2023)?"],
        'ACEN': 'Avatar',
        'wrong': ['Avengers: Endgame', 'Titanic', 'Star Wars', 'Jurassic World']
    },
    'Avengers: Endgame': {
        'questions': ["In which movie does Iron Man snap his fingers?", "Which movie concludes the Infinity Saga?"],
        'ACEN': 'Avengers: Endgame',
        'wrong': ['Infinity War', 'Civil War', 'Age of Ultron', 'Justice League']
    },
    'Titanic': {
        'questions': ["Which movie features Jack and Rose?", "Which 1997 movie was directed by James Cameron?"],
        'ACEN': 'Titanic',
        'wrong': ['The Notebook', 'Avatar', 'Romeo + Juliet', 'Pearl Harbor']
    },
    
    # Brands/Tech
    'Facebook': {
        'questions': ["Which platform was founded by Mark Zuckerberg?", "Which company owns Instagram and WhatsApp?"],
        'ACEN': 'Facebook (Meta)',
        'wrong': ['Google', 'Twitter', 'Snapchat', 'Amazon']
    },
    'TikTok': {
        'questions': ["Which app popularized short-form vertical video?", "Owned by ByteDance?"],
        'ACEN': 'TikTok',
        'wrong': ['Instagram', 'Snapchat', 'Vine', 'YouTube']
    },
    
    # Generic Fields
    'song': {
        'questions': ["Which is NOT a musical term?", "What is a bridge in music?"],
        'ACEN': 'Connecting section',
        'wrong': ['Main chorus', 'Introduction', 'Ending']
    }
}

def get_knowledge_question(entity: str) -> Optional[Dict[str, Any]]:
    """Get a specific question/answer pair from knowledge base if available."""
    if entity in KNOWLEDGE_BASE:
        data = KNOWLEDGE_BASE[entity]
        question = random.choice(data['questions'])
        # Ensure we have enough wrong answers
        wrong_pool = data['wrong']
        if len(wrong_pool) >= 2:
            wrong = random.sample(wrong_pool, 2)
        else:
            wrong = wrong_pool + ['Other', 'Unknown']
            wrong = wrong[:2]
            
        return {
            'QEN': question,
            'ACEN': data['ACEN'],
            'AW1EN': wrong[0],
            'AW2EN': wrong[1]
        }
    return None

def generate_wrong_answers(correct_answer: str, category: str, reference_lists: Dict[str, List[str]] = None) -> List[str]:
    """
    Generate plausible wrong answers for a question.
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
            wrong_answers.append(_get_generic_wrong_answer(category))
        else:
            wrong_answers = [_get_generic_wrong_answer(category) for _ in range(2)]
    else:
        wrong_answers = [_get_generic_wrong_answer(category) for _ in range(2)]
    
    while len(wrong_answers) < 2:
        wrong_answers.append(_get_generic_wrong_answer(category))
    
    return wrong_answers[:2]


def _get_generic_wrong_answer(category: str) -> str:
    """Get a generic wrong answer based on category."""
    generic_answers = {
        'countries': ['France', 'Germany', 'Italy', 'Spain', 'Japan'],
        'artists': ['Madonna', 'Prince', 'Eminem', 'Beyonce'],
        'movies': ['The Godfather', 'Pulp Fiction', 'Inception'],
        'brands': ['Apple', 'Nike', 'Coca-Cola'],
        'themes': ['Other', 'Various'],
        'fields': ['Daily', 'Weekly', 'Never'],
    }
    
    if category in generic_answers:
        return random.choice(generic_answers[category])
    return 'Other'


def generate_answers_for_country(country: str, reference_lists: Dict[str, List[str]]) -> Dict[str, str]:
    """Generate answers for a country question."""
    # Check KB first
    kb_data = get_knowledge_question(country)
    if kb_data:
        return kb_data
        
    wrong = generate_wrong_answers(country, 'countries', reference_lists)
    return {
        'ACEN': country,
        'AW1EN': wrong[0],
        'AW2EN': wrong[1]
    }


def generate_answers_for_artist(artist: str, reference_lists: Dict[str, List[str]]) -> Dict[str, str]:
    """Generate answers for an artist question."""
    kb_data = get_knowledge_question(artist)
    if kb_data:
        return kb_data

    wrong = generate_wrong_answers(artist, 'artists', reference_lists)
    return {
        'ACEN': artist,
        'AW1EN': wrong[0],
        'AW2EN': wrong[1]
    }


def generate_answers_for_movie(movie: str, reference_lists: Dict[str, List[str]]) -> Dict[str, str]:
    """Generate answers for a movie question."""
    kb_data = get_knowledge_question(movie)
    if kb_data:
        return kb_data

    wrong = generate_wrong_answers(movie, 'movies', reference_lists)
    return {
        'ACEN': movie,
        'AW1EN': wrong[0],
        'AW2EN': wrong[1]
    }


def generate_answers_for_brand(brand: str, reference_lists: Dict[str, List[str]]) -> Dict[str, str]:
    """Generate answers for a brand question."""
    kb_data = get_knowledge_question(brand)
    if kb_data:
        return kb_data

    wrong = generate_wrong_answers(brand, 'brands', reference_lists)
    return {
        'ACEN': brand,
        'AW1EN': wrong[0],
        'AW2EN': wrong[1]
    }


def generate_answers_for_theme(theme: str, keywords: List[str], reference_lists: Dict[str, List[str]] = None) -> Dict[str, str]:
    """Generate answers for a theme question."""
    # Specific fix for the Emoji question seen in logs
    if 'emoji' in theme.lower() or 'emoji' in str(keywords).lower():
        if '🍕💔' in theme or 'pizza' in str(keywords):
            return {
                'ACEN': 'Pizza Heartbreak',
                'AW1EN': 'Hungry Love',
                'AW2EN': 'Food Poisoning'
            }
            
    # For themes, use keywords or theme name as answer
    correct = keywords[0] if keywords else theme.split()[0] if theme else 'Unknown'
    wrong = generate_wrong_answers(correct, 'themes', reference_lists)
    
    return {
        'ACEN': correct,
        'AW1EN': wrong[0],
        'AW2EN': wrong[1]
    }


def generate_answers_for_field(field: str, reference_lists: Dict[str, List[str]] = None) -> Dict[str, str]:
    """Generate answers for a field question."""
    field_answers = {
        'Domestic Sphere': {
            'ACEN': 'Weekly',
            'AW1EN': 'Monthly',
            'AW2EN': 'Daily'
        },
        'Digital Life': {
            'ACEN': 'Pizza Heartbreak', # Fixing the specific emoji case
            'AW1EN': 'I love pizza',
            'AW2EN': 'Hungry'
        },
        'Nostalgia': {
            'ACEN': 'Tamagotchi', # Specific 90s toy answer
            'AW1EN': 'iPad',
            'AW2EN': 'Hoverboard'
        },
        'Visual Memory': {
            'ACEN': 'Green and Black', # Spotify
            'AW1EN': 'Red and Yellow',
            'AW2EN': 'Blue and White'
        },
        'Common Sense': {
            'ACEN': '7-9 hours',
            'AW1EN': '2-4 hours',
            'AW2EN': '12-14 hours'
        },
        'Somatic/Body': {
            'ACEN': 'Cortisol',
            'AW1EN': 'Insulin',
            'AW2EN': 'Melatonin'
        }
    }
    
    if field in field_answers:
        return field_answers[field]
    
    return {
        'ACEN': 'Option A',
        'AW1EN': 'Option B',
        'AW2EN': 'Option C'
    }
