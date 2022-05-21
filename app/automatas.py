#!/usr/bin/env python3
from typing import Tuple
from .utils import LETTERS,DIGITS, WS,KEYWORD_LEXEM_TO_TOKEN,KEYWORD_LEXEM_TO_TOKEN,LEXEM_TO_SPECIAL_SYMBOL_TOKEN,LEXEM_TO_OPERATOR_TOKEN,LEXEM_TO_RELATIONAL_OPERATOR_TOKEN, SYMBOLS, ESPECIAL_SYMBOLS

def white_space_recognizer(pending_source_code:str,tokens:list) -> Tuple[str,list]:
    """Eras whitespaces from source code"""
    while(len(pending_source_code)>0 and pending_source_code[0] in WS): pending_source_code=pending_source_code[1:]
    return pending_source_code,tokens

def comment_recognizer(pending_source_code:str, tokens: list)->Tuple[str,list]:
    """Erase comments from source code"""
    if(len(pending_source_code)>0 and pending_source_code[0]=='{'):
        pending_source_code=pending_source_code[1:]
        while pending_source_code[0]!='}': pending_source_code=pending_source_code[1:]
        pending_source_code= pending_source_code[1:]
        pass
    return pending_source_code,tokens

def identifier_keyword_recognizer(pending_source_code:str,tokens: list)-> Tuple[str,list]:
    """Add a keyword/identifier token if it corresponds and return the pending code to anylise"""
    if(len(pending_source_code)>0 and pending_source_code[0] in LETTERS or pending_source_code[0]=='_'):
        
        NEXT_VALID_CHARS=LETTERS+DIGITS
        NEXT_VALID_CHARS.append("_")
        
        lexem=pending_source_code[0]
        pending_source_code=pending_source_code[1:]
        
        while(len(pending_source_code)>0 and pending_source_code[0] in NEXT_VALID_CHARS):
            lexem = lexem+pending_source_code[0]
            pending_source_code = pending_source_code[1:]
            if(pending_source_code[0] in ESPECIAL_SYMBOLS):
                raise Exception("El simbolo "+ pending_source_code[0] +" no está permitido en los identificadores")
            pass
        token=KEYWORD_LEXEM_TO_TOKEN.get(lexem,False)
        if not(token):
            token=("TK_identifier", lexem)
        elif token[0] in ['TK_datatype', 'TK_boolean_literal']:
            pass
        else:
            token = (token,)
        tokens.append(token)
        pass
    return pending_source_code,tokens

def number_recognizer(pending_source_code:str,tokens: list)->Tuple[str,list]:
    """Add a number token if it corresponds and return the pending code to anylise"""
    lexem=""
    #Check of first char is zero
    if(pending_source_code[0]=="0"):
        lexem="0"
        pending_source_code=pending_source_code[1:]
        pass
    
    #Erase extra zeros
    while(len(pending_source_code)>0 and pending_source_code[0]=="0"):
        pending_source_code=pending_source_code[1:]
        pass
    
    # If previus number were zero and the current is a digit we redefine the lexem value
    if(pending_source_code[0] in DIGITS):
        lexem=pending_source_code[0]
        pending_source_code=pending_source_code[1:]
        pass
    
    #We consider the rest of the numbers
    while(len(pending_source_code)>0 and pending_source_code[0] in DIGITS):
        lexem=lexem+pending_source_code[0]
        pending_source_code=pending_source_code[1:]
        pass
    if(len(lexem)!=0): tokens.append(("TK_number", lexem))
    
    return pending_source_code,tokens

def special_symbol_recognizer(pending_source_code:str,tokens: list)->Tuple[str,list]:
    """Add a special symbol token if it corresponds and return the pending code to anylise"""
    if(len(pending_source_code)>1 and pending_source_code[0:2]==":="):
        tokens.append(("TK_assignment",))
        return pending_source_code[2:],tokens
    if(len(pending_source_code)>0):
        token=LEXEM_TO_SPECIAL_SYMBOL_TOKEN.get(pending_source_code[0],False)
        
        if(token):
            tokens.append((token,))
            return pending_source_code[1:],tokens
        pass
    return pending_source_code,tokens

def arithmetical_operator_recognizer(pending_source_code:str,tokens: list)->Tuple[str,list]:
    """Add a arithmetical operator token if it corresponds and return the pending code to anylise"""
    if(len(pending_source_code)>0):
        token=LEXEM_TO_OPERATOR_TOKEN.get(pending_source_code[0],False)
        if(token):
            tokens.append(token)
            return pending_source_code[1:],tokens
        pass
    return pending_source_code,tokens

def relational_operator_recognizer(pending_source_code:str,tokens: list)-> Tuple[str,list]:
    """Add a relational operator token if it corresponds and return the pending code to anylise"""
    if(len(pending_source_code)>1):
        token=LEXEM_TO_RELATIONAL_OPERATOR_TOKEN.get(pending_source_code[0:2],False)
        if(token):
            tokens.append(token)
            return pending_source_code[2:],tokens
        pass
    if(len(pending_source_code)>0):
        token=LEXEM_TO_RELATIONAL_OPERATOR_TOKEN.get(pending_source_code[0],False)
        if(token):
            tokens.append(token)
            return pending_source_code[1:],tokens
        pass
    return pending_source_code,tokens

def parenthesis_recognizer(pending_source_code:str,tokens: list)->Tuple[str,list]:
    """Add a parenthesis token if it corresponds and return the pending code to anylise"""
    if(len(pending_source_code)>1):
        if(pending_source_code[0]=="("):
            tokens.append(("TK_parenthesis","OPPAR"))
            return pending_source_code[1:],tokens
        elif(pending_source_code[0]==")"):
            tokens.append(("TK_parenthesis","CLPAR"))
            return pending_source_code[1:],tokens
        pass
    return pending_source_code,tokens

