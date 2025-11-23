"""Shared utilities for gap analysis."""

import re
from typing import List, Dict, Any
import pandas as pd


def clean_text(text: str) -> str:
    """Clean text by removing extra spaces and normalizing."""
    if pd.isna(text):
        return ""
    text = str(text).strip()
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)
    return text


def parse_tag_ids(tag_string: str) -> List[int]:
    """Parse comma-separated tag IDs from string."""
    if pd.isna(tag_string) or tag_string == "":
        return []
    try:
        return [int(t.strip()) for t in str(tag_string).split(',') if t.strip().isdigit()]
    except (ValueError, AttributeError):
        return []


def get_character_count(text: str) -> int:
    """Get character count of text."""
    if pd.isna(text):
        return 0
    return len(str(text))


def validate_character_limit(text: str, limit: int = 100) -> bool:
    """Check if text is within character limit."""
    return get_character_count(text) <= limit

