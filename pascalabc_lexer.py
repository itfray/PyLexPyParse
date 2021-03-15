from lexer.prog_lang_lexer import MultiTokenBounds, MultiTokenBound


CASE_SENSITIVE = False
SKIP_KIND = 'SKIP'
ID_KIND = 'ID'
KEYWORD_KIND = 'KEYWORD'
KEYWORDS = ('and', 'array', 'as', 'auto', 'begin',
            'case', 'class', 'const', 'constructor',
            'destructor', 'div', 'do', 'downto', 'else',
            'end', 'event', 'except', 'extensionmethod', 'file',
            'finalization', 'finally', 'for', 'foreach',
            'function', 'goto', 'if', 'implementation', 'in',
            'inherited', 'initializtion', 'interface', 'is', 'label',
            'lock', 'loop', 'mod', 'nil', 'not', 'of', 'operator',
            'or', 'procedure', 'program', 'property', 'record', 'repeat',
            'raise', 'sealed', 'set', 'sequence', 'shl', 'shr',
            'sizeof', 'template', 'then', 'to', 'try',
            'type', 'typeof', 'until', 'uses', 'using',
            'var', 'while', 'where', 'with', 'xor', 'yield',
            'unit', 'library', 'abstract', 'default', 'external',
            'forward', 'internal', 'on', 'overload', 'override',
            'params', 'private', 'protected', 'public',
            'reintroduce', 'virtual',

            'read', 'write', 'new', 'name',     # context keywords
            'create', 'destroy', 'text', 'static',)

MULTICOMMENT_KIND1 = "MULTI_COMENT1"
MULTICOMMENT_BOUNDS1 = MultiTokenBounds(MultiTokenBound('{', r'{'),
                                        MultiTokenBound('}', r'}'))
MULTICOMMENT_KIND2 = "MULTI_COMENT2"
MULTICOMMENT_BOUNDS2 = MultiTokenBounds(MultiTokenBound('(*', r'\(\*'),
                                        MultiTokenBound('*)', r'\*\)'))
MULTITOKENS = {
    MULTICOMMENT_KIND1: MULTICOMMENT_BOUNDS1,
    MULTICOMMENT_KIND2: MULTICOMMENT_BOUNDS2,
}

SPECIFICATION = [
    (SKIP_KIND, r'[\s\t]+'),
    (ID_KIND, r'[_A-Za-zА-Яа-я&][_A-Za-zА-Яа-я\d]*'),
    ('NUM', r'\d+(\.\d+)?((e|E)(\+|-)?\d+)?'),
    ('HEX_NUM', r'\$[A-Fa-f0-9]+'),
    ('STR', r"'[^']*'"),
    ('RANGE', r'\.\.'),
    ('PTR', r'[\^@]'),
    ('LAMBDA', r'->'),
    ('COND', r'\?\[?'),
    ('LINE_COMMENT', r'//.*'),
    ('OP_ASN', r'[-\+\*/:]='),
    ('OP_ARTHM', r'(\*\*|[-\*\+/])'),
    ('OP_COMP', r'(<>|[<>]?=|[<>])'),
    ('DIRECTIVE', r'{\$.*}'),
    (MULTICOMMENT_KIND1, MULTICOMMENT_BOUNDS1.start.regex),
    (MULTICOMMENT_KIND2, MULTICOMMENT_BOUNDS2.start.regex),
    ('DELIM', r'[:;,()\.\[\]]'),
]

"""
ID: r'''
    [_A-Za-zА-Яа-я]          # first character in identidier
    [_A-Za-zА-Яа-я\d]*       # remaining characters
    ''',

NUM: r'''
      \d+                    # integer part
      (\.\d+)?               # float part
      ((e|E)(\+|-)?\d+)?     # decimal order
      '''

STR: r"
      '[^']*'               # string literal
     "
"""


if __name__ == "__main__":
    from str_reader.file_reader import FileStrReader
    from lexer.lexer import Token
    from lexer.prog_lang_lexer import ProgLangLexer, UnexceptedLexError
    from time import time

    filename = "pascal_code.pas"
    data_reader = FileStrReader(filename, buffering=1024, encoding='utf-8-sig')

    lexer = ProgLangLexer(data_reader=data_reader,
                          specification=SPECIFICATION,
                          skip_kind=SKIP_KIND,
                          keyword_kind=KEYWORD_KIND,
                          id_kind=ID_KIND,
                          keywords=KEYWORDS,
                          multitokens=MULTITOKENS,
                          case_sensitive=CASE_SENSITIVE)

    t0 = time()
    try:
        for token in lexer.tokens():
            print(f"{lexer.num_line}:{lexer.num_column}: " +
                  f"(kind='{lexer.kinds[token.kind]}'; " +
                  f"value='{lexer.lexemes[token.kind][token.value]}'; " +
                  f"id=[{token.kind},{token.value}])")
    except UnexceptedLexError as err:
        print(err)
    print(time() - t0, " sec")