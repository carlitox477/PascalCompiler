#!/usr/bin/env python3
from time import sleep
from context import white_space_recognizer,comment_recognizer,identifier_keyword_recognizer,relational_operator_recognizer, parenthesis_recognizer,arithmetical_operator_recognizer,special_symbol_recognizer,number_recognizer,read_source_code,get_pascal_program_file_name_path

PASCAL_PROGRAM_FILE_NAME="pascal-program.pas"


def source_code_to_lexems(source_code:str):
    tokens = []
    pending_source_code = source_code+" "
    while(len(pending_source_code) > 0):
        pending_source_code, tokens = white_space_recognizer(pending_source_code,tokens)
        if(len(pending_source_code) == 0):
            return tokens
        pending_source_code, tokens = identifier_keyword_recognizer(pending_source_code, tokens)
        pending_source_code, tokens = special_symbol_recognizer(pending_source_code, tokens)
        pending_source_code, tokens = comment_recognizer(pending_source_code, tokens)
        pending_source_code, tokens = number_recognizer(pending_source_code, tokens)
        pending_source_code, tokens = arithmetical_operator_recognizer(pending_source_code, tokens)
        pending_source_code, tokens = relational_operator_recognizer(pending_source_code, tokens)
        pending_source_code, tokens = parenthesis_recognizer(pending_source_code, tokens)
        #print(pending_source_code)
        #sleep(1)
        pass


source_code=read_source_code(get_pascal_program_file_name_path(PASCAL_PROGRAM_FILE_NAME))
print(source_code_to_lexems(source_code))
