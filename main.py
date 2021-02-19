from str_reader.str_reader import StrReader
from str_reader.file_reader import FileStrReader
from lexer import Token, ILexer
from lexer.lexer import Lexer
import time

stmt = """
    a := 0;\t       
    _b := 123;
"""
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

t0 = time.time()
lines = 1
for token in lexer.tokens():
    if token.kind == "NEWLINE":
        lines += 1
    print(token, end="; ")
    print("line: ", lines)
print(time.time() - t0, " sec")
print(lines)