#!/usr/bin/env python3
import pytest
from context import white_space_recognizer,comment_recognizer

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

@pytest.mark.parametrize(
    "line, expected",
    [
        ("{fffdfd fd fdfd}if","if"),
        ("{ }if","if"),
        ("{}if","if")
    ]
)
def test_comment_recognizer(line,expected):
    print(line)
    assert comment_recognizer(line)==expected
    