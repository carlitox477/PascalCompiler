WHITE_SPACE_RECOGNIZER_TEST_CASES=[
        (("    if ",[]),("if ",[])),
        (("\tif ",[]),("if ",[])),
        (("\nif ",[]),("if ",[])),
        ((" \t \n\n\n\t   \t \nif ",[]),("if ",[])),
        (("Hello ",[]),("Hello ",[]))
    ]

COMMENT_RECOGNIZER_TEST_CASES=[
        (("{fffdfd fd fdfd}if",[]),("if",[])),
        (("{ }if",[]),("if",[])),
        (("{}if",[]),("if",[])),
        (("Hello ",[]),("Hello ",[]))
    ]

IDENTIFIER_TEST_CASES=[
        (("program ",[]),(" ",["TK_program"])),
        (("function ",[]),(" ",["TK_function"])),
        (("procedure ",[]),(" ",["TK_procedure"])),
        (("var ",[]),(" ",["TK_var"])),
        (("begin ",[]),(" ",["TK_begin"])),
        (("end ",[]),(" ",["TK_end"])),
        (("if ",[]),(" ",["TK_if"])),
        (("then ",[]),(" ",["TK_then"])),
        (("else ",[]),(" ",["TK_else"])),
        (("do ",[]),(" ",["TK_do"])),
        (("and ",[]),(" ",["TK_and"])),
        (("or ",[]),(" ",["TK_or"])),
        (("read ",[]),(" ",["TK_read"])),
        (("write ",[]),(" ",["TK_write"])),
        (("not ",[]),(" ",["TK_not"])),
        (("integer ",[]),(" ",[('TK_datatype','integer')])),
        (("boolean ",[]),(" ",[('TK_datatype','boolean')])),
        (("true ",[]),(" ",[('TK_boolean_literal',1)])),
        (("false ",[]),(" ",[('TK_boolean_literal',0)])),
        
        (("POLOLO ",[]),(" ",[("TK_identifier","POLOLO")])),
        (("vari ",[]),(" ",[("TK_identifier","vari")])),
        (("_vari ",[]),(" ",[("TK_identifier","_vari")])),
        (("___vari ",[]),(" ",[("TK_identifier","___vari")])),
        (("_vari232 ",[]),(" ",[("TK_identifier","_vari232")])),
        (("___va23r32i ",[]),(" ",[("TK_identifier","___va23r32i")])),
        
        (("0 ",[]),("0 ",[])),
    ]

NUMBER_TEST_CASES=[
    (("0 ",[]),(" ", [("TK_number","0")])),
    (("00 ",[]),(" ",[("TK_number","0")])),
    (("1 ",[]),(" ",[("TK_number","1")])),
    (("123 ",[]),(" ",[("TK_number","123")])),
    (("0023232 ",[]),(" ",[("TK_number","23232")])),
    (("Hello ",[]),("Hello ",[]))
]

SPECIAL_SYMBOL_CASES=[
    ((":= ",[]),(" ",["TK_assignment"])),
    ((": ",[]),(" ",["TK_colon"])),
    ((", ",[]),(" ",["TK_comma"])),
    (("; ",[]),(" ",["TK_semicolon"])),
    ((". ",[]),(" ",["TK_dot"])),
    (("Hello ",[]),("Hello ",[]))
]

ARITHMETICAL_OPERATOR_TEST_CASES=[
    (("+ ",[]),(" ",[("TK_arithOp","ADD")])),
    (("- ",[]),(" ",[("TK_arithOp","SUB")])),
    (("* ",[]),(" ",[("TK_arithOp","MUL")])),
    (("/ ",[]),(" ",[("TK_arithOp","DIV")])),
    (("Hello ",[]),("Hello ",[]))
]

RELATIONAL_OPERATOR_TEST_CASES=[
    (("= ",[]),(" ",[("TK_relOp","EQ")])),
    (("< ",[]),(" ",[("TK_relOp","LT")])),
    (("<> ",[]),(" ",[("TK_relOp","DIF")])),
    (("<= ",[]),(" ",[("TK_relOp","LEQ")])),
    (("> ",[]),(" ",[("TK_relOp","GT")])),
    ((">= ",[]),(" ",[("TK_relOp","GEQ")])),
    (("Hello ",[]),("Hello ",[]))
]

PARENTHESIS_TEST_CASES=[
    (("( ",[]),(" ",[("TK_parenthesis","OPPAR")])),
    ((") ",[]),(" ",[("TK_parenthesis","CLPAR")])),
    (("Hello ",[]),("Hello ",[])),
]

