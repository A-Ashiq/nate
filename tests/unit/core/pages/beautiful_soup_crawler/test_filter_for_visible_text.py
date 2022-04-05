"""
This module holds tests for the `filter_for_visible_text` function
"""
from typing import Iterator
from unittest import mock

from core.pages.beautiful_soup_crawler import filter_for_visible_text


class TestFilterForVisibleText:
    @mock.patch("core.beautiful_soup_crawler.is_tag_valid")
    def test_calls_is_tag_valid_with_text(self, mocked_is_tag_valid):
        """
        Given a list of fake html text elements
        When `filter_for_visible_text()` is called
        Then `is_tag_valid()` is called for each item in filtered visible text

        Patches:
             `mocked_is_tag_valid`: For the main assertion
        """
        # Given
        first_fake_html_text = "first_fake_html_text"
        second_fake_html_text = "second_fake_html_text"

        # When
        filtered_text_items: Iterator = filter_for_visible_text(
            [first_fake_html_text, second_fake_html_text]
        )

        # Then
        for filtered_text in filtered_text_items:
            mocked_is_tag_valid.assert_called_with(filtered_text)
