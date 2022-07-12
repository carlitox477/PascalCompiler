from typing import Tuple
from .utils import match_token, report_match_error, isTokenInList

#We copy identifier_list_rule to avoid circular reference in python
def identifier_list_rule(pending_source_code:str,current_column:int, current_row:int) -> Tuple[str,int,int]:
    """Simbolo no terminal <lista_de_identificadores>"""
    
    # At list one identifier
    pending_source_code,current_column, current_row=report_match_error('TK_identifier',pending_source_code,current_column, current_row)
    
    # More than one identifier
    _,_,_,success,_=match_token('TK_comma',pending_source_code,current_column, current_row)
    
    while success:
        pending_source_code,current_column, current_row=report_match_error('TK_comma',pending_source_code,current_column, current_row)
        pending_source_code,current_column, current_row=report_match_error('TK_identifier',pending_source_code,current_column, current_row)
        pass
    return pending_source_code,current_column, current_row


def write_command_rule(pending_source_code:str,current_column:int, current_row:int) -> Tuple[str,int,int]:
    """simbolo no terminal <comando_salida>"""
    pending_source_code,current_column,current_row=report_match_error('TK_write',pending_source_code,current_column,current_row)
    pending_source_code,current_column,current_row=report_match_error('TK_parenthesis',pending_source_code,current_column,current_row,['OPPAR'])

    pending_source_code,current_column,current_row=simple_expresion_rule(pending_source_code,current_column,current_row)
    
    pending_source_code,current_column,current_row=report_match_error('TK_parenthesis',pending_source_code,current_column,current_row,['CLPAR'])
    return pending_source_code,current_column,current_row

def lecture_command_rule(pending_source_code:str,current_column:int, current_row:int) -> Tuple[str,int,int]:
    """simbolo no terminal <comando_lectura>"""
    
    pending_source_code,current_column,current_row=report_match_error('TK_read',pending_source_code,current_column,current_row)
    pending_source_code,current_column,current_row=report_match_error('TK_parenthesis',pending_source_code,current_column,current_row,['OPPAR'])
    pending_source_code,current_column,current_row=identifier_list_rule(pending_source_code,current_column,current_row)
    pending_source_code,current_column,current_row=report_match_error('TK_parenthesis',pending_source_code,current_column,current_row,['CLPAR'])
    return pending_source_code,current_column,current_row

def expresion_rule(pending_source_code:str,current_column:int, current_row:int) -> Tuple[str,int,int]:
    """Simbolo no terminal <expresion>"""
    pending_source_code,current_column, current_row,success_tk_boolean_literal,_=match_token('TK_boolean_literal',pending_source_code,current_column, current_row)
    if success_tk_boolean_literal:
        return pending_source_code,current_column, current_row
    
    pending_source_code,current_column, current_row=simple_expresion_rule(pending_source_code,current_column, current_row)
    _,_,_,success_tk_rel_op,_=match_token('TK_relOp',pending_source_code,current_column, current_row)
    
    while success_tk_rel_op:
        pending_source_code,current_column, current_row,success_tk_rel_op,_=match_token('TK_relOp',pending_source_code,current_column, current_row)
        if success_tk_rel_op:
            pending_source_code,current_column, current_row=simple_expresion_rule(pending_source_code,current_column, current_row)
            pass
        pass
    return pending_source_code,current_column, current_row

def simple_expresion_rule(pending_source_code:str,current_column:int, current_row:int) -> Tuple[str,int,int]:
    """Simbolo no terminal <expresion_simple>"""
    
    pending_source_code,current_column, current_row,_,_=match_token('TK_arithOp',pending_source_code,current_column, current_row,['ADD', 'SUB'])
    pending_source_code,current_column, current_row=term_rule(pending_source_code,current_column, current_row)
    
    _,_, _,success_valid_tk_arith_op,_=match_token('TK_arithOp',pending_source_code,current_column, current_row,['ADD', 'SUB'])
    _,_, _,success_tk_or,_=match_token('TK_or',pending_source_code,current_column, current_row)
    
    while(success_valid_tk_arith_op or success_tk_or):
        if(success_valid_tk_arith_op):
            pending_source_code,current_column, current_row=report_match_error('TK_arithOp',pending_source_code,current_column, current_row,['ADD', 'SUB'])
        else:
            pending_source_code,current_column, current_row=report_match_error('TK_or',pending_source_code,current_column, current_row)
        pending_source_code,current_column, current_row=term_rule(pending_source_code,current_column, current_row)
        _,_, _,success_valid_tk_arith_op,_=match_token('TK_arithOp',pending_source_code,current_column, current_row,['ADD', 'SUB'])
        _,_, _,success_tk_or,_=match_token('TK_or',pending_source_code,current_column, current_row)
        pass
    return pending_source_code,current_column, current_row

def term_rule(pending_source_code:str,current_column:int, current_row:int) -> Tuple[str,int,int]:
    """Simbolo no terminal <termino>"""
    pending_source_code,current_column, current_row=factor_rule(pending_source_code,current_column, current_row)
    _,_, _,success_valid_tk_arith_op,_=match_token('TK_arithOp',pending_source_code,current_column, current_row,['MUL', 'DIV'])
    _,_, _,success_tk_and,_=match_token('TK_and',pending_source_code,current_column, current_row)
    
    
    while success_valid_tk_arith_op or success_tk_and:
        if success_valid_tk_arith_op:
            pending_source_code,current_column, current_row=report_match_error('TK_arithOp',pending_source_code,current_column, current_row,['MUL', 'DIV'])
        else:
            pending_source_code,current_column, current_row=report_match_error('TK_and',pending_source_code,current_column, current_row)
        pending_source_code,current_column, current_row=factor_rule(pending_source_code,current_column, current_row)        
        _,_, _,success_valid_tk_arith_op,_=match_token('TK_arithOp',pending_source_code,current_column, current_row,['MUL', 'DIV'])
        _,_, _,success_tk_and,_=match_token('TK_and',pending_source_code,current_column, current_row)
        pass
    return pending_source_code,current_column, current_row

def factor_rule(pending_source_code:str,current_column:int, current_row:int) -> Tuple[str,int,int]:
    """Simbolo no terminal <factor>"""
    
    valid_first_tokens=['TK_identifier', 'TK_number','TK_not_literal', 'TK_parenthesis']
    
    if not isTokenInList(pending_source_code,current_column,current_row,valid_first_tokens):
        raise Exception(f"SYNTAX ERROR: Expected to find a token in {valid_first_tokens}, but found other in row {current_row}, column {current_column}")
    
    pending_source_code,current_column, current_row,success_tk_identifier,_=match_token('TK_identifier',pending_source_code,current_column, current_row)
    if success_tk_identifier:
        _,_, _,success_open_par,_=match_token('TK_parenthesis',pending_source_code,current_column, current_row,['OPPAR'])
        if success_open_par:
            pending_source_code,current_column, current_row=rest_of_function_call_rule(pending_source_code,current_column, current_row)
            pass
        return pending_source_code,current_column, current_row
    
    pending_source_code,current_column, current_row,success_tk_number,_=match_token('TK_number',pending_source_code,current_column, current_row)
    if success_tk_number:
        return pending_source_code,current_column, current_row
    
    pending_source_code,current_column, current_row,success_tk_not_literal,_=match_token('TK_not_literal',pending_source_code,current_column, current_row)
    if success_tk_not_literal:
        pending_source_code,current_column, current_row=factor_rule(pending_source_code,current_column, current_row)
        return pending_source_code,current_column, current_row

    _,_, _,success_open_par,_=match_token('TK_parenthesis',pending_source_code,current_column, current_row,['OPPAR'])
    if success_open_par:
        pending_source_code,current_column, current_row=report_match_error('TK_parenthesis',pending_source_code,current_column, current_row,['OPPAR'])
        pending_source_code,current_column, current_row=expresion_rule(pending_source_code,current_column, current_row)
        pending_source_code,current_column, current_row=report_match_error('TK_parenthesis',pending_source_code,current_column, current_row,['CLPAR'])
        return pending_source_code,current_column, current_row
    raise Exception(f'SYNTAX ERROR: Expecting factor')

def expresion_list_rule(pending_source_code:str,current_column:int, current_row:int) -> Tuple[str,int,int]:
    """Simbolo no terminal <lista_de_expresiones>"""
    pending_source_code,current_column, current_row=simple_expresion_rule(pending_source_code,current_column, current_row)
    
    _,_, _,success_comma,_=match_token('TK_comma',pending_source_code,current_column, current_row)
    while success_comma:
        pending_source_code,current_column, current_row,success_comma,_=match_token('TK_comma',pending_source_code,current_column, current_row)
        pending_source_code,current_column, current_row=simple_expresion_rule(pending_source_code,current_column, current_row)
        pass
    return pending_source_code,current_column, current_row

def rest_of_function_call_rule(pending_source_code:str,current_column:int, current_row:int) -> Tuple[str,int,int]:
    """Simbolo no terminal <resto_llamada_funcion>"""
    pending_source_code,current_column, current_row=report_match_error('TK_parenthesis',pending_source_code,current_column, current_row,['OPPAR'])
    pending_source_code,current_column, current_row=expresion_list_rule(pending_source_code,current_column, current_row)
    pending_source_code,current_column, current_row=report_match_error('TK_parenthesis',pending_source_code,current_column, current_row,['CLPAR'])
    return pending_source_code,current_column, current_row

