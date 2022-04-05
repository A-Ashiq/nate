"""
This module holds the functionality for crawling pages with `BeautifulSoup`.
"""
import urllib.request
from typing import Iterator, List, Optional

import bs4

INVISIBLE_TAGS: List[str] = ["style", "script", "head", "title", "meta", "[document]"]


def is_tag_valid(
    tag: bs4.element.Doctype, invalid_tag_types: Optional[List[str]] = None
) -> bool:
    """
    Checks the given `tag` against the `invalid_tag_types`.

    The `invalid_tag_types` arg can be used to determine
    if a tag is considered as valid.
    Note that if all tags are to be considered valid
    then pass an empty list to the `invalid_tag_types` arg.

    Defaults to a list of tag types which are roughly used
    to determine if the given `tag` is of an invisible type.

    Args:
        tag: The tag element as parsed by `BeautifulSoup`.
        invalid_tag_types: A list of invalid tag types.

    Returns:
        (bool) - True if the tag is of a valid type, False otherwise.

    """
    if invalid_tag_types is None:
        invalid_tag_types = INVISIBLE_TAGS

    if isinstance(tag, bs4.Comment):
        return False

    if tag.parent.name in invalid_tag_types:
        return False

    return True


def filter_for_visible_text(all_html_text: bs4.element.ResultSet) -> Iterator[str]:
    """
    Creates a generator of strings from the given html
    by filtering out elements of an invalid type.

    Args:
        all_html_text: The result of BeautifulSoup scraping the target url.

    Returns:
        (Generator) - Strings of text elements from the html
            which are of a valid type.

    """
    valid_text_elements = (
        html_text for html_text in all_html_text if is_tag_valid(html_text)
    )

    return (
        word
        for valid_text_element in valid_text_elements
        for word in valid_text_element.split()
    )


def find_all_text_in_html(
    html: bytes, parser: str = "html.parser"
) -> bs4.element.ResultSet:
    """
    Gets all text elements within the given `html`.

    The `parser` arg is passed to an invocation of `BeautifulSoup`
    which is used to determine the features of the `parser`.
    This can be the following types:
        - "lxml",
        - "lxml-xml"
        - "html.parser"
        - "html5lib"

    Args:
        html: The html doctype bytes object.
        parser: The parser to pass to `BeautifulSoup`.

    Returns:
        (ResultSet) - HTML text elements scraped from the page.
    """
    beautiful_soup_parser = bs4.BeautifulSoup(markup=html, features=parser)
    return beautiful_soup_parser.findAll(text=True)


def open_url(target_url: str) -> bytes:
    """
    Opens the `target_url` with a request.

    Sends a request using urllib and opens the
    received http response.

    Args:
        target_url: The URL to scrape text from.

    Returns:
        (bytes) - HTML opened from the `target_url`.

    """
    return urllib.request.urlopen(target_url).read()


def scrape_text_from_target_url(target_url: str) -> Iterator[str]:
    """
    Scrapes visible text from the given `target_url` by leveraging `BeautifulSoup`.

    Args:
        target_url: The URL to scrape text from.

    Returns:
        (Generator) - Strings which are visible on the page.

    """
    html = open_url(target_url)
    all_text = find_all_text_in_html(html)
    return filter_for_visible_text(all_text)
