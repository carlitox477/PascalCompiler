#from grammar_rules.basic_rules import program_rule
from io import TextIOWrapper
from .gr_program_rule import ProgramRuleRecognizer

def use_syntax_analyzer(source_code:str, output_file: TextIOWrapper) -> bool:
    # Create symbol table here and pass it as parameter
    return ProgramRuleRecognizer.recognize_program_rule(source_code,1,1,output_file)