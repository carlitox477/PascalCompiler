#!/usr/bin/env python3
from __future__ import absolute_import
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.automatas import white_space_recognizer,comment_recognizer