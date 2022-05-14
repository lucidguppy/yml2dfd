# Copyright 2022 Matthew Karas
from yml2dfd.test.data.example import simple
from yml2dfd.yml2dfd import build_diagram


def test_simple():
    build_diagram(simple)