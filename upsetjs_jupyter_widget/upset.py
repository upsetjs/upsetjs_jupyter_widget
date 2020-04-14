# coding: utf-8
# Copyright (c) Samuel Gratzl.
"""
UpSet.js Jupyter Widget
"""

import typing as t

from ipywidgets import DOMWidget, Layout, ValueWidget, register
from traitlets import Bool, Dict, Enum, Float, Int, List, Tuple, Unicode, Union, default

from ._frontend import MODULE_NAME, MODULE_VERSION
from ._model import (
    T,
    UpSetQuery,
    UpSetSet,
    UpSetSetCombination,
    UpSetSetComposite,
    UpSetSetIntersection,
    UpSetSetLike,
    UpSetSetUnion,
)
from ._generate import generate_unions, generate_intersections


def _sort_sets(
    sets: t.Sequence[UpSetSetLike[T]], order_by: str, limit: t.Optional[int] = None,
) -> t.List[UpSetSetLike[T]]:
    out_list: t.List[UpSetSetLike[T]]
    if order_by == "cardinality":
        out_list = sorted(sets, key=lambda s: s.cardinality, reverse=True)
    elif order_by == "degree":
        out_list = sorted(sets, key=lambda s: s.degree, reverse=True)
    else:
        out_list = list(sets)
    if limit is not None:
        return out_list[:limit]
    return out_list


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
    _elem_to_index: t.Dict[T, int] = {}

    _sets_obj: t.List[UpSetSet[T]] = []
    _sets: t.List[t.Mapping] = List(Dict(), default_value=[],).tag(sync=True)

    _combinations_obj: t.List[UpSetSetCombination[T]] = []
    _combinations: t.List[t.Mapping] = List(Dict(), default_value=[],).tag(sync=True)

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
            return frozenset([self.elems[i] for i in value])
        if isinstance(value, dict):
            typee = value.get("type", "set")
            name = value["name"]

            if typee == "set":
                found_set = next((s for s in self.sets if s.name == name), None)
                if found_set:
                    return found_set
            else:
                found_set = next(
                    (
                        s
                        for s in self.combinations
                        if s.name == name and str(s.set_type) == typee
                    ),
                    None,
                )
                if found_set:
                    return found_set

            # generate since not found
            elems = frozenset(self.elems[i] for i in value.get("elems", []))
            set_by_name = {s.name: s for s in self.sets}
            sets = frozenset(set_by_name[n] for n in value.get("set_names", []))
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
        """
        the current selection
        """
        return self._selection

    @selection.setter
    def selection(self, value: t.Union[None, t.FrozenSet[T], UpSetSetLike[T]]):
        self._selection = value

        self.unobserve(self._sync_value, "value")

        if value is None:
            self.value = None
        elif isinstance(value, (list, set, frozenset)):
            self.value = [self._elem_to_index[e] for e in value]
        elif isinstance(value, UpSetSet):
            self.value = dict(type="set", name=value.name)
        else:
            assert isinstance(
                value, (UpSetSetIntersection, UpSetSetUnion, UpSetSetComposite)
            )
            self.value = dict(type=str(value.set_type), name=value.name)
        # unknown
        self.observe(self._sync_value, "value")

    @property
    def sets(self) -> t.Sequence[UpSetSet[T]]:
        """
        the UpSet list of sets
        """
        return self._sets_obj

    @sets.setter
    def sets(self, value: t.List[UpSetSet[T]]):
        self._sets_obj = value
        self._sets = [
            dict(
                type=str(s.set_type),
                name=s.name,
                cardinality=s.cardinality,
                elems=[self._elem_to_index[e] for e in s.elems],
            )
            for s in self._sets_obj
        ]

    @property
    def combinations(self) -> t.Sequence[UpSetSetCombination[T]]:
        """
        the UpSet list of set combinations
        """
        return self._combinations_obj

    @combinations.setter
    def combinations(self, value: t.List[UpSetSetCombination[T]]):
        self._combinations_obj = value
        self._combinations = [
            dict(
                type=str(s.set_type),
                name=s.name,
                cardinality=s.cardinality,
                degree=s.degree,
                set_names=[c.name for c in s.sets],
                elems=[self._elem_to_index[e] for e in s.elems],
            )
            for s in self._combinations_obj
        ]

    def on_selection_changed(self, callback):
        """
        add callback listener to listen for selection changes
        """
        self.observe(lambda: callback(self.selection), "value")

    def append_query(
        self,
        name: str,
        color: str,
        upset: t.Optional[UpSetSetLike[T]] = None,
        elems: t.Optional[t.FrozenSet[T]] = None,
    ) -> "UpSetWidget":
        """
        adds another UpSetQuery to be visualized
        """
        query: UpSetQuery[T]
        if upset is not None:
            query = UpSetQuery[T](name, color, upset=upset)
        else:
            query = UpSetQuery[T](name, color, elems=elems or frozenset())
        self._queries_obj.append(query)
        query_dict: t.Dict = dict(name=query.name, color=query.color)
        if query.set:
            query_dict["set"] = dict(name=query.set.name, type=str(query.set.set_type))
        else:
            query_dict["elems"] = [self._elem_to_index[e] for e in query.elems or []]
        self._queries.append(query_dict)
        return self

    @property
    def queries(self):
        """
        current list of UpSet queries
        """
        return self._queries_obj

    def clear_queries(self):
        """
        deletes the list of queries
        """
        self._queries = []
        self._queries_obj = []

    @default("layout")
    def _default_layout(self):  # pylint: disable=no-self-use
        return Layout(height="400px", align_self="stretch")

    def from_dict(
        self,
        sets: t.Dict[str, t.Sequence[T]],
        order_by: str = "cardinality",
        limit: t.Optional[int] = None,
    ) -> "UpSetWidget":
        """
        generates the list of sets from a dict
        """
        elems: t.Set[T] = set()
        for set_elems in sets.values():
            elems.update(set_elems)
        self.elems = sorted(elems)
        self._elem_to_index = {e: i for i, e in enumerate(self.elems)}

        base_sets: t.List[UpSetSet[T]] = [
            UpSetSet[T](name=k, elems=frozenset(v)) for k, v in sets.items()
        ]
        self.sets = t.cast(t.Any, _sort_sets(base_sets, order_by, limit))
        return self.generate_intersections(order_by=order_by)

    def from_dataframe(
        self,
        data_frame: t.Any,
        order_by: str = "cardinality",
        limit: t.Optional[int] = None,
    ):
        """
        generates the list of sets from a dataframe
        """
        self.elems = sorted(data_frame.index)
        self._elem_to_index = {e: i for i, e in enumerate(self.elems)}

        def to_set(name: str, series):
            elems = series[series.astype(bool)].index
            return UpSetSet[T](name=name, elems=frozenset(elems))

        base_sets = [to_set(name, series) for name, series in data_frame.items()]
        self.sets = t.cast(t.Any, _sort_sets(base_sets, order_by, limit))
        return self.generate_intersections(order_by=order_by)

    def generate_intersections(
        self,
        min_degree: int = 0,
        max_degree: t.Optional[int] = None,
        empty: bool = False,
        order_by: str = "cardinality",
        limit: t.Optional[int] = None,
    ):
        """
        customize the generation of the sets
        """
        set_intersections = generate_intersections(
            self.sets, min_degree, max_degree, empty, self.elems
        )

        self.combinations = t.cast(
            t.Any, _sort_sets(set_intersections, order_by, limit)
        )
        return self

    def generate_unions(
        self,
        min_degree: int = 0,
        max_degree: t.Optional[int] = None,
        empty: bool = False,
        order_by: str = "cardinality",
        limit: t.Optional[int] = None,
    ):
        """
        customize the generation of the sets
        """
        set_unions = generate_unions(
            self.sets, min_degree, max_degree, empty, self.elems
        )

        self.combinations = t.cast(t.Any, _sort_sets(set_unions, order_by, limit))
        return self
