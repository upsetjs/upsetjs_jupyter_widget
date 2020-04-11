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
    UNION = "union"
    COMPOSITE = "composite"

    def __str__(self):
        if self == UpSetSetType.SET:
            return "set"
        if self == UpSetSetType.INTERSECTION:
            return "intersection"
        if self == UpSetSetType.UNION:
            return "union"
        return "composite"


class UpSetBaseSet(t.Generic[T]):
    """
    a set base class
    """

    set_type: UpSetSetType
    name: str
    elems: t.FrozenSet[T]

    def __init__(
        self,
        set_type: UpSetSetType,
        name: str,
        elems: t.Optional[t.FrozenSet[T]] = None,
    ):
        super().__init__()
        self.set_type = set_type
        self.name = name
        self.elems = elems or frozenset()

    @property
    def cardinality(self):
        """
        the cardinality of this set
        """
        return len(self.elems)


class UpSetSet(UpSetBaseSet[T]):
    """
    a set representation within UpSet
    """

    def __init__(self, name: str = "", elems: t.Optional[t.FrozenSet[T]] = None):
        super().__init__(UpSetSetType.SET, name, elems)

    @property
    def degree(self):
        """
        the degree of this set, i.e., the number of contained sets
        """
        return 1

    def __repr__(self):
        return f"UpSetSet(name={self.name}, elems={set(self.elems)})"


class UpSetSetCombination(UpSetBaseSet[T]):
    """
    a set cobmination within UpSet like an intersection
    """

    sets: t.FrozenSet[UpSetSet[T]]

    def __init__(
        self,
        set_type: UpSetSetType,
        name: str = "",
        elems: t.Optional[t.FrozenSet[T]] = None,
        sets: t.Optional[t.FrozenSet[UpSetSet[T]]] = None,
    ):
        super().__init__(set_type, name, elems)
        self.sets = sets or frozenset()

    @property
    def degree(self):
        """
        the degree of this set, i.e., the number of contained sets
        """
        return len(self.sets)

    def __repr__(self):
        set_names = {s.name for s in self.sets}
        return f"{self.__class__.__name__}(name={self.name}, sets={set_names}, elems={set(self.elems)})"


class UpSetSetIntersection(UpSetSetCombination[T]):
    """
    a set intersection representation in UpSet
    """

    def __init__(
        self,
        name: str = "",
        elems: t.Optional[t.FrozenSet[T]] = None,
        sets: t.Optional[t.FrozenSet[UpSetSet[T]]] = None,
    ):
        super().__init__(UpSetSetType.INTERSECTION, name, elems, sets)


class UpSetSetUnion(UpSetSetCombination[T]):
    """
    a set union representation in UpSet
    """

    def __init__(
        self,
        name: str = "",
        elems: t.Optional[t.FrozenSet[T]] = None,
        sets: t.Optional[t.FrozenSet[UpSetSet[T]]] = None,
    ):
        super().__init__(UpSetSetType.UNION, name, elems, sets)


class UpSetSetComposite(UpSetSetCombination[T]):
    """
    a set composite representation in UpSet
    """

    def __init__(
        self,
        name: str = "",
        elems: t.Optional[t.FrozenSet[T]] = None,
        sets: t.Optional[t.FrozenSet[UpSetSet[T]]] = None,
    ):
        super().__init__(UpSetSetType.COMPOSITE, name, elems, sets)


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
