from str_reader.str_reader import StrReader
from lexer.prog_lang_lexer import ProgLangLexer, UnexceptedLexError
from sparser.sparser import SParser, print_sparse_tab, Rule
from time import time
import os.path


CASE_SENSITIVE = False
SKIP_KIND = 'SKIP'
ID_KIND = 'ID'

SPECIFICATION = [
    (SKIP_KIND, r'[\s\t]+'),
    (ID_KIND, r'[_A-Za-zА-Яа-я&][_A-Za-zА-Яа-я\d]*'),
    ('OP_ARTHM', r'(\*\*|[-\*\+/])'),
    ('DELIM', r'[:;,()\.\[\]]'),
]

# stmt = """ D * A * (B + C * K) - G"""
stmt = "A + B * D"
data_reader = StrReader(stmt)
lexer = ProgLangLexer(data_reader=data_reader,
                      specification=SPECIFICATION,
                      skip_kind=SKIP_KIND,
                      id_kind=ID_KIND,
                      case_sensitive=CASE_SENSITIVE)
t0 = time()
try:
    for token in lexer.tokens():
        print(f"{lexer.num_line}:{lexer.num_column}: {token}")
except UnexceptedLexError as err:
    print(err)
print(time() - t0, " sec")

GOAL_NTERM = "E"
END_TERM = '⊥'
RULES = """
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

stab_filename = "stab_file.prstab"
parser = SParser(lexer=lexer,
                 tokens=TOKENS,
                 goal_nterm=GOAL_NTERM,
                 end_term=END_TERM,
                 parsing_of_rules=RULES)
if os.path.exists(stab_filename) and\
   os.path.isfile(stab_filename):
    parser.read_stab_from_file(stab_filename)
else:
    parser.create_sparse_tab()
    parser.write_stab_to_file(stab_filename)
print_sparse_tab(parser._SParser__sparse_tab, 6)
node = parser.parse()
print(node)