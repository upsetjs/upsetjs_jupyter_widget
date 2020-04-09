# coding: utf-8
# Copyright (c) Samuel Gratzl.
"""
test case
"""


def test_nbextension_path():
    """
    test case
    """
    # Check that magic function can be imported from package root:
    # pylint: disable=C0415
    from upsetjs_jupyter_widget import _jupyter_nbextension_paths

    # Ensure that it can be called without incident:
    path = _jupyter_nbextension_paths()
    # Some sanity checks:
    assert len(path) == 1
    assert isinstance(path[0], dict)
