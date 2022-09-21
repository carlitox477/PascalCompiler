
from typing import Tuple

from app2.syntax_analizer.semantic_analizer.symbol_table import SymbolTable
from .utils import match_token, report_match_error
from .gr_commands_rules import CommandRulesRecognizer
from .syntax_error_analyzer import SyntaxErrorAnalyzer

class DeclarationRulesRecognizer:
    @staticmethod
    def verify_block_rule(pending_source_code:str,current_column:int, current_row:int, symbol_table: SymbolTable) -> Tuple[str,int,int]:
        """
            Identifies rule: <bloque> ::= [<parte_declaracion_de_variables>] [<parte_declaracion_de_subrutinas>] <comando_compuesto>
            
            Args:
                pending_source_code(str): Pending code to analize. Acts as look ahead
                current_column(int): column where the look ahead is
                current_row(int): row where the look ahead is

            Returns:
                pending_source_code(str): Updated look ahead
                current_column(int): Column where the updated look ahead is
                current_row(int): Row where the updated look ahead is
        """
        pending_source_code,current_column, current_row=DeclarationRulesRecognizer.verify_variables_declaration_part_rule(pending_source_code,current_column, current_row)
        pending_source_code,current_column, current_row=DeclarationRulesRecognizer.verify_subrutine_declaration_part_rule(pending_source_code,current_column, current_row)

        pending_source_code,current_column, current_row=CommandRulesRecognizer.verify_compound_command_rule(pending_source_code,current_column, current_row)
        return pending_source_code,current_column, current_row
    
    @staticmethod
    def verify_variables_declaration_part_rule(pending_source_code:str,current_column:int, current_row:int) -> Tuple[str,int,int]:
        """
            Identifies rule: <parte_declaration_de_variables> ::= var <declaracion_de_variables>; {<declaracion_de_variables>;}
            
            Args:
                pending_source_code(str): Pending code to analize. Acts as look ahead
                current_column(int): column where the look ahead is
                current_row(int): row where the look ahead is

            Returns:
                pending_source_code(str): Updated look ahead
                current_column(int): Column where the updated look ahead is
                current_row(int): Row where the updated look ahead is
        """
        try:
            pending_source_code,current_column, current_row,_,_=match_token('TK_var',pending_source_code,current_column, current_row)
        except Exception:
            # # Assume non var declaration
            return pending_source_code,current_column, current_row

        # At least one line of variables declaration
        pending_source_code,current_column, current_row=DeclarationRulesRecognizer.verify_variables_declaration_rule(pending_source_code,current_column, current_row)    
        pending_source_code,current_column, current_row, _,_= match_token('TK_semicolon',pending_source_code,current_column, current_row)

        success = True
        while success:
            if success:
                try:
                    pending_source_code,current_column, current_row = DeclarationRulesRecognizer.verify_variables_declaration_rule(pending_source_code,current_column, current_row)
                except Exception:
                    success = False
                if success:
                    pending_source_code,current_column, current_row,_,_=match_token('TK_semicolon',pending_source_code,current_column, current_row)
                pass
            pass
        return pending_source_code,current_column, current_row
    
    @staticmethod
    def verify_variables_declaration_rule(pending_source_code:str,current_column:int, current_row:int) -> Tuple[str,int,int]:
        """
            Identifies rule: <declaracion_de_variables> ::= <lista_de_identificadores> : <tipo_de_dato>
            
            Args:
                pending_source_code(str): Pending code to analize. Acts as look ahead
                current_column(int): column where the look ahead is
                current_row(int): row where the look ahead is

            Returns:
                pending_source_code(str): Updated look ahead
                current_column(int): Column where the updated look ahead is
                current_row(int): Row where the updated look ahead is
        """
        # Add semantic here to add variables, accumulate identifiers in a list, then add them to table
        pending_source_code,current_column, current_row=DeclarationRulesRecognizer.verify_identifier_list_rule(pending_source_code,current_column, current_row)
        pending_source_code,current_column, current_row,_,_=match_token('TK_colon',pending_source_code,current_column, current_row)
        pending_source_code,current_column, current_row=DeclarationRulesRecognizer.verify_datatype_rule(pending_source_code,current_column, current_row)
        
        # SEMANTIC
        # Add identifier list to table
        return pending_source_code,current_column, current_row
    
    @staticmethod
    def verify_identifier_list_rule(pending_source_code:str,current_column:int, current_row:int) -> Tuple[str,int,int]:
        """
            Identifies rule: <lista_de_identificadores> ::= <identificador {, <identificador>}
            
            Args:
                pending_source_code(str): Pending code to analize. Acts as look ahead
                current_column(int): column where the look ahead is
                current_row(int): row where the look ahead is

            Returns:
                pending_source_code(str): Updated look ahead
                current_column(int): Column where the updated look ahead is
                current_row(int): Row where the updated look ahead is
        """
        # Return a list of identifiers names
        
        # At least one identifier
        pending_source_code,current_column, current_row, identifier_token,_=match_token('TK_identifier',pending_source_code,current_column, current_row)
        
        success = True
        # More than one identifier
        while success:
            try:
                pending_source_code,current_column, current_row,_,_=match_token('TK_comma',pending_source_code,current_column, current_row)
            except Exception:
                success = False
            if success:
                pending_source_code,current_column, current_row, identifier_token,_=match_token('TK_identifier',pending_source_code,current_column, current_row)
                pass        
            pass
        return pending_source_code,current_column, current_row

    @staticmethod
    def verify_datatype_rule(pending_source_code:str,current_column:int, current_row:int) -> Tuple[str,int,int]:
        """
            Identifies rule: <tipo_de_dato> ::= integer | boolean
            
            Args:
                pending_source_code(str): Pending code to analize. Acts as look ahead
                current_column(int): column where the look ahead is
                current_row(int): row where the look ahead is

            Returns:
                pending_source_code(str): Updated look ahead
                current_column(int): Column where the updated look ahead is
                current_row(int): Row where the updated look ahead is
        """
        pending_source_code,current_column, current_row,_,_=match_token('TK_datatype',pending_source_code,current_column, current_row)    
        return pending_source_code,current_column, current_row

    @staticmethod
    def verify_subrutine_declaration_part_rule(pending_source_code:str,current_column:int, current_row:int) -> Tuple[str,int,int]:
        """
            Identifies rule: <parte_declaracion_de_subrutinas> ::= {<declaracion_de_funcion>; | <declaracion_de_funcion>;}
            
            Args:
                pending_source_code(str): Pending code to analize. Acts as look ahead
                current_column(int): column where the look ahead is
                current_row(int): row where the look ahead is

            Returns:
                pending_source_code(str): Updated look ahead
                current_column(int): Column where the updated look ahead is
                current_row(int): Row where the updated look ahead is
        """
        try:
            match_token('TK_function',pending_source_code,current_column, current_row)
            function_tk_match_success = True
        except Exception:
            function_tk_match_success=False
            

        try:
            match_token('TK_procedure',pending_source_code,current_column, current_row)
            procedure_tk_match_success = True
        except Exception:
            procedure_tk_match_success=False

        while(function_tk_match_success or procedure_tk_match_success):
            if function_tk_match_success:
                pending_source_code,current_column, current_row=DeclarationRulesRecognizer.verify_function_declaration_rule(pending_source_code,current_column, current_row)
            elif procedure_tk_match_success:
                pending_source_code,current_column, current_row=DeclarationRulesRecognizer.verify_procedure_declaration_rule(pending_source_code,current_column, current_row)
            
            pending_source_code,current_column, current_row,_,_=match_token('TK_semicolon',pending_source_code,current_column, current_row)        
            
            try:
                match_token('TK_function',pending_source_code,current_column, current_row)
                function_tk_match_success = True
            except Exception:
                function_tk_match_success=False

            try:
                match_token('TK_procedure',pending_source_code,current_column, current_row)
                procedure_tk_match_success = True
            except Exception:
                procedure_tk_match_success=False
            pass
        return pending_source_code,current_column, current_row

    @staticmethod
    def verify_procedure_declaration_rule(pending_source_code:str,current_column:int,current_row:int) -> Tuple[str,int,int]:
        """
            Identifies rule: <declaracion_de_procedimiento> ::= procedure <identificador>[ "(" <parametros_formales> ")"]; <bloque>
            
            Args:
                pending_source_code(str): Pending code to analize. Acts as look ahead
                current_column(int): column where the look ahead is
                current_row(int): row where the look ahead is

            Returns:
                pending_source_code(str): Updated look ahead
                current_column(int): Column where the updated look ahead is
                current_row(int): Row where the updated look ahead is
        """
        pending_source_code,current_column, current_row,_,_= match_token('TK_procedure',pending_source_code,current_column, current_row)
        pending_source_code,current_column, current_row,identifier_token,_=match_token('TK_identifier',pending_source_code,current_column, current_row)
        
        success = False
        try:
            pending_source_code,current_column, current_row,_,_=match_token('TK_parenthesis',pending_source_code,current_column, current_row,{"type": ['OPPAR']})
            success= True
        finally:
            if(success):
                pending_source_code,current_column, current_row=DeclarationRulesRecognizer.verify_formal_parameters_rule(pending_source_code,current_column, current_row)
                pending_source_code,current_column, current_row,_,_=match_token('TK_parenthesis',pending_source_code,current_column, current_row,{"type": ['CLPAR']})
                pass
            pass

        pending_source_code,current_column, current_row,_,_=match_token('TK_semicolon',pending_source_code,current_column, current_row)
        pending_source_code,current_column, current_row=DeclarationRulesRecognizer.verify_block_rule(pending_source_code,current_column, current_row)
        return pending_source_code,current_column, current_row

    @staticmethod
    def verify_function_declaration_rule(pending_source_code:str,current_column:int,current_row:int) -> Tuple[str,int,int]:
        """
            Identifies rule: <declaracion_de_funcion> ::= function <identificador>[ "(" <parametros_formales> ")"] : <tipo_de_dato> ; <bloque>
            
            Args:
                pending_source_code(str): Pending code to analize. Acts as look ahead
                current_column(int): column where the look ahead is
                current_row(int): row where the look ahead is

            Returns:
                pending_source_code(str): Updated look ahead
                current_column(int): Column where the updated look ahead is
                current_row(int): Row where the updated look ahead is
        """
        
        pending_source_code,current_column, current_row,_,_=match_token('TK_function',pending_source_code,current_column, current_row)
        pending_source_code,current_column, current_row,identifier_token,_=match_token('TK_identifier',pending_source_code,current_column, current_row)
        
        success = False
        try:
            pending_source_code,current_column, current_row,_,_=match_token('TK_parenthesis',pending_source_code,current_column, current_row,{"type": ['OPPAR']})
            success= True
        finally:
            if(success):
                pending_source_code,current_column, current_row=DeclarationRulesRecognizer.verify_formal_parameters_rule(pending_source_code,current_column, current_row)
                pending_source_code,current_column, current_row,_,_=match_token('TK_parenthesis',pending_source_code,current_column, current_row,{"type": ['CLPAR']})
                pass
            pass

        pending_source_code,current_column, current_row,_,_=match_token('TK_colon',pending_source_code,current_column, current_row)
        pending_source_code,current_column, current_row=DeclarationRulesRecognizer.verify_datatype_rule(pending_source_code,current_column, current_row)
        
        pending_source_code,current_column, current_row,_,_=match_token('TK_semicolon',pending_source_code,current_column, current_row)
        pending_source_code,current_column, current_row=DeclarationRulesRecognizer.verify_block_rule(pending_source_code,current_column, current_row)
        return pending_source_code,current_column, current_row

    @staticmethod
    def verify_formal_parameters_rule(pending_source_code:str,current_column:int,current_row:int) -> Tuple[str,int,int]:
        """
            Identifies rule: <parametros_formales> ::= <seccion_declaracion_de_variables> { ; <seccion_declaracion_de_variables> }
            
            Args:
                pending_source_code(str): Pending code to analize. Acts as look ahead
                current_column(int): column where the look ahead is
                current_row(int): row where the look ahead is

            Returns:
                pending_source_code(str): Updated look ahead
                current_column(int): Column where the updated look ahead is
                current_row(int): Row where the updated look ahead is
        """
        pending_source_code,current_column,current_row=DeclarationRulesRecognizer.verify_variables_declaration_section_rule(pending_source_code,current_column,current_row)        
        continue_analysis=True
        while continue_analysis:
            try:
                 pending_source_code,current_column, current_row,_,_=match_token('TK_semicolon',pending_source_code,current_column, current_row)
            except Exception:
                continue_analysis = False

            if continue_analysis:
                pending_source_code,current_column,current_row=DeclarationRulesRecognizer.verify_variables_declaration_section_rule(pending_source_code,current_column,current_row)
                pass        
            pass
        return pending_source_code,current_column,current_row

    @staticmethod
    def verify_variables_declaration_section_rule(pending_source_code:str,current_column:int,current_row:int) -> Tuple[str,int,int]:
        """
            Identifies rule: <seccion_declaracion_de_variables> ::= [ var ] <declaracion_de_variables>
            
            Args:
                pending_source_code(str): Pending code to analize. Acts as look ahead
                current_column(int): column where the look ahead is
                current_row(int): row where the look ahead is

            Returns:
                pending_source_code(str): Updated look ahead
                current_column(int): Column where the updated look ahead is
                current_row(int): Row where the updated look ahead is
        """
        #pending_source_code,current_column,current_row=report_match_error('TK_var',pending_source_code,current_column, current_row)
        pending_source_code,current_column,current_row=DeclarationRulesRecognizer.verify_variables_declaration_rule(pending_source_code,current_column,current_row)
        return pending_source_code,current_column,current_row

    pass
