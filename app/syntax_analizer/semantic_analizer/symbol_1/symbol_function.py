
from .symbol import Symbol1

class FunctionSymbol(ProcedureSymbol):
    # symbol_type: VAR | FUNCTION | PROCEDURE
    # symbol_name: name of VAR | FUNCTION | PROCEDURE
    # parameter_list: By default always null, if FUNCTION | PROCEDURE a Symbol list
    # output_type: INTEGER | BOOLEAN if VAR or FUNCTION, otherwise NULL
    # offset: 

    def __init__(self, symbol_name: str, parameter_list: list, output_type: str, label: str, line: int) -> None:
        """
        Args:
            symbol_type(str): VAR | FUNCTION | PROCEDURE | LITERAL
            symbol_name(str): name of identifier | literal value
            parameter_list(list[INTEGER | BOOLEAN]): By default always an empty list, if FUNCTION | PROCEDURE a str list 
            output_type(str): INTEGER | BOOLEAN if VAR, FUNCTION or LITERAL, otherwise NULL
            offset(int): position in symbol table where it is in or parameter list (if symbol in parameter list) | -1 if Literal
            line(int): where the symbol | literal is
        """
        super.__init__(symbol_name,parameter_list,output_type,label,line)
        pass

    def to_string(self)-> str:
        """ Gets summary of the symbol """
        return f"FUNCTION { self.symbol_name }: <RETURNS: {self.output_type}>; <LABEL: { self.offset }>; <PARAMETER_LIST: { self.get_parameter_list_str() }>"
  
    def copy(self):
        return FunctionSymbol(self.symbol_name,self.parameter_list,self.output_type,self.label,self.line)  

    pass