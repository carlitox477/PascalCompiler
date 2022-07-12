#!/usr/bin/env python3
import string

VALID_FILE_EXTENSION=["txt","pas"]
def read_source_code(file_name:str)->str:    
    if not(file_name.split(".")[-1] in VALID_FILE_EXTENSION):
        raise Exception("Invalid extension")
    
    source_code =""
    with open(file_name, 'r+') as program:
        for line in program:
            source_code= source_code + line
            pass
        pass
    return source_code