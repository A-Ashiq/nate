"""
This module holds tests for the `find_all_text_in_html` function
"""
from unittest import mock

from core.pages.beautiful_soup_crawler import find_all_text_in_html


class TestFindAllTextInHtml:
    @mock.patch("core.beautiful_soup_crawler.bs4.BeautifulSoup")
    def test_beautiful_soup_parser_is_initialized_with_correct_args(
        self, mocked_beautiful_soup
    ):
        """
        Given fake html
        When `find_all_text_in_html()` is called with the mocked html
        Then a `bs4.BeautifulSoup` object is initialized with the correct args

        Patches:
             `mocked_beautiful_soup`: For the main assertion
        """
        # Given
        fake_html = "fake_html"

        # When
        find_all_text_in_html(html=fake_html)

        # Then
        mocked_beautiful_soup.assert_called_once_with(
            markup=fake_html, features="html.parser"
        )

    @mock.patch("core.beautiful_soup_crawler.bs4.BeautifulSoup")
    def test_beautiful_soup_parser_can_be_initialized_with_non_default_parser(
        self, mocked_beautiful_soup
    ):
        """
        Given fake html and a non-default parser
        When `find_all_text_in_html()` is called with those args
        Then a `bs4.BeautifulSoup` object is initialized with the correct args

        Patches:
             `mocked_beautiful_soup`: For the main assertion
        """
        # Given
        fake_html = "fake_html"
        fake_parser = "lxml"

        # When
        find_all_text_in_html(html=fake_html, parser=fake_parser)

        # Then
        mocked_beautiful_soup.assert_called_once_with(
            markup=fake_html, features=fake_parser
        )

    @mock.patch("core.beautiful_soup_crawler.bs4.BeautifulSoup")
    def test_beautiful_soup_parser_calls_find_all(self, mocked_beautiful_soup):
        """
        Given a mocked html
        When `find_all_text_in_html()` is called
        Then `findAll` is called with the correct args
            from the `bs4.BeautifulSoup` object

        Patches:
             `mocked_beautiful_soup`: To mock the returned `bs4.BeautifulSoup` object
                which the main assertion can be performed upon.
        """
        # Given
        mocked_beautiful_soup_parser = mock.Mock()
        mocked_beautiful_soup.return_value = mocked_beautiful_soup_parser

        # When
        find_all_text_in_html(html=mock.Mock())

        # Then
        mocked_beautiful_soup_parser.findAll.assert_called_once_with(text=True)

    @mock.patch("core.beautiful_soup_crawler.bs4.BeautifulSoup")
    def test_returns_value_from_find_all(self, mocked_beautiful_soup):
        """
        Given a mocked instance of `bs4.BeautifulSoup`
        When `find_all_text_in_html()`
        Then the return value is the result of the call to `findAll`

        Patches:
             `mocked_beautiful_soup`:` To mock the return
                from the `bs4.BeautifulSoup` object
                for which the main assertion can be performed upon.
        """
        # Given
        mocked_beautiful_soup_parser = mock.Mock()
        mocked_beautiful_soup.return_value = mocked_beautiful_soup_parser
        mocked_find_all_return_value = mock.Mock()
        mocked_beautiful_soup_parser.findAll.return_value = mocked_find_all_return_value

        # When
        text_found_in_html = find_all_text_in_html(html=mock.Mock())

        # Then
        assert text_found_in_html == mocked_find_all_return_value
