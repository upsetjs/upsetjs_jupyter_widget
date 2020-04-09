# coding: utf-8
# Copyright (c) Samuel Gratzl.
"""
UpSet.js Jupyter Widget
"""

from ipywidgets import DOMWidget, Layout, ValueWidget, register
from traitlets import default, Unicode
from ._frontend import MODULE_NAME, MODULE_VERSION


@register
class UpSetWidget(ValueWidget, DOMWidget):
    """UpSet Widget
    """

    _model_name = Unicode("UpSetModel").tag(sync=True)
    _model_module = Unicode(MODULE_NAME).tag(sync=True)
    _model_module_version = Unicode(MODULE_VERSION).tag(sync=True)
    _view_name = Unicode("UpSetView").tag(sync=True)
    _view_module = Unicode(MODULE_NAME).tag(sync=True)
    _view_module_version = Unicode(MODULE_VERSION).tag(sync=True)

    value = Unicode("Test").tag(sync=True)

    @property
    def selection(self):
        return self.value

    @selection.setter
    def selection(self, value):
        self.value = value

    @default("layout")
    def _default_layout(self):
        return Layout(height="600px", align_self="stretch")

    def on_selection_changed(self, callback):
        self.observe(lambda evt: callback(evt.new), "value")
