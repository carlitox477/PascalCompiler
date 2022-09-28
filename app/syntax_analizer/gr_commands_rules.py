
from typing import Tuple

from app.syntax_analizer.mepa_writer import MepaWriter
from .lexical_analizer.automatas.token import Token

from .semantic_analizer.symbol_table import SymbolTable
from .semantic_error_analizer import SemanticErrorAnalyzer

from .syntax_exception import SyntaxException
from .utils import check_token, match_token, isTokenInList
from .gr_expresions_rules import ExpresionRulesRecognizer

class CommandRulesRecognizer:
    @staticmethod
    def verify_compound_command_rule(pending_source_code:str,current_column:int, current_row:int, symbol_table:SymbolTable, mepa_writer: MepaWriter) -> Tuple[str,int,int]:
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
        
        pending_source_code,current_column, current_row=CommandRulesRecognizer.verify_command(pending_source_code,current_column, current_row,symbol_table,mepa_writer)
        pending_source_code,current_column, current_row,_,_=match_token('TK_semicolon',pending_source_code,current_column, current_row)
        
        valid_first_tokens=['TK_begin', 'TK_if','TK_identifier', 'TK_while', 'TK_read', 'TK_write']
        #isTokenInList(pending_source_code,current_column, current_row,valid_first_tokens)
        
        while isTokenInList(pending_source_code,current_column, current_row,valid_first_tokens):
            pending_source_code,current_column, current_row=CommandRulesRecognizer.verify_command(pending_source_code,current_column, current_row,symbol_table,mepa_writer)
            pending_source_code,current_column, current_row,_,_=match_token('TK_semicolon',pending_source_code,current_column, current_row)
            pass
            
        pending_source_code,current_column, current_row,_,_=match_token('TK_end',pending_source_code,current_column, current_row)
        return pending_source_code,current_column, current_row
    
    @staticmethod
    def verify_command(pending_source_code:str,current_column:int, current_row:int, symbol_table: SymbolTable, mepa_writer: MepaWriter) -> Tuple[str,int,int]:
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
            #print(pending_source_code)
            return CommandRulesRecognizer.verify_compound_command_rule(pending_source_code,current_column, current_row,symbol_table, mepa_writer)

        if check_token('TK_if',pending_source_code,current_column, current_row):
            #print("IFFFFFFFFFFF")
            return CommandRulesRecognizer.verify_conditional_command_rule(pending_source_code,current_column, current_row,symbol_table, mepa_writer)

        if check_token('TK_identifier',pending_source_code,current_column, current_row):
            pending_source_code,current_column, current_row,identifier_token,_=match_token('TK_identifier',pending_source_code,current_column, current_row)            
            # We send identifier token as param, in case it is an assignation command it will help to semantic analizer, if not it will help to check if function is in symbol table
            return CommandRulesRecognizer.verify_command_2_rule(pending_source_code,current_column, current_row,symbol_table,identifier_token)
        
        if check_token('TK_while',pending_source_code,current_column, current_row):
            return CommandRulesRecognizer.verify_repetitive_command_rule(pending_source_code,current_column, current_row,symbol_table, mepa_writer)
        
        if check_token('TK_read',pending_source_code,current_column, current_row):
            return ExpresionRulesRecognizer.verify_lecture_command_rule(pending_source_code,current_column,current_row, symbol_table)
        
        if check_token('TK_write',pending_source_code,current_column, current_row):
            return ExpresionRulesRecognizer.verify_write_command_rule(pending_source_code,current_column,current_row,symbol_table)
        
        raise Exception(f"SYNTAX ERROR: Expected to find a token in {['TK_begin', 'TK_if', 'TK_identifier', 'TK_while', 'TK_read', 'TK_write']}, but found other in row {current_row}, column {current_column}: {pending_source_code[0:20]}")

    @staticmethod
    def verify_conditional_command_rule(pending_source_code:str,current_column:int, current_row:int, symbol_table:SymbolTable,mepa_writer: MepaWriter) -> Tuple[str,int,int]:
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
        pending_source_code,current_column, current_row,_ = ExpresionRulesRecognizer.verify_expresion_rule(pending_source_code,current_column, current_row,symbol_table,"BOOLEAN")
        
        pending_source_code,current_column, current_row,_,_ = match_token('TK_then',pending_source_code,current_column, current_row)
        
        pending_source_code,current_column, current_row = CommandRulesRecognizer.verify_command(pending_source_code,current_column, current_row,symbol_table,mepa_writer)
        
        success_tk_else = True
        try:
            pending_source_code,current_column, current_row,_,_=match_token('TK_else',pending_source_code,current_column, current_row)
        except SyntaxException:
            success_tk_else= False
        if success_tk_else:
            pending_source_code,current_column, current_row=CommandRulesRecognizer.verify_command(pending_source_code,current_column, current_row,symbol_table,mepa_writer)
            pass
        return pending_source_code,current_column, current_row

    @staticmethod
    def verify_repetitive_command_rule(pending_source_code:str,current_column:int, current_row:int, symbol_table: SymbolTable, mepa_writer: MepaWriter) -> Tuple[str,int,int]:
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
        pending_source_code,current_column,current_row,_= ExpresionRulesRecognizer.verify_expresion_rule(pending_source_code,current_column,current_row,symbol_table,"BOOLEAN")
        pending_source_code,current_column,current_row,_,_ = match_token('TK_do',pending_source_code,current_column,current_row)
        pending_source_code,current_column,current_row = CommandRulesRecognizer.verify_command(pending_source_code,current_column,current_row, mepa_writer)
        return pending_source_code,current_column,current_row

    @staticmethod
    def verify_command_2_rule(pending_source_code:str,current_column:int, current_row:int,symbol_table: SymbolTable, identifier_token: Token) -> Tuple[str,int,int]:
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
            # Verify if identifier is in symbol table
            SemanticErrorAnalyzer.check_var_identifier_is_accesible(identifier_token,symbol_table)
            identifier_signature = identifier_token.getAttribute("name")
            expected_datatype = symbol_table.getSymbol(identifier_signature).output_type
            # print(symbol_table.getSymbol(identifier_signature).to_string())
            pending_source_code,current_column,current_row=CommandRulesRecognizer.verify_rest_of_assignation_rule(pending_source_code,current_column,current_row,symbol_table, expected_datatype)
            #print(symbol_table.to_string())
        elif success_open_par:
            # IMPORTANT: By design decision, only procedure are callable here
            # Verify if there is at least one procedure with the identifier name
            SemanticErrorAnalyzer.check_exists_any_accesible_procedure_with_name(identifier_token,symbol_table)
            # Get expresion datatypes to see if there is a function with the correct signature, otherwise raise error
            
            pending_source_code,current_column, current_row,parameters_datatypes= ExpresionRulesRecognizer.verify_rest_of_function_call_rule(pending_source_code,current_column,current_row,symbol_table,identifier_token,True)
            

            # check if procedure is callable
            SemanticErrorAnalyzer.check_procedure_is_callable(identifier_token,parameters_datatypes,symbol_table)
                  
            pass

        return pending_source_code,current_column,current_row

    @staticmethod
    def verify_rest_of_assignation_rule(pending_source_code:str,current_column:int, current_row:int, symbol_table: SymbolTable,expected_datatype:str) -> Tuple[str,int,int]:
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
            pending_source_code, current_column, current_row, identifier_token, _ = match_token('TK_identifier',pending_source_code,current_column,current_row)

            # Check identifier is in table an is of the expected datatype
            SemanticErrorAnalyzer.check_var_identifier_is_accesible(identifier_token,symbol_table)
            SemanticErrorAnalyzer.check_var_identifier_is_specific_datatype(identifier_token,symbol_table, expected_datatype)
            pass
        pending_source_code,current_column,current_row,_,_ = match_token('TK_assignment',pending_source_code,current_column,current_row)
        pending_source_code,current_column,current_row,_=ExpresionRulesRecognizer.verify_expresion_rule(pending_source_code,current_column,current_row, symbol_table, expected_datatype)
        return pending_source_code,current_column,current_row
    
    pass






