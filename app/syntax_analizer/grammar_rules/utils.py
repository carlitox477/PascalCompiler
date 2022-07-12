from typing import Tuple
from ...lexical_analizer.lexical_analizer import getLexicalToken

def match_token(searched_token: str,pending_source_code:str,current_column:int, current_row:int, attributes_values=None) -> Tuple[str,int,int,bool,str]:
    """
    Verifies if the pre-analysis simbol matches with the terminal_symbol
    """ 
    new_pending_source_code,new_column,new_row,current_token=getLexicalToken(pending_source_code,current_column,current_row)
    
    if current_token[0] == searched_token:
        if attributes_values==None:
            return new_pending_source_code,new_column,new_row, True, None
        elif attributes_values!=None and current_token[1] in attributes_values:
            return new_pending_source_code,new_column,new_row, True, None
        elif attributes_values!=None:
            return pending_source_code,current_column, current_row, False, f"SYNTAX ERROR: Expected {searched_token} with value in {attributes_values} at row {current_row}, column {current_column}, instead it is {current_token[0]} with value {current_token[1]}"
        # Move lookahead
    elif attributes_values!=None:
        return pending_source_code,current_column, current_row, False, f"SYNTAX ERROR: Expected {searched_token} with value in {attributes_values} at row {current_row}, column {current_column}, instead it is {current_token[0]}"
    else:
        return pending_source_code,current_column, current_row, False, f"SYNTAX ERROR: Expected {searched_token} at row {current_row}, column {current_column}, instead it is {current_token[0]}"        

def report_match_error(expected_token:str,pending_source_code:str,current_column:str, current_row:str,attribute_values=None)-> Tuple[str,int,int]:
    pending_source_code,current_column, current_row,success,error_message=match_token(expected_token,pending_source_code,current_column, current_row,attribute_values)
    if not success: raise Exception(error_message+f", {pending_source_code[0:20]}")
    return pending_source_code,current_column, current_row
        

def isTokenInList(pending_source_code:str,current_column:str, current_row:str,token_list:list)->bool:
    _,_,_,current_token=getLexicalToken(pending_source_code,current_column,current_row)
    return current_token[0] in token_list

def delete_whitespaces(pending_source_code:str,current_column:int,current_row:int):
    extra_code,_,_,_ = getLexicalToken(pending_source_code+" ",current_column,current_row)
    if(len(extra_code)!=0):
        raise Exception(f'SYNTAX ERROR: Code found after end of the program. End is at row {current_row} and column {current_column}')
    pass