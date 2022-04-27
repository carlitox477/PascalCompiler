#!/usr/bin/env python3
import pytest
from context import white_space_recognizer,comment_recognizer,identifier_keyword_recognizer,relational_operator_recognizer, parenthesis_recognizer,arithmetical_operator_recognizer,special_symbol_recognizer,number_recognizer
from utils import COMMENT_RECOGNIZER_TEST_CASES, WHITE_SPACE_RECOGNIZER_TEST_CASES,IDENTIFIER_TEST_CASES,NUMBER_TEST_CASES,SPECIAL_SYMBOL_CASES,ARITHMETICAL_OPERATOR_TEST_CASES,RELATIONAL_OPERATOR_TEST_CASES,PARENTHESIS_TEST_CASES

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
    IDENTIFIER_TEST_CASES
)
def test_identifier_keyword_recognizer(tuple,expected):
    pending_code, tokens=tuple
    expected_pending_code,expected_tokens=expected
    actual_pending_code,actual_tokens=identifier_keyword_recognizer(pending_code, tokens)
    assert actual_pending_code == expected_pending_code
    assert actual_tokens == expected_tokens
    pass


@pytest.mark.parametrize(
    "tuple, expected",
    NUMBER_TEST_CASES
)
def test_number_recognizer(tuple,expected):
    pending_code, tokens=tuple
    expected_pending_code,expected_tokens=expected
    actual_pending_code,actual_tokens=number_recognizer(pending_code, tokens)
    assert actual_pending_code == expected_pending_code
    assert actual_tokens == expected_tokens
    pass


@pytest.mark.parametrize(
    "tuple, expected",
    SPECIAL_SYMBOL_CASES
)
def test_special_symbol_recognizer(tuple,expected):
    pending_code, tokens=tuple
    expected_pending_code,expected_tokens=expected
    actual_pending_code,actual_tokens=special_symbol_recognizer(pending_code, tokens)
    assert actual_pending_code == expected_pending_code
    assert actual_tokens == expected_tokens
    pass

@pytest.mark.parametrize(
    "tuple, expected",
    ARITHMETICAL_OPERATOR_TEST_CASES
)
def test_arithmetical_operator_recognizer(tuple,expected):
    pending_code, tokens=tuple
    expected_pending_code,expected_tokens=expected
    actual_pending_code,actual_tokens=arithmetical_operator_recognizer(pending_code, tokens)
    assert actual_pending_code == expected_pending_code
    assert actual_tokens == expected_tokens
    pass

@pytest.mark.parametrize(
    "tuple, expected",
    RELATIONAL_OPERATOR_TEST_CASES
)
def test_relational_operator_recognizer(tuple,expected):
    pending_code, tokens=tuple
    expected_pending_code,expected_tokens=expected
    actual_pending_code,actual_tokens=relational_operator_recognizer(pending_code, tokens)
    assert actual_pending_code == expected_pending_code
    assert actual_tokens == expected_tokens
    pass

@pytest.mark.parametrize(
    "tuple, expected",
    PARENTHESIS_TEST_CASES
)
def test_parenthesis_recognizer(tuple,expected):
    pending_code, tokens=tuple
    expected_pending_code,expected_tokens=expected
    actual_pending_code,actual_tokens=parenthesis_recognizer(pending_code, tokens)
    assert actual_pending_code == expected_pending_code
    assert actual_tokens == expected_tokens
    pass