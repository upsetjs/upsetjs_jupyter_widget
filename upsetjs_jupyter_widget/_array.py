"""
helper function for UpSet
"""
import typing as t


def compress_index_array(indices: t.Iterable[int]) -> t.Union[t.List[int], str]:
    return list(indices)
