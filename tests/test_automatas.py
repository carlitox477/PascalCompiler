#!/usr/bin/env python3
import pytest
from context import white_space_recognizer,comment_recognizer
from utils import COMMENT_RECOGNIZER_TEST_CASES, WHITE_SPACE_RECOGNIZER_TEST_CASES,IDENTIFIER_TEST_CASES,NUMBER_TEST_CASES,SPECIAL_SYMBOL_CASES,OPERATOR_TEST_CASES,RELATIONAL_OPERATOR_TEST_CASES,PARENTHESIS_TEST_CASES

@pytest.mark.parametrize(
    "tuple, expected",
    WHITE_SPACE_RECOGNIZER_TEST_CASES
)
def test_white_space_recognizer(tuple,expected):
    pending_code, tokens=tuple
    expected_pending_code,expected_tokens=expected
    actual_pending_code,actual_tokens=white_space_recognizer(pending_code, tokens)
    assert actual_pending_code == expected_pending_code
    assert actual_tokens == expected_tokens
    pass

@pytest.mark.parametrize(
    "tuple, expected",
    COMMENT_RECOGNIZER_TEST_CASES
)
def test_comment_recognizer(tuple,expected):
    pending_code, tokens=tuple
    expected_pending_code,expected_tokens=expected
    actual_pending_code,actual_tokens=comment_recognizer(pending_code, tokens)
    assert actual_pending_code == expected_pending_code
    assert actual_tokens == expected_tokens
    pass


@pytest.mark.parametrize(
    "tuple, expected",
    COMMENT_RECOGNIZER_TEST_CASES
)
def test_parenthesis_recognizer(tuple,expected):
    pending_code, tokens=tuple
    expected_pending_code,expected_tokens=expected
    actual_pending_code,actual_tokens=comment_recognizer(pending_code, tokens)
    assert actual_pending_code == expected_pending_code
    assert actual_tokens == expected_tokens
    pass