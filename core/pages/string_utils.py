"""
This module contains utilities for working with strings
"""
import re
from typing import Iterator, Optional

REGEX_MATCH_FOR_DIGITS: str = "\d"


def filter_out_text_with_digits(text_items: Iterator[str]) -> Iterator[str]:
    """
    Builds a generator object and filters out text containing digits.

    Args:
        text_items: Generator of strings to be filtered.

    Returns:
        (Generator) - Strings which do not contain digits.

    """
    return (text_item for text_item in text_items if not contains_numbers(text_item))


def contains_numbers(text: str) -> Optional[re.Match]:
    """
    Matches for the presence of any digit character in the given `text`.

    Args:
        text: The string which is being checked for digits.

    Raises:
        TypeError: If the `text` parameter is not
            of string or bytes-like object.

    Returns:
        (re.Match) - If a match is found, None otherwise.

    """
    return re.search(REGEX_MATCH_FOR_DIGITS, text)
