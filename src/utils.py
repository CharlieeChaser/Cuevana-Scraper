"""
Utility functions for similarity calculation, matching, formatting, and validation.
"""

import re
from difflib import SequenceMatcher
from typing import Any, List, Optional, Tuple, Union
from unidecode import unidecode


# ==================== Similarity Calculation ====================

def calculate_similarity(str1: str, str2: str) -> float:
    """
    Calculate similarity ratio between two strings using SequenceMatcher.
    
    Args:
        str1: First string to compare
        str2: Second string to compare
    
    Returns:
        Similarity ratio between 0 and 1 (1 being identical)
    """
    if not str1 or not str2:
        return 0.0
    
    str1_normalized = normalize_text(str1)
    str2_normalized = normalize_text(str2)
    
    return SequenceMatcher(None, str1_normalized, str2_normalized).ratio()


def levenshtein_distance(str1: str, str2: str) -> int:
    """
    Calculate the Levenshtein distance between two strings.
    
    Args:
        str1: First string
        str2: Second string
    
    Returns:
        Minimum number of single-character edits required to change str1 into str2
    """
    if not str1:
        return len(str2)
    if not str2:
        return len(str1)
    
    str1 = normalize_text(str1)
    str2 = normalize_text(str2)
    
    rows = len(str1) + 1
    cols = len(str2) + 1
    dist = [[0 for _ in range(cols)] for _ in range(rows)]
    
    for i in range(1, rows):
        dist[i][0] = i
    for j in range(1, cols):
        dist[0][j] = j
    
    for i in range(1, rows):
        for j in range(1, cols):
            if str1[i - 1] == str2[j - 1]:
                cost = 0
            else:
                cost = 1
            dist[i][j] = min(
                dist[i - 1][j] + 1,      # deletion
                dist[i][j - 1] + 1,      # insertion
                dist[i - 1][j - 1] + cost  # substitution
            )
    
    return dist[-1][-1]


def normalize_text(text: str) -> str:
    """
    Normalize text for comparison: lowercase, remove accents, extra spaces.
    
    Args:
        text: Text to normalize
    
    Returns:
        Normalized text
    """
    if not text:
        return ""
    
    # Remove accents and convert to lowercase
    text = unidecode(text).lower()
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def fuzzy_match(query: str, target: str, threshold: float = 0.8) -> bool:
    """
    Check if query fuzzy matches target with a similarity threshold.
    
    Args:
        query: Query string
        target: Target string
        threshold: Minimum similarity ratio required (default 0.8)
    
    Returns:
        True if similarity >= threshold, False otherwise
    """
    similarity = calculate_similarity(query, target)
    return similarity >= threshold


# ==================== Matching Functions ====================

def find_best_match(query: str, candidates: List[str], threshold: float = 0.8) -> Optional[str]:
    """
    Find the best matching candidate for a query string.
    
    Args:
        query: Query string
        candidates: List of candidate strings to match against
        threshold: Minimum similarity threshold (default 0.8)
    
    Returns:
        Best matching candidate or None if no match meets threshold
    """
    if not candidates:
        return None
    
    best_match = None
    best_score = threshold
    
    for candidate in candidates:
        score = calculate_similarity(query, candidate)
        if score > best_score:
            best_score = score
            best_match = candidate
    
    return best_match


def find_all_matches(query: str, candidates: List[str], threshold: float = 0.8) -> List[Tuple[str, float]]:
    """
    Find all candidates matching the query above threshold, sorted by score.
    
    Args:
        query: Query string
        candidates: List of candidate strings
        threshold: Minimum similarity threshold
    
    Returns:
        List of tuples (candidate, score) sorted by score descending
    """
    matches = []
    
    for candidate in candidates:
        score = calculate_similarity(query, candidate)
        if score >= threshold:
            matches.append((candidate, score))
    
    # Sort by score descending
    matches.sort(key=lambda x: x[1], reverse=True)
    return matches


def match_titles(title1: str, title2: str, allow_partial: bool = False) -> bool:
    """
    Match two movie/show titles with intelligent comparison.
    
    Args:
        title1: First title
        title2: Second title
        allow_partial: If True, allow partial matches (one title contains the other)
    
    Returns:
        True if titles match, False otherwise
    """
    norm1 = normalize_text(title1)
    norm2 = normalize_text(title2)
    
    # Exact match after normalization
    if norm1 == norm2:
        return True
    
    # Allow partial matches if enabled
    if allow_partial:
        if norm1 in norm2 or norm2 in norm1:
            return True
    
    # Fuzzy match with high threshold
    return fuzzy_match(title1, title2, threshold=0.85)


# ==================== Formatting Functions ====================

def format_title(title: str) -> str:
    """
    Format a title string for display (capitalize words, handle special cases).
    
    Args:
        title: Title to format
    
    Returns:
        Formatted title
    """
    if not title:
        return ""
    
    # Split by common delimiters and capitalize each word
    words = re.split(r'([-–—:()])', title)
    formatted_words = []
    
    for word in words:
        if not word or word in ['-', '–', '—', ':', '(', ')']:
            formatted_words.append(word)
        else:
            # Capitalize first letter, keep rest as is (preserves acronyms)
            formatted_words.append(word[0].upper() + word[1:] if len(word) > 0 else "")
    
    return "".join(formatted_words).strip()


def format_year(year: Union[int, str, None]) -> Optional[str]:
    """
    Format a year value.
    
    Args:
        year: Year as int, string, or None
    
    Returns:
        Formatted year string or None if invalid
    """
    if year is None:
        return None
    
    year_str = str(year).strip()
    
    if not year_str or not year_str.isdigit():
        return None
    
    year_int = int(year_str)
    
    # Validate reasonable year range
    if 1800 <= year_int <= 2100:
        return year_str
    
    return None


def format_rating(rating: Union[float, str, None]) -> Optional[str]:
    """
    Format a rating value.
    
    Args:
        rating: Rating value as float, string, or None
    
    Returns:
        Formatted rating string (x.x format) or None if invalid
    """
    if rating is None:
        return None
    
    try:
        rating_float = float(rating)
        
        # Validate rating range (0-10)
        if 0 <= rating_float <= 10:
            return f"{rating_float:.1f}"
    except (ValueError, TypeError):
        pass
    
    return None


def format_duration(minutes: Union[int, str, None]) -> Optional[str]:
    """
    Format duration in minutes to human-readable format.
    
    Args:
        minutes: Duration in minutes as int, string, or None
    
    Returns:
        Formatted duration string (e.g., "2h 30m") or None if invalid
    """
    if minutes is None:
        return None
    
    try:
        minutes_int = int(minutes)
        
        if minutes_int <= 0:
            return None
        
        hours = minutes_int // 60
        mins = minutes_int % 60
        
        if hours == 0:
            return f"{mins}m"
        elif mins == 0:
            return f"{hours}h"
        else:
            return f"{hours}h {mins}m"
    except (ValueError, TypeError):
        return None


def extract_year_from_string(text: str) -> Optional[int]:
    """
    Extract year from text (looks for 4-digit number between 1800-2100).
    
    Args:
        text: Text to search
    
    Returns:
        Extracted year or None
    """
    if not text:
        return None
    
    # Find all 4-digit numbers
    matches = re.findall(r'\b(1[8-9]\d{2}|20\d{2})\b', text)
    
    if matches:
        return int(matches[0])
    
    return None


# ==================== Validation Functions ====================

def is_valid_title(title: str) -> bool:
    """
    Validate if a string is a valid title.
    
    Args:
        title: Title to validate
    
    Returns:
        True if valid, False otherwise
    """
    if not title or not isinstance(title, str):
        return False
    
    # Title must have at least 1 character and max 500
    if len(title.strip()) < 1 or len(title) > 500:
        return False
    
    # Should contain mostly alphanumeric and common characters
    clean = re.sub(r'[a-z0-9\s\-–—:()&.,!?\'"ñáéíóú]', '', title, flags=re.IGNORECASE)
    
    # Allow some special characters but not too many
    if len(clean) > len(title) * 0.2:
        return False
    
    return True


def is_valid_year(year: Any) -> bool:
    """
    Validate if value is a valid year.
    
    Args:
        year: Value to validate
    
    Returns:
        True if valid year, False otherwise
    """
    try:
        year_int = int(year)
        return 1800 <= year_int <= 2100
    except (ValueError, TypeError):
        return False


def is_valid_rating(rating: Any) -> bool:
    """
    Validate if value is a valid rating (0-10).
    
    Args:
        rating: Value to validate
    
    Returns:
        True if valid rating, False otherwise
    """
    try:
        rating_float = float(rating)
        return 0 <= rating_float <= 10
    except (ValueError, TypeError):
        return False


def is_valid_duration(duration: Any) -> bool:
    """
    Validate if value is a valid duration in minutes.
    
    Args:
        duration: Value to validate
    
    Returns:
        True if valid duration, False otherwise
    """
    try:
        duration_int = int(duration)
        return duration_int > 0
    except (ValueError, TypeError):
        return False


def is_valid_url(url: str) -> bool:
    """
    Basic validation that string looks like a URL.
    
    Args:
        url: URL to validate
    
    Returns:
        True if valid URL format, False otherwise
    """
    if not url or not isinstance(url, str):
        return False
    
    # Simple URL pattern
    url_pattern = r'^https?://[^\s/$.?#].[^\s]*$'
    return bool(re.match(url_pattern, url, re.IGNORECASE))


def is_valid_language(language: str) -> bool:
    """
    Validate if string is a valid language code or name.
    
    Args:
        language: Language to validate
    
    Returns:
        True if valid language, False otherwise
    """
    if not language or not isinstance(language, str):
        return False
    
    # Common language codes and names
    valid_languages = {
        'en', 'es', 'fr', 'de', 'it', 'pt', 'ru', 'ja', 'zh', 'ko',
        'english', 'spanish', 'french', 'german', 'italian', 'portuguese',
        'russian', 'japanese', 'chinese', 'korean'
    }
    
    return language.lower().strip() in valid_languages


def validate_data_dict(data: dict, required_fields: List[str]) -> Tuple[bool, List[str]]:
    """
    Validate that a dictionary contains required fields.
    
    Args:
        data: Dictionary to validate
        required_fields: List of required field names
    
    Returns:
        Tuple of (is_valid, list_of_missing_fields)
    """
    if not isinstance(data, dict):
        return False, required_fields
    
    missing = [field for field in required_fields if field not in data or data[field] is None]
    
    return len(missing) == 0, missing


# ==================== Text Processing ====================

def remove_special_characters(text: str, keep_spaces: bool = True) -> str:
    """
    Remove special characters from text.
    
    Args:
        text: Text to clean
        keep_spaces: If True, keep spaces
    
    Returns:
        Cleaned text
    """
    if not text:
        return ""
    
    if keep_spaces:
        # Keep alphanumeric and spaces
        return re.sub(r'[^a-z0-9\s]', '', text, flags=re.IGNORECASE).strip()
    else:
        # Keep only alphanumeric
        return re.sub(r'[^a-z0-9]', '', text, flags=re.IGNORECASE).strip()


def extract_words(text: str) -> List[str]:
    """
    Extract words from text.
    
    Args:
        text: Text to process
    
    Returns:
        List of words
    """
    if not text:
        return []
    
    # Split by non-alphanumeric characters
    words = re.findall(r'\b\w+\b', text.lower())
    return words


def remove_stop_words(text: str, stop_words: Optional[List[str]] = None) -> str:
    """
    Remove common stop words from text.
    
    Args:
        text: Text to process
        stop_words: Custom list of stop words (uses default English stop words if None)
    
    Returns:
        Text without stop words
    """
    if not text:
        return ""
    
    if stop_words is None:
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'is', 'was', 'are', 'were', 'be', 'been'
        }
    else:
        stop_words = set(word.lower() for word in stop_words)
    
    words = extract_words(text)
    filtered = [w for w in words if w not in stop_words]
    
    return " ".join(filtered)


if __name__ == "__main__":
    # Example usage
    print("Utils module loaded successfully!")
