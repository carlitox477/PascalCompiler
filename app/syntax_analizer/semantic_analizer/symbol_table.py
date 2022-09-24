from typing_extensions import Self
from .semantic_exception import SemanticException
from .symbol import Symbol
# https://ruslanspivak.com/lsbasi-part14/

class SymbolTable:
    def __init__(
        self,
        scope_name: str,
        scope_type:str,
        scope_level:int,
        parent_symbol_table: Self.__class__,
        scope_content: dict,
        offset: int,
        line: int
    ) -> None:
        """
        Args:
            scope_name(str): FUNCTION | PROCEDURE | PROGRAM name
            scope_type(str): FUNCTION | PROCEDURE | PROGRAM
            scope_level(int): For nested FUNCTION | PROCEDURE (to differenciate them)
            parent_symbol_table(SymbolTable | None ): Pointer to parent table. To know where to look if something is not found here. None for global
            scope_content(dic(str -> Symbol)): Dictionary with all VAR, FUNCTION and PROCEDURE inside this FUNCTION/PROCEDURE as symbols. The key is its name
            offset(int): Counter to add new symbols in the table
            line: Where the function scope is?
        """
        self.scope_name=scope_name
        self.scope_type=scope_type
        self.scope_level=scope_level
        self.parent_symbol_table=parent_symbol_table
        self.scope_content=scope_content
        self.offset=offset
        self.line=line
        pass
    
    def addSymbolList(self, symbol_list:list):
        for symbol in symbol_list:
            self.addSymbol(symbol)
            pass
        pass
    
    def getSymbol(self, symbol_name: str)->Symbol:
        symbol= self.scope_content[symbol_name]
        if(symbol != None):
            return symbol
        if(self.parent_symbol_table != None):
            return self.parent_symbol_table.getSymbol()
        return None
    
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

    def isInLocalTable(self, symbol_to_add: Symbol)->bool:
        if symbol_to_add.symbol_name == self.scope_name:
            if(self.scope_type in ["FUNCTION", "PROGRAM"]):
                return True
        # if function or procedure check there isn't a var with the same name
        if(symbol_to_add.symbol_type in ["FUNCTION", "PROCEDURE"]):
            for symbol in self.scope_content.values():
                if (symbol.symbol_type=="VAR"):
                    if(symbol.symbol_name == symbol_to_add.symbol_name):
                        return True
                    pass
                pass
            pass
        elif(symbol_to_add.symbol_type in ["VAR"]):  # Same for var
            for symbol in self.scope_content.values():
                if (symbol.symbol_type in ["FUNCTION", "PROCEDURE"]):
                    if(symbol.symbol_name == symbol_to_add.symbol_name):
                        return True
                    pass
                pass
            pass



        if(symbol_to_add.get_signature() in self.scope_content.keys()):
            return True        
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

    pass