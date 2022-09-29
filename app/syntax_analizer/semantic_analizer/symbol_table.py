from typing_extensions import Self
from .semantic_exception import SemanticException
from .symbol import Symbol
# https://ruslanspivak.com/lsbasi-part14/


class SymbolTable:
    label_number=0
    def __init__(
        self,
        scope_name: str,
        scope_type:str,
        scope_level:int,
        parent_symbol_table: Self.__class__,
        scope_content: dict,
        offset: int,
        line: int,
        paramters_types=[]
    ) -> None:
        """
        Args:
            scope_name(str): FUNCTION | PROCEDURE | PROGRAM name
            scope_type(str): FUNCTION | PROCEDURE | PROGRAM
            scope_level(int): For nested FUNCTION | PROCEDURE (to differenciate them)
            parent_symbol_table(SymbolTable | None ): Pointer to parent table. To know where to look if something is not found here. None for global
            scope_content(dic(str -> Symbol)): Dictionary with all VAR, FUNCTION and PROCEDURE inside this FUNCTION/PROCEDURE as symbols. The key is its name
            offset(int): Counter to add new symbols in the table
            line: Where the function scope is
            paramters_types(list[str]): 
        """
        self.scope_name=scope_name
        self.scope_type=scope_type
        self.scope_level=scope_level
        self.parent_symbol_table=parent_symbol_table
        self.scope_content=scope_content
        self.offset=offset
        self.line=line
        self.label_number=SymbolTable.label_number
        self.paramters_types=[]
        #self.output_type= None
        #if scope_type=="FUNCTION":
        #    self.scope_content[scope_name]=Symbol("VAR",scope_name,[],output_type,offset,line)
        #    self.offset=1
        #    pass
        SymbolTable.label_number = SymbolTable.label_number + 1
        pass
    
    def get_parameter_list_str(self) -> str:
        parameter_list_str=""
        if(self.paramters_types== None or len(self.paramters_types)==0):
            return parameter_list_str
        for parameter_type in self.paramters_types:
            parameter_list_str = parameter_list_str + parameter_type + ", "
            pass
        return parameter_list_str[:-2]

    def addSymbolList(self, symbol_list:list):
        for symbol in symbol_list:
            self.addSymbol(symbol)
            pass
        pass
    
    def getSymbol(self, symbol_signature: str):
        # Return symbol and scope_level
        symbol= self.scope_content.get(symbol_signature,None)
        if(symbol != None):
            return symbol, self.scope_level
        if(self.parent_symbol_table != None):
            return self.parent_symbol_table.getSymbol(symbol_signature)
        return None,-1
    
    def addSymbol(self, symbol_to_add:Symbol):
        if self.isInLocalTable(symbol_to_add):
            symbol_name=symbol_to_add.symbol_name
            scope_name=self.scope_name
            scope_level= self.scope_level
            line = symbol_to_add.line
            raise SemanticException(f"{ symbol_name } in line {line} is already added in Symbol Table {scope_name}[{scope_level}]")
        symbol_to_add.offset=self.offset
        
        self.scope_content[symbol_to_add.get_signature()]=symbol_to_add
        self.offset=self.offset+1
        pass
    
    def add_parameters(self,parameters:list):
        index = 0
        for symbol in parameters:
            symbol.offset= -(2+(len(parameters)-index))
            index = index + 1
            self.scope_content[symbol.get_signature()]=symbol
        pass

    def add_recursion_call(self, self_symbol:Symbol):
        # Allows to add access to the function or procedure itself to allow recursion
        self_symbol_copy=self_symbol.copy()
        self_symbol_copy.offset=-2
        self.scope_content[self_symbol_copy.get_signature()]=self_symbol_copy
        self.paramters_types=self_symbol.parameter_list.copy()
        pass

    def isInLocalTable(self, symbol_to_add: Symbol)->bool:
        if symbol_to_add.symbol_name == self.scope_name:
            if(self.scope_type == "PROGRAM"):
                return True
            elif(self.scope_content.get(self.scope_name,None)!= None):
                # Every time a function is declered we should allow to add it in local table
                return True
            else:
                return False

        if(self.scope_content.get(symbol_to_add.get_signature(),None) != None):
            return True

        # if function or procedure check there isn't a var with the same name
        if(symbol_to_add.symbol_type in ["FUNCTION", "PROCEDURE"]):
            for symbol in self.scope_content.values():
                if(symbol.symbol_name == symbol_to_add.symbol_name and symbol.symbol_type=="VAR"):
                    return True
                pass
            pass
        elif(symbol_to_add.symbol_type == "VAR"):  # Same for var
            for symbol in self.scope_content.values():
                if (symbol.symbol_type in ["FUNCTION", "PROCEDURE"]):
                    if(symbol.symbol_name == symbol_to_add.symbol_name):
                        return True
                    pass
                pass
            pass

         
        return False

    def get_all_symbols(self):
        
        return list(self.scope_content.values())
    
    def to_string(self):
        name = f"SYMBOL TABLE {self.scope_name}[{self.scope_level}]"
        type = f"Type: {self.scope_type}"
        parent_table_value= "None"
        
        if self.parent_symbol_table!= None:
            parent_table_value= f"{self.parent_symbol_table.scope_type} {self.parent_symbol_table.scope_name}[{self.parent_symbol_table.scope_level}]"
            pass


        parent_table = f"Parent table: {parent_table_value}"
        line = f"Line: {self.line}"
        content = "Content: "


        for symbol in self.scope_content.values():
            content= content + "\n" +"\t" + symbol.to_string()
        if (content=="Content: "):
            content = f"{content}None"
        content = f"{content}\n"
        return f"{name}\n{type}\n{parent_table}\n{line}\n{content}"


    def exists_any_accesible_procedure(self,function_name:str):
        for symbol in self.scope_content.values():
            if(symbol.symbol_name==function_name):
                if(symbol.symbol_type== "PROCEDURE"):
                    return True
                elif(symbol.symbol_type== "VAR"):
                    # VAR overshadow function and procedure with same name
                    return False
                pass
            pass
        
        parent_table = self.parent_symbol_table
        response = False
        while parent_table!= None and not(response):
            response=parent_table.exists_any_accesible_procedure(function_name)
            parent_table=parent_table.parent_symbol_table
            pass
        return response

    def exists_any_accesible_function(self,function_name:str):
        for symbol in self.scope_content.values():
            if(symbol.symbol_name==function_name):
                if(symbol.symbol_type== "FUNCTION"):
                    return True
                elif(symbol.symbol_type== "VAR"):
                    # VAR overshadow function and procedure with same name
                    return False
                pass
            pass
        
        parent_table = self.parent_symbol_table
        response = False
        while parent_table!= None and not(response):
            response=parent_table.exists_any_accesible_function(function_name)
            parent_table=parent_table.parent_symbol_table
            pass
        return response

    def add_return_slot(self,return_symbol: Symbol):
        return_symbol.offset=-1
        self.scope_content[return_symbol.get_signature()]=return_symbol
        pass
    
    def get_label(self):
        return f"l{self.label_number}_{self.scope_name}({self.get_parameter_list_str()})[{self.scope_level}]"
    pass