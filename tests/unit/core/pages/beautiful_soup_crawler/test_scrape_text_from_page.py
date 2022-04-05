"""
This module holds tests for the `scrape_text_from_page` function
"""
from unittest import mock

from core.pages.beautiful_soup_crawler import scrape_text_from_target_url


class TestScrapeTextFromPage:
    @mock.patch("core.pages.beautiful_soup_crawler.open_url")
    def test_open_url_is_called_with_target_url(self, mocked_open_url):
        """
        Given a fake target url
        When `scrape_text_from_target_url()` is called
        Then `open_url()` is called with the fake target url

        Patches:
            `mocked_open_url`: For the main assertion
        """
        # Given
        fake_target_url = "fake_target_url"
        mocked_open_url.return_value = "fake_html"

        # When
        scrape_text_from_target_url(fake_target_url)

        # Then
        mocked_open_url.assert_called_once_with(fake_target_url)

    @mock.patch("core.pages.beautiful_soup_crawler.find_all_text_in_html")
    @mock.patch("core.pages.beautiful_soup_crawler.open_url")
    def test_find_all_text_in_html_is_called_with_correct_arg(
        self, mocked_open_url, mocked_find_all_text_in_html
    ):
        """
        Given fake html
        When `scrape_text_from_target_url()` is called
        Then `find_all_text_in_html()` is called with the fake html

        Patches:
            `mocked_open_url`: So the return value can be caught
                and set to the fake html
            `mocked_find_all_text_in_html`: For the main assertion
                of being called with the fake html
        """
        # Given
        fake_html = "fake_html"
        mocked_open_url.return_value = fake_html

        # When
        scrape_text_from_target_url(mock.Mock())

        # Then
        mocked_find_all_text_in_html.assert_called_once_with(fake_html)

    @mock.patch("core.pages.beautiful_soup_crawler.filter_for_visible_text")
    @mock.patch("core.pages.beautiful_soup_crawler.open_url")
    def test_filter_for_visible_text_is_called_with_correct_arg(
        self, mocked_open_url, mocked_filter_for_visible_text
    ):
        """
        Given fake html
        When `scrape_text_from_target_url()` is called
        Then `filter_for_visible_text()` is called
            with an iterable containing the fake html

        Patches:
            `mocked_open_url`: So the return value can be caught
                and set to the fake html
            `mocked_filter_for_visible_text`: For the main assertion
                of being called with an iterable containing the fake html
        """
        # Given
        fake_html = "fake_html"
        mocked_open_url.return_value = fake_html

        # When
        scrape_text_from_target_url(mock.Mock())

        # Then
        mocked_filter_for_visible_text.assert_called_once_with([fake_html])
