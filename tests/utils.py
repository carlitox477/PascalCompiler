WHITE_SPACE_RECOGNIZER_TEST_CASES=[
        (("    if ",[]),("if ",[])),
        (("\tif ",[]),("if ",[])),
        (("\nif ",[]),("if ",[])),
        ((" \t \n\n\n\t   \t \nif ",[]),("if ",[])),
    ]

COMMENT_RECOGNIZER_TEST_CASES=[
        (("{fffdfd fd fdfd}if",[]),("if",[])),
        (("{ }if",[]),("if",[])),
        (("{}if",[]),("if",[]))
    ]

IDENTIFIER_TEST_CASES=[
        (("POLOLO ",[]),(" ",[("TK_identifier","POLOLO")])),
        (("vari ",[]),(" ",[("TK_identifier","vari")])),
        (("program ",[]),(" ",["TK_program"])),
        (("integer ",[]),(" ",[('TK_datatype','integer')])),
        (("boolean ",[]),(" ",[('TK_datatype','boolean')])),
        (("true ",[]),(" ",[('TK_boolean_literal',1)])),
        (("false ",[]),(" ",[('TK_boolean_literal',0)]))
    ]

NUMBER_TEST_CASES=[
    (("0 ",[]),("if",[])),
    (("123 ",[]),("if",[])),
    (("0023232 ",[]),("if",[]))
]

SPECIAL_SYMBOL_CASES=[
    ((":= ",[]),(" ",["TK_assignment"])),
    ((": ",[]),(" ",["TK_colon"])),
    ((", ",[]),(" ",["TK_comma"])),
    (("; ",[]),(" ",["TK_semicolon"])),
    ((". ",[]),(" ",["TK_dot"]))
]

OPERATOR_TEST_CASES=[
    (("+ ",[]),(" ",[("TK_arithOp","ADD")])),
    (("- ",[]),(" ",[("TK_arithOp","SUB")])),
    (("* ",[]),(" ",[("TK_arithOp","MUL")])),
    (("/ ",[]),(" ",[("TK_arithOp","DIV")])),
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

