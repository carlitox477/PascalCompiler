from abc import abstractclassmethod
from .symbol import Symbol1

class Symbol1:
    # symbol_name: name of VAR | FUNCTION | PROCEDURE
    # output_type: INTEGER | BOOLEAN if VAR or FUNCTION, otherwise NONE
    # line: where the VAR | FUNCTION | PROCEDURE is declared  

    def __init__(self, symbol_name: str, output_type: str, line: int) -> None:
        """
        Args:
            symbol_type(str): VAR | FUNCTION | PROCEDURE | LITERAL
            symbol_name(str): name of identifier | literal value
            parameter_list(list[INTEGER | BOOLEAN]): By default always an empty list, if FUNCTION | PROCEDURE a str list 
            output_type(str): INTEGER | BOOLEAN if VAR, FUNCTION or LITERAL, otherwise NULL
            offset(int): position in symbol table where it is in or parameter list (if symbol in parameter list) | -1 if Literal
            line(int): where the symbol | literal is
        """
        self.symbol_name = symbol_name
        self.output_type = output_type
        self.line = line
        pass

    def get_signature(self)->str:
        """Get unique identifier for insertion in Symbol Table"""
        pass

    def copy(self) -> Symbol1:
        pass
    
    def to_string(self)->str:
        pass

    def equal(self,symbol: Symbol1):
        """ This function is specially useful for function/procedure overload"""
        if self.symbol_name != symbol.symbol_name:
            return False
        if self.symbol_type != symbol.symbol_type:
            return False

        return self.get_signature() == symbol.get_signature()
    
    def isVar() -> bool:
        return False
    
    def isFunction() -> bool:
        return False

    def isProcedure() -> bool:
        return False
    
    pass