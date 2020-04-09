# coding: utf-8
# Copyright (c) Samuel Gratzl.
"""
UpSet.js Jupyter Widget
"""

from ipywidgets import DOMWidget
from traitlets import Unicode
from ._frontend import MODULE_NAME, MODULE_VERSION


class UpSetWidget(DOMWidget):
    """UpSet Widget
    """

    _model_name = Unicode("UpSetModel").tag(sync=True)
    _model_module = Unicode(MODULE_NAME).tag(sync=True)
    _model_module_version = Unicode(MODULE_VERSION).tag(sync=True)
    _view_name = Unicode("UpSetView").tag(sync=True)
    _view_module = Unicode(MODULE_NAME).tag(sync=True)
    _view_module_version = Unicode(MODULE_VERSION).tag(sync=True)

    value = Unicode("Test").tag(sync=True)
