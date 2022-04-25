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

COMMENT_RECOGNIZER_TEST_CASES=[
        (("{fffdfd fd fdfd}if",[]),("if",[])),
        (("{ }if",[]),("if",[])),
        (("{}if",[]),("if",[]))
    ]

IDENTIFIER_TEST_CASES=[
        (("POLOLO ",[]),(" ",[("TK_identifier","POLOLO")])),
        (("vari ",[]),(" ",[("TK_identifier","vari")])),
        (("program ",[]),(" ",[("TK_identifier","vari")]))
    ]