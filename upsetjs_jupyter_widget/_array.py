# coding: utf- 8
# @upsetjs/jupyter_widget
# https://github.com/upsetjs/upsetjs_jupyter_widget
#
# Copyright (c) 2020 Samuel Gratzl <sam@sgratzl.com>

"""
helper function for UpSet
"""
import typing as t


def compress_index_array(indices: t.Iterable[int]) -> t.Union[t.List[int], str]:
    """
    compresses an indices array similar to a python range expression
    """
    elems: t.List[int] = list(indices)
    if len(elems) <= 1:
        return elems

    encoded: t.List[str] = []

    sub_slice: t.List[int] = []

    def push():
        if len(sub_slice) == 1:
            encoded.append(str(sub_slice[0]))
        elif len(sub_slice) == 2 and sub_slice[-1] < 10:
            encoded.append(str(sub_slice[0]))
            encoded.append(str(sub_slice[1]))
        else:
            encoded.append(f"{sub_slice[0]}+{len(sub_slice) - 1}")
        return []

    for j, index in enumerate(elems):
        if j > 0:
            expected = sub_slice[-1] + 1
            if index != expected:
                # slice break
                sub_slice = push()
        sub_slice.append(index)

    push()

    compressed = ",".join(encoded)

    if len(compressed) < len(elems) * 0.6:
        return compressed
    return elems
