from typing_extensions import Self
from app2.syntax_analizer.semantic_analizer import SemanticException
from .symbol import Symbol
# https://ruslanspivak.com/lsbasi-part14/

class SymbolTable:
    def __init__(
        self,
        scope_name: str,
        scope_level:int,
        parent_symbol_table: Self.__class__,
        scope_content: dict(str, Symbol),
        offset: int,
        line: int
    ) -> None:
        """
        Args:
            scope_name(str): FUNCTION | PROCEDURE | PROGRAM name
            scope_level(int): For nested FUNCTION | PROCEDURE (to differenciate them)
            parent_symbol_table(SymbolTable | None ): Pointer to parent table. To know where to look if something is not found here. None for global
            scope_content(dic(str -> Symbol)): Dictionary with all VAR, FUNCTION and PROCEDURE inside this FUNCTION/PROCEDURE as symbols. The key is its name
            offset(int): Counter to add new symbols in the table
        """
        self.scope_name=scope_name
        self.scope_level=scope_level
        self.parent_symbol_table=parent_symbol_table
        self.scope_content=scope_content
        self.offset=offset
        self.line=line
        pass
    
    def addSymbolList(self, symbol_list:list(Symbol)):
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
            raise SemanticException(f"{ symbol_to_add.symbol_name } is already added in Symbol Table {self.scope_name}[{self.scope_level}]")
        symbol_to_add.offset=self.offset
        self.scope_content[symbol_to_add.symbol_name]=symbol_to_add
        self.offset=+1
        pass


    def isInLocalTable(self, symbol_to_add: Symbol)->bool:
        if symbol_to_add.symbol_name == self.scope_name:
            return True
        if symbol_to_add.symbol_name in self.scope_content.keys():
            return True
        return False
    
    pass