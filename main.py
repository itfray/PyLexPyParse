from str_reader.str_reader import StrReader
from lexer import Token, ILexer
from lexer.lexer import Lexer

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
lexer = Lexer(data_reader=reader, specification=token_specification)

for token in lexer.tokens():
    print(token)