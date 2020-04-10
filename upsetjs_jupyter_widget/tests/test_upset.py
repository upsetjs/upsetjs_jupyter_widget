# coding: utf-8
# Copyright (c) Samuel Gratzl.
"""
test case
"""

from ..upset import UpSetWidget  # pylint: disable=C0415


def test_upset_creation_blank():
    """
    test case
    """
    widget = UpSetWidget()
    assert widget.value is None
