
from .semantic_analizer.symbol_table import SymbolTable
from .lexical_analizer.automatas.token import Token
from .semantic_analizer.semantic_exception import SemanticException
from .utils import get_signature

class SemanticErrorAnalyzer:
    @staticmethod
    def check_var_identifier_is_accesible(var_identifier_token: Token, symbol_table: SymbolTable):
        identifer_name=var_identifier_token.getAttribute("name")
        if(symbol_table.getSymbol(identifer_name)==None):
            raise SemanticException(f"SEMANTIC ERROR: {identifer_name}[VAR] in line {var_identifier_token.row} column {var_identifier_token.column} was never declared")
        pass
    
    @staticmethod
    def check_var_identifier_is_specific_datatype(var_identifier_token: Token, symbol_table: SymbolTable, datatype: str):
        if(datatype != None):
            identifer_name=var_identifier_token.getAttribute("name")
            if(symbol_table.getSymbol(symbol_table.getSymbol(identifer_name)).output_type!=datatype):
                raise SemanticException(f"SEMANTIC ERROR: {identifer_name}[VAR] in line {var_identifier_token.row} column {var_identifier_token.column} should be {datatype} according to previous identifier declaration in list")
            pass   
        pass
    
    @staticmethod
    def check_exists_any_accesible_procedure_with_name(procedure_identifier_token: Token, symbol_table: SymbolTable):
        procedure_name= procedure_identifier_token.getAttribute("name")
        if(not(symbol_table.exists_any_accesible_procedure(procedure_name))):
            raise SemanticException(f"SEMANTIC ERROR: {procedure_name} procedure in line {procedure_identifier_token.row} column {procedure_identifier_token.column} was never decleared or it is inaccesible")
        pass


    @staticmethod
    def check_procedure_is_callable(procedure_identifier_token: Token,parameters_datatypes:list, symbol_table: SymbolTable):
        procedure_name= procedure_identifier_token.getAttribute("name")
        procedure_signature = get_signature(procedure_name,parameters_datatypes)
        assumed_procedure_symbol=symbol_table.getSymbol(procedure_signature)
        if(assumed_procedure_symbol == None):
            raise SemanticException(f"SEMANTIC ERROR: {procedure_signature} procedure in line {procedure_identifier_token.row} column {procedure_identifier_token.column} was never decleared or it is inaccesible")

        if(assumed_procedure_symbol.output_type!=None):
            raise SemanticException(f"SEMANTIC ERROR: {procedure_signature} in line {procedure_identifier_token.row} column {procedure_identifier_token.column} should be a procedure, but it is a function")
        pass
    
    @staticmethod
    def check_function_is_callable(function_identifier_token: Token,parameters_datatypes:list, symbol_table: SymbolTable):
        function_name= function_identifier_token.getAttribute("name")
        function_signature =get_signature(function_name,parameters_datatypes)
        #print(function_signature)
        assumed_function_symbol=symbol_table.getSymbol(function_signature)
        if(assumed_function_symbol == None):
            raise SemanticException(f"SEMANTIC ERROR: {function_signature} function in line {function_identifier_token.row} column {function_identifier_token.column} was never decleared or it is inaccesible")

        if(assumed_function_symbol.output_type==None):
            raise SemanticException(f"SEMANTIC ERROR: {function_signature} in line {function_identifier_token.row} column {function_identifier_token.column} should be a function, but it is a procedure")
        pass
    

    @staticmethod
    def check_function_or_procedure_is_accesible(function_identifier_token: Token,parameters_datatypes:list, symbol_table: SymbolTable):
        function_name= function_identifier_token.getAttribute("name")
        datatypes_str=""
        for datatype in parameters_datatypes:
            datatypes_str=datatypes_str+f"{datatype},"
            pass
        if(len(datatypes_str)>0):
            # Case function has non parameters
            datatypes_str=datatypes_str[:-1]
        signature=f"{function_name}({datatypes_str})"
        

        if(symbol_table.getSymbol(signature)==None):
            raise SemanticException(f"SEMANTIC ERROR: {signature} function in line {function_identifier_token.row} column {function_identifier_token.column} is not accesible or does not exist")   
        pass

    def check_correct_literal_datatype(datatype:str, row: int, column: int,expected_datatype):
        if(expected_datatype!=None):
            if(datatype!=expected_datatype):
                raise SemanticException(f"SEMATIC ERROR: {datatype} literal found in {row} line, column {column}. It should have been {expected_datatype}")
            pass
        pass

    def check_expresion_relational_operator_error(relop_token: Token,expected_output_type:str, next_expected_type:str):
        operation_name=relop_token.getAttribute("operation")
        if(expected_output_type=="INTEGER"):
            raise SemanticException(f"SEMANTIC ERROR: Expected type of expresion in line {relop_token.row} is {expected_output_type}, but you are trying to execute operation with a BOOLEAN result due to perform {operation_name}")
        elif(next_expected_type=="BOOLEAN" and not(operation_name in ["EQ","DIF"])):
            raise SemanticException(f"SEMANTIC ERROR: A relational operation {operation_name} is not poossible with a BOOLEAN expresion in line {relop_token.row}")
        pass

    def check_comparison_datatypes(first_datatype:str, second_datatype: str, relational_operatrion_token:Token):
        if(first_datatype != second_datatype):
            operation_name=relational_operatrion_token.getAttribute("operation")
            raise SemanticException(f"SEMANTIC ERROR: Trying to perform an invalid relational operation {operation_name} between datatypes {first_datatype} and {second_datatype} in line {relational_operatrion_token.row}")
        pass

    def check_correct_boolean_operation(expected_output:str, operation_token:Token):
        operation_name = operation_token.getAttribute("operation")
        #print(operation_name)
        if(expected_output != "BOOLEAN" and operation_name == None):
            operation_name="AND"
            if(operation_token.type=="TK_or"):
                operation_name="OR"
            raise SemanticException(f"SEMANTIC ERROR: Trying to perform an invalid arithmetical operation {operation_name} when you expect a {expected_output} expresion in line {operation_token.row}")
        pass


    def check_correct_math_operation(expected_next_output:str, operation_token:Token):
        operation_name = operation_token.getAttribute("operation")
        if(operation_name!= None and operation_name in ["ADD","SUB","MUL","DIV"] and expected_next_output=="BOOLEAN"):
            raise SemanticException(f"SEMANTIC ERROR: Trying to perform an invalid arithmetical operation {operation_name} when you expect a {expected_next_output} expresion in line {operation_token.row}")
        pass
    

    pass