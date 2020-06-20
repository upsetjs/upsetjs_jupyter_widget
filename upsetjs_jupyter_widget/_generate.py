# coding: utf- 8
# @upsetjs/jupyter_widget
# https://github.com/upsetjs/upsetjs_jupyter_widget
#
# Copyright (c) 2020 Samuel Gratzl <sam@sgratzl.com>

"""
generate set intersection helper
"""
import typing as t
from itertools import combinations
from ._model import (
    T,
    UpSetSet,
    UpSetSetIntersection,
    UpSetSetUnion,
    UpSetSetDistinctIntersection,
)


def generate_intersections(
    sets: t.Sequence[UpSetSet[T]],
    min_degree: int = 0,
    max_degree: t.Optional[int] = None,
    empty: bool = False,
    elems: t.Optional[t.List[T]] = None,
    colors: t.Mapping[str, str] = None,
) -> t.List[UpSetSetIntersection[T]]:
    """
    generate intersections
    """
    color_lookup = colors or {}

    def compute_intersection(combo: t.List[UpSetSet[T]]):
        if len(combo) == 0:
            if not elems:
                return []
            return {e for e in elems if all(e not in c.elems for c in sets)}
        if len(combo) == 1:
            return combo[0].elems
        first = combo[0].elems
        for uset in combo:
            first = first.intersection(uset.elems)
        return first

    set_intersections: t.List[UpSetSetIntersection[T]] = []
    max_degree = max_degree or len(sets)
    for i in range(min_degree, max_degree + 1):
        for combo in combinations(sets, i):
            set_list = list(combo)
            degree = len(set_list)
            intersection = compute_intersection(set_list)
            if len(intersection) == 0 and not empty:
                continue
            name = (
                set_list[0].name
                if degree == 1
                else f"({' ∩ '.join(c.name for c in set_list)})"
            )
            set_intersections.append(
                UpSetSetIntersection[T](
                    name,
                    frozenset(intersection),
                    sets=frozenset(set_list),
                    color=color_lookup.get(
                        name, color_lookup.get("&".join(s.name for s in set_list))
                    ),
                )
            )
    return set_intersections


def generate_distinct_intersections(
    sets: t.Sequence[UpSetSet[T]],
    min_degree: int = 0,
    max_degree: t.Optional[int] = None,
    empty: bool = False,
    elems: t.Optional[t.List[T]] = None,
    colors: t.Mapping[str, str] = None,
) -> t.List[UpSetSetDistinctIntersection[T]]:
    """
    generate distinct intersections
    """
    set_intersections = generate_intersections(
        sets, min_degree, max_degree, empty, elems, colors=colors
    )

    def remove_others(
        elems: t.FrozenSet[T], contained_sets: t.FrozenSet[UpSetSet[T]]
    ) -> t.List[T]:
        others = [s for s in sets if s not in contained_sets]
        return [e for e in elems if all(e not in o.elems for o in others)]

    return [
        UpSetSetDistinctIntersection[T](
            s.name,
            frozenset(remove_others(s.elems, s.sets)),
            sets=s.sets,
            color=s.color,
        )
        for s in set_intersections
    ]


def generate_unions(
    sets: t.Sequence[UpSetSet[T]],
    min_degree: int = 0,
    max_degree: t.Optional[int] = None,
    empty: bool = False,
    elems: t.Optional[t.List[T]] = None,
    colors: t.Mapping[str, str] = None,
) -> t.List[UpSetSetUnion[T]]:
    """
    generate unions
    """
    color_lookup = colors or {}

    def compute_union(combo: t.List[UpSetSet[T]]):
        if len(combo) == 0:
            return elems
        if len(combo) == 1:
            return combo[0].elems
        first = combo[0].elems
        for uset in combo:
            first = first.union(uset.elems)
        return first

    set_unions: t.List[UpSetSetUnion[T]] = []
    for i in range(min_degree, len(sets) if max_degree is None else (max_degree + 1)):
        for combo in combinations(sets, i):
            set_list = list(combo)
            degree = len(set_list)
            union = compute_union(set_list)
            if len(union) == 0 and not empty:
                continue
            name = (
                set_list[0].name
                if degree == 1
                else f"({' ∪ '.join(c.name for c in set_list)})"
            )
            set_unions.append(
                UpSetSetUnion[T](
                    name,
                    frozenset(union),
                    sets=frozenset(set_list),
                    color=color_lookup.get(
                        name, color_lookup.get("&".join(s.name for s in set_list))
                    ),
                )
            )
    return set_unions
