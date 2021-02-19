from str_reader.str_reader import StrReader
from str_reader.file_reader import FileStrReader
from lexer.prog_lang_lexer import ProgLangLexer
from time import time



skip_kind = 'SKIP'
id_kind = 'ID'
keyword_kind = 'KEYWORD'
keywords = ('if', 'then', 'begin', 'end')
token_specification = [
    ('ID', r'(_|[A-Za-z]){1}(_|[A-Za-z]|\d)*', ()),
    ('NUMBER', r'\d+', ()),
    ('OPASN', r':=', ()),
    ('DELIM', r'[;,()]', ()),
    ('SKIP', r'[\s\t]+', ()),
    ('MISMATCH', r'.', ())
]

stmt = """
    a := 0;
    if a < 0 then
        _b := 123;
"""
reader = StrReader(stmt)

# filename = "test_code.txt"
# reader = FileStrReader(filename, buffering=1024)

lexer = ProgLangLexer(data_reader=reader, specification=token_specification,
                      skip_kind=skip_kind, keyword_kind=keyword_kind,
                      id_kind=id_kind, keywords=keywords)
t0 = time()
for token in lexer.tokens():
    print(f"{lexer.num_line}:{lexer.num_column}: {token}")
print(time() - t0, " sec")