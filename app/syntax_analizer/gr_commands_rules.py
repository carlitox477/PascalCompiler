
from typing import Tuple

from app.syntax_analizer.semantic_analizer.symbol import Symbol

from .mepa_writer import MepaWriter
from .lexical_analizer.automatas.token import Token

from .semantic_analizer.symbol_table import SymbolTable
from .semantic_error_analizer import SemanticErrorAnalyzer

from .syntax_exception import SyntaxException
from .utils import check_token, get_signature, match_token, isTokenInList
from .gr_expresions_rules import ExpresionRulesRecognizer

class CommandRulesRecognizer:
    mepa_writer= None

    @staticmethod
    def setMepaWriter(mepa_writer: MepaWriter):
        print(mepa_writer)
        CommandRulesRecognizer.mepa_writer=mepa_writer
        pass

    @staticmethod
    def verify_compound_command_rule(pending_source_code:str,current_column:int, current_row:int, symbol_table:SymbolTable) -> Tuple[str,int,int]:
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
        pending_source_code,current_column, current_row=CommandRulesRecognizer.verify_command(pending_source_code,current_column, current_row,symbol_table)
        pending_source_code,current_column, current_row,_,_=match_token('TK_semicolon',pending_source_code,current_column, current_row)
        
        valid_first_tokens=['TK_begin', 'TK_if','TK_identifier', 'TK_while', 'TK_read', 'TK_write']
        #isTokenInList(pending_source_code,current_column, current_row,valid_first_tokens)
        
        while isTokenInList(pending_source_code,current_column, current_row,valid_first_tokens):
            pending_source_code,current_column, current_row=CommandRulesRecognizer.verify_command(pending_source_code,current_column, current_row,symbol_table)
            pending_source_code,current_column, current_row,_,_=match_token('TK_semicolon',pending_source_code,current_column, current_row)
            pass
            
        pending_source_code,current_column, current_row,_,_=match_token('TK_end',pending_source_code,current_column, current_row)
        return pending_source_code,current_column, current_row
    
    @staticmethod
    def verify_command(pending_source_code:str,current_column:int, current_row:int, symbol_table: SymbolTable) -> Tuple[str,int,int]:
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
            return CommandRulesRecognizer.verify_compound_command_rule(pending_source_code,current_column, current_row,symbol_table)

        if check_token('TK_if',pending_source_code,current_column, current_row):
            return CommandRulesRecognizer.verify_conditional_command_rule(pending_source_code,current_column, current_row,symbol_table)

        if check_token('TK_identifier',pending_source_code,current_column, current_row):
            pending_source_code,current_column, current_row,identifier_token,_=match_token('TK_identifier',pending_source_code,current_column, current_row)            
            # We send identifier token as param, in case it is an assignation command it will help to semantic analizer, if not it will help to check if function is in symbol table
            return CommandRulesRecognizer.verify_command_2_rule(pending_source_code,current_column, current_row,symbol_table,identifier_token)
        
        if check_token('TK_while',pending_source_code,current_column, current_row):
            return CommandRulesRecognizer.verify_repetitive_command_rule(pending_source_code,current_column, current_row,symbol_table)
        
        if check_token('TK_read',pending_source_code,current_column, current_row):
            return ExpresionRulesRecognizer.verify_lecture_command_rule(pending_source_code,current_column,current_row, symbol_table)
        
        if check_token('TK_write',pending_source_code,current_column, current_row):
            return ExpresionRulesRecognizer.verify_write_command_rule(pending_source_code,current_column,current_row,symbol_table)
        
        raise Exception(f"SYNTAX ERROR: Expected to find a token in {['TK_begin', 'TK_if', 'TK_identifier', 'TK_while', 'TK_read', 'TK_write']}, but found other in row {current_row}, column {current_column}: {pending_source_code[0:20]}")

    @staticmethod
    def verify_conditional_command_rule(pending_source_code:str,current_column:int, current_row:int, symbol_table:SymbolTable) -> Tuple[str,int,int]:
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
        # Generate MEPA label to add jump if after end of then statement
        label=ExpresionRulesRecognizer.mepa_writer.generateLabel()
        pending_source_code,current_column, current_row,_,_ = match_token('TK_if',pending_source_code,current_column, current_row)
        pending_source_code,current_column, current_row,_ = ExpresionRulesRecognizer.verify_expresion_rule(pending_source_code,current_column, current_row,symbol_table,"BOOLEAN")
        
        # MEPA: add jump instruction if false
        ExpresionRulesRecognizer.mepa_writer.jz(label)


        pending_source_code,current_column, current_row,_,_ = match_token('TK_then',pending_source_code,current_column, current_row)
        
        pending_source_code,current_column, current_row = CommandRulesRecognizer.verify_command(pending_source_code,current_column, current_row,symbol_table)
        
        success_tk_else = True

        try:
            pending_source_code,current_column, current_row,_,_=match_token('TK_else',pending_source_code,current_column, current_row)
        except SyntaxException:
            success_tk_else= False
        if success_tk_else:
            # MEPA Given there is an else command, we need to know where to jump after else and add
            # Jump if we achieve this mepa line
            after_conditional_label=CommandRulesRecognizer.mepa_writer.generateLabel()
            CommandRulesRecognizer.mepa_writer.jmp(after_conditional_label)

            # MEPA: After then add label line, so if FALSE Jump here
            ExpresionRulesRecognizer.mepa_writer.nop(label)

            pending_source_code,current_column, current_row=CommandRulesRecognizer.verify_command(pending_source_code,current_column, current_row,symbol_table)
            
            # MEPA: after conditional label
            ExpresionRulesRecognizer.mepa_writer.nop(after_conditional_label)
        else:
            # MEPA: After then add label line, so if FALSE Jump here
            ExpresionRulesRecognizer.mepa_writer.nop(label)
            pass
        
        
        return pending_source_code,current_column, current_row

    @staticmethod
    def verify_repetitive_command_rule(pending_source_code:str,current_column:int, current_row:int, symbol_table: SymbolTable) -> Tuple[str,int,int]:
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
        
        while_label=CommandRulesRecognizer.mepa_writer.generateLabel()
        while_end_label=CommandRulesRecognizer.mepa_writer.generateLabel()
        
        # MEPA: Add label to while
        CommandRulesRecognizer.mepa_writer.nop(while_label)
        pending_source_code,current_column,current_row,_,_ = match_token('TK_while',pending_source_code,current_column,current_row)

        pending_source_code,current_column,current_row,_= ExpresionRulesRecognizer.verify_expresion_rule(pending_source_code,current_column,current_row,symbol_table,"BOOLEAN")
        # MEPA: Jump to while end label if expresion is false
        CommandRulesRecognizer.mepa_writer.jz(while_end_label)
        
        pending_source_code,current_column,current_row,_,_ = match_token('TK_do',pending_source_code,current_column,current_row)
        pending_source_code,current_column,current_row = CommandRulesRecognizer.verify_command(pending_source_code,current_column,current_row,symbol_table)
        
        # MEPA: Jump to begin of while loop always
        CommandRulesRecognizer.mepa_writer.jmp(while_label)

        # MEPA: Add End of while loop label line
        CommandRulesRecognizer.mepa_writer.nop(while_end_label)

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
            identifier_symbol,identifier_symbol_level = symbol_table.getSymbol(identifier_signature)
            pending_source_code,current_column,current_row=CommandRulesRecognizer.verify_rest_of_assignation_rule(pending_source_code,current_column,current_row,symbol_table,identifier_symbol,identifier_symbol_level)
        elif success_open_par:
            # IMPORTANT: By design decision, only procedure are callable here
            # Verify if there is at least one procedure with the identifier name
            SemanticErrorAnalyzer.check_exists_any_accesible_procedure_with_name(identifier_token,symbol_table)
            # Get expresion datatypes to see if there is a function with the correct signature, otherwise raise error
            
            pending_source_code,current_column, current_row,parameters_datatypes= ExpresionRulesRecognizer.verify_rest_of_function_call_rule(pending_source_code,current_column,current_row,symbol_table,identifier_token,True)

            # check if procedure is callable
            SemanticErrorAnalyzer.check_procedure_is_callable(identifier_token,parameters_datatypes,symbol_table)
            
            # MEPA: Call procedure
            #procedure_signature=get_signature(identifier_token.getAttribute("name"),parameters_datatypes)
            #procedure_symbol,_= symbol_table.getSymbol(procedure_signature)
            #CommandRulesRecognizer.mepa_writer.call(procedure_symbol.label)

            pass

        return pending_source_code,current_column,current_row

    @staticmethod
    def verify_rest_of_assignation_rule(pending_source_code:str,current_column:int, current_row:int, symbol_table: SymbolTable,first_identifier_symbol: Symbol, first_identifier_level) -> Tuple[str,int,int]:
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
        expected_datatype= first_identifier_symbol.output_type
        identifers_to_be_set=[]
        identifers_to_be_set.append(first_identifier_symbol)
        while check_token('TK_comma',pending_source_code,current_column,current_row):
            pending_source_code, current_column, current_row, _, _ = match_token('TK_comma',pending_source_code,current_column,current_row)
            pending_source_code, current_column, current_row, identifier_token, _ = match_token('TK_identifier',pending_source_code,current_column,current_row)

            # Check identifier is in table an is of the expected datatype
            SemanticErrorAnalyzer.check_var_identifier_is_accesible(identifier_token,symbol_table)
            SemanticErrorAnalyzer.check_var_identifier_is_specific_datatype(identifier_token,symbol_table, expected_datatype)
            identifier_symbol,_= symbol_table.getSymbol(identifier_token.getAttribute("name"))
            identifers_to_be_set.append(identifier_symbol)
            pass
        pending_source_code,current_column,current_row,_,_ = match_token('TK_assignment',pending_source_code,current_column,current_row)
        pending_source_code,current_column,current_row,_=ExpresionRulesRecognizer.verify_expresion_rule(pending_source_code,current_column,current_row, symbol_table,expected_datatype)
        
        #for id_symbol in identifers_to_be_set:
            # Preguntar como asignar una misma expresión a múltiples identificadores
            # MEPA
            # Assignate the same value to all variables

        #    pass

        # Suponiendo que solo tenemos una variable
        # MEPA: Assignation to variable
        CommandRulesRecognizer.mepa_writer.store(first_identifier_level,first_identifier_symbol.offset)
        
        return pending_source_code,current_column,current_row
    
    pass






