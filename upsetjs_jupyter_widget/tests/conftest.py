# coding: utf- 8
# @upsetjs/jupyter_widget
# https://github.com/upsetjs/upsetjs_jupyter_widget
#
# Copyright (c) 2021 Samuel Gratzl <sam@sgratzl.com>

# coding: utf-8
# Copyright (c) Samuel Gratzl.
# pylint: disable=W0221,C0103,C0116,W0212,signature-differs
"""
test case
"""


import pytest

from ipykernel.comm import Comm  # type: ignore
from ipywidgets import Widget  # type: ignore


class MockComm(Comm):
    """A mock Comm object.

    Can be used to inspect calls to Comm's open/send/close methods.
    """

    comm_id = "a-b-c-d"
    kernel = "Truthy"

    def __init__(self, *args, **kwargs):
        """
        test case
        """
        self.log_open = []
        self.log_send = []
        self.log_close = []
        super().__init__(*args, **kwargs)

    def open(self, *args, **kwargs):
        """
        test case
        """
        self.log_open.append((args, kwargs))

    def send(self, *args, **kwargs):
        """
        test case
        """
        self.log_send.append((args, kwargs))

    def close(self, *args, **kwargs):
        """
        test case
        """
        self.log_close.append((args, kwargs))


_widget_attrs = {}
undefined = object()


@pytest.fixture
def mock_comm():
    _widget_attrs["_comm_default"] = getattr(Widget, "_comm_default", undefined)
    Widget._comm_default = lambda self: MockComm()
    _widget_attrs["_ipython_display_"] = Widget._ipython_display_

    def raise_not_implemented(*args, **kwargs):
        raise NotImplementedError()

    Widget._ipython_display_ = raise_not_implemented

    yield MockComm()

    for attr, value in _widget_attrs.items():
        if value is undefined:
            delattr(Widget, attr)
        else:
            setattr(Widget, attr, value)
