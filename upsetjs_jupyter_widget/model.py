import typing as t
from enum import Enum

T = t.TypeVar("T")


class UpSetSetType(Enum):
    SET = ("set",)
    INTERSECTION = "intersection"
    UNION = "union"
    COMPOSITE = "composite"


class UpSetBaseSet(t.Generic[T], t.NamedTuple):
    type: UpSetSetType
    name: str
    elems: t.List[T]

    @property
    def cardinality(self):
        return len(self.elems)


class UpSetSet(UpSetBaseSet[T]):
    def __init__(self, name: str = "", elems: t.Optional[t.List[T]] = None):
        super().__init__(UpSetSetType.SET, name, elems)


class UpSetSetCombination(UpSetBaseSet[T]):
    sets: t.Set[UpSetSet[T]]

    def __init__(
        self,
        type: UpSetSetType,
        name: str = "",
        elems: t.Optional[t.List[T]] = None,
        sets: t.Optional[t.Set[UpSetSet[T]]] = None,
    ):
        super().__init__(type, name, elems)
        self.sets = sets or set()

    @property
    def degree(self):
        return len(self.sets)


class UpSetSetIntersection(UpSetSetCombination[T]):
    def __init__(
        self,
        name: str = "",
        elems: t.Optional[t.List[T]] = None,
        sets: t.Optional[t.Set[UpSetSet[T]]] = None,
    ):
        super().__init__(UpSetSetType.INTERSECTION, name, elems, sets)


class UpSetSetUnion(UpSetSetCombination[T]):
    def __init__(
        self,
        name: str = "",
        elems: t.Optional[t.List[T]] = None,
        sets: t.Optional[t.Set[UpSetSet[T]]] = None,
    ):
        super().__init__(UpSetSetType.UNION, name, elems, sets)


class UpSetSetComposite(UpSetSetCombination[T]):
    def __init__(
        self,
        name: str = "",
        elems: t.Optional[t.List[T]] = None,
        sets: t.Optional[t.Set[UpSetSet[T]]] = None,
    ):
        super().__init__(UpSetSetType.COMPOSITE, name, elems, sets)


UpSetSetLike = t.Union[
    UpSetSet[T], UpSetSetIntersection[T], UpSetSetUnion[T], UpSetSetComposite[T]
]


class UpSetQuery(t.NamedTuple, t.Generic[T]):
    name: str
    color: str
    set: t.Optional[UpSetSetLike[T]]
    elems: t.Optional[t.List[T]]
