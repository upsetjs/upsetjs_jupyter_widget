#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Samuel Gratzl
# Distributed under the terms of the Modified BSD License.

def _jupyter_nbextension_paths():
    return [{
        'section': 'notebook',
        'src': 'nbextension/static',
        'dest': 'upsetjs_jupyter_widget',
        'require': 'upsetjs_jupyter_widget/extension'
    }]
