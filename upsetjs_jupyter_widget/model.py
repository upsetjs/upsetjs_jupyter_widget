import typing as t
from enum import Enum

T = t.TypeVar("T")


class UpSetSetType(Enum):
    SET = ("set",)
    INTERSECTION = "intersection"
    UNION = "union"
    COMPOSITE = "composite"

    def __str__(self):
        if self == UpSetSetType.SET:
            return "set"
        elif self == UpSetSetType.INTERSECTION:
            return "intersection"
        elif self == UpSetSetType.UNION:
            return "union"
        return "composite"


class UpSetBaseSet(t.Generic[T]):
    type: UpSetSetType
    name: str
    elems: t.FrozenSet[T]

    def __init__(
        self, type: UpSetSetType, name: str, elems: t.Optional[t.FrozenSet[T]] = None
    ):
        super().__init__()
        self.type = type
        self.name = name
        self.elems = elems or frozenset()

    @property
    def cardinality(self):
        return len(self.elems)


class UpSetSet(UpSetBaseSet[T]):
    def __init__(self, name: str = "", elems: t.Optional[t.FrozenSet[T]] = None):
        super().__init__(UpSetSetType.SET, name, elems)

    @property
    def degree(self):
        return 1

    def __repr__(self):
        return f"UpSetSet(name={self.name}, elems={set(self.elems)})"


class UpSetSetCombination(UpSetBaseSet[T]):
    sets: t.FrozenSet[UpSetSet[T]]

    def __init__(
        self,
        type: UpSetSetType,
        name: str = "",
        elems: t.Optional[t.FrozenSet[T]] = None,
        sets: t.Optional[t.FrozenSet[UpSetSet[T]]] = None,
    ):
        super().__init__(type, name, elems)
        self.sets = sets or frozenset()

    @property
    def degree(self):
        return len(self.sets)

    def __repr__(self):
        set_names = {s.name for s in self.sets}
        return f"{self.__class__.__name__}(name={self.name}, sets={set_names}, elems={set(self.elems)})"


class UpSetSetIntersection(UpSetSetCombination[T]):
    def __init__(
        self,
        name: str = "",
        elems: t.Optional[t.FrozenSet[T]] = None,
        sets: t.Optional[t.FrozenSet[UpSetSet[T]]] = None,
    ):
        super().__init__(UpSetSetType.INTERSECTION, name, elems, sets)


class UpSetSetUnion(UpSetSetCombination[T]):
    def __init__(
        self,
        name: str = "",
        elems: t.Optional[t.FrozenSet[T]] = None,
        sets: t.Optional[t.FrozenSet[UpSetSet[T]]] = None,
    ):
        super().__init__(UpSetSetType.UNION, name, elems, sets)


class UpSetSetComposite(UpSetSetCombination[T]):
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
    name: str
    color: str
    set: t.Optional[UpSetSetLike[T]]
    elems: t.Optional[t.FrozenSet[T]]

    def __init__(
        self,
        name: str,
        color: str,
        set: t.Optional[UpSetSetLike[T]] = None,
        elems: t.Optional[t.FrozenSet[T]] = None,
    ):
        super().__init__()
        self.type = type
        self.name = name
        self.color = color
        self.set = set
        self.elems = elems

    def __repr__(self):
        if self.set:
            return (
                f"UpSetSetQuery(name={self.name}, color={self.color}, set={self.set})"
            )
        return f"UpSetSetQuery(name={self.name}, color={self.color}, elems={set(self.elems)})"
