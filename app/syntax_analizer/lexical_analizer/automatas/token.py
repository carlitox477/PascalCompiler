class Token:
    def __init__(self, type: str, row: int, column: int, attributes: dict) -> None:
        self.type = type
        self.column = column
        self.row = row
        self.attributes = attributes
        pass
    
    def getAttribute(self, attribute_name: str):
        """Get attribute value. If attribute does not exists, it return None

        Args:
            - attribute_name(str): attribute to found

        Returns:
            - attribute_value
        """
        if self.attributes == None:
            return None
        return self.attributes.get(attribute_name, None)
    
    def verify_attributes_in_lists(self, attributes: dict) -> bool:
        if(attributes== None):
            return True 
        
        keys=attributes.keys()

        for k in keys:
            try:
                attribute_value=self.attributes[k]
                if not (attribute_value in attributes[k]):
                    return False
            except Exception:
                return False
            pass
        return True 

    def verify_attributes(self, attributes: dict) -> bool:
        if(attributes!= None):
            return True 
        pass

    def to_string(self):
        type= self.type
        row= self.row
        column = self.column
        attributes = ""
        for k in self.attributes.keys():
            attributes=attributes+f"{k}: {self.attributes[k]}; "
        attributes=attributes[:-2]
        output=f"{type}(r:{row}, c:{column})"
        if(len(attributes)>0):
            output=output+": <"+ attributes+">"
        
        return output
    pass
