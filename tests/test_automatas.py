#!/usr/bin/env python3
import pytest
from context import white_space_recognizer

@pytest.mark.parametrize(
    "line, expected",
    [
        ("    if ","if "),
        ("\tif ","if "),
        ("\nif ","if "),
        (" \t \n\n\n\t   \t \nif ","if "),
    ]
)
def test_white_space_recognizer(line,expected):
    assert white_space_recognizer(line)==expected
    pass