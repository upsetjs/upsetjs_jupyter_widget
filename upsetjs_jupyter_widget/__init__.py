# coding: utf- 8
# @upsetjs/jupyter_widget
# https://github.com/upsetjs/upsetjs_jupyter_widget
#
# Copyright (c) 2020 Samuel Gratzl <sam@sgratzl.com>

"""
UpSet.js Jupyter Widget
"""

from .widget import (
    UpSetJSWidget,
    UpSetJSVennDiagramWidget,
    UpSetJSEulerDiagramWidget,
    UpSetJSKarnaughMapWidget,
)
from ._model import (
    UpSetBaseSet,
    UpSetQuery,
    UpSetSet,
    UpSetSetCombination,
    UpSetSetComposite,
    UpSetSetDistinctIntersection,
    UpSetSetIntersection,
    UpSetSetLike,
    UpSetSetType,
    UpSetSetUnion,
)
from ._version import __version__, version_info

from .nbextension import _jupyter_nbextension_paths
