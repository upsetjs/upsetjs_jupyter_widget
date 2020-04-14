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
            "dest": "@upsetjs/jupyter_widget",
            "require": "@upsetjs/jupyter_widget/extension",
        }
    ]
