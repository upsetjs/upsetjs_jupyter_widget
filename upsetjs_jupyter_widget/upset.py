# coding: utf-8
# Copyright (c) Samuel Gratzl.
"""
UpSet.js Jupyter Widget
"""

import typing as t

from ipywidgets import DOMWidget, Layout, ValueWidget, register
from traitlets import Bool, Dict, Enum, Float, Int, List, Tuple, Unicode, Union, default

from ._frontend import MODULE_NAME, MODULE_VERSION
from .model import (
    T,
    UpSetQuery,
    UpSetSet,
    UpSetSetCombination,
    UpSetSetComposite,
    UpSetSetIntersection,
    UpSetSetLike,
    UpSetSetUnion,
)


def sort_sets(
    sets: t.Sequence[UpSetSetLike[T]], order_by: str, limit: t.Optional[int] = None,
) -> t.List[UpSetSetLike[T]]:
    o: t.List[UpSetSetLike[T]]
    if order_by == "cardinality":
        o = sorted(sets, key=lambda s: s.cardinality, reverse=True)
    elif order_by == "degree":
        o = sorted(sets, key=lambda s: s.degree, reverse=True)
    else:
        o = list(sets)
    if limit is not None:
        return o[:limit]
    return o


@register
class UpSetWidget(ValueWidget, DOMWidget, t.Generic[T]):
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

    elems: t.List[T] = List(default_value=[]).tag(sync=True)
    _elemToIndex: t.Dict[T, int] = {}

    _sets_obj: t.List[UpSetSet[T]] = []
    _sets: t.List[t.Mapping] = List(Dict(), default_value=[],).tag(sync=True)

    combinations = Dict(
        traits=dict(
            type=Enum(("intersection", "union"), default_value="intersection"),
            min=Int(None, allow_none=True),
            max=Int(None, allow_none=True),
            empty=Bool(False),
        ),
        default_value=dict(type="intersection"),
    ).tag(sync=True)

    value: t.Union[None, t.Mapping, t.List[int]] = Union(
        (Dict(allow_none=True, default_value=None), List(Int(), default_value=[]))
    ).tag(sync=True)
    _selection: t.Union[None, t.FrozenSet[T], UpSetSetLike[T]] = None

    _queries_obj: t.List[UpSetQuery[T]] = []
    _queries: t.List[t.Mapping] = List(Dict(), default_value=[]).tag(sync=True)

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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.observe(self._sync_value, "value")

    def _sync_value(self, evt: t.Any):
        self._selection = self._value_to_selection(evt["new"])

    def get_interact_value(self):
        """Return the value for this widget which should be passed to
        interactive functions. Custom widgets can change this method
        to process the raw value ``self.value``.
        """
        return self.selection

    def _value_to_selection(self, value):
        if value is None:
            return None
        if isinstance(value, list):
            return [self.elems[i] for i in value]
        if isinstance(value, dict):
            typee = value.get("type", "set")
            name = value["name"]
            elems = frozenset(self.elems[i] for i in value.get("elems", []))
            setByName = {s.name: s for s in self.sets}
            sets = frozenset(setByName[n] for n in value.get("set_names", []))
            # look by name
            if typee == "set":
                return UpSetSet[T](name, elems)
            if typee == "intersection":
                return UpSetSetIntersection[T](name, elems, sets)
            if typee == "union":
                return UpSetSetUnion[T](name, elems, sets)
            return UpSetSetComposite[T](name, elems, sets)
        return None

    @property
    def selection(self) -> t.Union[None, t.FrozenSet[T], UpSetSetLike[T]]:
        return self._selection

    @selection.setter
    def selection(self, value: t.Union[None, t.FrozenSet[T], UpSetSetLike[T]]):
        self._selection = value

        self.unobserve(self._sync_value, "value")

        if value is None:
            self.value = None
        elif (
            isinstance(value, list)
            or isinstance(value, set)
            or isinstance(value, frozenset)
        ):
            self.value = [self._elemToIndex[e] for e in value]
        elif isinstance(value, UpSetSet):
            self.value = dict(type="set", name=value.name, elems=[])
        elif isinstance(value, UpSetSetIntersection):
            self.value = dict(type="intersection", name=value.name, elems=[])
        elif isinstance(value, UpSetSetUnion):
            self.value = dict(type="union", name=value.name, elems=[])
        elif isinstance(value, UpSetSetComposite):
            self.value = dict(type="composite", name=value.name, elems=[])
        # unknown
        self.observe(self._sync_value, "value")

    @property
    def sets(self) -> t.Sequence[UpSetSet[T]]:
        return self._sets_obj

    @sets.setter
    def sets(self, value: t.List[UpSetSet[T]]):
        self._sets_obj = value
        self._sets = [
            dict(
                type="set",
                name=s.name,
                cardinality=s.cardinality,
                elems=[self._elemToIndex[e] for e in s.elems],
            )
            for s in self._sets_obj
        ]

    def on_selection_changed(self, callback):
        self.observe(lambda: callback(self.selection), "value")

    def append_query(
        self,
        name: str,
        color: str,
        set: t.Optional[UpSetSetLike[T]] = None,
        elems: t.Optional[t.FrozenSet[T]] = None,
    ) -> "UpSetWidget":
        q: UpSetQuery[T]
        if set is not None:
            q = UpSetQuery[T](name, color, set=set)
        else:
            q = UpSetQuery[T](name, color, elems=elems or frozenset())
        self._queries_obj.append(q)
        qs: t.Dict = dict(name=q.name, color=q.color)
        if q.set:
            qs["set"] = q.set.name
        else:
            qs["elems"] = [self._elemToIndex[e] for e in q.elems or []]
        self._queries.append(qs)
        return self

    @property
    def queries(self):
        return self._queries_obj

    def clear_queries(self):
        self._queries = []
        self._queries_obj = []

    @default("layout")
    def _default_layout(self):
        return Layout(height="400px", align_self="stretch")

    def from_list(
        self,
        sets: t.Dict[str, t.Sequence[T]],
        order_by: str = "cardinality",
        limit: t.Optional[int] = None,
    ) -> "UpSetWidget":
        elems: t.Set[T] = set()
        for s in sets.values():
            elems.update(s)
        self.elems = sorted(elems)
        self._elemToIndex = {e: i for i, e in enumerate(self.elems)}

        base_sets: t.List[UpSetSet[T]] = [
            UpSetSet[T](name=k, elems=frozenset(v)) for k, v in sets.items()
        ]
        self.sets = t.cast(t.Any, sort_sets(base_sets, order_by, limit))
        self.combinations["order"] = order_by
        return self
