from typing import Tuple
from .utils import match_token, report_match_error, isTokenInList
from .expresions_rules import rest_of_function_call_rule, expresion_rule, write_command_rule,lecture_command_rule

def compound_command_rule(pending_source_code:str,current_column:int, current_row:int) -> Tuple[str,int,int]:
    """Simbolo no terminal <comando_compuesto>"""
    pending_source_code,current_column, current_row=report_match_error('TK_begin',pending_source_code,current_column, current_row)
    
    pending_source_code,current_column, current_row=command_rule(pending_source_code,current_column, current_row)
    pending_source_code,current_column, current_row=report_match_error('TK_semicolon',pending_source_code,current_column, current_row)
    
    valid_first_tokens=['TK_begin', 'TK_if','TK_identifier', 'TK_while', 'TK_read', 'TK_write']
    isTokenInList(pending_source_code,current_column, current_row,valid_first_tokens)
    
    while isTokenInList(pending_source_code,current_column, current_row,valid_first_tokens):
        pending_source_code,current_column, current_row=command_rule(pending_source_code,current_column, current_row)
        pending_source_code,current_column, current_row=report_match_error('TK_semicolon',pending_source_code,current_column, current_row)
        pass
        
    pending_source_code,current_column, current_row=report_match_error('TK_end',pending_source_code,current_column, current_row)
    return pending_source_code,current_column, current_row

def command_rule(pending_source_code:str,current_column:int, current_row:int) -> Tuple[str,int,int]:
    """Simbolo no terminal <comando>"""
    _,_,_,success_tk_begin,_=match_token('TK_begin',pending_source_code,current_column, current_row)
    if success_tk_begin:
        return compound_command_rule(pending_source_code,current_column, current_row)
    
    _,_, _,success_tk_if,_=match_token('TK_if',pending_source_code,current_column, current_row)
    if success_tk_if:
        return conditional_command_rule(pending_source_code,current_column, current_row)
    
    pending_source_code,current_column, current_row,success_tk_identifier,_=match_token('TK_identifier',pending_source_code,current_column, current_row)
    if success_tk_identifier:
        return command_2_rule(pending_source_code,current_column, current_row)
    
    _,_, _,success_tk_while,_=match_token('TK_while',pending_source_code,current_column, current_row)
    if success_tk_while:
        return repetitive_command_rule(pending_source_code,current_column, current_row)
    
    _,_, _,success_tk_read,_=match_token('TK_read',pending_source_code,current_column, current_row)
    if success_tk_read:
        return lecture_command_rule(pending_source_code,current_column,current_row)
    
    _,_, _,success_tk_write,_=match_token('TK_write',pending_source_code,current_column, current_row)
    if success_tk_write:
        return write_command_rule(pending_source_code,current_column,current_row)
    
    raise Exception(f"SYNTAX ERROR: Expected to find a token in {['TK_begin', 'TK_if', 'TK_identifier', 'TK_while', 'TK_read', 'TK_write']}, but found other in row {current_row}, column {current_column}: {pending_source_code[0:20]}")
    #raise Exception(f"SYNTAX ERROR: Expected to find a token in {['TK_begin', 'TK_if', 'TK_identifier','TK_while', 'TK_read', 'TK_write']}, but found other in row {current_row}, column {current_column}")

def conditional_command_rule(pending_source_code:str,current_column:int, current_row:int) -> Tuple[str,int,int]:
    """Simbolo no terminal <comando_condicional>"""
    pending_source_code,current_column, current_row=report_match_error('TK_if',pending_source_code,current_column, current_row)
    pending_source_code,current_column, current_row=expresion_rule(pending_source_code,current_column, current_row)
    pending_source_code,current_column, current_row=report_match_error('TK_then',pending_source_code,current_column, current_row)
    pending_source_code,current_column, current_row=command_rule(pending_source_code,current_column, current_row)
    
    pending_source_code,current_column, current_row,success_tk_else,_=match_token('TK_else',pending_source_code,current_column, current_row)
    if success_tk_else:
        pending_source_code,current_column, current_row=command_rule(pending_source_code,current_column, current_row)
        pass
    return pending_source_code,current_column, current_row


def repetitive_command_rule(pending_source_code:str,current_column:int, current_row:int) -> Tuple[str,int,int]:
    """Simbolo no terminal <comando_repetitivo>"""
    pending_source_code,current_column,current_row=report_match_error('TK_while',pending_source_code,current_column,current_row)
    pending_source_code,current_column,current_row=expresion_rule(pending_source_code,current_column,current_row)
    pending_source_code,current_column,current_row=report_match_error('TK_do',pending_source_code,current_column,current_row)
    pending_source_code,current_column,current_row=command_rule(pending_source_code,current_column,current_row)
    return pending_source_code,current_column,current_row


def command_2_rule(pending_source_code:str,current_column:int, current_row:int) -> Tuple[str,int,int]:
    """simbolo no terminal <comando'>"""
    _,_,_,success_tkn_comma,_=match_token('TK_comma',pending_source_code,current_column,current_row)
    _,_,_,success_tkn_assignment,_=match_token('TK_assignment',pending_source_code,current_column,current_row)
    _,_, _,success_open_par,_=match_token('TK_parenthesis',pending_source_code,current_column, current_row,['OPPAR'])
    
    if success_tkn_comma or success_tkn_assignment:
        pending_source_code,current_column,current_row=rest_of_assignation_rule(pending_source_code,current_column,current_row)
    elif success_open_par:
        return rest_of_function_call_rule(pending_source_code,current_column,current_row)
    return pending_source_code,current_column,current_row


def rest_of_assignation_rule(pending_source_code:str,current_column:int, current_row:int) -> Tuple[str,int,int]:
    """Simbolo no terminal <resto_asignacion>"""
    _,_,_,success_tkn_comma,_=match_token('TK_comma',pending_source_code,current_column,current_row)
    while success_tkn_comma:
        match_token('TK_comma')
        match_token('TK_identifier')
        
        pending_source_code,current_column,current_row=report_match_error('TK_comma',pending_source_code,current_column,current_row)
        pending_source_code,current_column,current_row=report_match_error('TK_identifier',pending_source_code,current_column,current_row)
        _,_,_,success_tkn_comma,_=match_token('TK_comma',pending_source_code,current_column,current_row)
        pass
    pending_source_code,current_column,current_row=report_match_error('TK_assignment',pending_source_code,current_column,current_row)
    return expresion_rule(pending_source_code,current_column,current_row)

