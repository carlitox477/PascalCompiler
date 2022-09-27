
from typing import Tuple

from syntax_analizer.semantic_analizer.symbol import Symbol
from syntax_analizer.syntax_exception import SyntaxException
from .lexical_analizer.automatas.token import Token

from .semantic_analizer.symbol_table import SymbolTable
from .utils import match_token, create_symbol_list_from_identifier_list
from .gr_commands_rules import CommandRulesRecognizer

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
        pending_source_code,current_column, current_row=DeclarationRulesRecognizer.verify_variables_declaration_part_rule(pending_source_code,current_column, current_row,symbol_table)
        pending_source_code,current_column, current_row=DeclarationRulesRecognizer.verify_subrutine_declaration_part_rule(pending_source_code,current_column, current_row,symbol_table)

        pending_source_code,current_column, current_row=CommandRulesRecognizer.verify_compound_command_rule(pending_source_code,current_column, current_row,symbol_table)
        return pending_source_code,current_column, current_row
    
    @staticmethod
    def verify_variables_declaration_part_rule(pending_source_code:str,current_column:int, current_row:int,symbol_table: SymbolTable) -> Tuple[str,int,int]:
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
        except SyntaxException:
            # # Assume non var declaration
            return pending_source_code,current_column, current_row

        # At least one line of variables declaration
        pending_source_code,current_column, current_row,_=DeclarationRulesRecognizer.verify_variables_declaration_rule(pending_source_code,current_column, current_row,symbol_table)    
        pending_source_code,current_column, current_row, _,_= match_token('TK_semicolon',pending_source_code,current_column, current_row)

        success = True
        while success:
            if success:
                try:
                    pending_source_code,current_column, current_row, _ = DeclarationRulesRecognizer.verify_variables_declaration_rule(pending_source_code,current_column, current_row,symbol_table)
                except SyntaxException:
                    success = False
                if success:
                    pending_source_code,current_column, current_row,_,_=match_token('TK_semicolon',pending_source_code,current_column, current_row)
                pass
            pass
        return pending_source_code,current_column, current_row
    
    @staticmethod
    def verify_variables_declaration_rule(pending_source_code:str,current_column:int, current_row:int,symbol_table: SymbolTable) -> Tuple[str,int,int,list]:
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
        
        pending_source_code,current_column, current_row, identifier_token_list=DeclarationRulesRecognizer.verify_identifier_list_rule(pending_source_code,current_column, current_row)
        
        pending_source_code,current_column, current_row,_,_=match_token('TK_colon',pending_source_code,current_column, current_row)
        pending_source_code,current_column, current_row,datatype_token=DeclarationRulesRecognizer.verify_datatype_rule(pending_source_code,current_column, current_row)
        
        # SEMANTIC
        # Add identifier list to table
        symbols_to_add=create_symbol_list_from_identifier_list(identifier_token_list,datatype_token)
        
        symbol_table.addSymbolList(symbols_to_add)
        return pending_source_code,current_column, current_row,symbols_to_add
    
    @staticmethod
    def verify_identifier_list_rule(pending_source_code:str,current_column:int, current_row:int) -> Tuple[str,int,int,list]:
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
        identifier_token_list=[]
        # At least one identifier
        pending_source_code,current_column, current_row, identifier_token,_=match_token('TK_identifier',pending_source_code,current_column, current_row)
        
        identifier_token_list.append(identifier_token)

        success = True
        # More than one identifier
        while success:
            try:
                pending_source_code,current_column, current_row,_,_=match_token('TK_comma',pending_source_code,current_column, current_row,None,True)
            except SyntaxException:
                success = False
            if success:
                pending_source_code,current_column, current_row, identifier_token,_=match_token('TK_identifier',pending_source_code,current_column, current_row)
                identifier_token_list.append(identifier_token)
                pass        
            pass
        return pending_source_code,current_column, current_row,identifier_token_list

    @staticmethod
    def verify_datatype_rule(pending_source_code:str,current_column:int, current_row:int) -> Tuple[str,int,int,Token]:
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
        pending_source_code,current_column, current_row,datatype_token,_=match_token('TK_datatype',pending_source_code,current_column, current_row)    
        return pending_source_code,current_column, current_row,datatype_token

    @staticmethod
    def verify_subrutine_declaration_part_rule(pending_source_code:str,current_column:int, current_row:int,symbol_table: SymbolTable) -> Tuple[str,int,int]:
        """
            Identifies rule: <parte_declaracion_de_subrutinas> ::= {<declaracion_de_funcion>; | <declaracion_de_procedimiento>;}
            
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
        except SyntaxException:
            function_tk_match_success=False
            

        try:
            match_token('TK_procedure',pending_source_code,current_column, current_row)
            procedure_tk_match_success = True
        except SyntaxException:
            procedure_tk_match_success=False

        while(function_tk_match_success or procedure_tk_match_success):
            if function_tk_match_success:
                pending_source_code,current_column, current_row=DeclarationRulesRecognizer.verify_function_declaration_rule(pending_source_code,current_column, current_row,symbol_table)
            elif procedure_tk_match_success:
                pending_source_code,current_column, current_row=DeclarationRulesRecognizer.verify_procedure_declaration_rule(pending_source_code,current_column, current_row,symbol_table)
            
            pending_source_code,current_column, current_row,_,_=match_token('TK_semicolon',pending_source_code,current_column, current_row)        
            
            try:
                match_token('TK_function',pending_source_code,current_column, current_row)
                function_tk_match_success = True
            except SyntaxException:
                function_tk_match_success=False

            try:
                match_token('TK_procedure',pending_source_code,current_column, current_row)
                procedure_tk_match_success = True
            except SyntaxException:
                procedure_tk_match_success=False
            pass
        return pending_source_code,current_column, current_row

    @staticmethod
    def verify_procedure_declaration_rule(pending_source_code:str,current_column:int,current_row:int,symbol_table: SymbolTable) -> Tuple[str,int,int]:
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
        
        # Add procedure to parent table
        #  parameter_list will be define later
        # output is none due to the fact that it is a procedure
        # offset will be define later
        procedure_symbol=Symbol("PROCEDURE", identifier_token.getAttribute("name"),[],None,0,identifier_token.row)

        # Create procedure table
        procedure_symbol_table = SymbolTable(identifier_token.getAttribute("name"),"PROCEDURE",symbol_table.scope_level+1,symbol_table,{},0,identifier_token.row)


        success = False
        parameters_symbols=[]
        try:
            pending_source_code,current_column, current_row,_,_=match_token('TK_parenthesis',pending_source_code,current_column, current_row,{"type": ['OPPAR']})
            success= True
        except SyntaxException:
            pass

        if(success):
            pending_source_code,current_column, current_row,parameters_symbols=DeclarationRulesRecognizer.verify_formal_parameters_rule(pending_source_code,current_column, current_row,procedure_symbol_table)
            pending_source_code,current_column, current_row,_,_=match_token('TK_parenthesis',pending_source_code,current_column, current_row,{"type": ['CLPAR']})
            procedure_symbol.add_parameters(parameters_symbols)
            pass

        
        symbol_table.addSymbol(procedure_symbol)

        pending_source_code,current_column, current_row,_,_=match_token('TK_semicolon',pending_source_code,current_column, current_row)
        pending_source_code,current_column, current_row=DeclarationRulesRecognizer.verify_block_rule(pending_source_code,current_column, current_row, procedure_symbol_table)
        
        #print("---------------------")
        #print(procedure_symbol_table.to_string())
        return pending_source_code,current_column, current_row

    @staticmethod
    def verify_function_declaration_rule(pending_source_code:str,current_column:int,current_row:int,symbol_table: SymbolTable) -> Tuple[str,int,int]:
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
        # Create function table
        function_symbol_table = SymbolTable(identifier_token.getAttribute("name"),"FUNCTION",symbol_table.scope_level+1,symbol_table,{},0,identifier_token.row)

        success = False
        try:
            pending_source_code,current_column, current_row,_,_=match_token('TK_parenthesis',pending_source_code,current_column, current_row,{"type": ['OPPAR']}, True)
            success= True
        except SyntaxException:
            pass
        
        parameters_symbols=[]
        if(success):
            pending_source_code,current_column, current_row,parameters_symbols=DeclarationRulesRecognizer.verify_formal_parameters_rule(pending_source_code,current_column, current_row,function_symbol_table)
            pending_source_code,current_column, current_row,_,_=match_token('TK_parenthesis',pending_source_code,current_column, current_row,{"type": ['CLPAR']})
            pass
        pending_source_code,current_column, current_row,_,_=match_token('TK_colon',pending_source_code,current_column, current_row)
        pending_source_code,current_column, current_row, datatype_token=DeclarationRulesRecognizer.verify_datatype_rule(pending_source_code,current_column, current_row)
        
        # Function symbol to add goes here
        #  parameter_list will be define later
        # output is none due to the fact that it is a procedure
        # offset will be define later
        function_symbol=Symbol("FUNCTION", identifier_token.getAttribute("name"),[],None,0,identifier_token.row)
        function_symbol.add_parameters(parameters_symbols)
        function_symbol.output_type=datatype_token.getAttribute("name")
        
        symbol_table.addSymbol(function_symbol)
        # Add function name as var
        #print(function_symbol_table.to_string())
        function_symbol_table.addSymbol(Symbol("VAR",identifier_token.getAttribute("name"),[],function_symbol.output_type,0,function_symbol.line))
        
        #print("---------------------")
        #print(function_symbol_table.to_string())
        #print("---------------------")
        #print(symbol_table.to_string())

        pending_source_code,current_column, current_row,_,_=match_token('TK_semicolon',pending_source_code,current_column, current_row)
        
        pending_source_code,current_column, current_row=DeclarationRulesRecognizer.verify_block_rule(pending_source_code,current_column, current_row, function_symbol_table)
        return pending_source_code,current_column, current_row

    @staticmethod
    def verify_formal_parameters_rule(pending_source_code:str,current_column:int,current_row:int,symbol_table: SymbolTable) -> Tuple[str,int,int,list]:
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
        pending_source_code,current_column,current_row,variable_symbol_list=DeclarationRulesRecognizer.verify_variables_declaration_section_rule(pending_source_code,current_column,current_row,symbol_table)        
        continue_analysis=True
        while continue_analysis:
            try:
                 pending_source_code,current_column, current_row,_,_=match_token('TK_semicolon',pending_source_code,current_column, current_row)
            except SyntaxException:
                continue_analysis = False

            if continue_analysis:
                pending_source_code,current_column,current_row,more_variable_symbol_list=DeclarationRulesRecognizer.verify_variables_declaration_section_rule(pending_source_code,current_column,current_row,symbol_table)
                variable_symbol_list.extend(more_variable_symbol_list)
                pass        
            pass
        return pending_source_code,current_column,current_row,variable_symbol_list

    @staticmethod
    def verify_variables_declaration_section_rule(pending_source_code:str,current_column:int,current_row:int,symbol_table: SymbolTable) -> Tuple[str,int,int,list]:
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
        # Optional
        pending_source_code,current_column,current_row,_,_=match_token('TK_var',pending_source_code,current_column, current_row, [], False)
        pending_source_code,current_column,current_row, variables_symbols=DeclarationRulesRecognizer.verify_variables_declaration_rule(pending_source_code,current_column,current_row,symbol_table)
        return pending_source_code,current_column,current_row,variables_symbols
        

    pass
