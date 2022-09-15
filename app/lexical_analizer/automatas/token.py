
class Token:
    def __init__(self, type: str, row: int, column: int, attributes: dict) -> None:
        self.type = type
        self.column = column
        self.row = row
        self.attributes = attributes
        pass
    
    def getAttribute(self, attribute_name: str):
        if self.attributes == None:
            return None
        return self.attributes.get(attribute_name, None)
    pass
