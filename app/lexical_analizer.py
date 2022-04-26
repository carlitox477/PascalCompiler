#!/usr/bin/env python3
from .automatas import comment_recognizer, white_space_recognizer, identifier_keyword_recognizer, number_recognizer,special_symbol_recognizer,arithmetical_operator_recognizer,relational_operator_recognizer,parenthesis_recognizer


code = open("ArchivoDePrueba.txt", "r")
source_code = code.readline()
code.close()


def source_code_to_lexems(source_code:str):
    tokens = []
    pending_source_code = source_code+" "
    while(len(pending_source_code) > 0):
        pending_source_code, tokens = white_space_recognizer(pending_source_code)
        if(len(pending_source_code) == 0):
            return tokens
        pending_source_code, tokens = identifier_keyword_recognizer(pending_source_code, tokens)

        pending_source_code, tokens = special_symbol_recognizer(pending_source_code, tokens)

        pending_source_code, tokens = comment_recognizer(pending_source_code, tokens)

        pending_source_code, tokens = number_recognizer(pending_source_code, tokens)

        pending_source_code, tokens = arithmetical_operator_recognizer(pending_source_code, tokens)

        pending_source_code, tokens = relational_operator_recognizer(pending_source_code, tokens)

        pending_source_code, tokens = parenthesis_recognizer(pending_source_code, tokens)
