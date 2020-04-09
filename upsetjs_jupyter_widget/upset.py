# coding: utf-8
# Copyright (c) Samuel Gratzl.
"""
UpSet.js Jupyter Widget
"""

from ipywidgets import ValueWidget, DOMWidget, register, widget_serialization, Layout
from ipywidgets.widgets.trait_types import InstanceDict
from traitlets import Unicode
from ._frontend import MODULE_NAME, MODULE_VERSION


class MyLayout(Layout):
    _model_module_version = Unicode("^3").tag(sync=True)


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

    # layout = InstanceDict(MyLayout).tag(sync=True, **widget_serialization)

    value = Unicode("Test").tag(sync=True)

    @property
    def selection(self):
        return self.value

    @selection.setter
    def selection(self, value):
        self.value = value

    def on_selection_changed(self, callback):
        self.observe(lambda evt: callback(evt.new), "value")
