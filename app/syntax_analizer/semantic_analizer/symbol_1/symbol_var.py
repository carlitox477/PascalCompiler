#from .symbol import Symbol

from .symbol import Symbol1


class VarSymbol(Symbol1):
    # symbol_type: VAR | FUNCTION | PROCEDURE
    # symbol_name: name of VAR | FUNCTION | PROCEDURE
    # parameter_list: By default always null, if FUNCTION | PROCEDURE a Symbol list
    # output_type: INTEGER | BOOLEAN if VAR or FUNCTION, otherwise NULL
    # offset: 

    def __init__(self,symbol_name: str, output_type: str, offset: int, line: int) -> None:
        """
        Args:
            symbol_type(str): VAR | FUNCTION | PROCEDURE | LITERAL
            symbol_name(str): name of identifier | literal value
            parameter_list(list[INTEGER | BOOLEAN]): By default always an empty list, if FUNCTION | PROCEDURE a str list 
            output_type(str): INTEGER | BOOLEAN if VAR, FUNCTION or LITERAL, otherwise NULL
            offset(int): position in symbol table where it is in or parameter list (if symbol in parameter list) | -1 if Literal
            line(int): where the symbol | literal is
        """
        super.__init__(symbol_name,output_type,line)
        self.offset= offset
        pass

    def get_signature(self):
        return f"{self.symbol_name}"
    
    def to_string(self)->str:
        """ Gets all the information of the symbol """
        return f"VAR { self.symbol_name }: <RETURNS: {self.output_type}>; <OFFSET: { self.offset }>"

    def copy(self):
        return VarSymbol(self.symbol_name,self.output_type,self.offset,self.line)

    def isVar() -> bool:
        return True

    pass