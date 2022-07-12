#!/usr/bin/env python3
from .automatas.automatas import white_space_recognizer,comment_recognizer,identifier_keyword_recognizer,relational_operator_recognizer, parenthesis_recognizer,arithmetical_operator_recognizer,special_symbol_recognizer,number_recognizer
from .utils import ALPHABET

def getLexicalToken(source_code: str, currentColumn: int, currentRow: int):
    """Gets the first token found in the source code given as parameter and
    updates the current column and row where the lookahead is positionated
    """  
    
    previous_cleaned_source_code=source_code
    #Erase comments
    cleaned_source_code, updatedColumn, updatedRow = comment_recognizer(source_code,  currentColumn, currentRow)
        
    #Erase whitespaces, tabs and jumps
    cleaned_source_code, updatedColumn, updatedRow = white_space_recognizer(cleaned_source_code,updatedColumn, updatedRow) 

    cont = len(previous_cleaned_source_code) != len(cleaned_source_code)
    
    while(cont):
        #print("continue")
        #Erase comments
        previous_cleaned_source_code, updatedColumn, updatedRow = comment_recognizer(cleaned_source_code,  updatedColumn, updatedRow)
        
        #Erase whitespaces, tabs and jumps
        cleaned_source_code, updatedColumn, updatedRow = white_space_recognizer(previous_cleaned_source_code,updatedColumn, updatedRow) 

        cont = len(previous_cleaned_source_code) != len(cleaned_source_code)
        pass
    pending_source_code=cleaned_source_code


    if(len(pending_source_code)==0):
        return "",updatedColumn,updatedRow, None
    
    # Check if we find a wierd char
    if(not(pending_source_code[0] in ALPHABET)):
        raise Exception(
            f"Caracter raro: {pending_source_code[0]} en fila {updatedRow}, columna {updatedColumn}")
    
    
    # Try to find an identifier or reserved word
    pending_source_code, newColumn,newRow,token = identifier_keyword_recognizer(pending_source_code,  updatedColumn, updatedRow)
    if(token!=None):
        #if token[0]=="TK_write": print("Write token found")
        return  pending_source_code, newColumn,newRow,token
    
    # Try to find a number
    pending_source_code, newColumn,newRow,token = number_recognizer(pending_source_code,  updatedColumn, updatedRow)
    if(token!=None):
        return  pending_source_code, newColumn,newRow,token
       
    # Try to find a special symbol (valid puntuaction or assignment)
    pending_source_code, newColumn,newRow,token = special_symbol_recognizer(pending_source_code,  updatedColumn, updatedRow)
    if(token!=None):
        return  pending_source_code, newColumn,newRow,token
    
    #Try to find arithmetical operator
    pending_source_code, newColumn,newRow,token = arithmetical_operator_recognizer(pending_source_code,  updatedColumn, updatedRow)
    if(token!=None):
        return  pending_source_code, newColumn,newRow,token
    
    #Try to find relational operator
    pending_source_code, newColumn,newRow,token = relational_operator_recognizer(pending_source_code,  updatedColumn, updatedRow)
    if(token!=None):
        return  pending_source_code, newColumn,newRow,token
    
    pending_source_code, newColumn,newRow,token = parenthesis_recognizer(pending_source_code,  updatedColumn, updatedRow)
    if(token!=None):
        return pending_source_code, newColumn,newRow,token
    
    raise Exception(
            f"Algo raro sucedio en la  fila {newRow}, columna {newColumn}: {pending_source_code[0:20]}")
    #raise Exception(f"Algo raro sucedio en la  fila {newRow}, columna {newColumn}")
    
