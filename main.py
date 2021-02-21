from str_reader.file_reader import FileStrReader
from lexer.prog_lang_lexer import ProgLangLexer, UnexceptedLexemeError
from time import time
import pascalabc_lexer as lexconf




filename = "pascal_code.pas"
data_reader = FileStrReader(filename, buffering=1024, encoding='utf-8-sig')

lexer = ProgLangLexer(data_reader=data_reader,
                      specification=lexconf.SPECIFICATION,
                      skip_kind=lexconf.SKIP_KIND,
                      keyword_kind=lexconf.KEYWORD_KIND,
                      id_kind=lexconf.ID_KIND,
                      keywords=lexconf.KEYWORDS,
                      multitokens=lexconf.MULTITOKENS,
                      case_sensitive=lexconf.CASE_SENSITIVE)

t0 = time()
try:
    for token in lexer.tokens():
        print(f"{lexer.num_line}:{lexer.num_column}: {token}")
except UnexceptedLexemeError as err:
    print(err)
print(time() - t0, " sec")