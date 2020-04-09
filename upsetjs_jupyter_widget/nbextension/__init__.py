#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Samuel Gratzl


def _jupyter_nbextension_paths():
    return [
        {
            "section": "notebook",
            "src": "nbextension/static",
            "dest": "upsetjs_jupyter_widget",
            "require": "upsetjs_jupyter_widget/extension",
        }
    ]
