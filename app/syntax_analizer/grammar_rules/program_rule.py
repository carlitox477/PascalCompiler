from .utils import report_match_error,delete_whitespaces
from .declaration_rules import block_rule


def program_rule(pending_source_code:str,current_column:int, current_row:int)->bool:
    pending_source_code,current_column, current_row=report_match_error('TK_program',pending_source_code,current_column, current_row)
    pending_source_code,current_column, current_row=report_match_error('TK_identifier',pending_source_code,current_column, current_row)
    pending_source_code,current_column, current_row=report_match_error('TK_semicolon',pending_source_code,current_column, current_row)
    
    pending_source_code,current_column, current_row=block_rule(pending_source_code,current_column, current_row)
    pending_source_code,current_column, current_row=report_match_error('TK_dot',pending_source_code,current_column, current_row)
    
    # we delete comments, whitespaces and tabs
    delete_whitespaces(pending_source_code,current_column,current_row)
    print("Programa sin errores sintacticos.")
    return True
