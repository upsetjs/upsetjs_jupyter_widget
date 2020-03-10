#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Samuel Gratzl.

import pytest

from ..upset import UpSetWidget


def test_upset_creation_blank():
    w = UpSetWidget()
    assert w.value == 'Test'
