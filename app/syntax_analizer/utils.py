#!/usr/bin/env python3
from typing import Tuple

from app.syntax_analizer.semantic_analizer.symbol import Symbol
from .lexical_analizer.lexical_analizer import LexicalAnalyzer
from .syntax_error_analyzer import SyntaxErrorAnalyzer
from .syntax_error_analyzer import SyntaxException
from .lexical_analizer.automatas.token import Token
from .semantic_analizer.symbol_table import SymbolTable

def match_token(searched_token: str, pending_source_code: str, current_column:int, current_row:int, attributes_values=None, raise_error=True) -> Tuple[str,int,int,Token,bool]:
    """
    Verifies if the pre-analysis symbol matches with the terminal_symbol
    """ 
    new_pending_source_code,new_column,new_row,current_token=LexicalAnalyzer.get_lexical_token(pending_source_code,current_column,current_row)
    
    try:
        SyntaxErrorAnalyzer.verifyExpectedToken(current_token,searched_token,attributes_values,current_row,current_column)
    except SyntaxException as exception:
        if(raise_error):
            raise exception
            #raise Exception(pending_source_code[0:20])
        return pending_source_code,current_column, current_row, None, False
    return new_pending_source_code,new_column,new_row,current_token, True

def report_match_error(expected_token:str, pending_source_code:str, current_column:str, current_row:str, attribute_values=None)-> Tuple[str,int,int]:
    pending_source_code,current_column, current_row,success,error_message, token = match_token(expected_token,pending_source_code,current_column, current_row,attribute_values)
    if not success:
        raise Exception(error_message+f", {pending_source_code[0:20]}")
    return pending_source_code,current_column, current_row, token

def check_token(expected_token:str, pending_source_code:str, current_column:int, current_row:int, attribute_values=None)->bool:
    try:
        match_token(expected_token,pending_source_code,current_column, current_row,attribute_values)
    except SyntaxException:
        return False
    return True

def isTokenInList(pending_source_code:str,current_column:int, current_row:int,token_list:list)->bool:
    _,_,_,current_token=LexicalAnalyzer.get_lexical_token(pending_source_code,current_column,current_row)
    return current_token.type in token_list

def delete_whitespaces_and_comments(pending_source_code:str,current_column:int,current_row:int):
    extra_code,_,_,_ = LexicalAnalyzer.get_lexical_token(pending_source_code+" ",current_column,current_row)
    
    # Add Error here
    if(len(extra_code)!=0):
        raise Exception(f'SYNTAX ERROR: Code found after end of the program. End is at row {current_row} and column {current_column}')
    pass

# Sematic helper

def create_symbol_list_from_identifier_list(identifier_token_list: list, datatype_token: Token):
    symbol_list=[]

    for id_token in identifier_token_list:
        symbol = Symbol("VAR",id_token.getAttribute("name"),[],datatype_token.getAttribute("name"),0,id_token.row) # offset will change when it is added to table
        symbol_list.append(symbol)
        pass
    return symbol_list
