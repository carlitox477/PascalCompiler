from typing import Tuple
from .utils import check_token, match_token, isTokenInList
from .syntax_exception import SyntaxException


class ExpresionRulesRecognizer:
    @staticmethod
    def verify_identifier_list_rule(pending_source_code: str, current_column: int, current_row: int) -> Tuple[str,int,int]:
        """
            Identifies rule: <lista_de_identificadores> ::= <identificador> {, <identificador>}
            
            Args:
                pending_source_code(str): Pending code to analize. Acts as look ahead
                current_column(int): column where the look ahead is
                current_row(int): row where the look ahead is

            Returns:
                pending_source_code(str): Updated look ahead
                current_column(int): Column where the updated look ahead is
                current_row(int): Row where the updated look ahead is
        """
        # Return identifier types
        # At list one identifier
        # Tries to find <identificador> 
        pending_source_code,current_column, current_row,identifier_token,_= match_token('TK_identifier',pending_source_code,current_column, current_row,None,True)
        
        while identifier_token != None:
            try:
                pending_source_code,current_column, current_row,_, _= match_token('TK_comma',pending_source_code,current_column, current_row, None, True)
            except SyntaxException:
                identifier_token = None
            if identifier_token != None:
                pending_source_code,current_column, current_row,identifier_token, _= match_token('TK_identifier',pending_source_code,current_column, current_row, None, True)
            pass
        return pending_source_code,current_column, current_row

    @staticmethod
    def verify_write_command_rule(pending_source_code:str,current_column:int, current_row:int) -> Tuple[str,int,int]:
        """
        Identifies rule: <comando_salida> ::= write(<expresion_simple>)
            
            Args:
                pending_source_code(str): Pending code to analize. Acts as look ahead
                current_column(int): column where the look ahead is
                current_row(int): row where the look ahead is

            Returns:
                pending_source_code(str): Updated look ahead
                current_column(int): Column where the updated look ahead is
                current_row(int): Row where the updated look ahead is
        """
        pending_source_code,current_column,current_row,_,_ = match_token('TK_write',pending_source_code,current_column,current_row)
        pending_source_code,current_column,current_row,_,_ = match_token('TK_parenthesis',pending_source_code,current_column,current_row,{"type": ['OPPAR']})

        pending_source_code,current_column,current_row=ExpresionRulesRecognizer.verify_simple_expresion_rule(pending_source_code,current_column,current_row)
        
        pending_source_code,current_column,current_row,_,_ = match_token('TK_parenthesis',pending_source_code,current_column,current_row,{"type": ['CLPAR']})
        return pending_source_code,current_column,current_row

    @staticmethod
    def verify_lecture_command_rule(pending_source_code:str,current_column:int, current_row:int) -> Tuple[str,int,int]:
        """
        Identifies rule: <comando_lectura> ::= read(<expresion_simple>)
            
            Args:
                pending_source_code(str): Pending code to analize. Acts as look ahead
                current_column(int): column where the look ahead is
                current_row(int): row where the look ahead is

            Returns:
                pending_source_code(str): Updated look ahead
                current_column(int): Column where the updated look ahead is
                current_row(int): Row where the updated look ahead is
        """
        
        pending_source_code,current_column,current_row,_,_ = match_token('TK_read',pending_source_code,current_column,current_row)
        pending_source_code,current_column,current_row,_,_=match_token('TK_parenthesis',pending_source_code,current_column,current_row,{"type": ['OPPAR']})
        pending_source_code,current_column,current_row=ExpresionRulesRecognizer.verify_identifier_list_rule(pending_source_code,current_column,current_row)
        pending_source_code,current_column,current_row,_,_=match_token('TK_parenthesis',pending_source_code,current_column,current_row,{"type": ['CLPAR']})
        return pending_source_code,current_column,current_row

    @staticmethod
    def verify_expresion_rule(pending_source_code:str,current_column:int, current_row:int) -> Tuple[str,int,int]:
        """
        Identifies rule: <expresion> ::= <literal_booleano> | <expresion_simple> {<operador_relacional> <expresion_simple> }
            
            Args:
                pending_source_code(str): Pending code to analize. Acts as look ahead
                current_column(int): column where the look ahead is
                current_row(int): row where the look ahead is

            Returns:
                pending_source_code(str): Updated look ahead
                current_column(int): Column where the updated look ahead is
                current_row(int): Row where the updated look ahead is
        """
        # literal_booleano means that the expresion type is zero
        # Both expresion_simple should be the same type
        # If first expresion_simple is boolean only == and <> are valid

        # Tries to find <literal_booleano>
        try:
            pending_source_code,current_column, current_row,_,_=match_token('TK_boolean_literal',pending_source_code,current_column, current_row)
            return pending_source_code,current_column, current_row
        except SyntaxException:
            pass
        
        # Tries to find <expresion_simple>
        pending_source_code,current_column, current_row=ExpresionRulesRecognizer.verify_simple_expresion_rule(pending_source_code,current_column, current_row)

        while check_token('TK_relOp',pending_source_code,current_column, current_row):
            pending_source_code,current_column, current_row,_,_=match_token('TK_relOp',pending_source_code,current_column, current_row)
            pending_source_code,current_column, current_row=ExpresionRulesRecognizer.verify_simple_expresion_rule(pending_source_code,current_column, current_row)
            pass
        return pending_source_code,current_column, current_row

    @staticmethod
    def verify_simple_expresion_rule(pending_source_code:str,current_column:int, current_row:int) -> Tuple[str,int,int]:
        """
        Identifies rule: <expresion_simple> ::= [ + | - ] | <termino> { ( + | - | or ) <termino> }
            
            Args:
                pending_source_code(str): Pending code to analize. Acts as look ahead
                current_column(int): column where the look ahead is
                current_row(int): row where the look ahead is

            Returns:
                pending_source_code(str): Updated look ahead
                current_column(int): Column where the updated look ahead is
                current_row(int): Row where the updated look ahead is
        """
        # If [+|-] are found, both termino must be integer type and "or" is not allowed
        # If [+|-] are not found and first <termino> is boolean, or is the only option, and secondo <termino> must be boolean
        try:
            pending_source_code,current_column, current_row,_,_ = match_token('TK_arithOp',pending_source_code,current_column, current_row,{"operation":['ADD', 'SUB']})
        except SyntaxException:
            # Ignore if mismatch
            pass
        pending_source_code,current_column, current_row=ExpresionRulesRecognizer.verify_term_rule(pending_source_code,current_column, current_row)
        
        success_valid_tk_arith_op=check_token('TK_arithOp',pending_source_code,current_column, current_row,{"operation":['ADD', 'SUB']})
        success_tk_or=check_token('TK_or',pending_source_code,current_column, current_row)
        
        while(success_valid_tk_arith_op or success_tk_or):
            if(success_valid_tk_arith_op):
                pending_source_code,current_column, current_row,_,_=match_token('TK_arithOp',pending_source_code,current_column, current_row,{"operation":['ADD', 'SUB']})
            else:
                pending_source_code,current_column, current_row,_,_=match_token('TK_or',pending_source_code,current_column, current_row)
            pending_source_code,current_column, current_row=ExpresionRulesRecognizer.verify_term_rule(pending_source_code,current_column, current_row)
            
            success_valid_tk_arith_op=check_token('TK_arithOp',pending_source_code,current_column, current_row,{"operation":['ADD', 'SUB']})
            success_tk_or=check_token('TK_or',pending_source_code,current_column, current_row)
            pass
        return pending_source_code,current_column, current_row

    @staticmethod
    def verify_term_rule(pending_source_code:str,current_column:int, current_row:int) -> Tuple[str,int,int]:
        """
        Identifies rule: <termino> ::= <factor> { ( * | / | and ) <factor> }
            
            Args:
                pending_source_code(str): Pending code to analize. Acts as look ahead
                current_column(int): column where the look ahead is
                current_row(int): row where the look ahead is

            Returns:
                pending_source_code(str): Updated look ahead
                current_column(int): Column where the updated look ahead is
                current_row(int): Row where the updated look ahead is
        """

        # First factor type determines if we want an "and" or not, and second factor type
        
        pending_source_code,current_column, current_row=ExpresionRulesRecognizer.verify_factor_rule(pending_source_code,current_column, current_row)
        success_valid_tk_arith_op=check_token('TK_arithOp',pending_source_code,current_column, current_row,{"operation":['MUL', 'DIV']})
        success_tk_and=check_token('TK_and',pending_source_code,current_column, current_row)
        
        
        while success_valid_tk_arith_op or success_tk_and:
            if success_valid_tk_arith_op:
                pending_source_code,current_column, current_row,_,_=match_token('TK_arithOp',pending_source_code,current_column, current_row,{"operation":['MUL', 'DIV']})
            else:
                pending_source_code,current_column, current_row,_,_=match_token('TK_and',pending_source_code,current_column, current_row)
            pending_source_code,current_column, current_row=ExpresionRulesRecognizer.verify_factor_rule(pending_source_code,current_column, current_row)        
            success_valid_tk_arith_op=check_token('TK_arithOp',pending_source_code,current_column, current_row,{"operation":['MUL', 'DIV']})
            success_tk_and=check_token('TK_and',pending_source_code,current_column, current_row)
            pass
        return pending_source_code,current_column, current_row

    @staticmethod
    def verify_factor_rule(pending_source_code:str,current_column:int, current_row:int) -> Tuple[str,int,int]:
        """
        Identifies rule: <factor> ::= <identificador> | <numero> | <llamada_funcion> | NOT <factor> | "(" <expresion> ")"
            
            Args:
                pending_source_code(str): Pending code to analize. Acts as look ahead
                current_column(int): column where the look ahead is
                current_row(int): row where the look ahead is

            Returns:
                pending_source_code(str): Updated look ahead
                current_column(int): Column where the updated look ahead is
                current_row(int): Row where the updated look ahead is
        """
        # Just identifier = Look identifier in symbol table
        # Just number = integer type
        # Just function call = get parameters send type and look for function in table, return it type
        # Not factor = factor type must be boolean
        # expresion = return its type

        valid_first_tokens=['TK_identifier', 'TK_number','TK_not_literal', 'TK_parenthesis']
        
        # <identificador> | <llamada_funcion>
        success_tk_identifier = True
        success_open_par = True
        try:
            pending_source_code,current_column, current_row,_,_=match_token('TK_identifier',pending_source_code,current_column, current_row)
        except SyntaxException:
            success_tk_identifier = False
        
        # Check if it is <llamada_funcion>, otherwise just return
        if success_tk_identifier:
            try:
                _,_,_,_,_ = match_token('TK_parenthesis',pending_source_code,current_column, current_row,{"type": ['OPPAR']})
            except SyntaxException:
                success_open_par = False
            if success_open_par:
                pending_source_code,current_column, current_row=ExpresionRulesRecognizer.verify_rest_of_function_call_rule(pending_source_code,current_column, current_row)
                pass
            return pending_source_code,current_column, current_row

        # <numero>
        success_tk_number = True
        try: 
            pending_source_code,current_column, current_row,_,_=match_token('TK_number',pending_source_code,current_column, current_row)
        except SyntaxException:
            success_tk_number = False
        if success_tk_number:
            return pending_source_code,current_column, current_row
        
        # not <factor>
        success_tk_not=True
        try:
            pending_source_code,current_column, current_row,_,_=match_token('TK_not',pending_source_code,current_column, current_row)
        except SyntaxException:
            success_tk_not = False 
            pass
        if success_tk_not:
            pending_source_code,current_column, current_row=ExpresionRulesRecognizer.verify_factor_rule(pending_source_code,current_column, current_row)
            return pending_source_code,current_column, current_row

        # (<expresion>)
        success_open_par= True
        try:
            pending_source_code,current_column, current_row,_,_=match_token('TK_parenthesis',pending_source_code,current_column, current_row,{"type": ['OPPAR']})
        except SyntaxException:
            success_open_par = False
        if success_open_par:
            pending_source_code,current_column, current_row=ExpresionRulesRecognizer.verify_expresion_rule(pending_source_code,current_column, current_row)
            pending_source_code,current_column, current_row,_,_=match_token('TK_parenthesis',pending_source_code,current_column, current_row,{"type": ['CLPAR']})
            return pending_source_code,current_column, current_row
        raise SyntaxException(f"SYNTAX ERROR: Expected to find a token in {valid_first_tokens}, but found other in row {current_row}, column {current_column}")

    @staticmethod
    def verify_expresion_list_rule(pending_source_code:str,current_column:int, current_row:int) -> Tuple[str,int,int]:
        """
        Identifies rule: <lista_de_expresiones> ::= <expresion_simple> { , <expresion_simple> }
            
            Args:
                pending_source_code(str): Pending code to analize. Acts as look ahead
                current_column(int): column where the look ahead is
                current_row(int): row where the look ahead is

            Returns:
                pending_source_code(str): Updated look ahead
                current_column(int): Column where the updated look ahead is
                current_row(int): Row where the updated look ahead is
        """
        # Return list of expresion types
        
        pending_source_code,current_column, current_row=ExpresionRulesRecognizer.verify_simple_expresion_rule(pending_source_code,current_column, current_row)
        
        success_comma = True
        while success_comma:
            try:
                pending_source_code,current_column, current_row,_,_=match_token('TK_comma',pending_source_code,current_column, current_row)
            except SyntaxException:
                success_comma = False
                pass
            if success_comma:
                pending_source_code,current_column, current_row=ExpresionRulesRecognizer.verify_simple_expresion_rule(pending_source_code,current_column, current_row)
            pass
        return pending_source_code,current_column, current_row

    @staticmethod
    def verify_rest_of_function_call_rule(pending_source_code:str,current_column:int, current_row:int) -> Tuple[str,int,int]:
        """
        Identifies rule: <resto_llamada_funcion> ::= [ "(" <lista_de_expresiones> ")" ]
            
            Args:
                pending_source_code(str): Pending code to analize. Acts as look ahead
                current_column(int): column where the look ahead is
                current_row(int): row where the look ahead is

            Returns:
                pending_source_code(str): Updated look ahead
                current_column(int): Column where the updated look ahead is
                current_row(int): Row where the updated look ahead is
        """
        # Check correct function call
        # Compare parameter type sent
        pending_source_code,current_column, current_row,_,_ = match_token('TK_parenthesis',pending_source_code,current_column, current_row,{"type": ['OPPAR']})
        pending_source_code,current_column, current_row = ExpresionRulesRecognizer.verify_expresion_list_rule(pending_source_code,current_column, current_row)
        pending_source_code,current_column, current_row,_,_ = match_token('TK_parenthesis',pending_source_code,current_column, current_row,{"type": ['CLPAR']})
        return pending_source_code,current_column, current_row

    pass
