import typing as t
from enum import Enum
from .model import T, UpSetSet, UpSetSetIntersection, UpSetSetUnion
from itertools import combinations


def generate_intersections(
    sets: t.Sequence[UpSetSet[T]],
    min: int = 0,
    max: t.Optional[int] = None,
    empty: bool = False,
    elems: t.Optional[t.List[T]] = None,
) -> t.List[UpSetSetIntersection[T]]:
    def compute_intersection(combo: t.List[UpSetSet[T]]):
        if len(combo) == 0:
            if not elems:
                return []
            return {e for e in elems if all(e not in c.elems for c in sets)}
        if len(combo) == 1:
            return combo[0].elems
        first = combo[0].elems
        for c in combo:
            first = first.intersection(c.elems)
        return first

    r: t.List[UpSetSetIntersection[T]] = []
    for i in range(0, len(sets)):
        for combo in combinations(sets, i):
            cl = list(combo)
            degree = len(cl)
            if degree < min or (max is not None and degree > max):
                continue
            intersection = compute_intersection(cl)
            if len(intersection) == 0 and not empty:
                continue
            name = cl[0].name if degree == 1 else f"({' ∩ '.join(c.name for c in cl)})"
            r.append(
                UpSetSetIntersection[T](
                    name, frozenset(intersection), sets=frozenset(cl)
                )
            )
    return r


def generate_unions(
    sets: t.Sequence[UpSetSet[T]],
    min: int = 0,
    max: t.Optional[int] = None,
    empty: bool = False,
    elems: t.Optional[t.List[T]] = None,
) -> t.List[UpSetSetUnion[T]]:
    def compute_union(combo: t.List[UpSetSet[T]]):
        if len(combo) == 0:
            return elems
        if len(combo) == 1:
            return combo[0].elems
        first = combo[0].elems
        for c in combo:
            first = first.union(c.elems)
        return first

    r: t.List[UpSetSetUnion[T]] = []
    for i in range(0, len(sets)):
        for combo in combinations(sets, i):
            cl = list(combo)
            degree = len(cl)
            if degree < min or (max is not None and degree > max):
                continue
            union = compute_union(cl)
            if len(union) == 0 and not empty:
                continue
            name = cl[0].name if degree == 1 else f"({' ∪ '.join(c.name for c in cl)})"
            r.append(UpSetSetUnion[T](name, frozenset(union), sets=frozenset(cl)))
    return r
