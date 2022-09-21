class Symbol:
    # symbol_type: VAR | FUNCTION | PROCEDURE
    # symbol_name: name of VAR | FUNCTION | PROCEDURE
    # parameter_list: By default always null, if FUNCTION | PROCEDURE a Symbol list
    # output_type: INTEGER | BOOLEAN if VAR or FUNCTION, otherwise NULL
    # offset: 

    def __init__(self,symbol_type: str, symbol_name: str, parameter_list: list, output_type: str, offset: int, line: int) -> None:
        """
        Args:
            symbol_type(str): VAR | FUNCTION | PROCEDURE
            symbol_name(str): name of identifier
            parameter_list(list[Symbol]): By default always null, if FUNCTION | PROCEDURE a Symbol list 
            output_type(str): INTEGER | BOOLEAN if VAR or FUNCTION, otherwise NULL
            offset(int): position in symbol table where it is in or parameter list (if symbol in parameter list)
        """
        self.symbol_type = symbol_type
        self.symbol_name = symbol_name
        self.parameter_list = parameter_list
        self.output_type = output_type
        self.offset = offset
        self.line = line
        pass
    
    def getNumberOfParameters(self) -> int:
        """ Gets lenght of parameter_list list """
        return len(self.parameter_list)
    
    def getSummary(self)-> str:
        """ Gets summary of the symbol """
        return f"{ self.symbol_type } { self.symbol_name }: <RETURNS: {self.output_type}>; <OFFSET: { self.offset }>"
    
    def getParametersSummary(self):
        if(self.parameter_list == None or len(self.parameter_list)==0):
            return 
        
        parameter_list=""
        for symbol in self.parameter_list:
            parameter_list = parameter_list + symbol.toString() + "; "
            pass
        parameter_list=parameter_list[:-2]
        return f"<PARAMETER_LIST: [{ parameter_list }]>"
    
    def toString(self)->str:
        """ Gets all the information of the symbol """
        summary = self.getSummary()
        if(self.symbol_type == "VAR"):
            return f"{ summary }"
        return f"{ summary }; {self.getParametersSummary()}"
    
    pass