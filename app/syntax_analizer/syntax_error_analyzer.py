from .lexical_analizer.automatas.token import Token
from .syntax_exception import SyntaxException

class SyntaxErrorAnalyzer:

    @staticmethod
    def verifyExpectedToken(token: Token, expected_token_type: str, expected_attributes, current_row: int, current_column:int):
        if(token.type != expected_token_type):
            raise SyntaxException(f"SYNTAX ERROR: Expected {expected_token_type} at row {current_row}, column {current_column}, instead it is {token.type}")
        elif not(token.verify_attributes_in_lists(expected_attributes)):
            raise SyntaxException(f"SYNTAX ERROR: Expected {token.type} with value in {expected_attributes} at row {current_row}, column {current_column}, instead it is {token.attributes}")        
        pass
    pass