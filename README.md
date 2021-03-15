# PyLexPyParse

## Overview

PyLexPyParse is a Python library for creating lexers and parsers. 
Lexical analyzer recognizes lexical patterns in text.
Parser converts an annotated context-free grammar into a deterministic 
LR parser employing LALR(1) parser tables.
You can use PyLexPyParse to develop a wide range of lexical analyzers and parsers,
from those used in simple desk calculators to complex programming languages.

## Requirements

- Python `^3.7.4`
- Pip `^19.0.3`

## Installation

```bash
git clone https://github.com/itfray/PyLexPyParse.git /your_project_path
cd /your_project_path
```

### Windows

```bash
python -m pip install -r requirements.txt
```

### Linux and MacOS

```bash
python3 -m pip install -r requirements.txt
```

## Usage

### String reader

```python
from str_reader.str_reader import StrReader

stmt = "A + B * D"
data_reader = StrReader(stmt)

data = data_reader.read(3)
data_reader.reset()
print(data)

data = data_reader.read(5)
print(data)
```
```
A +
A + B
```
```python
from str_reader.file_reader import FileStrReader

filename = "hello.txt"
data_reader = FileStrReader(filename, buffering=1024, encoding='utf-8')

data = data_reader.read(5)
print(data)
```
```
Hello
```

### Lexer

```python
from str_reader.str_reader import StrReader
from lexer.lexer import Lexer

SPECIFICATION = [
    ('SKIP', r'[\s\t]+'),
    ('ID', r'[_A-Za-zА-Яа-я&][_A-Za-zА-Яа-я\d]*'),
    ('OP_ARTHM', r'(\*\*|[-\*\+/])'),
    ('DELIM', r'[:;,()\.\[\]]'),
]

stmt = "A + B * D"

data_reader = StrReader(stmt)

lexer = Lexer(data_reader=data_reader,
              specification=SPECIFICATION)

for token in lexer.tokens():
    print(f"{lexer.num_line}:{lexer.num_column}: " +
        f"(kind='{lexer.kinds[token.kind]}'; " +
        f"value='{lexer.lexemes[token.kind][token.value]}'; " +
        f"id=[{token.kind},{token.value}])")
```
```
1:1: (kind='ID'; value='A'; id=[0,0])
1:2: (kind='SKIP'; value=' '; id=[1,0])
1:3: (kind='OP_ARTHM'; value='+'; id=[2,0])
1:4: (kind='SKIP'; value=' '; id=[1,0])
1:5: (kind='ID'; value='B'; id=[0,1])
1:6: (kind='SKIP'; value=' '; id=[1,0])
1:7: (kind='OP_ARTHM'; value='*'; id=[2,1])
1:8: (kind='SKIP'; value=' '; id=[1,0])
1:9: (kind='ID'; value='D'; id=[0,2])
```

```python
from str_reader.str_reader import StrReader
from lexer.prog_lang_lexer import ProgLangLexer, UnexceptedLexError

CASE_SENSITIVE = False
SKIP_KIND = 'SKIP'
ID_KIND = 'ID'

SPECIFICATION = [
    (SKIP_KIND, r'[\s\t]+'),
    (ID_KIND, r'[_A-Za-zА-Яа-я&][_A-Za-zА-Яа-я\d]*'),
    ('OP_ARTHM', r'(\*\*|[-\*\+/])'),
    ('DELIM', r'[:;,()\.\[\]]'),
]

stmt = "A + B * D"

data_reader = StrReader(stmt)

lexer = ProgLangLexer(data_reader=data_reader,
                      specification=SPECIFICATION,
                      skip_kind=SKIP_KIND,
                      id_kind=ID_KIND,
                      case_sensitive=CASE_SENSITIVE)

try:
    for token in lexer.tokens():
        print(f"{lexer.num_line}:{lexer.num_column}: " +
              f"(kind='{lexer.kinds[token.kind]}'; " +
              f"value='{lexer.lexemes[token.kind][token.value]}'; " +
              f"id=[{token.kind},{token.value}])")
except UnexceptedLexError as err:
    print(err)
```
```
1:1: (kind='ID'; value='a'; id=[0,0])
1:3: (kind='OP_ARTHM'; value='+'; id=[1,0])
1:5: (kind='ID'; value='b'; id=[0,1])      
1:7: (kind='OP_ARTHM'; value='*'; id=[1,1])
1:9: (kind='ID'; value='d'; id=[0,2])
```

### Parser

```python
from str_reader.str_reader import StrReader
from lexer.prog_lang_lexer import ProgLangLexer
from sparser.sparser import SParser
from work_with_syntax_tree import print_tokens_syntax_tree

CASE_SENSITIVE = False
SKIP_KIND = 'SKIP'
ID_KIND = 'ID'

SPECIFICATION = [
    (SKIP_KIND, r'[\s\t]+'),
    (ID_KIND, r'[_A-Za-zА-Яа-я&][_A-Za-zА-Яа-я\d]*'),
    ('OP_ARTHM', r'(\*\*|[-\*\+/])'),
    ('DELIM', r'[:;,()\.\[\]]'),
]

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

stmt = "A + B * D"
data_reader = StrReader(stmt)
lexer = ProgLangLexer(data_reader=data_reader,
                      specification=SPECIFICATION,
                      skip_kind=SKIP_KIND,
                      id_kind=ID_KIND,
                      case_sensitive=CASE_SENSITIVE)

parser = SParser(lexer=lexer,
                 tokens=TOKENS,
                 goal_nterm=GOAL_NTERM,
                 end_term=END_TERM,
                 parsing_of_rules=RULES)

parser.create_sparse_tab()

node = parser.parse()

print_tokens_syntax_tree(parser, lexer, node)
```
```
 node : E
    a
    +
    node : T
        b
        *
        d
```

## License

MIT. See [LICENSE](LICENSE).