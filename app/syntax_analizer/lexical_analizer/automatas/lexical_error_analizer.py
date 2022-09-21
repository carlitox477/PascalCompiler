from .utils import LETTERS, ALPHABET
from .lexical_exception import LexicalException

class LexicalErrorAnalizer:
    
    @staticmethod
    def raise_no_closed_comment_exception(character: str, row: int, col: int):
        """
            Raise lexical error due to unclosed comments
        """
        raise LexicalException(f"LEXICAL ERROR: Comment opened in line {row}, column {col} was never closed")
            
        pass
    
    @staticmethod
    def check_is_not_invalid_identifier(extra_code: str, row: int, col: int):
        """
            Checks there is no extra code to analyze, if not raise Exception
        """
        if(extra_code[0] in [*LETTERS, '_']):
            raise LexicalException(f'SYNTAX ERROR: Invalid identifier foun at row {row} and column {col}')
        pass

    @staticmethod
    def check_non_character_out_of_alphabet(character: str, row: int, col: int):
        """
            Checks if a character is in Pascal Alphabet
            Args:
                - character(str) Character to check
                - row(int): row where the look ahead is
                - col(int): column where the look ahead is
        """
        if(not(character in ALPHABET)):
            raise LexicalException(f"LEXICAL ERROR: {character} in line {row}, column {col} does not belong to PASCAL alphabet")
    
        pass

    pass