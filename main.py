from str_reader.str_reader import StrReader
from lexer import Token, ILexer
from lexer.lexer import Lexer

stmt = "a:=0;"
token_specification = [
    ('ID', '(_|[A-Za-z]){1}(_|[A-Za-z]|\d)*', ()),
    ('NUMBER', '\d+', ()),
    ('OPASN', ':=', ()),
    ('DELIM', '[;,()]', ()),
]

reader = StrReader(stmt)
lexer = Lexer(data_reader=reader, specification=token_specification)

for token in lexer.tokens():
    print(token)