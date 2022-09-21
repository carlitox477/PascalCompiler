#!/usr/bin/env python3
from __future__ import absolute_import
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.automatas import white_space_recognizer,comment_recognizer,identifier_keyword_recognizer,number_recognizer,special_symbol_recognizer,arithmetical_operator_recognizer,relational_operator_recognizer,parenthesis_recognizer
from app.utils import read_source_code
