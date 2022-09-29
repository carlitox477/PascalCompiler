from io import TextIOWrapper
from typing import ClassVar
from typing_extensions import Self
from .gr_commands_rules import CommandRulesRecognizer
from .gr_expresions_rules import ExpresionRulesRecognizer
from .utils import delete_whitespaces_and_comments, match_token
from .gr_declaration_rules import DeclarationRulesRecognizer
from .semantic_analizer import SymbolTable
from .mepa_writer import MepaWriter


class ProgramRuleRecognizer:
    mepa_writer= None

    @staticmethod
    def setMepaWriter(output_file: TextIOWrapper):
        
        mepa_writer= MepaWriter(output_file)
        #print(mepa_writer)
        ProgramRuleRecognizer.mepa_writer=mepa_writer
        ExpresionRulesRecognizer.mepa_writer=mepa_writer
        DeclarationRulesRecognizer.mepa_writer=mepa_writer
        CommandRulesRecognizer.mepa_writer=mepa_writer
        #DeclarationRulesRecognizer.setMepaWriter(ProgramRuleRecognizer.mepa_writer)
        #CommandRulesRecognizer.setMepaWriter(ProgramRuleRecognizer.mepa_writer)
        pass

    @staticmethod
    def recognize_program_rule(pending_source_code: str, current_column:int, current_row:int)->bool:
        # Add program name to symbol table
        pending_source_code,current_column, current_row,_,_ = match_token('TK_program',pending_source_code,current_column, current_row)
        pending_source_code,current_column, current_row,program_identifier_token,_  = match_token('TK_identifier',pending_source_code,current_column, current_row)
        pending_source_code,current_column, current_row,_,_  = match_token('TK_semicolon',pending_source_code,current_column, current_row)
        

        program_table = SymbolTable(program_identifier_token.getAttribute("name"),"PROGRAM",0,None,{},0,current_row)
        ProgramRuleRecognizer.mepa_writer.init()

        pending_source_code,current_column, current_row = DeclarationRulesRecognizer.verify_block_rule(pending_source_code,current_column, current_row, program_table,True)
        
        pending_source_code,current_column, current_row,_,_ = match_token('TK_dot',pending_source_code,current_column, current_row)
        ProgramRuleRecognizer.mepa_writer.halt()

        # we delete comments, whitespaces and tabs
        delete_whitespaces_and_comments(pending_source_code, current_column, current_row)
        # print("Programa sin errores sintacticos.")
        print("--------------------------------")
        print(program_table.to_string())
        ProgramRuleRecognizer.mepa_writer.close_file()
        
        return True
    pass