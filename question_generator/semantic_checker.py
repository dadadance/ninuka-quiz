"""Semantic quality checker for generated questions."""

import re
from typing import Dict, Any, Tuple, List

def check_tautology(question: str, answer: str, entity: str = None) -> bool:
    """
    Check if the answer is a tautology (repeats the question or entity).
    
    Args:
        question: The question text
        answer: The answer text
        entity: The source entity (optional)
        
    Returns:
        True if it IS a tautology (bad), False otherwise.
    """
    q_norm = question.lower().strip()
    a_norm = answer.lower().strip()
    
    # Direct repetition
    if a_norm == q_norm:
        return True
        
    # Answer is just the entity name (common issue: "Who is Drake?" -> "Drake")
    if entity:
        e_norm = entity.lower().strip()
        if a_norm == e_norm:
            # If the question is "Who is {entity}?", answer cannot be "{entity}"
            if f"who is {e_norm}" in q_norm or f"what is {e_norm}" in q_norm:
                return True
                
    # Answer contained entirely in question (heuristics)
    # Exception: Fill in the blank questions might repeat parts, but usually not the *whole* answer
    # strict check: if answer is > 3 chars and is a substring of question
    if len(a_norm) > 3 and a_norm in q_norm:
        # But allow if question is "What is the capital of France?" -> "Paris" (not in Q)
        # Disallow "What is France?" -> "France"
        return True
        
    return False

def check_type_consistency(question: str, answer: str) -> bool:
    """
    Check if answer type matches question word (heuristic).
    
    Args:
        question: The question text
        answer: The answer text
        
    Returns:
        True if consistent, False if inconsistent.
    """
    q_norm = question.lower()
    
    # Year/Date check
    if "which year" in q_norm or "what year" in q_norm or "when was" in q_norm:
        # Answer should contain digits
        if not any(c.isdigit() for c in answer):
            return False
            
    # Count/Number check
    if "how many" in q_norm:
        # Answer should be a number or number word
        number_words = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'zero']
        if not (any(c.isdigit() for c in answer) or any(w in answer.lower() for w in number_words)):
            return False
            
    return True

def validate_semantics(question_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Run all semantic checks on a question.
    
    Args:
        question_data: Dictionary with QEN, ACEN, etc.
        
    Returns:
        Tuple of (is_valid, errors)
    """
    errors = []
    qen = question_data.get('QEN', '')
    acen = question_data.get('ACEN', '')
    entity = question_data.get('source_entity', '') # May strictly need to be passed or extracted
    
    if not qen or not acen:
        return False, ["Missing text"]
        
    # 1. Tautology Check
    if check_tautology(qen, acen, entity):
        errors.append(f"Tautology detected: Answer '{acen}' repeats Question/Entity")
        
    # 2. Type Consistency
    if not check_type_consistency(qen, acen):
        errors.append(f"Type mismatch: Question implies specific type (e.g., Year) but answer is '{acen}'")
        
    # 3. Length balance (Heuristic: Answer shouldn't be longer than Question usually, unless it's "Explain...")
    # For trivia, Q is usually longer.
    if len(acen) > len(qen) + 20: # Loose buffer
        errors.append("Answer suspiciously long compared to question")

    return len(errors) == 0, errors

