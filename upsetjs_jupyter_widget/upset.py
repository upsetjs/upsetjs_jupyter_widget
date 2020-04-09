#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Samuel Gratzl.

"""
TODO: Add module docstring
"""

from ipywidgets import DOMWidget
from traitlets import Unicode
from ._frontend import module_name, module_version


class UpSetWidget(DOMWidget):
    """TODO: Add docstring here
    """

    _model_name = Unicode("UpSetModel").tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode("UpSetView").tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    value = Unicode("Test").tag(sync=True)

    # TODO
