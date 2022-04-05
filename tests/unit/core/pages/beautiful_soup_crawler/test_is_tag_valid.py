"""
This module holds tests for the `is_tag_valid` function
"""
from unittest import mock

import bs4
import pytest

from core.pages.beautiful_soup_crawler import is_tag_valid


class TestIsTagInvalid:
    @pytest.mark.parametrize(
        "tag_type", ["style", "script", "head", "title", "meta", "[document]"]
    )
    def test_uses_default_invalid_tags(self, tag_type):
        """
        Given a tag with a parent of one of the default invalid types
        When `is_tag_valid()` is called without specifying `invalid_tag_types`
        Then `False` is returned
        """
        # Given
        mocked_tag = mock.Mock()
        mocked_tag.parent.name = tag_type

        # When
        tag_is_valid = is_tag_valid(mocked_tag)

        # Then
        assert not tag_is_valid

    @pytest.mark.parametrize(
        "tag_type", ["style", "script", "head", "title", "meta", "[document]"]
    )
    def test_uses_specified_valid_tags(self, tag_type):
        """
        Given a tag with a parent of one of the default invalid types
        When `is_tag_valid()` is called and specifying `invalid_tag_types`
        Then `True` is returned
        """
        # Given
        mocked_tag = mock.Mock()
        mocked_tag.parent.name = tag_type
        fake_invalid_tag_types = ["fake_tag_type"]

        # When
        tag_is_valid = is_tag_valid(
            tag=mocked_tag, invalid_tag_types=fake_invalid_tag_types
        )

        # Then
        assert tag_is_valid

    def test_returns_false_if_tag_is_a_comment(self):
        """
        Given a tag which is a bs4 Comment
        When `is_tag_valid()` is called
        Then `False` is returned
        """
        fake_tag = bs4.Comment("fake_value")

        # When
        tag_is_valid = is_tag_valid(fake_tag)

        # Then
        assert not tag_is_valid

    def test_returns_true_if_tag_is_valid(self):
        """
        Given a tag of a valid type
        When `is_tag_valid()` is called
        Then `True` is returned
        """
        # Given
        mocked_tag = mock.Mock()

        # When
        tag_is_valid = is_tag_valid(mocked_tag)

        # Then
        assert tag_is_valid
