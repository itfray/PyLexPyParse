from str_reader.str_reader import StrReader
from lexer.prog_lang_lexer import ProgLangLexer
from sparser.sparser import SParser, print_sparse_tab
from time import time


CASE_SENSITIVE = False
SKIP_KIND = 'SKIP'
ID_KIND = 'ID'

SPECIFICATION = [
    (SKIP_KIND, r'[\s\t]+'),
    (ID_KIND, r'[_A-Za-zА-Яа-я&][_A-Za-zА-Яа-я\d]*'),
    ('OP_ARTHM', r'(\*\*|[-\*\+/])'),
    ('DELIM', r'[:;,()\.\[\]]'),
]

stmt = """ A * B + C"""
data_reader = StrReader(stmt)
lexer = ProgLangLexer(data_reader=data_reader,
                      specification=SPECIFICATION,
                      skip_kind=SKIP_KIND,
                      id_kind=ID_KIND,
                      case_sensitive=CASE_SENSITIVE)
# t0 = time()
# try:
#     for token in lexer.tokens():
#         print(f"{lexer.num_line}:{lexer.num_column}: {token}")
# except UnexceptedLexemeError as err:
#     print(err)
# print(time() - t0, " sec")

GOAL_NTERM = "E'"
END_TERM = '⊥'
RULES = """
         E' -> E;
         E -> E '+' T |
              E '-' T |
              T;
         T -> T '*' F |
              T '/' F |
              F;
         F -> '(' E ')' |
              ID
        """
TOKENS = ('ID',)

parser = SParser(lexer=lexer,
                 tokens=TOKENS,
                 goal_nterm=GOAL_NTERM,
                 end_term=END_TERM)
parser.parse_rules_from(RULES)

from sparser.sparser import first_term
print(first_term(parser.rules, parser.is_terminal, "F"))
# parser.create_sparse_tab()
# print_sparse_tab(parser.sparse_tab, 10)
# node = parser.parse()
# print(node)