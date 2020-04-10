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
import typing as t


def sort_sets(
    sets: t.List[t.Dict[str, t.Union[str, t.List[int], int]]],
    order_by: str,
    limit: t.Optional[int] = None,
):
    if order_by == "cardinality":
        o = sorted(sets, key=lambda s: s["cardinality"], reverse=True)
    elif order_by == "degree":
        o = sorted(sets, key=lambda s: s["degree"], reverse=True)
    else:
        o = sets
    if limit is not None:
        return o[:limit]
    return o


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

    mode: str = Enum(("hover", "click"), default_value="hover").tag(sync=True)
    padding: float = Float(None, allow_none=True).tag(sync=True)
    bar_padding: float = Float(None, allow_none=True).tag(sync=True)
    dot_padding: float = Float(None, allow_none=True).tag(sync=True)
    width_ratios: t.Tuple[float, float, float] = Tuple(
        Float(), Float(), Float(), default_value=(0.25, 0.1, 0.65)
    ).tag(sync=True)
    height_ratios: t.Tuple[float, float] = Tuple(
        Float(), Float(), default_value=(0.6, 0.4)
    ).tag(sync=True)

    # # TODO data, sets
    _elems: t.List[t.Any] = List(default_value=[]).tag(sync=True)
    _elemToIndex: t.Dict[t.Any, int] = {}
    _sets: t.List[t.Dict[str, t.Union[str, t.List[int], int]]] = List(
        Dict(dict(name=Unicode(), elems=List(Int(), default_value=[]))),
        default_value=[],
    ).tag(sync=True)

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

    theme: str = Enum(("light", "dark"), default_value="light").tag(sync=True)
    selection_color: str = Unicode(None, allow_none=True).tag(sync=True)
    alternating_background_color: str = Unicode(None, allow_none=True).tag(sync=True)
    color: str = Unicode(None, allow_none=True).tag(sync=True)
    text_color: str = Unicode(None, allow_none=True).tag(sync=True)
    hover_hint_color: str = Unicode(None, allow_none=True).tag(sync=True)
    not_member_color: str = Unicode(None, allow_none=True).tag(sync=True)

    bar_label_offset: float = Float(None, allow_none=True).tag(sync=True)
    set_name_axis_offset: float = Float(None, allow_none=True).tag(sync=True)
    combination_name_axis_offset: float = Float(None, allow_none=True).tag(sync=True)

    query_legend: bool = Bool(None, allow_none=True).tag(sync=True)
    export_buttons: bool = Bool(None, allow_none=True).tag(sync=True)
    font_family: str = Unicode(None, allow_none=True).tag(sync=True)
    font_sizes: t.Dict[str, str] = Dict(
        traits=dict(
            chart_label=Unicode(None, allow_none=True),
            axis_tick=Unicode(None, allow_none=True),
            set_label=Unicode(None, allow_none=True),
            bar_label=Unicode(None, allow_none=True),
            legend=Unicode(None, allow_none=True),
        )
    ).tag(sync=True)
    numeric_scale: str = Enum(("linear", "log"), default_value="linear").tag(sync=True)
    band_scale: str = Enum(("band", "band2"), default_value="band").tag(sync=True)

    set_name: str = Unicode(None, allow_none=True).tag(sync=True)
    combination_name: str = Unicode(None, allow_none=True).tag(sync=True)

    @property
    def selection(self):
        if self.value is None:
            return None
        if isinstance(self.value, list):
            return [self._elems[i] for i in self.value]
        return dict(
            name=self.value["name"], elems=[self._elems[i] for i in self.value["elems"]]
        )

    @selection.setter
    def selection(self, value):
        if value is None:
            self.value = None
        elif isinstance(value, list):
            self.value = [self._elemToIndex[e] for e in value]
        else:
            self.value = dict(name=value, elems=[])

    def on_selection_changed(self, callback):
        self.observe(lambda evt: callback(evt.new), "value")

    def append_query(
        self,
        name: str,
        color: str,
        set: t.Optional[str] = None,
        elems: t.Optional[t.List[t.Any]] = None,
    ):
        q: t.Dict[str, t.Any] = dict(name=name, color=color)
        if set is not None:
            q["set"] = set
        else:
            q["elems"] = elems or []
        self.queries.append(q)
        return self

    def clear_queries(self):
        self.queries = []

    @default("layout")
    def _default_layout(self):
        return Layout(height="400px", align_self="stretch")

    def from_list(
        self,
        sets: t.Dict[str, t.List[t.Any]],
        order_by: str = "cardinality",
        limit: t.Optional[int] = None,
    ):
        elems: t.Set[t.Any] = set()
        for s in sets.values():
            elems.update(s)
        self._elems = list(elems)
        self._elemToIndex = {e: i for i, e in enumerate(self._elems)}

        self._sets = [
            dict(name=k, elems=[self._elemToIndex[vi] for vi in v], cardinality=len(v))
            for k, v in sets.items()
        ]
        self._sets = sort_sets(self._sets, order_by, limit)
        self.combinations["order"] = order_by
