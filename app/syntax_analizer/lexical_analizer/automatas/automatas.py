#!/usr/bin/env python3
from typing import Tuple
from .utils import LETTERS,DIGITS, WS,KEYWORD_LEXEM_TO_TOKEN,KEYWORD_LEXEM_TO_TOKEN,LEXEM_TO_SPECIAL_SYMBOL_TOKEN,LEXEM_TO_OPERATOR_TOKEN,LEXEM_TO_RELATIONAL_OPERATOR_TOKEN
from .token import Token
from .lexical_error_analizer import LexicalErrorAnalizer

class Automata:
    @staticmethod
    def recognize_white_space(pending_source_code: str, current_column: int, current_row: int) -> Tuple[str, int, int]:
        """
        Erase whitespaces from pending_source_code
        
        Args:
            - pending_source_code(str): code pending to read
            - current column(int): column where the look ahead is in the original code
            - current_row(int): row where the look ahead is in the original code
            
        Returns:
            - pending_source_code(str): Acts as look ahead, it is the code pending to read
            - new_column(int): Column where the look ahead is now
            - new_row(int): Row where the look ahead is now
        """
        new_column = current_column
        new_row = current_row
        while(len(pending_source_code) > 0 and pending_source_code[0] in WS):
            if pending_source_code[0] == ' ':
                new_column += 1
            elif pending_source_code[0] == '\t':
                #According to VS code a tab is equal 3 whitespaces
                new_column += 3
            elif pending_source_code[0] == '\n':
                new_row += 1
                new_column = 1
            
            pending_source_code = pending_source_code[1:]
        return pending_source_code, new_column, new_row

    @staticmethod
    def recognize_comment(pending_source_code: str, current_column: int, current_row: int) -> Tuple[str, int, int]:
        """
        Erase comments from source code
        
        Args:
            - pending_source_code(str): code pending to read
            - current column(int): column where the look ahead is in the original code
            - current_row(int): row where the look ahead is in the original code
            
        Returns:
            - pending_source_code(str): Acts as look ahead, it is the code pending to read
            - new_column(int): Column where the look ahead is now
            - new_row(int): Row where the look ahead is now
        """
        new_column = current_column
        new_row = current_row
        if(len(pending_source_code)>0 and pending_source_code[0]=='{'):
            try:
                pending_source_code=pending_source_code[1:]
                new_column+=1
                while pending_source_code[0]!='}':
                    if(pending_source_code[0]=="\n"):
                        new_row+=1
                        new_column=1
                    else:
                        new_column+=1
                    pending_source_code=pending_source_code[1:]
                pending_source_code= pending_source_code[1:]
                new_column+=1
                pass
            except IndexError:
                LexicalErrorAnalizer.raise_no_closed_comment_exception()
            pass
        return pending_source_code, new_column, new_row

    @staticmethod
    def recognize_identifier_or_keyword(pending_source_code: str, current_column: int, current_row: int) -> Tuple[str, int, int, Token]:
        """
        Add a keyword/identifier token if it corresponds and return the pending code to anylise

        Args:
            - pending_source_code(str): code pending to read
            - current column(int): column where the look ahead is in the original code
            - current_row(int): row where the look ahead is in the original code
            
        Returns:
            - pending_source_code(str): Acts as look ahead, it is the code pending to read
            - new_column(int): Column where the look ahead is now
            - new_row(int): Row where the look ahead is now
            - token(Token): recognized token
        """
        new_column = current_column
        token = None
        if(len(pending_source_code) > 0 and pending_source_code[0] in LETTERS or pending_source_code[0] == '_'):

            NEXT_VALID_CHARS = LETTERS+DIGITS
            NEXT_VALID_CHARS.append("_")

            lexem = pending_source_code[0]
            pending_source_code = pending_source_code[1:]
            new_column = current_column + 1
            

            while(len(pending_source_code) > 0 and pending_source_code[0] in NEXT_VALID_CHARS):
                lexem = lexem + pending_source_code[0]
                pending_source_code = pending_source_code[1:]
                new_column += 1
                pass

            lower_lexem = lexem.lower()
            token_info = KEYWORD_LEXEM_TO_TOKEN.get(lower_lexem, False)
            if not(token_info):
                token = Token("TK_identifier", current_row, current_column, {"name": lexem})
            elif token_info[0] == 'TK_datatype':
                token = Token(token_info[0], current_row, current_column, {"name": token_info[1]})
            elif token_info[0] == 'TK_boolean_literal':
                token = Token(token_info[0], current_row, current_column, {"value": token_info[1]})
            else:
                #Reserved word
                token = Token(token_info, current_row, current_column, None)
            
        return pending_source_code, new_column, current_row, token

    @staticmethod
    def recognize_number(pending_source_code: str, current_column: int, current_row:int) -> Tuple[str, int, int, Token]:
        """
        Add a number token if it corresponds and return the pending code to anylise
        
        Args:
            - pending_source_code(str): code pending to read
            - current column(int): column where the look ahead is in the original code
            - current_row(int): row where the look ahead is in the original code
                
        Returns:
            - pending_source_code(str): Acts as look ahead, it is the code pending to read
            - new_column(int): Column where the look ahead is now
            - new_row(int): Row where the look ahead is now
            - token(Token): recognized token
        """
        lexem = ""
        new_column = current_column
        
        token = None
        
        # Check of first char is zero
        if(pending_source_code[0] == "0"):
            lexem = "0"
            pending_source_code = pending_source_code[1:]
            new_column += 1
            pass
        
        # Erase extra zeros
        while(len(pending_source_code)>0 and pending_source_code[0]=="0"):
            pending_source_code = pending_source_code[1:]
            new_column += 1
            pass
        
        # If previous number were zero and the current is a digit we redefine the lexem value
        if(pending_source_code[0] in DIGITS):
            new_column += 1
            lexem = pending_source_code[0]
            pending_source_code = pending_source_code[1:]
            pass
        
        #We consider the rest of the numbers
        while(len(pending_source_code) > 0 and pending_source_code[0] in DIGITS):
            new_column += 1
            lexem = lexem + pending_source_code[0]
            pending_source_code = pending_source_code[1:]
        if(len(lexem)!=0):
            token = Token("TK_number", current_row, current_column, {"value": lexem})
        
        #Verify the look ahead isn't in a char, otherwise we are trying to create an invalid identifier
        LexicalErrorAnalizer.check_is_not_invalid_identifier(pending_source_code, current_row, current_column)
        return pending_source_code, new_column, current_row, token

    @staticmethod
    def recognize_special_symbol(pending_source_code: str, current_column: int, current_row: int) -> Tuple[str, int, int, Token]:
        """
        Add a special symbol token if it corresponds and return the pending code to anylise
        
        Args:
            - pending_source_code(str): code pending to read
            - current column(int): column where the look ahead is in the original code
            - current_row(int): row where the look ahead is in the original code
                
        Returns:
            - pending_source_code(str): Acts as look ahead, it is the code pending to read
            - new_column(int): Column where the look ahead is now
            - new_row(int): Row where the look ahead is now
            - token(Token): recognized token
        """
        
        token = None
        if(len(pending_source_code) > 1 and pending_source_code[0:2] == ":="):
            return pending_source_code[2:], current_column + 2, current_row, Token("TK_assignment", current_row, current_column, None)
        if(len(pending_source_code) > 0):
            token = LEXEM_TO_SPECIAL_SYMBOL_TOKEN.get(pending_source_code[0], False)
            if(token):
                return pending_source_code[1:], current_column + 1, current_row, Token(token, current_row, current_column, None)
        return pending_source_code, current_column, current_row, None

    @staticmethod
    def recognize_arithmetical_operator(pending_source_code:str,current_column:int, current_row:int)->Tuple[str, int, int, Token]:
        """
        Add a arithmetical operator token if it corresponds and return the pending code to anylise
        
        Args:
            - pending_source_code(str): code pending to read
            - current column(int): column where the look ahead is in the original code
            - current_row(int): row where the look ahead is in the original code
                
        Returns:
            - pending_source_code(str): Acts as look ahead, it is the code pending to read
            - new_column(int): Column where the look ahead is now
            - new_row(int): Row where the look ahead is now
            - token(Token): recognized token
        """
        if(len(pending_source_code) > 0):
            token=LEXEM_TO_OPERATOR_TOKEN.get(pending_source_code[0],False)
            if(token):
                return pending_source_code[1:], current_column + 1, current_row, Token(token[0], current_row, current_column, {"operation": token[1]})
            pass
        return pending_source_code, current_column, current_row, None

    @staticmethod
    def recognize_relational_operator(pending_source_code:str,current_column:int, current_row:int)->Tuple[str, int, int, Token]:
        """
        Add a relational operator token if it corresponds and return the pending code to anylise
        
        Args:
            - pending_source_code(str): code pending to read
            - current column(int): column where the look ahead is in the original code
            - current_row(int): row where the look ahead is in the original code
                
        Returns:
            - pending_source_code(str): Acts as look ahead, it is the code pending to read
            - new_column(int): Column where the look ahead is now
            - new_row(int): Row where the look ahead is now
            - token(Token): recognized token        
        """
        if(len(pending_source_code)>1):
            token = LEXEM_TO_RELATIONAL_OPERATOR_TOKEN.get(pending_source_code[0:2], False)
            if(token):
                return pending_source_code[2:], current_column + 2, current_row, Token(token[0], current_row, current_column,{"operation": token[1]})
            pass
        if(len(pending_source_code)>0):
            token = LEXEM_TO_RELATIONAL_OPERATOR_TOKEN.get(pending_source_code[0],False)
            if(token):
                return pending_source_code[1:],current_column+1,current_row,Token(token[0], current_row, current_column, {"operation": token[1]})
            pass
        return pending_source_code,current_column,current_row, None

    @staticmethod
    def recognize_parenthesis(pending_source_code: str, current_column: int, current_row: int)->Tuple[str, int, int, Token]:
        """
        Add a parenthesis token if it corresponds and return the pending code to anylise
        
        Args:
            - pending_source_code(str): code pending to read
            - current column(int): column where the look ahead is in the original code
            - current_row(int): row where the look ahead is in the original code
                
        Returns:
            - pending_source_code(str): Acts as look ahead, it is the code pending to read
            - new_column(int): Column where the look ahead is now
            - new_row(int): Row where the look ahead is now
            - token(Token): recognized token          
        """

        if(len(pending_source_code) > 1):
            if(pending_source_code[0] == "("):
                return pending_source_code[1:], current_column + 1, current_row, Token("TK_parenthesis", current_row, current_column, {"type": "OPPAR"})
            elif(pending_source_code[0] == ")"):
                return pending_source_code[1:], current_column + 1, current_row, Token("TK_parenthesis", current_row, current_column, {"type": "CLPAR"})
            pass
        return pending_source_code, current_column, current_row, None

    pass

