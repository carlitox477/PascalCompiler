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