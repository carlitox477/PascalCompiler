#!/usr/bin/env python3
from .utils import LETTERS,DIGITS, WS,KEYWORD_LEXEM_TO_TOKEN,KEYWORD_LEXEM_TO_TOKEN,LEXEM_TO_SPECIAL_SYMBOL_TOKEN,LEXEM_TO_OPERATOR_TOKEN,LEXEM_TO_RELATIONAL_OPERATOR_TOKEN

def white_space_recognizer(pending_source_code:str) -> str:
    """Eras whitespaces from source code"""
    while(len(pending_source_code)>0 and pending_source_code[0] in WS): pending_source_code=pending_source_code[1:]
    return pending_source_code

def comment_recognizer(pending_source_code:str)->str:
    """Erase comments from source code"""
    if(len(pending_source_code)>0 and pending_source_code[0]=='{'):
        pending_source_code=pending_source_code[1:]
        while pending_source_code[0]!='}': pending_source_code=pending_source_code[1:]
        return pending_source_code[1:]
    return pending_source_code

def identifier_keyword_recognizer(pending_source_code:str,tokens: list)->str:
    """Add a keyword/identifier token if it corresponds and return the pending code to anylise"""
    if(len(pending_source_code)>0 and pending_source_code[0] in LETTERS or pending_source_code[0]=='_'):
        NEXT_VALID_CHARS=pending_source_code[0] in LETTERS.append("_")+DIGITS
        lexem=pending_source_code[0]
        pending_source_code=pending_source_code[1:]
        
        while(len(pending_source_code)>0 and pending_source_code[0] in NEXT_VALID_CHARS):
            lexem=lexem+pending_source_code[0]
            pending_source_code=pending_source_code[1:]
            pass
        token=KEYWORD_LEXEM_TO_TOKEN[lexem]
        if not(token):
            token=("TK_identifier",lexem)
            pass
        tokens.append(token)
        pass
    return pending_source_code

def number_recognizer(pending_source_code:str,tokens: list)->str:
    """Add a number token if it corresponds and return the pending code to anylise"""
    lexem=""
    while(len(pending_source_code)>0 and pending_source_code[0] in DIGITS):
        lexem=lexem+pending_source_code[0]
        pending_source_code=pending_source_code[1:]
        pass
    if(len(lexem)!=0): tokens.append(("TK_number",lexem))
    
    return pending_source_code

def special_symbol_recognizer(pending_source_code:str,tokens: list)->str:
    """Add a special symbol token if it corresponds and return the pending code to anylise"""
    if(len(pending_source_code)>1 and pending_source_code[0:2]==":="):
        tokens.append("TK_assignment")
        return pending_source_code[2:]
    if(len(pending_source_code)>0):
        token=LEXEM_TO_SPECIAL_SYMBOL_TOKEN[pending_source_code[0]]
        
        if(token):
            tokens.append(token)
            return pending_source_code[1:]
        pass
    return pending_source_code

def arithmetical_operator_recognizer(pending_source_code:str,tokens: list)->str:
    """Add a arithmetical operator token if it corresponds and return the pending code to anylise"""
    if(len(pending_source_code)>0):
        token=LEXEM_TO_OPERATOR_TOKEN[pending_source_code[0]]
        if(token):
            tokens.append(token)
            return pending_source_code[1:]
        pass
    return pending_source_code

def relational_operator_recognizer(pending_source_code:str,tokens: list)-> str:
    """Add a relational operator token if it corresponds and return the pending code to anylise"""
    if(len(pending_source_code)>1):
        token=LEXEM_TO_RELATIONAL_OPERATOR_TOKEN[pending_source_code[0:2]]
        if(token):
            tokens.append(token)
            return pending_source_code[2:]
        pass
    if(len(pending_source_code)>0):
        token=LEXEM_TO_RELATIONAL_OPERATOR_TOKEN[pending_source_code[0:2]]
        if(token):
            tokens.append(token)
            return pending_source_code[1:]
        pass
    return pending_source_code

def parenthesis_recognizer(pending_source_code:str,tokens: list)->str:
    """Add a parenthesis token if it corresponds and return the pending code to anylise"""
    if(len(pending_source_code)>1):
        if(pending_source_code[0]=="("):
            tokens.append(("TK_parenthesis","OPPAR"))
            return pending_source_code[1:]
        elif(pending_source_code[0]==")"):
            tokens.append(("TK_parenthesis","CLPAR"))
            return pending_source_code[1:]
        pass
    return pending_source_code

