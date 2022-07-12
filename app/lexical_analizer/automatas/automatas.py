#!/usr/bin/env python3
from typing import Tuple
from ..utils import LETTERS,DIGITS, WS,KEYWORD_LEXEM_TO_TOKEN,KEYWORD_LEXEM_TO_TOKEN,LEXEM_TO_SPECIAL_SYMBOL_TOKEN,LEXEM_TO_OPERATOR_TOKEN,LEXEM_TO_RELATIONAL_OPERATOR_TOKEN

def white_space_recognizer(pending_source_code:str,currentColumn:int, currentRow:int) -> Tuple[str,int,int]:
    """Erase whitespaces from pending_source_code"""
    newColumn=currentColumn
    newRow=currentRow
    while(len(pending_source_code)>0 and pending_source_code[0] in WS):
        if pending_source_code[0] == ' ':
            newColumn+=1
        elif pending_source_code[0] == '\t':
            #According to VS code a tab is equal 3 whitespaces
            newColumn+= 3
        elif pending_source_code[0] == '\n':
            newRow += 1
            newColumn = 1
        
        pending_source_code=pending_source_code[1:]
    return pending_source_code, newColumn,newRow


def comment_recognizer(pending_source_code:str, currentColumn:int, currentRow:int)->Tuple[str,int,int]:
    """Erase comments from source code"""
    newColumn=currentColumn
    newRow=currentRow
    if(len(pending_source_code)>0 and pending_source_code[0]=='{'):
        pending_source_code=pending_source_code[1:]
        newColumn+=1
        while pending_source_code[0]!='}':
            if(pending_source_code[0]=="\n"):
                newRow+=1
                newColumn=1
            else:
                newColumn+=1
            pending_source_code=pending_source_code[1:]
        pending_source_code= pending_source_code[1:]
        newColumn+=1
        pass
    return pending_source_code,newColumn,newRow


def identifier_keyword_recognizer(
        pending_source_code: str, currentColumn:int, currentRow:int) -> Tuple[str, int,int]:
    """Add a keyword/identifier token if it corresponds
        and return the pending code to anylise"""
    newColumn=currentColumn
    token=None
    if(len(pending_source_code) > 0 and
       pending_source_code[0] in LETTERS or pending_source_code[0] == '_'):

        NEXT_VALID_CHARS = LETTERS+DIGITS
        NEXT_VALID_CHARS.append("_")

        lexem = pending_source_code[0]
        pending_source_code = pending_source_code[1:]
        newColumn=currentColumn+1
        

        while(len(pending_source_code) > 0 and pending_source_code[0] in
              NEXT_VALID_CHARS):
            lexem = lexem+pending_source_code[0]
            pending_source_code = pending_source_code[1:]
            newColumn+=1
            pass
        token_info = KEYWORD_LEXEM_TO_TOKEN.get(lexem, False)
        if not(token_info):
            token = ("TK_identifier", lexem, (currentRow, currentColumn))
        elif token_info[0] in ['TK_datatype', 'TK_boolean_literal']:
            token = list(token_info)
            token.append((currentRow, currentColumn))
            token = tuple(token)
            pass
        else:
            #Reserved word
            #print(token_info)
            token = (token_info,None, (currentRow, currentColumn))
        
    return pending_source_code,newColumn,currentRow,token


def number_recognizer(
        pending_source_code: str, currentColumn:int, currentRow:int) -> Tuple[str, int, int,Tuple]:
    """Add a number token if it corresponds and
        return the pending code to anylise"""
    lexem = ""
    newColumn=currentColumn
    
    token=None
    # Check of first char is zero
    if(pending_source_code[0] == "0"):
        lexem="0"
        pending_source_code=pending_source_code[1:]
        newColumn+=1
        pass
    # Erase extra zeros
    while(len(pending_source_code)>0 and pending_source_code[0]=="0"):
        pending_source_code=pending_source_code[1:]
        newColumn+=1
        pass
    
    # If previus number were zero and the current is a digit we redefine the lexem value
    if(pending_source_code[0] in DIGITS):
        newColumn+=1
        lexem=pending_source_code[0]
        pending_source_code=pending_source_code[1:]
        pass
    
    #We consider the rest of the numbers
    while(len(pending_source_code)>0 and pending_source_code[0] in DIGITS):
        newColumn+=1
        lexem=lexem+pending_source_code[0]
        pending_source_code=pending_source_code[1:]
    if(len(lexem)!=0): token=("TK_number", lexem, (currentRow, currentColumn))
     
    return pending_source_code,newColumn,currentRow,token

def special_symbol_recognizer(pending_source_code:str,currentColumn:int, currentRow:int)->Tuple[str,int,int,Tuple]:
    """Add a special symbol token if it corresponds and return the pending code to anylise"""
    
    token=None
    if(len(pending_source_code)>1 and pending_source_code[0:2]==":="):
        return pending_source_code[2:],currentColumn+2,currentRow, ("TK_assignment", None, (currentRow, currentColumn))
    if(len(pending_source_code)>0):
        token=LEXEM_TO_SPECIAL_SYMBOL_TOKEN.get(pending_source_code[0],False)
        if(token):
            return pending_source_code[1:],currentColumn+1,currentRow,(token, None, (currentRow, currentColumn))
    return pending_source_code,currentColumn,currentRow, None


def arithmetical_operator_recognizer(pending_source_code:str,currentColumn:int, currentRow:int)->Tuple[str,int,int,Tuple]:
    """Add a arithmetical operator token if it corresponds and return the pending code to anylise"""
    if(len(pending_source_code)>0):
        token=LEXEM_TO_OPERATOR_TOKEN.get(pending_source_code[0],False)
        if(token):
            token = list(token)
            token.append((currentRow, currentColumn))
            token = tuple(token)
            return pending_source_code[1:],currentColumn+1,currentRow,token
        pass
    return pending_source_code,currentColumn,currentRow, None


def relational_operator_recognizer(pending_source_code:str,currentColumn:int, currentRow:int)->Tuple[str,int,int,Tuple]:
    """Add a relational operator token if it corresponds and return the pending code to anylise"""
    if(len(pending_source_code)>1):
        token=LEXEM_TO_RELATIONAL_OPERATOR_TOKEN.get(pending_source_code[0:2],False)
        if(token):
            token = list(token)
            token.append((currentRow, currentColumn))
            token = tuple(token)
            return pending_source_code[2:],currentColumn+2,currentRow,token
        pass
    if(len(pending_source_code)>0):
        token=LEXEM_TO_RELATIONAL_OPERATOR_TOKEN.get(pending_source_code[0],False)
        if(token):
            token = list(token)
            token.append((currentRow, currentColumn))
            token = tuple(token)
            
            return pending_source_code[2:],currentColumn+1,currentRow,token
        pass
    return pending_source_code,currentColumn,currentRow, None


def parenthesis_recognizer(pending_source_code:str,currentColumn:int, currentRow:int)->Tuple[str,int,int,Tuple]:
    """Add a parenthesis token if it corresponds and return the pending code to anylise"""

    if(len(pending_source_code)>1):
        if(pending_source_code[0]=="("):
            return pending_source_code[1:],currentColumn+1,currentRow,("TK_parenthesis","OPPAR", (currentRow, currentColumn))
        elif(pending_source_code[0]==")"):
            return pending_source_code[1:],currentColumn+1,currentRow,("TK_parenthesis","CLPAR", (currentRow, currentColumn))
        pass
    return pending_source_code,currentColumn,currentRow,None

