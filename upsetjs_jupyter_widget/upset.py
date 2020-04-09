# coding: utf-8
# Copyright (c) Samuel Gratzl.
"""
UpSet.js Jupyter Widget
"""

from ipywidgets import (
    ValueWidget,
    Layout,
    DOMWidget,
    register,
    widget_serialization,
    Layout,
)
from traitlets import default, Bool, Unicode, Enum, Dict, List, Int, Union, Float, Tuple
from ._frontend import MODULE_NAME, MODULE_VERSION


_setlike = dict(name=Unicode(), elems=List(trait=Int(), default_value=[]))


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

    mode = Enum(("hover", "click"), default_value="hover").tag(sync=True)
    padding = Float(None, allow_none=True).tag(sync=True)
    bar_padding = Float(None, allow_none=True).tag(sync=True)
    dot_padding = Float(None, allow_none=True).tag(sync=True)
    width_ratios = Tuple(
        Float(), Float(), Float(), default_value=(0.25, 0.1, 0.65)
    ).tag(sync=True)
    height_ratios = Tuple(Float(), Float(), default_value=(0.6, 0.4)).tag(sync=True)

    # # TODO data, sets
    _elems = List(default_value=[]).tag(sync=True)
    _sets = List(default_value=[]).tag(sync=True)

    combinations = Dict(
        traits=dict(
            type=Enum(("intersection", "union"), default_value="intersection"),
            min=Int(None, allow_none=True),
            max=Int(None, allow_none=True),
            empty=Bool(False),
        ),
        default_value=dict(type="intersection"),
    ).tag(sync=True)

    value = Union(
        (
            Dict(
                traits=dict(name=Unicode(), elems=List(Int(), default_value=[])),
                allow_none=True,
                default_value=None,
            ),
            List(Int(), default_value=[]),
        )
    ).tag(sync=True)
    queries = List(Dict(), default_value=[]).tag(sync=True)

    theme = Enum(("light", "dark"), default_value="light").tag(sync=True)
    selection_color = Unicode(None, allow_none=True).tag(sync=True)
    alternating_background_color = Unicode(None, allow_none=True).tag(sync=True)
    color = Unicode(None, allow_none=True).tag(sync=True)
    text_color = Unicode(None, allow_none=True).tag(sync=True)
    hover_hint_color = Unicode(None, allow_none=True).tag(sync=True)
    not_member_color = Unicode(None, allow_none=True).tag(sync=True)

    bar_label_offset = Float(None, allow_none=True).tag(sync=True)
    set_name_axis_offset = Float(None, allow_none=True).tag(sync=True)
    combination_name_axis_offset = Float(None, allow_none=True).tag(sync=True)

    query_legend = Bool(None, allow_none=True).tag(sync=True)
    export_buttons = Bool(None, allow_none=True).tag(sync=True)
    font_family = Unicode(None, allow_none=True).tag(sync=True)
    font_sizes = Dict(
        traits=dict(
            chart_label=Unicode(None, allow_none=True),
            axis_tick=Unicode(None, allow_none=True),
            set_label=Unicode(None, allow_none=True),
            bar_label=Unicode(None, allow_none=True),
            legend=Unicode(None, allow_none=True),
        )
    ).tag(sync=True)
    numeric_scale = Enum(("linear", "log"), default_value="linear").tag(sync=True)
    band_scale = Enum(("band", "band2"), default_value="band").tag(sync=True)

    set_name = Unicode(None, allow_none=True).tag(sync=True)
    combination_name = Unicode(None, allow_none=True).tag(sync=True)

    @property
    def selection(self):
        return self.value

    @selection.setter
    def selection(self, value):
        self.value = value

    def on_selection_changed(self, callback):
        self.observe(lambda evt: callback(evt.new), "value")

    @default("layout")
    def _default_layout(self):
        return Layout(height="400px", align_self="stretch")
