from typing import Tuple
from .utils import match_token, report_match_error
from .commands_rules import compound_command_rule

def block_rule(pending_source_code:str,current_column:int, current_row:int) -> Tuple[str,int,int]:
    """Simbolo no terminal <bloque>"""
    pending_source_code,current_column, current_row=variables_declaration_part_rule(pending_source_code,current_column, current_row)
    pending_source_code,current_column, current_row=subrutine_declaration_part_rule(pending_source_code,current_column, current_row)

    pending_source_code,current_column, current_row=compound_command_rule(pending_source_code,current_column, current_row)
    return pending_source_code,current_column, current_row


def variables_declaration_part_rule(pending_source_code:str,current_column:int, current_row:int) -> Tuple[str,int,int]:
    """
        Design problem?: Just one TK_VAR token allowed
        Simbolo no terminal <parte_declaration_de_variables>
    """
    
    pending_source_code,current_column, current_row,success,_=match_token('TK_var',pending_source_code,current_column, current_row)
    if not success:
        # Assume that there is not var declaration
        return pending_source_code,current_column, current_row
    
    # At least one line of variables declaration
    pending_source_code,current_column, current_row=variables_declaration_rule(pending_source_code,current_column, current_row)    
    pending_source_code,current_column, current_row=report_match_error('TK_semicolon',pending_source_code,current_column, current_row)

    while success:
        _,_,_,success,_=match_token('TK_identifier',pending_source_code,current_column, current_row)
        if(success):
            pending_source_code,current_column, current_row=variables_declaration_rule(pending_source_code,current_column, current_row)
            pending_source_code,current_column, current_row=report_match_error('TK_semicolon',pending_source_code,current_column, current_row)
        pass
    return pending_source_code,current_column, current_row

def variables_declaration_rule(pending_source_code:str,current_column:int, current_row:int) -> Tuple[str,int,int]:
    """Simbolo no terminal <declaracion_de_variables>"""
    pending_source_code,current_column, current_row=identifier_list_rule(pending_source_code,current_column, current_row)
    pending_source_code,current_column, current_row=report_match_error('TK_colon',pending_source_code,current_column, current_row)
    pending_source_code,current_column, current_row=datatype_rule(pending_source_code,current_column, current_row)
    return pending_source_code,current_column, current_row
    
def identifier_list_rule(pending_source_code:str,current_column:int, current_row:int) -> Tuple[str,int,int]:
    """Simbolo no terminal <lista_de_identificadores>"""
    
    # At list one identifier
    pending_source_code,current_column, current_row=report_match_error('TK_identifier',pending_source_code,current_column, current_row)
    
    # More than one identifier
    _,_,_,success,_=match_token('TK_comma',pending_source_code,current_column, current_row)
    
    while success:
        pending_source_code,current_column, current_row,success,_=match_token('TK_comma',pending_source_code,current_column, current_row)
        if success:
            pending_source_code,current_column, current_row=report_match_error('TK_identifier',pending_source_code,current_column, current_row)
            pass        
        pass
    return pending_source_code,current_column, current_row

def datatype_rule(pending_source_code:str,current_column:int, current_row:int) -> Tuple[str,int,int]:
    pending_source_code,current_column, current_row=report_match_error('TK_datatype',pending_source_code,current_column, current_row)    
    return pending_source_code,current_column, current_row

def subrutine_declaration_part_rule(pending_source_code:str,current_column:int, current_row:int) -> Tuple[str,int,int]:
    """Simbolo no terminal <parte_declaracion_de_subrutinas>"""
    
    _,_, _,function_tk_match_success,_=match_token('TK_function',pending_source_code,current_column, current_row)
    _,_, _,procedure_tk_match_success,_=match_token('TK_procedure',pending_source_code,current_column, current_row)
    
    
    while(function_tk_match_success or procedure_tk_match_success):
        if function_tk_match_success:
            pending_source_code,current_column, current_row=function_declaration_rule(pending_source_code,current_column, current_row)
        elif procedure_tk_match_success:
            pending_source_code,current_column, current_row=procedure_declaration_rule(pending_source_code,current_column, current_row)
        
        pending_source_code,current_column, current_row=report_match_error('TK_semicolon',pending_source_code,current_column, current_row)        
        _,_, _,function_tk_match_success,_=match_token('TK_function',pending_source_code,current_column, current_row)
        _,_, _,procedure_tk_match_success,_=match_token('TK_procedure',pending_source_code,current_column, current_row)
        pass
    return pending_source_code,current_column, current_row

def procedure_declaration_rule(pending_source_code:str,current_column:int,current_row:int) -> Tuple[str,int,int]:
    """Simbolo no terminal <declaracion_de_procedimiento>"""
    pending_source_code,current_column, current_row=report_match_error('TK_procedure',pending_source_code,current_column, current_row)
    pending_source_code,current_column, current_row=report_match_error('TK_identifier',pending_source_code,current_column, current_row)
    
    _,_, _,success,_=match_token('TK_parenthesis',pending_source_code,current_column, current_row,['OPPAR'])

    if success:
        pending_source_code,current_column, current_row=report_match_error('TK_parenthesis',pending_source_code,current_column, current_row,['OPPAR'])
        pending_source_code,current_column, current_row=formal_parameters_rule(pending_source_code,current_column, current_row)
        pending_source_code,current_column, current_row=report_match_error('TK_parenthesis',pending_source_code,current_column, current_row,['CLPAR'])
        pass

    pending_source_code,current_column, current_row=report_match_error('TK_semicolon',pending_source_code,current_column, current_row)
    pending_source_code,current_column, current_row=block_rule(pending_source_code,current_column, current_row)
    return pending_source_code,current_column, current_row

def function_declaration_rule(pending_source_code:str,current_column:int,current_row:int) -> Tuple[str,int,int]:
    """Simbolo no terminal <declaracion_de_funcion>"""
    
    pending_source_code,current_column, current_row=report_match_error('TK_function',pending_source_code,current_column, current_row)
    pending_source_code,current_column, current_row=report_match_error('TK_identifier',pending_source_code,current_column, current_row)
    
    _,_, _,success,_=match_token('TK_parenthesis',pending_source_code,current_column, current_row,['OPPAR'])
    if success:
        pending_source_code,current_column, current_row=report_match_error('TK_parenthesis',pending_source_code,current_column, current_row,['OPPAR'])
        pending_source_code,current_column, current_row=formal_parameters_rule(pending_source_code,current_column, current_row)
        pending_source_code,current_column, current_row=report_match_error('TK_parenthesis',pending_source_code,current_column, current_row,['CLPAR'])
        pass
        
    pending_source_code,current_column, current_row=report_match_error('TK_colon',pending_source_code,current_column, current_row)
    pending_source_code,current_column, current_row=datatype_rule(pending_source_code,current_column, current_row)
    pending_source_code,current_column, current_row=report_match_error('TK_semicolon',pending_source_code,current_column, current_row)
    pending_source_code,current_column, current_row=block_rule(pending_source_code,current_column, current_row)
    return pending_source_code,current_column, current_row

def formal_parameters_rule(pending_source_code:str,current_column:int,current_row:int) -> Tuple[str,int,int]:
    """Simbolo no terminal <parametros_formales>"""
    pending_source_code,current_column,current_row=variables_declaration_section_rule(pending_source_code,current_column,current_row)
    continue_analysis=True
    while continue_analysis:
        pending_source_code,current_column, current_row,continue_analysis,_=match_token('TK_semicolon',pending_source_code,current_column, current_row)
        if continue_analysis:
            pending_source_code,current_column,current_row=variables_declaration_section_rule(pending_source_code,current_column,current_row)
            pass        
        pass
    return pending_source_code,current_column,current_row

def variables_declaration_section_rule(pending_source_code:str,current_column:int,current_row:int) -> Tuple[str,int,int]:
    """Simbolo no terminal <seccion_declaracion_de_variables>"""
    #pending_source_code,current_column,current_row=report_match_error('TK_var',pending_source_code,current_column, current_row)
    pending_source_code,current_column,current_row=variables_declaration_rule(pending_source_code,current_column,current_row)
    return pending_source_code,current_column,current_row
