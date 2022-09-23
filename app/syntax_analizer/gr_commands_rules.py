from typing import Tuple

from .syntax_exception import SyntaxException
from .utils import check_token, match_token, report_match_error, isTokenInList
from .gr_expresions_rules import ExpresionRulesRecognizer

class CommandRulesRecognizer:
    @staticmethod
    def verify_compound_command_rule(pending_source_code:str,current_column:int, current_row:int) -> Tuple[str,int,int]:
        """
        Identifies rule: <comando_compuesto> ::= begin <comando> ; {<comando> ;} end
            
            Args:
                pending_source_code(str): Pending code to analize. Acts as look ahead
                current_column(int): column where the look ahead is
                current_row(int): row where the look ahead is

            Returns:
                pending_source_code(str): Updated look ahead
                current_column(int): Column where the updated look ahead is
                current_row(int): Row where the updated look ahead is
        """
        pending_source_code,current_column, current_row,_,_=match_token('TK_begin',pending_source_code,current_column, current_row)
        
        pending_source_code,current_column, current_row=CommandRulesRecognizer.verify_command(pending_source_code,current_column, current_row)
        pending_source_code,current_column, current_row,_,_=match_token('TK_semicolon',pending_source_code,current_column, current_row)
        
        valid_first_tokens=['TK_begin', 'TK_if','TK_identifier', 'TK_while', 'TK_read', 'TK_write']
        #isTokenInList(pending_source_code,current_column, current_row,valid_first_tokens)
        
        while isTokenInList(pending_source_code,current_column, current_row,valid_first_tokens):
            pending_source_code,current_column, current_row=CommandRulesRecognizer.verify_command(pending_source_code,current_column, current_row)
            pending_source_code,current_column, current_row,_,_=match_token('TK_semicolon',pending_source_code,current_column, current_row)
            pass
            
        pending_source_code,current_column, current_row,_,_=match_token('TK_end',pending_source_code,current_column, current_row)
        return pending_source_code,current_column, current_row
    
    @staticmethod
    def verify_command(pending_source_code:str,current_column:int, current_row:int) -> Tuple[str,int,int]:
        """
        Identifies rule: <comando> ::= <comando_condicional> | <comando_compuesto> | <identificador> <comando'> | <comando_repetitivo> | <comando_lectura> | <comando_salida>
            
            Args:
                pending_source_code(str): Pending code to analize. Acts as look ahead
                current_column(int): column where the look ahead is
                current_row(int): row where the look ahead is

            Returns:
                pending_source_code(str): Updated look ahead
                current_column(int): Column where the updated look ahead is
                current_row(int): Row where the updated look ahead is
        """
        if check_token('TK_begin',pending_source_code,current_column, current_row):
            return CommandRulesRecognizer.verify_compound_command_rule(pending_source_code,current_column, current_row)

        if check_token('TK_if',pending_source_code,current_column, current_row):
            return CommandRulesRecognizer.verify_conditional_command_rule(pending_source_code,current_column, current_row)

        if check_token('TK_identifier',pending_source_code,current_column, current_row):
            pending_source_code,current_column, current_row,_,_=match_token('TK_identifier',pending_source_code,current_column, current_row)
            return CommandRulesRecognizer.verify_command_2_rule(pending_source_code,current_column, current_row)
        
        if check_token('TK_while',pending_source_code,current_column, current_row):
            return CommandRulesRecognizer.verify_repetitive_command_rule(pending_source_code,current_column, current_row)
        
        if check_token('TK_read',pending_source_code,current_column, current_row):
            return ExpresionRulesRecognizer.verify_lecture_command_rule(pending_source_code,current_column,current_row)
        
        if check_token('TK_write',pending_source_code,current_column, current_row):
            return ExpresionRulesRecognizer.verify_write_command_rule(pending_source_code,current_column,current_row)
        
        raise Exception(f"SYNTAX ERROR: Expected to find a token in {['TK_begin', 'TK_if', 'TK_identifier', 'TK_while', 'TK_read', 'TK_write']}, but found other in row {current_row}, column {current_column}: {pending_source_code[0:20]}")

    @staticmethod
    def verify_conditional_command_rule(pending_source_code:str,current_column:int, current_row:int) -> Tuple[str,int,int]:
        """
        Identifies rule: <comando_condicional> ::= if <expresion> then <comando> [ else <comando> ]
            
            Args:
                pending_source_code(str): Pending code to analize. Acts as look ahead
                current_column(int): column where the look ahead is
                current_row(int): row where the look ahead is

            Returns:
                pending_source_code(str): Updated look ahead
                current_column(int): Column where the updated look ahead is
                current_row(int): Row where the updated look ahead is
        """
        pending_source_code,current_column, current_row,_,_ = match_token('TK_if',pending_source_code,current_column, current_row)
        pending_source_code,current_column, current_row = ExpresionRulesRecognizer.verify_expresion_rule(pending_source_code,current_column, current_row)
        pending_source_code,current_column, current_row,_,_ = match_token('TK_then',pending_source_code,current_column, current_row)
        pending_source_code,current_column, current_row = CommandRulesRecognizer.verify_command(pending_source_code,current_column, current_row)
        
        success_tk_else = True
        try:
            pending_source_code,current_column, current_row,_,_=match_token('TK_else',pending_source_code,current_column, current_row)
        except SyntaxException:
            success_tk_else= False
        if success_tk_else:
            pending_source_code,current_column, current_row=CommandRulesRecognizer.verify_command(pending_source_code,current_column, current_row)
            pass
        return pending_source_code,current_column, current_row

    @staticmethod
    def verify_repetitive_command_rule(pending_source_code:str,current_column:int, current_row:int) -> Tuple[str,int,int]:
        """
        Identifies rule: <comando_repetitivo> ::= while <expresion> do <comando>
            
            Args:
                pending_source_code(str): Pending code to analize. Acts as look ahead
                current_column(int): column where the look ahead is
                current_row(int): row where the look ahead is

            Returns:
                pending_source_code(str): Updated look ahead
                current_column(int): Column where the updated look ahead is
                current_row(int): Row where the updated look ahead is
        """
        pending_source_code,current_column,current_row,_,_ = match_token('TK_while',pending_source_code,current_column,current_row)
        pending_source_code,current_column,current_row = ExpresionRulesRecognizer.verify_expresion_rule(pending_source_code,current_column,current_row)
        pending_source_code,current_column,current_row,_,_ = match_token('TK_do',pending_source_code,current_column,current_row)
        pending_source_code,current_column,current_row = CommandRulesRecognizer.verify_command(pending_source_code,current_column,current_row)
        return pending_source_code,current_column,current_row

    @staticmethod
    def verify_command_2_rule(pending_source_code:str,current_column:int, current_row:int) -> Tuple[str,int,int]:
        """
        Identifies rule: <comando'> ::= <resto_asignacion> | <resto_llamada_funcion>
            
            Args:
                pending_source_code(str): Pending code to analize. Acts as look ahead
                current_column(int): column where the look ahead is
                current_row(int): row where the look ahead is

            Returns:
                pending_source_code(str): Updated look ahead
                current_column(int): Column where the updated look ahead is
                current_row(int): Row where the updated look ahead is
        """
        success_tkn_comma=check_token('TK_comma',pending_source_code,current_column,current_row)
        success_tkn_assignment=check_token('TK_assignment',pending_source_code,current_column,current_row)
        success_open_par=check_token('TK_parenthesis',pending_source_code,current_column, current_row,{"type": ['OPPAR']})

        if success_tkn_comma or success_tkn_assignment:
            pending_source_code,current_column,current_row=CommandRulesRecognizer.verify_rest_of_assignation_rule(pending_source_code,current_column,current_row)
        elif success_open_par:
            return ExpresionRulesRecognizer.verify_rest_of_function_call_rule(pending_source_code,current_column,current_row)
        return pending_source_code,current_column,current_row

    @staticmethod
    def verify_rest_of_assignation_rule(pending_source_code:str,current_column:int, current_row:int) -> Tuple[str,int,int]:
        """
        Identifies rule: <resto_asignacion> ::= { , <identificador> } := <expresion>
            
            Args:
                pending_source_code(str): Pending code to analize. Acts as look ahead
                current_column(int): column where the look ahead is
                current_row(int): row where the look ahead is

            Returns:
                pending_source_code(str): Updated look ahead
                current_column(int): Column where the updated look ahead is
                current_row(int): Row where the updated look ahead is
        """
        
        while check_token('TK_comma',pending_source_code,current_column,current_row):
            pending_source_code, current_column, current_row, _, _ = match_token('TK_comma',pending_source_code,current_column,current_row)
            pending_source_code, current_column, current_row, _, _ = match_token('TK_identifier',pending_source_code,current_column,current_row)
            pass
        pending_source_code,current_column,current_row,_,_ = match_token('TK_assignment',pending_source_code,current_column,current_row)
        return ExpresionRulesRecognizer.verify_expresion_rule(pending_source_code,current_column,current_row)
    
    pass






