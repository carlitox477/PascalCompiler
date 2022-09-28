from typing import Tuple
from .utils import get_signature
from .lexical_analizer.automatas.token import Token
from .semantic_analizer.semantic_exception import SemanticException
from .semantic_error_analizer import SemanticErrorAnalyzer

from .semantic_analizer.symbol_table import SymbolTable
from .utils import check_token, match_token
from .syntax_exception import SyntaxException


class ExpresionRulesRecognizer:
    @staticmethod
    def verify_identifier_list_rule(pending_source_code: str, current_column: int, current_row: int, symbol_table: SymbolTable) -> Tuple[str,int,int]:
        # Done
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
        
        # At list one identifier
        # Try to find <identificador>, which can only be a VAR
        pending_source_code,current_column, current_row,identifier_token,_= match_token('TK_identifier',pending_source_code,current_column, current_row,None,True)
        # Check identifier are in symbol table, these identifier can only be VAR
        SemanticErrorAnalyzer.check_var_identifier_is_accesible(identifier_token,symbol_table)

        while identifier_token != None:
            
            try:
                pending_source_code,current_column, current_row,_, _= match_token('TK_comma',pending_source_code,current_column, current_row, None, True)
            except SyntaxException:
                identifier_token = None
            if identifier_token != None:
                pending_source_code,current_column, current_row,identifier_token, _= match_token('TK_identifier',pending_source_code,current_column, current_row, None, True)
                SemanticErrorAnalyzer.check_var_identifier_is_accesible(identifier_token,symbol_table)
            pass
        return pending_source_code,current_column, current_row

    @staticmethod
    def verify_write_command_rule(pending_source_code:str,current_column:int, current_row:int, symbol_table: SymbolTable) -> Tuple[str,int,int]:
        """
        Identifies rule: <comando_salida> ::= write(<lista_de_expresiones>)
            
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

        pending_source_code,current_column,current_row,_=ExpresionRulesRecognizer.verify_expresion_list_rule(pending_source_code,current_column,current_row,symbol_table)
        
        pending_source_code,current_column,current_row,_,_ = match_token('TK_parenthesis',pending_source_code,current_column,current_row,{"type": ['CLPAR']})
        return pending_source_code,current_column,current_row

    @staticmethod
    def verify_lecture_command_rule(pending_source_code:str,current_column:int, current_row:int, symbol_table: SymbolTable) -> Tuple[str,int,int]:
        # Done
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
        pending_source_code,current_column,current_row=ExpresionRulesRecognizer.verify_identifier_list_rule(pending_source_code,current_column,current_row,symbol_table)
        pending_source_code,current_column,current_row,_,_=match_token('TK_parenthesis',pending_source_code,current_column,current_row,{"type": ['CLPAR']})
        return pending_source_code,current_column,current_row

    @staticmethod
    def verify_expresion_rule(pending_source_code:str,current_column:int, current_row:int, symbol_table: SymbolTable, expected_type=None) -> Tuple[str,int,int]:
        # DONE
        """
        Identifies rule: <expresion> ::= <expresion_simple> {<operador_relacional> <expresion_simple> }
            
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
        #try:
        #    pending_source_code,current_column, current_row,literal_token,_=match_token('TK_boolean_literal',pending_source_code,current_column, current_row)
        #    # Check if it gets expected datatype
        #    SemanticErrorAnalyzer.check_correct_literal_datatype("BOOLEAN",literal_token.row,literal_token.column,expected_type)

        #    return pending_source_code,current_column, current_row,literal_token,"BOOLEAN"
        #except SyntaxException:
        #    pass
        
        # Tries to find <expresion_simple>
        first_expected_type=None
        if(expected_type=="INTEGER"):
            first_expected_type="INTEGER"
        
        pending_source_code,current_column, current_row,first_expresion_datatype=ExpresionRulesRecognizer.verify_simple_expresion_rule(pending_source_code,current_column, current_row,symbol_table,first_expected_type)

        perfom_relation_operation= check_token('TK_relOp',pending_source_code,current_column, current_row)
        if(perfom_relation_operation):
            output_type="BOOLEAN"
            previous_type=first_expresion_datatype
            while perfom_relation_operation:            
                pending_source_code,current_column, current_row,relop_token,_=match_token('TK_relOp',pending_source_code,current_column, current_row)
                SemanticErrorAnalyzer.check_expresion_relational_operator_error(relop_token, expected_type,previous_type)
                
                pending_source_code,current_column, current_row,next_datatype=ExpresionRulesRecognizer.verify_simple_expresion_rule(pending_source_code,current_column, current_row,first_expresion_datatype)
                #pending_source_code,current_column, current_row,second_expresion_datatype=ExpresionRulesRecognizer.verify_simple_expresion_rule(pending_source_code,current_column, current_row,first_expresion_datatype)
                # SemanticErrorAnalyzer.check_comparison_datatypes(first_expresion_datatype,second_expresion_datatype, relop_token)
                previous_type= next_datatype
                perfom_relation_operation= check_token('TK_relOp',pending_source_code,current_column, current_row)
                pass
        elif(expected_type=="BOOLEAN" and first_expresion_datatype!="BOOLEAN"):
            raise SemanticException(f"SEMANTIC ERROR: Expected BOOLEAN expresion in line {current_row}")
        else:
            output_type=first_expresion_datatype
        return pending_source_code,current_column, current_row,output_type

    @staticmethod
    def verify_simple_expresion_rule(pending_source_code:str,current_column:int, current_row:int, symbol_table: SymbolTable,expected_datatype=None) -> Tuple[str,int,int]:
        # DONE
        """
        Identifies rule: <expresion_simple> ::= [ + | - ] <termino> { ( + | - | or ) <termino> }
            
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
            pending_source_code,current_column, current_row,arithmetical_operation_token,_ = match_token('TK_arithOp',pending_source_code,current_column, current_row,{"operation":['ADD', 'SUB']})
            SemanticErrorAnalyzer.check_correct_math_operation(expected_datatype,arithmetical_operation_token)
        except SyntaxException:
            # Ignore if mismatch
            pass
        from_row=current_row
        from_col=current_column
        pending_source_code,current_column, current_row,first_term_datatype=ExpresionRulesRecognizer.verify_term_rule(pending_source_code,current_column, current_row,symbol_table,expected_datatype)
        
        # Boolean with boolean, integer with integer
        if(expected_datatype != None and expected_datatype!=first_term_datatype):
            raise SemanticException(f"SEMANTIC ERROR: Expected term type {expected_datatype}, but it is {first_term_datatype} in (r:{from_row},c:{from_col})-(r:{current_row},c:{current_column})")

        success_valid_tk_arith_op=check_token('TK_arithOp',pending_source_code,current_column, current_row,{"operation":['ADD', 'SUB']})
        success_tk_or=check_token('TK_or',pending_source_code,current_column, current_row)


        while(success_valid_tk_arith_op or success_tk_or):
            if(success_valid_tk_arith_op):
                pending_source_code,current_column, current_row,operation_token,_=match_token('TK_arithOp',pending_source_code,current_column, current_row,{"operation":['ADD', 'SUB']})
                
                SemanticErrorAnalyzer.check_correct_math_operation(first_term_datatype,operation_token)
            else:
                pending_source_code,current_column, current_row,operation_token,_=match_token('TK_or',pending_source_code,current_column, current_row)
                
                SemanticErrorAnalyzer.check_correct_boolean_operation(first_term_datatype,operation_token)
            
            from_row=current_row
            from_col=current_column
            pending_source_code,current_column, current_row, term_datatype=ExpresionRulesRecognizer.verify_term_rule(pending_source_code,current_column, current_row,symbol_table)
            #print(pending_source_code)
            if(term_datatype != first_term_datatype):
                raise SemanticException(f"SEMANTIC ERROR: Expected term type {first_term_datatype}, but it is {term_datatype} in (r:{from_row},c:{from_col})-(r:{current_row},c:{current_column})")
            #print(pending_source_code)
            success_valid_tk_arith_op=check_token('TK_arithOp',pending_source_code,current_column, current_row,{"operation":['ADD', 'SUB']})
            success_tk_or=check_token('TK_or',pending_source_code,current_column, current_row)
            
            pass
        #print("-------------------")
        #print(pending_source_code)
        return pending_source_code,current_column, current_row, first_term_datatype

    @staticmethod
    def verify_term_rule(pending_source_code:str,current_column:int, current_row:int, symbol_table: SymbolTable, expected_datatype=None) -> Tuple[str,int,int]:
        # DONE
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
        from_row,from_col=current_row,current_column
        #print(symbol_table.to_string())
        pending_source_code,current_column, current_row,first_factor_datatype=ExpresionRulesRecognizer.verify_factor_rule(pending_source_code,current_column, current_row,symbol_table)
        if(expected_datatype!= None and expected_datatype!=first_factor_datatype):
            raise SemanticException(f"SEMANTIC ERROR: Expected factor type {expected_datatype}, but it is {first_factor_datatype} in (r:{from_row},c:{from_col})-(r:{current_row},c:{current_column})")
        
        success_valid_tk_arith_op=check_token('TK_arithOp',pending_source_code,current_column, current_row,{"operation":['MUL', 'DIV']})
        success_tk_and=check_token('TK_and',pending_source_code,current_column, current_row)
        
        
        while success_valid_tk_arith_op or success_tk_and:
            if success_valid_tk_arith_op:
                pending_source_code,current_column, current_row,operation_token,_=match_token('TK_arithOp',pending_source_code,current_column, current_row,{"operation":['MUL', 'DIV']})
                SemanticErrorAnalyzer.check_correct_math_operation(first_factor_datatype,operation_token)
            else:
                pending_source_code,current_column, current_row,operation_token,_=match_token('TK_and',pending_source_code,current_column, current_row)
                SemanticErrorAnalyzer.check_correct_boolean_operation(first_factor_datatype,operation_token)

            from_row,from_col=current_row,current_column
            
            pending_source_code,current_column, current_row, factor_type=ExpresionRulesRecognizer.verify_factor_rule(pending_source_code,current_column, current_row,symbol_table)        
            if(first_factor_datatype != factor_type):
                raise SemanticException(f"SEMANTIC ERROR: Expected term type {first_factor_datatype}, but it is {factor_type} in (r:{from_row},c:{from_col})-(r:{current_row},c:{current_column})")
            
            success_valid_tk_arith_op=check_token('TK_arithOp',pending_source_code,current_column, current_row,{"operation":['MUL', 'DIV']})
            success_tk_and=check_token('TK_and',pending_source_code,current_column, current_row)
            pass
        return pending_source_code,current_column, current_row,first_factor_datatype

    @staticmethod
    def verify_factor_rule(pending_source_code:str,current_column:int, current_row:int, symbol_table: SymbolTable,expected_datatype=None) -> Tuple[str,int,int]:
        """
        Identifies rule: <factor> ::= <literal_booleano> | <identificador> | <numero> | <llamada_funcion> | NOT <factor> | "(" <expresion> ")" | <
            
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

        valid_first_tokens=['TK_identifier', 'TK_number','TK_not', 'TK_parenthesis']
        
        # <literal_booleano>
        try:
            #print(pending_source_code)
            pending_source_code,current_column, current_row,literal_token,_=match_token('TK_boolean_literal',pending_source_code,current_column, current_row)
            # Check if it gets expected datatype
            SemanticErrorAnalyzer.check_correct_literal_datatype("BOOLEAN",literal_token.row,literal_token.column,expected_datatype)
            return pending_source_code,current_column, current_row, "BOOLEAN"
        except SyntaxException:
            pass

        # <identificador> | <llamada_funcion>
        try:
            pending_source_code,current_column, current_row,identifier_token,_=match_token('TK_identifier',pending_source_code,current_column, current_row)
            success_tk_identifier = True
        except SyntaxException:
            success_tk_identifier = False
        
        # Check if it is <llamada_funcion>, otherwise just return
        if success_tk_identifier:
            try:
                _,_,_,_,_ = match_token('TK_parenthesis',pending_source_code,current_column, current_row,{"type": ['OPPAR']})
                success_open_par = True
            except SyntaxException:
                success_open_par = False
                #Check identifier is in table


            if success_open_par:
                # Function
                pending_source_code,current_column, current_row,parameters_datatypes=ExpresionRulesRecognizer.verify_rest_of_function_call_rule(pending_source_code,current_column, current_row,symbol_table, identifier_token)
                SemanticErrorAnalyzer.check_function_or_procedure_is_accesible(identifier_token,parameters_datatypes,symbol_table)
                function_signature= get_signature(identifier_token.getAttribute("name"),parameters_datatypes)
                #print(function_signature)
                output_datatype=symbol_table.getSymbol(function_signature).output_type
                if(output_datatype==None):       
                    raise SemanticException(f"{function_signature} in line {identifier_token.row} column {identifier_token.column} is accessed as a PROCEDURE, and it must be a FUNCTION")
                pass
            else:
                # Look identifier datatype in symbol table
                SemanticErrorAnalyzer.check_var_identifier_is_accesible(identifier_token,symbol_table)
                var_signature= identifier_token.getAttribute("name")
                output_datatype=symbol_table.getSymbol(var_signature).output_type
                pass
            
            if(expected_datatype!= None and expected_datatype!=output_datatype):
                if(success_open_par):
                    raise SemanticException(f"SEMANTIC ERROR: {function_signature} function at line {identifier_token.row}, column {identifier_token.column} returns {output_datatype}, expected {expected_datatype}")
                else:
                    raise SemanticException(f"SEMANTIC ERROR: {var_signature} var at line {identifier_token.row}, column {identifier_token.column} returns {output_datatype}, expected {expected_datatype}")
                pass
            return pending_source_code,current_column, current_row,output_datatype

        # <numero>
        success_tk_number = True
        try: 
            pending_source_code,current_column, current_row,number_token,_=match_token('TK_number',pending_source_code,current_column, current_row)
            if(expected_datatype!= None and expected_datatype!="INTEGER"):
                number_value=number_token.getAttribute("value")
                raise SemanticException(f"SEMANTIC ERROR: {number_value} literal INTEGER found at line {identifier_token.row}, column {identifier_token.column}, expected BOOLEAN")        
        except SyntaxException:
            success_tk_number = False
        if success_tk_number:
            return pending_source_code,current_column, current_row,"INTEGER"
        
        # not <factor>
        success_tk_not=True
        try:
            pending_source_code,current_column, current_row,_,_=match_token('TK_not',pending_source_code,current_column, current_row)
        except SyntaxException:
            success_tk_not = False 
            pass
        if success_tk_not:
            pending_source_code,current_column, current_row,_=ExpresionRulesRecognizer.verify_factor_rule(pending_source_code,current_column, current_row,symbol_table,"BOOLEAN")
            return pending_source_code,current_column, current_row,"BOOLEAN"

        # (<expresion>)
        success_open_par= True
        try:
            pending_source_code,current_column, current_row,_,_=match_token('TK_parenthesis',pending_source_code,current_column, current_row,{"type": ['OPPAR']})
        except SyntaxException:
            success_open_par = False
        if success_open_par:
            
            pending_source_code,current_column, current_row,expresion_type=ExpresionRulesRecognizer.verify_expresion_rule(pending_source_code,current_column, current_row,symbol_table,expected_datatype)
            pending_source_code,current_column, current_row,_,_=match_token('TK_parenthesis',pending_source_code,current_column, current_row,{"type": ['CLPAR']})
            return pending_source_code,current_column, current_row,expresion_type
        raise SyntaxException(f"SYNTAX ERROR: Expected to find a token in {valid_first_tokens}, but found other in row {current_row}, column {current_column}")

    @staticmethod
    def verify_expresion_list_rule(pending_source_code:str,current_column:int, current_row:int, symbol_table: SymbolTable) -> Tuple[str,int,int]:
        # DONE
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
        datatype_list=[]
        pending_source_code,current_column, current_row,expression_datatype=ExpresionRulesRecognizer.verify_simple_expresion_rule(pending_source_code,current_column, current_row,symbol_table)
        datatype_list.append(expression_datatype)

        success_comma = True
        while success_comma:
            #print(success_comma)
            try:
                pending_source_code,current_column, current_row,_,_=match_token('TK_comma',pending_source_code,current_column, current_row)
            except SyntaxException:
                success_comma = False
                pass
            if success_comma:
                pending_source_code,current_column, current_row,expression_datatype=ExpresionRulesRecognizer.verify_simple_expresion_rule(pending_source_code,current_column, current_row,symbol_table)
                datatype_list.append(expression_datatype)
            pass
        return pending_source_code,current_column, current_row,datatype_list

    @staticmethod
    def verify_rest_of_function_call_rule(pending_source_code:str,current_column:int, current_row:int,symbol_table: SymbolTable, function_identifier_token: Token, is_procedure=False) -> Tuple[str,int,int]:
        # Done
        """
        Identifies rule: <resto_llamada_funcion> ::= "(" <lista_de_expresiones> ")"
            
            Args:
                pending_source_code(str): Pending code to analize. Acts as look ahead
                current_column(int): column where the look ahead is
                current_row(int): row where the look ahead is

            Returns:
                pending_source_code(str): Updated look ahead
                current_column(int): Column where the updated look ahead is
                current_row(int): Row where the updated look ahead is
        """
        pending_source_code,current_column, current_row,_,_ = match_token('TK_parenthesis',pending_source_code,current_column, current_row,{"type": ['OPPAR']})
        pending_source_code,current_column, current_row,expresions_datatypes = ExpresionRulesRecognizer.verify_expresion_list_rule(pending_source_code,current_column, current_row,symbol_table)
        pending_source_code,current_column, current_row,_,_ = match_token('TK_parenthesis',pending_source_code,current_column, current_row,{"type": ['CLPAR']})
        
        # Check function is accesible from table
        if(not(is_procedure)):
            SemanticErrorAnalyzer.check_function_is_callable(function_identifier_token,expresions_datatypes, symbol_table)
        else:
            SemanticErrorAnalyzer.check_procedure_is_callable(function_identifier_token,expresions_datatypes, symbol_table)
        return pending_source_code,current_column, current_row,expresions_datatypes

    pass
