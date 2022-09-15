#!/usr/bin/env python3
import string

LETTERS= list(string.ascii_lowercase + string.ascii_uppercase)
DIGITS = list(string.digits)
SYMBOLS= ['+', '-', '*', '/', '<', '>', '=', '_', ',', ';', ':', '(', ')', '{', '}', '[', ']', '.']
ESPECIAL_SYMBOLS=['$', '%', '#', '!', '¡', '¿', '?', '"', '"', '&', '@']
WS=[' ','\n','\t']
ALPHABET= [*LETTERS, *DIGITS, *WS, *SYMBOLS]


KEYWORD_LEXEM_TO_TOKEN={
    'program': 'TK_program',
    'function': 'TK_function',
    'procedure': 'TK_procedure',
    'var': 'TK_var',
    'begin': 'TK_begin',
    'end': 'TK_end',
    'if': 'TK_if',
    'then': 'TK_then',
    'else': 'TK_else',
    'while': 'TK_while',
    'do': 'TK_do',
    'and': 'TK_and',
    'or': 'TK_or',
    'read': 'TK_read',
    'write': 'TK_write',
    'not': 'TK_not',
    'integer': ('TK_datatype','integer'),
    'boolean': ('TK_datatype','boolean'),
    'true': ('TK_boolean_literal',1),
    'false': ('TK_boolean_literal',0)
}

LEXEM_TO_OPERATOR_TOKEN={
    '+': ("TK_arithOp","ADD"),
    '-': ("TK_arithOp","SUB"),
    '*': ("TK_arithOp","MUL"),
    '/': ("TK_arithOp","DIV"),
}

LEXEM_TO_SPECIAL_SYMBOL_TOKEN={
    ':': "TK_colon",
    ',': "TK_comma",
    ';': "TK_semicolon",
    '.': "TK_dot",
}

LEXEM_TO_RELATIONAL_OPERATOR_TOKEN={
    "=":("TK_relOp","EQ"),
    "<":("TK_relOp","LT"),
    "<>":("TK_relOp","DIF"),
    "<=":("TK_relOp","LEQ"),
    ">":("TK_relOp","GT"),
    ">=":("TK_relOp","GEQ"), 
}