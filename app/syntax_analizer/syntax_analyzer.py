#from grammar_rules.basic_rules import program_rule
from .grammar_rules.program_rule import program_rule

def use_syntax_analyzer(source_code:str) -> bool:
    return program_rule(source_code,1,1)