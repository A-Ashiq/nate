"""
This module holds tests for the `scrape_text_from_page` function
"""
from unittest import mock

from core.pages.beautiful_soup_crawler import open_url


class TestOpenURL:
    @mock.patch("core.pages.beautiful_soup_crawler.urllib.request")
    def test_urllib_request_urlopen_is_called_with_the_correct_arg(
        self, mocked_urllib_request
    ):
        """
        Given a fake target URL
        When `open_url()` is called with the fake URL
        Then `urllib.request.urlopen()` is called with the fake URL

        Patches:
            `mocked_urllib_request`: For the main assertion
        """
        # Given
        fake_target_url = "fake_target_url"

        # When
        open_url(fake_target_url)

        # Then
        mocked_urllib_request.urlopen.assert_called_once_with(fake_target_url)

    @mock.patch("core.pages.beautiful_soup_crawler.urllib.request")
    def test_urllib_request_is_read_and_returned(self, mocked_urllib_request):
        """
        Given a mocked urllib request
        When `open_url()` is called
        Then the requested URL is read and returned

        Patches:
            `mocked_urllib_request`: For the main assertion
        """
        # Given
        mocked_opened_request = mock.Mock()
        mocked_read_request = mock.Mock()
        mocked_opened_request.read.return_value = mocked_read_request
        mocked_urllib_request.urlopen.return_value = mocked_opened_request

        # When
        html = open_url(mock.Mock())

        # Then
        mocked_opened_request.read.assert_called_once()
        assert html == mocked_read_request
