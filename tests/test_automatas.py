#!/usr/bin/env python3
import pytest
from context import white_space_recognizer,comment_recognizer
from utils import COMMENT_RECOGNIZER_TEST_CASES,WHITE_SPACE_RECOGNIZER_TEST_CASES

@pytest.mark.parametrize(
    "tuple, expected",
    WHITE_SPACE_RECOGNIZER_TEST_CASES
)
def test_white_space_recognizer(tuple,expected):
    pending_code, tokens=tuple
    assert white_space_recognizer(pending_code, tokens)==expected
    pass

@pytest.mark.parametrize(
    "tuple, expected",
    COMMENT_RECOGNIZER_TEST_CASES
)
def test_comment_recognizer(tuple,expected):
    pending_code, tokens=tuple
    assert comment_recognizer(pending_code, tokens)==expected

