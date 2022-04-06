"""
This module contains functionality for scraping text from web pages
"""
import collections
from typing import Callable, Dict, Iterator, List, Optional

from core.pages import beautiful_soup_crawler, string_utils


def get_page_text_statistics(
    target_url: str,
    text_scraper: Optional[List[Callable]] = None,
    text_filters: Optional[List[Callable]] = None,
) -> Dict[str, int]:
    """
    Scrapes visible text elements from the `target_url` and returns a `Counter`.

    The `text_scraper` arg can be used to customize how text is scraped from the `target_url`.
    Defaults to `fetch_text_from_page()` which leverages `BeautifulSoup`.
    The interface to this would be the following:

        Given the `target_url`
        When the `text_scraper` is called with the `target_url`
        Then a iterable of text is returned

    The `text_filters` arg can be used to customize how text is filtered.
    The default is 1 filter for removing strings which contain numbers.
    Note that if no text filtering is required
    then pass an empty list to the `text_filters` arg.

    Args:
        target_url: The URL to scrape text from.
        text_filters: A list of callables which can be used
            to filter the output text.

    Returns:
        (Counter) - Keys are the items and values are the aggregated frequencies.

    """
    if not text_scraper:
        text_scraper = beautiful_soup_crawler.scrape_text_from_target_url

    text_from_page = text_scraper(target_url)

    if text_filters is None:
        text_filters = [string_utils.filter_out_text_with_digits]

    for text_filter in text_filters:
        text_from_page = text_filter(text_from_page)

    return count_word_frequencies(text_from_page)


def count_word_frequencies(words: Iterator[str]) -> Dict[str, int]:
    """
    Counts the frequency of each item in the `words` arg.

    Args:
        words: An iterable of items to be counted

    Returns:
        (Counter) - Keys are the items and values are the aggregated frequencies.

    """
    return collections.Counter(words)
