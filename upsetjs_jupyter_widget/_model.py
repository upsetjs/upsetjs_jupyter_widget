# coding: utf- 8
# @upsetjs/jupyter_widget
# https://github.com/upsetjs/upsetjs_jupyter_widget
#
# Copyright (c) 2020 Samuel Gratzl <sam@sgratzl.com>

"""
model definitions for UpSet
"""
import typing as t
from enum import Enum

T = t.TypeVar("T")  # pylint: disable=invalid-name


class UpSetSetType(Enum):
    """
    enum of which type the set is
    """

    SET = ("set",)
    INTERSECTION = "intersection"
    DISTINCT_INTERSECTION = "distinctIntersection"
    UNION = "union"
    COMPOSITE = "composite"

    def __str__(self):
        if self == UpSetSetType.SET:
            return "set"
        if self == UpSetSetType.INTERSECTION:
            return "intersection"
        if self == UpSetSetType.DISTINCT_INTERSECTION:
            return "distinctIntersection"
        if self == UpSetSetType.UNION:
            return "union"
        return "composite"


class UpSetBaseSet(t.Generic[T]):
    """
    a set base class
    """

    set_type: UpSetSetType
    name: str
    color: t.Optional[str]
    elems: t.FrozenSet[T]
    cardinality: int

    def __init__(
        self,
        set_type: UpSetSetType,
        name: str,
        elems: t.Optional[t.FrozenSet[T]] = None,
        color: t.Optional[str] = None,
        cardinality: t.Optional[int] = None,
    ):
        super().__init__()
        self.set_type = set_type
        self.name = name
        self.color = color
        self.elems = elems or frozenset()
        self.cardinality = cardinality or len(self.elems)


class UpSetSet(UpSetBaseSet[T]):
    """
    a set representation within UpSet
    """

    def __init__(
        self,
        name: str = "",
        elems: t.Optional[t.FrozenSet[T]] = None,
        color: t.Optional[str] = None,
        cardinality: t.Optional[int] = None,
    ):
        super().__init__(UpSetSetType.SET, name, elems, color, cardinality)

    @property
    def degree(self):
        """
        the degree of this set, i.e., the number of contained sets
        """
        return 1

    def __repr__(self):
        return f"UpSetSet(name={self.name}, cardinality={self.cardinality}, elems={set(self.elems)})"


class UpSetSetCombination(UpSetBaseSet[T]):
    """
    a set combination within UpSet.js like an intersection
    """

    sets: t.FrozenSet[UpSetSet[T]]
    """
    the set of UpSetSets this set combination is composed of
    """

    def __init__(
        self,
        set_type: UpSetSetType,
        name: str = "",
        elems: t.Optional[t.FrozenSet[T]] = None,
        sets: t.Optional[t.FrozenSet[UpSetSet[T]]] = None,
        color: t.Optional[str] = None,
        cardinality: t.Optional[int] = None,
    ):
        super().__init__(set_type, name, elems, color, cardinality)
        self.sets = sets or frozenset()

    @property
    def degree(self):
        """
        the degree of this set, i.e., the number of contained sets
        """
        return len(self.sets)

    def __repr__(self):
        set_names = {s.name for s in self.sets}
        return f"{self.__class__.__name__}(name={self.name}, sets={set_names}, cardinality={self.cardinality}, elems={set(self.elems)})"


class UpSetSetIntersection(UpSetSetCombination[T]):
    """
    a set intersection representation in UpSet
    """

    def __init__(
        self,
        name: str = "",
        elems: t.Optional[t.FrozenSet[T]] = None,
        sets: t.Optional[t.FrozenSet[UpSetSet[T]]] = None,
        color: t.Optional[str] = None,
        cardinality: t.Optional[int] = None,
    ):
        super().__init__(
            UpSetSetType.INTERSECTION, name, elems, sets, color, cardinality
        )


class UpSetSetDistinctIntersection(UpSetSetCombination[T]):
    """
    a distinct set intersection representation in UpSet
    """

    def __init__(
        self,
        name: str = "",
        elems: t.Optional[t.FrozenSet[T]] = None,
        sets: t.Optional[t.FrozenSet[UpSetSet[T]]] = None,
        color: t.Optional[str] = None,
        cardinality: t.Optional[int] = None,
    ):
        super().__init__(
            UpSetSetType.DISTINCT_INTERSECTION, name, elems, sets, color, cardinality
        )


class UpSetSetUnion(UpSetSetCombination[T]):
    """
    a set union representation in UpSet
    """

    def __init__(
        self,
        name: str = "",
        elems: t.Optional[t.FrozenSet[T]] = None,
        sets: t.Optional[t.FrozenSet[UpSetSet[T]]] = None,
        color: t.Optional[str] = None,
        cardinality: t.Optional[int] = None,
    ):
        super().__init__(UpSetSetType.UNION, name, elems, sets, color, cardinality)


class UpSetSetComposite(UpSetSetCombination[T]):
    """
    a set composite representation in UpSet
    """

    def __init__(
        self,
        name: str = "",
        elems: t.Optional[t.FrozenSet[T]] = None,
        sets: t.Optional[t.FrozenSet[UpSetSet[T]]] = None,
        color: t.Optional[str] = None,
        cardinality: t.Optional[int] = None,
    ):
        super().__init__(UpSetSetType.COMPOSITE, name, elems, sets, color, cardinality)


UpSetSetLike = t.Union[
    UpSetSet[T], UpSetSetIntersection[T], UpSetSetUnion[T], UpSetSetComposite[T]
]


class UpSetQuery(t.Generic[T]):
    """
    a query representation in UpSet
    """

    name: str
    color: str
    set: t.Optional[UpSetSetLike[T]]
    elems: t.Optional[t.FrozenSet[T]]

    def __init__(
        self,
        name: str,
        color: str,
        upset: t.Optional[UpSetSetLike[T]] = None,
        elems: t.Optional[t.FrozenSet[T]] = None,
    ):
        super().__init__()
        self.type = type
        self.name = name
        self.color = color
        self.set = upset
        self.elems = elems

    def __repr__(self):
        if self.set:
            return (
                f"UpSetSetQuery(name={self.name}, color={self.color}, set={self.set})"
            )
        return f"UpSetSetQuery(name={self.name}, color={self.color}, elems={set(self.elems)})"


class UpSetFontSizes:
    """
    helper structure for specifying font sizes
    """

    chart_label: t.Union[None, str, int] = None
    axis_tick: t.Union[None, str, int] = None
    set_label: t.Union[None, str, int] = None
    bar_label: t.Union[None, str, int] = None
    export_label: t.Union[None, str, int] = None
    value_label: t.Union[None, str, int] = None
    legend: t.Union[None, str, int] = None
    title: t.Union[None, str, int] = None
    description: t.Union[None, str, int] = None

    def __init__(self, **kwargs):
        super().__init__()
        self.__dict__.update(kwargs)

    def __copy__(self):
        return UpSetFontSizes(**self.__dict__)

    def copy(self):
        """
        returns a copy / clone of this instance
        """
        return UpSetFontSizes(**self.__dict__)

    def to_json(self):
        """
        converts this instance to a regular dictionary for transfering
        """
        return self.__dict__


class UpSetAttribute(t.Generic[T]):
    """
    helper structure for specifying font sizes
    """

    attr_type: str
    name: str
    domain: t.Optional[t.Tuple[float, float]]
    categories: t.Optional[t.List[t.Union[str, t.Dict]]]
    elems: t.Optional[t.List[T]]
    values: t.Union[t.List[str], t.List[float]]

    def __init__(
        self,
        attr_type: str,
        name: str,
        values: t.Union[t.List[str], t.List[float]],
        domain: t.Optional[t.Tuple[float, float]] = None,
        categories: t.Optional[t.List[t.Union[str, t.Dict]]] = None,
        elems: t.Optional[t.List[T]] = None,
    ):
        super().__init__()
        self.attr_type = attr_type
        self.name = name
        self.values = values
        self.domain = domain
        self.categories = categories
        self.elems = elems

    def to_json(self):
        """
        converts this instance to a regular dictionary for transfering
        """
        base = dict(
            type=self.attr_type, values=self.values, name=self.name, elems=self.elems
        )
        if self.attr_type == "number":
            base["domain"] = self.domain
        else:
            base["categories"] = self.categories
        return base
