from .utils import delete_whitespaces_and_comments, match_token
from .gr_declaration_rules import DeclarationRulesRecognizer
from .semantic_analizer import SymbolTable


class ProgramRuleRecognizer:
    @staticmethod
    def recognize_program_rule(pending_source_code: str, current_column:int, current_row:int)->bool:
        # Add program name to symbol table
        pending_source_code,current_column, current_row,_,_ = match_token('TK_program',pending_source_code,current_column, current_row)
        pending_source_code,current_column, current_row,program_identifier_token,_  = match_token('TK_identifier',pending_source_code,current_column, current_row)
        pending_source_code,current_column, current_row,_,_  = match_token('TK_semicolon',pending_source_code,current_column, current_row)

        program_table = SymbolTable(program_identifier_token.getAttribute("name"),"PROGRAM",0,None,{},0,current_row)

        pending_source_code,current_column, current_row = DeclarationRulesRecognizer.verify_block_rule(pending_source_code,current_column, current_row, program_table)
        pending_source_code,current_column, current_row,_,_ = match_token('TK_dot',pending_source_code,current_column, current_row)
        
        # we delete comments, whitespaces and tabs
        delete_whitespaces_and_comments(pending_source_code, current_column, current_row)
        print("Programa sin errores sintacticos.")
        print("--------------------------------")
        print(program_table.to_string())
        
        return True
    pass