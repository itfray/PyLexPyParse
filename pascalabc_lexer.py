from str_reader.str_reader import StrReader
from str_reader.file_reader import FileStrReader
from lexer.prog_lang_lexer import ProgLangLexer
from time import time


CASE_SENSITIVE = False
SKIP_KIND = 'SKIP'
ID_KIND = 'ID'
KEYWORD_KIND = 'KEYWORD'
KEYWORDS = ('and', 'array', 'as', 'begin',
            'break', 'case', 'class', 'const',
            'constructor', 'continue', 'destructor', 'div',
            'do', 'downto', 'else', 'end', 'event', 'except',
            'extensionmethod', 'file', 'finalization', 'finally',
            'for', 'foreach', 'forward', 'function', 'goto',
            'if', 'implementation', 'in', 'inherited', 'initializtion',
            'interface', 'is', 'label', 'lock', 'loop', 'mod',
            'nil', 'not', 'of', 'operator', 'or', 'private', 'procedure', 'program',
            'property', 'protected', 'public', 'record', 'repeat',
            'raise', 'sealed', 'set', 'sequence', 'shl', 'shr',
            'sizeof', 'template', 'then', 'to', 'type', 'typeof',
            'unit', 'until', 'uses', 'using', 'var', 'while', 'where', 'with',
            'xor', 'abstract', 'default', 'external', 'internal', 'on',
            'overload', 'override', 'params', 'read', 'reintroduce',
            'virtual', 'write')
SPECIFICATION = [
    (SKIP_KIND, r'[\s\t]+'),
    (ID_KIND, r'(_|\w){1}(_|\w|\d)*'),
    ('NUM', r'(\+|-)?\d+(\.\d+)?((e|E)(\+|-)?\d+)?'),
    ('HEX_NUM', r'\$[A-Fa-f0-9]+'),
    ('OPASN', r':='),
    ('OPARITHM', r'[-\*\+/]'),
    ('DELIM', r'[:;,()\.]'),
]

"""
ID: r'''
    (_|\w){1}                # first character in identidier
    (_|\w|\d)*               # remaining characters
    ''',

NUM: r'''
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
    program test;
    begin
        a := 0;
        if (a) then
            _b := -123.0;
        result := +3.3E+6;
        kek := $C000fd;
        result := kek / result;
    end.
    """
    data_reader = StrReader(stmt)

    lexer = ProgLangLexer(data_reader=data_reader, specification=SPECIFICATION,
                          skip_kind=SKIP_KIND, keyword_kind=KEYWORD_KIND,
                          id_kind=ID_KIND, keywords=KEYWORDS,
                          case_sensitive=CASE_SENSITIVE)
    t0 = time()
    for token in lexer.tokens():
        print(f"{lexer.num_line}:{lexer.num_column}: {token}")
    print(time() - t0, " sec")