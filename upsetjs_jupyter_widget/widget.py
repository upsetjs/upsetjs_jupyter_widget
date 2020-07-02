# coding: utf- 8
# @upsetjs/jupyter_widget
# https://github.com/upsetjs/upsetjs_jupyter_widget
#
# Copyright (c) 2020 Samuel Gratzl <sam@sgratzl.com>

"""
UpSet.js Jupyter Widget
"""

import typing as t

from ipywidgets import DOMWidget, Layout, ValueWidget, register
from ipywidgets.widgets.trait_types import Color
from traitlets import (
    Bool,
    Dict,
    Enum,
    Float,
    Int,
    List,
    Tuple,
    Unicode,
    Union,
    default,
    Instance,
)

from ._frontend import MODULE_NAME, MODULE_VERSION
from ._model import (
    T,
    UpSetQuery,
    UpSetSet,
    UpSetSetType,
    UpSetSetCombination,
    UpSetSetComposite,
    UpSetSetIntersection,
    UpSetSetDistinctIntersection,
    UpSetSetLike,
    UpSetSetUnion,
    UpSetFontSizes,
    UpSetAttribute,
)
from ._generate import (
    generate_unions,
    generate_intersections,
    generate_distinct_intersections,
)
from ._array import compress_index_array


__all__ = ["UpSetJSWidget"]


def _sort_sets(
    sets: t.Sequence[UpSetSet[T]], order_by: str, limit: t.Optional[int] = None,
) -> t.List[UpSetSet[T]]:
    key = None
    if order_by == "cardinality":
        key = lambda s: (-s.cardinality, s.name)
    else:
        key = lambda s: s.name
    out_list = sorted(sets, key=key)
    if limit is not None:
        return out_list[:limit]
    return out_list


def _sort_combinations(
    combinations: t.Sequence[UpSetSetCombination[T]],
    sets: t.Sequence[UpSetSet[T]],
    order_by: t.Union[str, t.Sequence[str]],
    limit: t.Optional[int] = None,
) -> t.List[UpSetSetCombination[T]]:
    def to_key(order: str):
        if order == "cardinality":
            return lambda s: -s.cardinality
        if order == "degree":
            return lambda s: s.degree
        if order == "group":
            return lambda c: next(
                (i for i, s in enumerate(sets) if s in c.sets), len(sets)
            )
        return lambda s: s.name

    keys = (
        [to_key(order_by)]
        if isinstance(order_by, str)
        else [to_key(v) for v in order_by]
    )
    out_list = sorted(combinations, key=lambda s: tuple([k(s) for k in keys]))
    if limit is not None:
        return out_list[:limit]
    return out_list


def _to_set_list(arr: t.List[UpSetSet], model: "UpSetJSWidget"):
    return [
        dict(
            type=str(s.set_type),
            name=s.name,
            color=s.color,
            cardinality=s.cardinality,
            elems=compress_index_array(model.elem_to_index[e] for e in s.elems),
        )
        for s in arr
    ]


def _to_combination_list(arr: t.List[UpSetSetCombination], model: "UpSetJSWidget"):
    return [
        dict(
            type=str(s.set_type),
            name=s.name,
            color=s.color,
            cardinality=s.cardinality,
            degree=s.degree,
            set_names=[c.name for c in s.sets],
            elems=compress_index_array(model.elem_to_index[e] for e in s.elems),
        )
        for s in arr
    ]


def _to_query_list(arr: t.List[UpSetQuery], model: "UpSetJSWidget"):
    def _to_query(query: UpSetQuery):
        query_dict: t.Dict = dict(name=query.name, color=query.color)
        if query.set:
            query_dict["set"] = dict(name=query.set.name, type=str(query.set.set_type))
        else:
            query_dict["elems"] = compress_index_array(
                model.elem_to_index[e] for e in query.elems or []
            )
        return query_dict

    return [_to_query(q) for q in arr]


def _create_combination(
    cs_name: str,
    combination_type: UpSetSetType,
    count: int,
    sets: t.FrozenSet[UpSetSet],
    color_lookup: t.Mapping[str, str],
) -> UpSetSetCombination:
    if combination_type == UpSetSetType.DISTINCT_INTERSECTION:
        return UpSetSetDistinctIntersection[T](
            cs_name, sets=sets, color=color_lookup.get(cs_name), cardinality=count,
        )
    if combination_type == UpSetSetType.INTERSECTION:
        return UpSetSetIntersection[T](
            cs_name, sets=sets, color=color_lookup.get(cs_name), cardinality=count,
        )
    if combination_type == UpSetSetType.UNION:
        return UpSetSetUnion[T](
            cs_name, sets=sets, color=color_lookup.get(cs_name), cardinality=count,
        )
    return UpSetSetComposite[T](
        cs_name, sets=sets, color=color_lookup.get(cs_name), cardinality=count,
    )


class UpSetJSBaseWidget(ValueWidget, DOMWidget, t.Generic[T]):
    """UpSet.js Base Widget
    """

    _model_name = Unicode("UpSetModel").tag(sync=True)
    _model_module = Unicode(MODULE_NAME).tag(sync=True)
    _model_module_version = Unicode(MODULE_VERSION).tag(sync=True)
    _view_name = Unicode("UpSetView").tag(sync=True)
    _view_module = Unicode(MODULE_NAME).tag(sync=True)
    _view_module_version = Unicode(MODULE_VERSION).tag(sync=True)

    mode: str = Enum(
        ("hover", "click", "static", "contextMenu"), default_value="hover"
    ).tag(sync=True)
    """
    interactivity mode of the widget whether the plot is static, reacts on hover or click events
    """
    padding: float = Float(None, allow_none=True).tag(sync=True)
    """
    padding within the svg
    """

    elems: t.List[T] = List(default_value=[]).tag(sync=True)
    elem_to_index: t.Dict[T, int] = {}

    sets: t.List[UpSetSet[T]] = List(Instance(UpSetSet), default_value=[],).tag(
        sync=True, to_json=_to_set_list
    )

    combinations: t.List[UpSetSetCombination[T]] = List(
        Instance(UpSetSetCombination), default_value=[],
    ).tag(sync=True, to_json=_to_combination_list)

    value: t.Union[None, t.Mapping, t.List[int]] = Union(
        (Dict(allow_none=True, default_value=None), List(Int(), default_value=[]))
    ).tag(sync=True)
    _selection: t.Union[None, t.FrozenSet[T], UpSetSetLike[T]] = None

    queries: t.List[UpSetQuery[T]] = List(Instance(UpSetQuery), default_value=[]).tag(
        sync=True, to_json=_to_query_list
    )

    theme: str = Enum(("light", "dark", "vega"), default_value="light").tag(sync=True)
    selection_color: str = Union(
        (Color(None, allow_none=True), Unicode(None, allow_none=True))
    ).tag(sync=True)
    has_selection_color: str = Color(None, allow_none=True).tag(sync=True)
    opacity: float = Float(None, allow_none=True).tag(sync=True)
    has_selection_opacity: float = Float(None, allow_none=True).tag(sync=True)

    color: str = Color(None, allow_none=True).tag(sync=True)
    text_color: str = Color(None, allow_none=True).tag(sync=True)

    query_legend: bool = Bool(None, allow_none=True).tag(sync=True)
    export_buttons: bool = Bool(None, allow_none=True).tag(sync=True)
    font_family: str = Unicode(None, allow_none=True).tag(sync=True)
    font_sizes: UpSetFontSizes = Instance(UpSetFontSizes).tag(
        sync=True, to_json=lambda v, _: v.to_json()
    )

    title: str = Unicode(None, allow_none=True).tag(sync=True)
    description: str = Unicode(None, allow_none=True).tag(sync=True)

    _expression_data: bool = Bool(None, allow_none=True).tag(sync=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.observe(self._sync_value, "value")

    def _base_copy(self, clone: "UpSetJSBaseWidget"):
        clone.title = self.title
        clone.description = self.description
        clone.mode = self.mode
        clone.padding = self.padding
        clone.elems = list(self.elems)
        clone.elem_to_index = self.elem_to_index.copy()
        clone.sets = list(self.sets)
        clone.combinations = list(self.combinations)
        clone.queries = list(self.queries)
        # pylint: disable=protected-access
        clone._expression_data = self._expression_data

        clone.value = self.value
        clone.selection = self.selection

        clone.theme = self.theme
        clone.selection_color = self.selection_color
        clone.color = self.color
        clone.has_selection_color = self.has_selection_color
        clone.opacity = self.opacity
        clone.has_selection_opacity = self.has_selection_opacity
        clone.text_color = self.text_color

        clone.query_legend = self.query_legend
        clone.export_buttons = self.export_buttons
        clone.font_family = self.font_family
        clone.font_sizes = self.font_sizes.copy()

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
            set_type = value.get("type", "set")
            name = value["name"]

            if set_type == "set":
                found_set = next((s for s in self.sets if s.name == name), None)
                if found_set:
                    return found_set
            else:
                found_set = next(
                    (
                        s
                        for s in self.combinations
                        if s.name == name and str(s.set_type) == set_type
                    ),
                    None,
                )
                if found_set:
                    return found_set

            # generate since not found
            elems = frozenset(self.elems[i] for i in value.get("elems", []))
            set_by_name = {s.name: s for s in self.sets}
            sets = frozenset(set_by_name[n] for n in value.get("set_names", []))
            if set_type == "set":
                return UpSetSet[T](name, elems)
            if set_type == "intersection":
                return UpSetSetIntersection[T](name, elems, sets)
            if set_type == "distinctIntersection":
                return UpSetSetDistinctIntersection[T](name, elems, sets)
            if set_type == "union":
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
            self.value = [self.elem_to_index[e] for e in value]
        elif isinstance(value, UpSetSet):
            self.value = dict(type="set", name=value.name)
        else:
            assert isinstance(
                value,
                (
                    UpSetSetIntersection,
                    UpSetSetUnion,
                    UpSetSetComposite,
                    UpSetSetDistinctIntersection,
                ),
            )
            self.value = dict(type=str(value.set_type), name=value.name)
        # unknown
        self.observe(self._sync_value, "value")

    def on_selection_changed(self, callback):
        """
        add callback listener to listen for selection changes
        """
        self.observe(lambda _: callback(self.selection), "value")

    def clear_queries(self):
        """
        deletes the list of queries
        """
        self.queries = []

    def append_query(
        self,
        name: str,
        color: str,
        upset: t.Optional[UpSetSetLike[T]] = None,
        elems: t.Optional[t.FrozenSet[T]] = None,
    ) -> "UpSetJSWidget":
        """
        adds another UpSetQuery to be visualized
        """
        query: UpSetQuery[T]
        if upset is not None:
            query = UpSetQuery[T](name, color, upset=upset)
        else:
            query = UpSetQuery[T](name, color, elems=elems or frozenset())
        self.queries = self.queries + [query]
        return self

    @property
    def width(self) -> t.Union[str, int]:
        """
        get the widget width
        """
        if self.layout.width.endswidth("px"):
            return int(self.layout.width[:-2])
        return self.layout.width

    @width.setter
    def width(self, value: t.Union[str, int]):
        if isinstance(value, int):
            self.layout.width = f"{value}px"
        else:
            self.layout.width = value

    @property
    def height(self) -> t.Union[str, int]:
        """
        get the widget height
        """
        if self.layout.height.endswidth("px"):
            return int(self.layout.height[:-2])
        return self.layout.height

    @height.setter
    def height(self, value: t.Union[str, int]):
        if isinstance(value, int):
            self.layout.height = f"{value}px"
        else:
            self.layout.height = value

    @default("layout")
    def _default_layout(self):  # pylint: disable=no-self-use
        return Layout(height="400px", align_self="stretch")

    @default("font_sizes")
    def _default_font_sizes(self):  # pylint: disable=no-self-use
        return UpSetFontSizes()

    def _from_dict(
        self,
        sets: t.Mapping[str, t.Sequence[T]],
        order_by: str = "cardinality",
        limit: t.Optional[int] = None,
        colors: t.Mapping[str, str] = None,
    ) -> t.List[UpSetSet[T]]:
        """
        generates the list of sets from a dict
        """
        elems: t.Set[T] = set()
        for set_elems in sets.values():
            elems.update(set_elems)
        self.elems = sorted(elems)
        self.elem_to_index = {e: i for i, e in enumerate(self.elems)}
        self._expression_data = False
        color_lookup = colors or {}

        base_sets: t.List[UpSetSet[T]] = [
            UpSetSet[T](name=k, elems=frozenset(v), color=color_lookup.get(k))
            for k, v in sets.items()
        ]
        self.clear_queries()
        self.selection = None
        self.sets = _sort_sets(base_sets, order_by, limit)

        return base_sets if limit is None else self.sets

    def from_expression(
        self,
        combinations: t.Mapping[str, int],
        combination_type: UpSetSetType = UpSetSetType.INTERSECTION,
        symbol: str = "&",
        order_by: t.Union[str, t.Sequence[str]] = "cardinality",
        set_order_by: str = "cardinality",
        colors: t.Mapping[str, str] = None,
    ) -> "UpSetJSBaseWidget":
        """
        generates the list of sets from a dict
        """
        self.elems = []
        self.elem_to_index = {}
        self._expression_data = True
        color_lookup = colors or {}

        base_sets: t.Dict[str, UpSetSet[T]] = {}
        set_intersections: t.List[UpSetSetCombination[T]] = []

        for cs_name, count in combinations.items():
            contained_sets: t.List[UpSetSet[T]] = []

            for set_name in cs_name.split(symbol):
                if set_name not in base_sets:
                    base_sets[set_name] = UpSetSet[T](
                        set_name,
                        elems=None,
                        color=color_lookup.get(set_name),
                        cardinality=0,
                    )
                contained_sets.append(base_sets[set_name])

            if combination_type == UpSetSetType.DISTINCT_INTERSECTION:
                for s_obj in contained_sets:
                    s_obj.cardinality += count
            elif len(contained_sets) == 1:
                contained_sets[0].cardinality = count
            elif combination_type == UpSetSetType.INTERSECTION:
                for s_obj in contained_sets:
                    s_obj.cardinality = max(s_obj.cardinality, count)
            elif combination_type == UpSetSetType.UNION:
                for s_obj in contained_sets:
                    s_obj.cardinality = min(s_obj.cardinality, count)

            set_intersections.append(
                _create_combination(
                    cs_name,
                    combination_type,
                    count,
                    frozenset(contained_sets),
                    color_lookup,
                )
            )

        self.clear_queries()
        self.selection = None
        self.sets = _sort_sets(list(base_sets.values()), set_order_by, None)
        self.combinations = _sort_combinations(
            set_intersections, self.sets, order_by, None
        )
        return self

    def _from_dataframe(
        self,
        data_frame: t.Any,
        attributes: t.Union[t.Sequence[str], t.Any, None] = None,
        order_by: str = "cardinality",
        limit: t.Optional[int] = None,
        colors: t.Mapping[str, str] = None,
    ) -> t.List[UpSetSet[T]]:
        """
        generates the list of sets from a dataframe
        """
        self.elems = sorted(data_frame.index)
        self.elem_to_index = {e: i for i, e in enumerate(self.elems)}
        self._expression_data = False
        color_lookup = colors or {}

        def to_set(name: str, series):
            elems = series[series.astype(bool)].index
            return UpSetSet[T](
                name=name, elems=frozenset(elems), color=color_lookup.get(name)
            )

        attribute_columns = attributes if isinstance(attributes, (list, tuple)) else []

        base_sets: t.List[UpSetSet[T]] = [
            to_set(name, series)
            for name, series in data_frame.items()
            if name not in attribute_columns
        ]
        self.clear_queries()
        self.selection = None
        self.sets = _sort_sets(base_sets, order_by, limit)
        return base_sets if limit is None else self.sets


@register
class UpSetJSWidget(UpSetJSBaseWidget, t.Generic[T]):
    """UpSet.js Widget
    """

    _render_mode = Unicode("upset").tag(sync=True)

    bar_padding: float = Float(None, allow_none=True).tag(sync=True)
    """
    padding argument for scaleBand (0..1)
    """
    dot_padding: float = Float(None, allow_none=True).tag(sync=True)
    width_ratios: t.Tuple[float, float, float] = Tuple(
        Float(), Float(), Float(), default_value=(0.25, 0.1, 0.65)
    ).tag(sync=True)
    height_ratios: t.Tuple[float, float] = Tuple(
        Float(), Float(), default_value=(0.6, 0.4)
    ).tag(sync=True)

    attrs: t.List[UpSetAttribute[T]] = List(
        Instance(UpSetAttribute), default_value=[]
    ).tag(sync=True, to_json=lambda v, _: [vi.to_json() for vi in v])

    alternating_background_color: str = Color(None, allow_none=True).tag(sync=True)
    hover_hint_color: str = Color(None, allow_none=True).tag(sync=True)
    not_member_color: str = Color(None, allow_none=True).tag(sync=True)

    bar_label_offset: float = Float(None, allow_none=True).tag(sync=True)
    set_name_axis_offset: float = Float(None, allow_none=True).tag(sync=True)
    combination_name_axis_offset: float = Float(None, allow_none=True).tag(sync=True)

    numeric_scale: str = Enum(("linear", "log"), default_value="linear").tag(sync=True)
    band_scale: str = Enum(("band"), default_value="band").tag(sync=True)

    set_name: str = Unicode(None, allow_none=True).tag(sync=True)
    combination_name: str = Unicode(None, allow_none=True).tag(sync=True)

    def copy(self) -> "UpSetJSWidget":
        """
        returns a copy of itself
        """
        clone = UpSetJSWidget[T]()  # pylint: disable=unsubscriptable-object
        self._base_copy(clone)
        clone.bar_padding = self.bar_padding
        clone.dot_padding = self.dot_padding
        clone.width_ratios = self.width_ratios
        clone.height_ratios = self.height_ratios

        clone.alternating_background_color = self.alternating_background_color
        clone.hover_hint_color = self.hover_hint_color
        clone.not_member_color = self.not_member_color

        clone.bar_label_offset = self.bar_label_offset
        clone.set_name_axis_offset = self.set_name_axis_offset
        clone.combination_name_axis_offset = self.combination_name_axis_offset

        clone.numeric_scale = self.numeric_scale
        clone.band_scale = self.band_scale

        clone.set_name = self.set_name
        clone.combination_name = self.combination_name

        return clone

    def from_dict(
        self,
        sets: t.Mapping[str, t.Sequence[T]],
        order_by: str = "cardinality",
        limit: t.Optional[int] = None,
        colors: t.Mapping[str, str] = None,
    ) -> "UpSetJSWidget":
        """
        generates the list of sets from a dict
        """
        base_sets = super()._from_dict(sets, order_by, limit, colors)
        self.attrs = []
        return self._generate_intersections(base_sets, order_by, colors)

    def from_dataframe(
        self,
        data_frame: t.Any,
        attributes: t.Union[t.Sequence[str], t.Any, None] = None,
        order_by: str = "cardinality",
        limit: t.Optional[int] = None,
        colors: t.Mapping[str, str] = None,
    ) -> "UpSetJSWidget":
        """
        generates the list of sets from a dataframe
        """
        base_sets = super()._from_dataframe(
            data_frame, attributes, order_by, limit, colors
        )

        def as_attr(name: str, values: t.List):
            attr_type = (
                "categorical" if not values or isinstance(values[0], str) else "number"
            )
            domain = (min(values), max(values)) if attr_type == "number" else None
            categories = sorted(set(values)) if attr_type == "categorical" else None
            return UpSetAttribute[T](
                attr_type, name, values, domain=domain, categories=categories
            )

        if attributes is not None:
            attribute_df = (
                data_frame[attributes]
                if isinstance(attributes, (list, tuple))
                else attributes
            )
            self.attrs = [
                as_attr(name, series.tolist()) for name, series in attribute_df.items()
            ]
        else:
            self.attrs = []

        return self._generate_intersections(base_sets, order_by, colors)

    def _generate_intersections(
        self,
        base_sets: t.List[UpSetSet[T]],
        order_by: t.Union[str, t.Sequence[str]] = "cardinality",
        colors: t.Mapping[str, str] = None,
    ) -> "UpSetJSWidget":
        """
        customize the generation of the sets
        """
        set_intersections = generate_intersections(
            base_sets, 0, None, False, self.elems, colors=colors
        )

        self.combinations = _sort_combinations(
            set_intersections, self.sets, order_by, None
        )
        return self

    def generate_intersections(
        self,
        min_degree: int = 0,
        max_degree: t.Optional[int] = None,
        empty: bool = False,
        order_by: t.Union[str, t.Sequence[str]] = "cardinality",
        limit: t.Optional[int] = None,
        colors: t.Mapping[str, str] = None,
    ) -> "UpSetJSWidget":
        """
        customize the generation of the sets
        """
        set_intersections = generate_intersections(
            self.sets, min_degree, max_degree, empty, self.elems, colors=colors
        )

        self.combinations = _sort_combinations(
            set_intersections, self.sets, order_by, limit
        )
        return self

    def generate_distinct_intersections(
        self,
        min_degree: int = 0,
        max_degree: t.Optional[int] = None,
        empty: bool = False,
        order_by: t.Union[str, t.Sequence[str]] = "cardinality",
        limit: t.Optional[int] = None,
        colors: t.Mapping[str, str] = None,
    ) -> "UpSetJSWidget":
        """
        customize the generation of the sets
        """
        set_intersections = generate_distinct_intersections(
            self.sets, min_degree, max_degree, empty, self.elems, colors=colors,
        )

        self.combinations = _sort_combinations(
            set_intersections, self.sets, order_by, limit
        )
        return self

    def generate_unions(
        self,
        min_degree: int = 0,
        max_degree: t.Optional[int] = None,
        empty: bool = False,
        order_by: t.Union[str, t.Sequence[str]] = "cardinality",
        limit: t.Optional[int] = None,
        colors: t.Mapping[str, str] = None,
    ) -> "UpSetJSWidget":
        """
        customize the generation of the sets
        """
        set_unions = generate_unions(
            self.sets, min_degree, max_degree, empty, self.elems, colors=colors,
        )

        self.combinations = _sort_combinations(set_unions, self.sets, order_by, limit)
        return self

    def clear_attributes(self) -> "UpSetJSWidget":
        """
        deletes the list of attributes
        """
        self.attrs = []
        return self

    def append_numeric_attribute(
        self,
        name: str,
        values: t.List[float],
        min_value: t.Optional[float] = None,
        max_value: t.Optional[float] = None,
    ) -> "UpSetJSWidget":
        """
        adds another numerical UpSetAttribute to be visualized
        """
        domain = (
            min_value if min_value is not None else min(values),
            max_value if max_value is not None else max(values),
        )
        self.attrs = self.attrs + [UpSetAttribute[T]("number", name, values, domain)]
        return self

    def append_categorical_attribute(
        self,
        name: str,
        values: t.List[str],
        categories: t.Optional[t.List[t.Union[str, t.Dict]]] = None,
    ) -> "UpSetJSWidget":
        """
        adds another categorical UpSetAttribute to be visualized
        """
        cats = categories if categories is not None else sorted(set(values))
        self.attrs = self.attrs + [
            UpSetAttribute[T]("categorical", name, values, categories=cats)
        ]
        return self


@register
class UpSetJSVennDiagramWidget(UpSetJSBaseWidget, t.Generic[T]):
    """UpSet.js Venn Diagram Widget
    """

    _render_mode = Unicode("venn").tag(sync=True)

    value_text_color: str = Color(None, allow_none=True).tag(sync=True)
    stroke_color: str = Color(None, allow_none=True).tag(sync=True)

    def copy(self) -> "UpSetJSVennDiagramWidget":
        """
        returns a copy of itself
        """
        clone = UpSetJSVennDiagramWidget[T]()  # pylint: disable=unsubscriptable-object
        self._base_copy(clone)
        clone.value_text_color = self.value_text_color
        clone.stroke_color = self.stroke_color

        return clone

    def from_dict(
        self,
        sets: t.Mapping[str, t.Sequence[T]],
        order_by: str = "cardinality",
        limit: t.Optional[int] = None,
        colors: t.Mapping[str, str] = None,
    ) -> "UpSetJSVennDiagramWidget":
        """
        generates the list of sets from a dict
        """
        base_sets = super()._from_dict(sets, order_by, limit, colors)
        return self._generate_distinct_intersections(base_sets, colors=colors)

    def from_dataframe(
        self,
        data_frame: t.Any,
        attributes: t.Union[t.Sequence[str], t.Any, None] = None,
        order_by: str = "cardinality",
        limit: t.Optional[int] = None,
        colors: t.Mapping[str, str] = None,
    ) -> "UpSetJSVennDiagramWidget":
        """
        generates the list of sets from a dataframe
        """
        base_sets = super()._from_dataframe(
            data_frame, attributes, order_by, limit, colors
        )

        return self._generate_distinct_intersections(base_sets, colors=colors)

    def _generate_distinct_intersections(
        self, base_sets: t.List[UpSetSet[T]], colors: t.Mapping[str, str] = None,
    ) -> "UpSetJSVennDiagramWidget":
        set_intersections = generate_distinct_intersections(
            base_sets, 1, None, True, self.elems, colors=colors
        )

        self.combinations = _sort_combinations(
            set_intersections, self.sets, ["degree", "group"]
        )
        return self


@register
class UpSetJSEulerDiagramWidget(UpSetJSVennDiagramWidget, t.Generic[T]):
    """UpSet.js Euler Diagram Widget
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._render_mode = "euler"

    def copy(self) -> "UpSetJSEulerDiagramWidget":
        """
        returns a copy of itself
        """
        clone = UpSetJSEulerDiagramWidget[T]()  # pylint: disable=unsubscriptable-object
        self._base_copy(clone)
        clone.value_text_color = self.value_text_color
        clone.stroke_color = self.stroke_color

        return clone


@register
class UpSetJSKarnaughMapWidget(UpSetJSBaseWidget, t.Generic[T]):
    """UpSet.js Karnaugh Map Widget
    """

    _render_mode = Unicode("kmap").tag(sync=True)

    bar_padding: float = Float(None, allow_none=True).tag(sync=True)
    """
    padding argument for scaleBand (0..1)
    """
    stroke_color: str = Color(None, allow_none=True).tag(sync=True)
    numeric_scale: str = Enum(("linear", "log"), default_value="linear").tag(sync=True)

    def copy(self) -> "UpSetJSKarnaughMapWidget":
        """
        returns a copy of itself
        """
        clone = UpSetJSKarnaughMapWidget[T]()  # pylint: disable=unsubscriptable-object
        self._base_copy(clone)
        clone.bar_padding = self.bar_padding
        clone.stroke_color = self.stroke_color
        clone.numeric_scale = self.numeric_scale

        return clone

    def from_dict(
        self,
        sets: t.Mapping[str, t.Sequence[T]],
        order_by: str = "cardinality",
        limit: t.Optional[int] = None,
        colors: t.Mapping[str, str] = None,
    ) -> "UpSetJSKarnaughMapWidget":
        """
        generates the list of sets from a dict
        """
        base_sets = super()._from_dict(sets, order_by, limit, colors)
        return self._generate_distinct_intersections(base_sets, colors=colors)

    def from_dataframe(
        self,
        data_frame: t.Any,
        attributes: t.Union[t.Sequence[str], t.Any, None] = None,
        order_by: str = "cardinality",
        limit: t.Optional[int] = None,
        colors: t.Mapping[str, str] = None,
    ) -> "UpSetJSKarnaughMapWidget":
        """
        generates the list of sets from a dataframe
        """
        base_sets = super()._from_dataframe(
            data_frame, attributes, order_by, limit, colors
        )

        return self._generate_distinct_intersections(base_sets, colors=colors)

    def _generate_distinct_intersections(
        self, base_sets: t.List[UpSetSet[T]], colors: t.Mapping[str, str] = None,
    ) -> "UpSetJSKarnaughMapWidget":
        set_intersections = generate_distinct_intersections(
            base_sets, 1, None, True, self.elems, colors=colors
        )

        self.combinations = _sort_combinations(
            set_intersections, self.sets, ["degree", "group"]
        )
        return self
