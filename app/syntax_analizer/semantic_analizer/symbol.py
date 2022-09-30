#from .symbol import Symbol

class Symbol:
    # symbol_type: VAR | FUNCTION | PROCEDURE
    # symbol_name: name of VAR | FUNCTION | PROCEDURE
    # parameter_list: By default always null, if FUNCTION | PROCEDURE a Symbol list
    # output_type: INTEGER | BOOLEAN if VAR or FUNCTION, otherwise NULL
    # offset: 

    def __init__(self,symbol_type: str, symbol_name: str, parameter_list: list, output_type: str, offset: int, line: int) -> None:
        """
        Args:
            symbol_type(str): VAR | FUNCTION | PROCEDURE | LITERAL
            symbol_name(str): name of identifier | literal value
            parameter_list(list[INTEGER | BOOLEAN]): By default always an empty list, if FUNCTION | PROCEDURE a str list 
            output_type(str): INTEGER | BOOLEAN if VAR, FUNCTION or LITERAL, otherwise NULL
            offset(int): position in symbol table where it is in or parameter list (if symbol in parameter list) | -1 if Literal
            line(int): where the symbol | literal is
        """
        self.symbol_type = symbol_type
        self.symbol_name = symbol_name
        self.parameter_list = parameter_list
        self.output_type = output_type
        self.offset = offset
        self.line = line
        self.label = ""
        pass

    def get_signature(self):
        if(self.symbol_type=="VAR"):
            return f"{self.symbol_name}"
        if(self.parameter_list== None or len(self.parameter_list)==0):
            signature = f"{self.symbol_name}()"
            return signature

        parameter_list_str=""
        for parameter_type in self.parameter_list:
            parameter_list_str = parameter_list_str + parameter_type + ","
            pass
        return f"{self.symbol_name}({parameter_list_str[:-1]})"
    
    def get_number_of_parameters(self) -> int:
        """ Gets lenght of parameter_list list """
        return len(self.parameter_list)
    
    def get_summary(self)-> str:
        """ Gets summary of the symbol """
        if(self.symbol_type=="VAR"):
            return f"{ self.symbol_type } { self.symbol_name }: <RETURNS: {self.output_type}>; <OFFSET: { self.offset }>"
        else:
            return f"{ self.symbol_type } { self.symbol_name }: <RETURNS: {self.output_type}>; <LABEL: { self.label }>"
    

    def get_parameters_summary(self):
        if(self.parameter_list == None or len(self.parameter_list)==0):
            return ""
        
        parameter_list_str=""
        for parameter_type in self.parameter_list:
            parameter_list_str = parameter_list_str + parameter_type + ", "
            pass
        parameter_list_str=parameter_list_str[:-2] # Erase las ", "
        return f"<PARAMETER_LIST: [{ parameter_list_str }]>"
    
    def to_string(self)->str:
        """ Gets all the information of the symbol """
        summary = self.get_summary()
        if(self.symbol_type == "VAR"):
            return f"{ summary }"
        return f"{ summary }; {self.get_parameters_summary()}"

    def add_parameters(self,parameters:list):
        for symbol in parameters:
            self.parameter_list.append(symbol.output_type)
        pass

    def equal(self,symbol):
        """ This function is specially useful for function/procedure overload"""
        

        if self.symbol_name != symbol.symbol_name:
            return False
        if self.symbol_type != symbol.symbol_type:
            return False

        #has_no_parameters= self.parameter_list == None or len(self.parameter_list)== 0
        #symbol_has_no_parameter = symbol.parameter_list == None or len(symbol.parameter_list)== 0

        #if(has_no_parameters and symbol_has_no_parameter):
        #    return False
        try:
            if(len(self.parameter_list) != len(symbol.parameter_list)):
                return False
        except Exception:
            raise Exception(f"{self.to_string()}")

        # compare parameter types in order, they should be the same type to be equal
        for i in range(0, len(symbol.parameter_list)):
            if(symbol.parameter_list[i] != self.parameter_list[i]):
                return False
            pass
        return True

    def copy(self):
        return Symbol(self.symbol_type,self.symbol_name,self.parameter_list,self.output_type,self.offset,self.line)
        pass


    pass