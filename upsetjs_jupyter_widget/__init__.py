# coding: utf-8
# Copyright (c) Samuel Gratzl.
"""
UpSet.js Jupyter Widget
"""

from .upset import UpSetWidget
from ._model import (
    UpSetBaseSet,
    UpSetQuery,
    UpSetSet,
    UpSetSetCombination,
    UpSetSetComposite,
    UpSetSetIntersection,
    UpSetSetLike,
    UpSetSetType,
    UpSetSetUnion,
)
from ._version import __version__, version_info

from .nbextension import _jupyter_nbextension_paths
