from str_reader.str_reader import StrReader
from str_reader.file_reader import FileStrReader
from lexer import Token, ILexer
from lexer.lexer import Lexer


stmt = """\na := 0;\t       \n_b := 123;\n"""
token_specification = [
    ('ID', r'(_|[A-Za-z]){1}(_|[A-Za-z]|\d)*', ()),
    ('NUMBER', r'\d+', ()),
    ('OPASN', r':=', ()),
    ('DELIM', r'[;,()]', ()),
    ('SKIP', r'[ \t]+', ()),
    ('NEWLINE', r'\n', ()),
    ('MISMATCH', r'.', ()),
]


reader = StrReader(stmt)
#reader = FileStrReader('test_code.txt', buffering=1024)
lexer = Lexer(data_reader=reader, specification=token_specification)
for token in lexer.tokens():
    print(f"{lexer.num_line}:{lexer.num_column} : {token}")
print(f"{lexer.num_line} lines...")