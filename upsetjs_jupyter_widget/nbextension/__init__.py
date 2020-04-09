# coding: utf-8
# Copyright (c) Samuel Gratzl
"""
UpSet.js Jupyter Widget
"""


def _jupyter_nbextension_paths():
    return [
        {
            "section": "notebook",
            "src": "nbextension/static",
            "dest": "upsetjs_jupyter_widget",
            "require": "upsetjs_jupyter_widget/extension",
        }
    ]
