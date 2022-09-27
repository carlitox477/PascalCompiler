#!/usr/bin/env python3
from typing import Tuple
from .automatas.automatas import Automata
from .automatas.token import Token
from .automatas.lexical_error_analizer import LexicalErrorAnalizer

class LexicalAnalyzer:
    def get_lexical_token(source_code: str, current_column: int, current_row: int)-> Tuple[str, int, int, Token]:
        """
        Gets the first token found in the source code given as parameter and updates the current column and row where the lookahead is positionated
        
        Args:
            - source_code(str): Code to analyze, acts as look ahead
            - current_column(int): Column where the look ahead is positionated
            - current_row(int): Row where the look ahead is positionated
        
        Returns:
            - pending_source_code(str): Pending code to analize, acts as look ahead
            - new_column(int): column where the look ahead is
            - new_row(int): row where the look ahead is
            - token(Token): Token found
        """  
        
        previous_cleaned_source_code = source_code
        #Erase comments
        cleaned_source_code, updated_column, updated_row = Automata.recognize_comment(source_code,  current_column, current_row)
            
        #Erase whitespaces, tabs and jumps
        cleaned_source_code, updated_column, updated_row = Automata.recognize_white_space(cleaned_source_code,updated_column, updated_row)
        cont = len(previous_cleaned_source_code) != len(cleaned_source_code)
        
        while(cont):
            #print("continue")
            #Erase comments
            previous_cleaned_source_code, updated_column, updated_row = Automata.recognize_comment(cleaned_source_code,  updated_column, updated_row)
            
            #Erase whitespaces, tabs and jumps
            cleaned_source_code, updated_column, updated_row = Automata.recognize_white_space(previous_cleaned_source_code,updated_column, updated_row) 

            cont = len(previous_cleaned_source_code) != len(cleaned_source_code)
            pass
        pending_source_code=cleaned_source_code


        if(len(pending_source_code)==0):
            return "",updated_column,updated_row, None
        
        LexicalErrorAnalizer.check_non_character_out_of_alphabet(pending_source_code[0], updated_row, updated_column)
        
        
        # Try to find an identifier or reserved word
        pending_source_code, new_column, new_row, token = Automata.recognize_identifier_or_keyword(pending_source_code,  updated_column, updated_row)
        if(token!=None):
            #if token.type=="TK_boolean_literal": print("BOOLEAN LITERAL FOUND")
            return  pending_source_code, new_column, new_row, token
        
        # Try to find a number
        pending_source_code, new_column, new_row, token = Automata.recognize_number(pending_source_code,  updated_column, updated_row)
        if(token!=None):
            return  pending_source_code, new_column, new_row, token
        
        # Try to find a special symbol (valid puntuaction or assignment)
        pending_source_code, new_column, new_row, token = Automata.recognize_special_symbol(pending_source_code,  updated_column, updated_row)
        if(token!=None):
            return  pending_source_code, new_column, new_row, token
        
        #Try to find arithmetical operator
        pending_source_code, new_column, new_row, token = Automata.recognize_arithmetical_operator(pending_source_code,  updated_column, updated_row)
        if(token!=None):
            return  pending_source_code, new_column, new_row, token
        
        #Try to find relational operator
        pending_source_code, new_column, new_row, token = Automata.recognize_relational_operator(pending_source_code,  updated_column, updated_row)
        if(token!=None):
            return  pending_source_code, new_column, new_row, token
        
        #Try to find parenthesis
        pending_source_code, new_column, new_row, token = Automata.recognize_parenthesis(pending_source_code,  updated_column, updated_row)
        if(token!=None):
            return pending_source_code, new_column, new_row, token
        
        # Just for debuging
        raise Exception(
            f"Algo raro sucedio en la  fila {new_row}, columna {new_column}: {pending_source_code[0:20]}")
        pass
        
    
    pass