from str_reader.str_reader import StrReader
from str_reader.file_reader import FileStrReader
from lexer.prog_lang_lexer import ProgLangLexer
from time import time


SKIP_KIND = 'SKIP'
ID_KIND = 'ID'
KEYWORD_KIND = 'KEYWORD'
KEYWORDS = ('if', 'then', 'begin', 'end')
SPECIFICATION = [
    (ID_KIND, r'(_|[A-Za-z]){1}(_|[A-Za-z]|\d)*'),
    ('NUM', r'(\+|-)?\d+(\.\d+)?((e|E)(\+|-)?\d+)?'),
    ('OPASN', r':='),
    (SKIP_KIND, r'[\s\t]+'),
    ('DELIM', r'[;,()]'),
]

"""
ID: r'''
    (_|[A-Za-z]){1}             # first character in identidier
    (_|[A-Za-z]|\d)*            # remaining characters
    ''',

NUMBER: r'''
         (\+|-)?                # sign of number
         \d+                    # integer part
         (\.\d+)?               # float part
         ((e|E)(\+|-)?\d+)?     # decimal order
         '''
"""


if __name__ == "__main__":
    # filename = "test_code.txt"
    # data_reader = FileStrReader(filename, buffering=1024)

    stmt = """
        a := 0;
        if (a) then
            _b := -123.0;
        result := +3.3E+6;
    """
    data_reader = StrReader(stmt)

    lexer = ProgLangLexer(data_reader=data_reader, specification=SPECIFICATION,
                          skip_kind=SKIP_KIND, keyword_kind=KEYWORD_KIND,
                          id_kind=ID_KIND, keywords=KEYWORDS)
    t0 = time()
    for token in lexer.tokens():
        print(f"{lexer.num_line}:{lexer.num_column}: {token}")
    print(time() - t0, " sec")