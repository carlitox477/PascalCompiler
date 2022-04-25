#!/usr/bin/env python3
from .automatas import comment_recognizer, white_space_recognizer, identifier_keyword_recognizer, number_recognizer,special_symbol_recognizer,arithmetical_operator_recognizer,relational_operator_recognizer,parenthesis_recognizer



def source_code_to_lexems(source_code:str):
    tokens=[]
    pending_source_code=source_code+" "
    while(len(pending_source_code)>0):
        pending_source_code,tokens=white_space_recognizer(pending_source_code)
        if(len(pending_source_code)==0): break
        
        #More automatas
        
        pass
    pass
