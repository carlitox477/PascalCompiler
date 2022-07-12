#!/usr/bin/env python3
from __future__ import absolute_import
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Just to export to different files
from app.utils import read_source_code
from app.syntax_analizer.syntax_analyzer import use_syntax_analyzer


VALID_FILE_EXTENSION=["txt","pas"]

def get_pascal_program_file_name_path(file_name:str)->str:
    return os.path.join(os.path.dirname(__file__),"",file_name)
