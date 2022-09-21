import sys
from utils import read_source_code
from context import get_pascal_program_file_name_path
from syntax_analizer.syntax_analyzer import use_syntax_analyzer

def main() -> None:
    PASCAL_PROGRAM_FILE_NAME = sys.argv[1]
    source_code = read_source_code(get_pascal_program_file_name_path(
        PASCAL_PROGRAM_FILE_NAME))
    use_syntax_analyzer(source_code)
    pass
    


if __name__ == '__main__':
    main()
