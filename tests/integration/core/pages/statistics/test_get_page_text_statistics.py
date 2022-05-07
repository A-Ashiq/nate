"""
This module contains integration tests for the `get_page_text_statistics` function
"""

from core.pages.statistics import get_page_text_statistics


class TestGetPageTextStatistics:
    def test_target_url_google_landing_page(self):
        """
        Given a `target_url` of the google landing page
        When `get_page_text_statistics()`
        Then "google" is found
        """
        # Given
        target_url = "https://www.google.com/"

        # When
        page_text_statistics = get_page_text_statistics(target_url=target_url)

        # Then
        assert "Google" in page_text_statistics
