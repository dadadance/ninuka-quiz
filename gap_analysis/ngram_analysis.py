"""N-gram analysis: extract patterns and identify gaps."""

import pandas as pd
import re
from collections import Counter
from typing import Dict, List, Tuple, Any
from nltk import ngrams, word_tokenize
from nltk.corpus import stopwords
import nltk


# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)


def preprocess_text(text: str, remove_stopwords: bool = False) -> List[str]:
    """
    Preprocess text for n-gram extraction.
    
    Args:
        text: Input text
        remove_stopwords: Whether to remove stopwords
        
    Returns:
        List of tokens
    """
    if pd.isna(text) or text == "":
        return []
    
    # Convert to lowercase
    text = str(text).lower()
    
    # Remove special characters but keep spaces
    text = re.sub(r'[^\w\s]', ' ', text)
    
    # Tokenize
    try:
        tokens = word_tokenize(text)
    except:
        # Fallback to simple split
        tokens = text.split()
    
    # Remove stopwords if requested
    if remove_stopwords:
        stop_words = set(stopwords.words('english'))
        tokens = [t for t in tokens if t not in stop_words and len(t) > 1]
    
    return tokens


def extract_ngrams(text: str, n: int, remove_stopwords: bool = False) -> List[Tuple[str, ...]]:
    """
    Extract n-grams from text.
    
    Args:
        text: Input text
        n: N-gram size (1=unigram, 2=bigram, 3=trigram)
        remove_stopwords: Whether to remove stopwords
        
    Returns:
        List of n-gram tuples
    """
    tokens = preprocess_text(text, remove_stopwords)
    
    if len(tokens) < n:
        return []
    
    return list(ngrams(tokens, n))


def extract_all_ngrams(df: pd.DataFrame, text_column: str, n_values: List[int] = [1, 2, 3]) -> Dict[int, Counter]:
    """
    Extract n-grams from all rows in a column.
    
    Args:
        df: Dataframe
        text_column: Column name to extract from
        n_values: List of n values to extract
        
    Returns:
        Dictionary mapping n to Counter of n-grams
    """
    all_ngrams = {n: Counter() for n in n_values}
    
    for text in df[text_column]:
        for n in n_values:
            ngram_list = extract_ngrams(text, n, remove_stopwords=(n > 1))
            all_ngrams[n].update(ngram_list)
    
    return all_ngrams


def analyze_question_ngrams(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyze n-grams in questions.
    
    Args:
        df: Questions dataframe
        
    Returns:
        Dictionary with n-gram analysis
    """
    print("Extracting n-grams from questions...")
    
    # Extract from questions
    question_ngrams = extract_all_ngrams(df, 'QEN', n_values=[1, 2, 3])
    
    # Get top n-grams
    top_unigrams = question_ngrams[1].most_common(50)
    top_bigrams = question_ngrams[2].most_common(50)
    top_trigrams = question_ngrams[3].most_common(50)
    
    return {
        'unigrams': question_ngrams[1],
        'bigrams': question_ngrams[2],
        'trigrams': question_ngrams[3],
        'top_unigrams': top_unigrams,
        'top_bigrams': top_bigrams,
        'top_trigrams': top_trigrams
    }


def analyze_answer_ngrams(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyze n-grams in answers.
    
    Args:
        df: Questions dataframe
        
    Returns:
        Dictionary with answer n-gram analysis
    """
    print("Extracting n-grams from answers...")
    
    # Combine all answers
    all_answers = pd.concat([
        df['ACEN'].fillna(''),
        df['AW1EN'].fillna(''),
        df['AW2EN'].fillna('')
    ])
    
    answer_df = pd.DataFrame({'text': all_answers})
    answer_ngrams = extract_all_ngrams(answer_df, 'text', n_values=[1, 2, 3])
    
    top_unigrams = answer_ngrams[1].most_common(50)
    top_bigrams = answer_ngrams[2].most_common(50)
    top_trigrams = answer_ngrams[3].most_common(50)
    
    return {
        'unigrams': answer_ngrams[1],
        'bigrams': answer_ngrams[2],
        'trigrams': answer_ngrams[3],
        'top_unigrams': top_unigrams,
        'top_bigrams': top_bigrams,
        'top_trigrams': top_trigrams
    }


def analyze_ngrams_by_category(df: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
    """
    Analyze n-grams grouped by category/tag.
    
    Args:
        df: Questions dataframe
        
    Returns:
        Dictionary mapping category to n-gram analysis
    """
    print("Analyzing n-grams by category...")
    
    category_ngrams = {}
    
    # Group by primary category
    if 'primary_category' in df.columns:
        for category in df['primary_category'].dropna().unique():
            cat_df = df[df['primary_category'] == category]
            if len(cat_df) > 0:
                q_ngrams = extract_all_ngrams(cat_df, 'QEN', n_values=[1, 2, 3])
                category_ngrams[category] = {
                    'count': len(cat_df),
                    'top_bigrams': q_ngrams[2].most_common(20),
                    'top_trigrams': q_ngrams[3].most_common(20)
                }
    
    return category_ngrams


def identify_common_patterns(ngram_counter: Counter, min_freq: int = 10) -> List[Tuple[Tuple[str, ...], int]]:
    """
    Identify common n-gram patterns.
    
    Args:
        ngram_counter: Counter of n-grams
        min_freq: Minimum frequency threshold
        
    Returns:
        List of (ngram, frequency) tuples
    """
    return [(ngram, count) for ngram, count in ngram_counter.items() if count >= min_freq]


def export_ngram_patterns(question_ngrams: Dict[str, Any], 
                         answer_ngrams: Dict[str, Any],
                         category_ngrams: Dict[str, Dict[str, Any]],
                         output_path: str = "outputs/ngram_patterns.csv") -> pd.DataFrame:
    """
    Export n-gram patterns to CSV.
    
    Args:
        question_ngrams: Question n-gram analysis
        answer_ngrams: Answer n-gram analysis
        category_ngrams: Category-based n-gram analysis
        output_path: Output file path
        
    Returns:
        Dataframe with n-gram patterns
    """
    rows = []
    
    # Question patterns
    for ngram, count in question_ngrams['top_bigrams']:
        rows.append({
            'type': 'question',
            'ngram_type': 'bigram',
            'ngram': ' '.join(ngram),
            'frequency': count
        })
    
    for ngram, count in question_ngrams['top_trigrams']:
        rows.append({
            'type': 'question',
            'ngram_type': 'trigram',
            'ngram': ' '.join(ngram),
            'frequency': count
        })
    
    # Answer patterns
    for ngram, count in answer_ngrams['top_bigrams']:
        rows.append({
            'type': 'answer',
            'ngram_type': 'bigram',
            'ngram': ' '.join(ngram),
            'frequency': count
        })
    
    df = pd.DataFrame(rows)
    df.to_csv(output_path, index=False)
    
    print(f"N-gram patterns exported to {output_path}")
    
    return df


def analyze_ngrams(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Complete n-gram analysis pipeline.
    
    Args:
        df: Questions dataframe
        
    Returns:
        Dictionary with all n-gram analyses
    """
    question_ngrams = analyze_question_ngrams(df)
    answer_ngrams = analyze_answer_ngrams(df)
    category_ngrams = analyze_ngrams_by_category(df)
    
    print("Exporting n-gram patterns...")
    patterns_df = export_ngram_patterns(question_ngrams, answer_ngrams, category_ngrams)
    
    return {
        'question_ngrams': question_ngrams,
        'answer_ngrams': answer_ngrams,
        'category_ngrams': category_ngrams,
        'patterns_df': patterns_df
    }

