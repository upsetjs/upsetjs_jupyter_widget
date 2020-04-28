# coding: utf- 8
# @upsetjs/jupyter_widget
# https://github.com/upsetjs/upsetjs_jupyter_widget
#
# Copyright (c) 2020 Samuel Gratzl <sam@sgratzl.com>

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
