
GOAL_NTERM = "program"
END_TERM = '⊥'
EMPTY_TERM = 'ε'
RULES = """
        program -> section_program section_uses;
        section_program -> 'program' ID ';' |
                            ε;
        section_uses -> usess |
                        ε;
        usess -> usess uses|
                 uses;
        uses -> 'uses' modules ';';
        modules -> modules ',' module |
                   module;
        module -> ID
        """
# RULES = """
#         program -> section_program;
#         section_program -> 'program' ID ';' section_uses |
#                             section_uses;
#         section_uses -> usess;
#         usess -> usess uses|
#                  uses;
#         uses -> 'uses' modules ';';
#         modules -> modules ',' module |
#                    module;
#         module -> ID
#         """
TOKENS = ('ID',)
STAB_FILENAME = "pascalabc_stab.prstab"


if __name__ == "__main__":
    from time import time
    from str_reader.str_reader import StrReader
#    from str_reader.file_reader import FileStrReader
    from lexer.prog_lang_lexer import ProgLangLexer, UnexceptedLexError
    from sparser.sparser import SParser, print_sparse_tab
    from pascalabc_lexer import (CASE_SENSITIVE, SKIP_KIND,
                                 SPECIFICATION, ID_KIND,
                                 KEYWORD_KIND, KEYWORDS,
                                 MULTITOKENS)

#    code_filename = "pascal_code.pas"
#    data_reader = FileStrReader(code_filename, buffering=1024, encoding='utf-8-sig')
    stmt = """
           program train;
           """
#     stmt = """
#            program train;
#            uses GraphABC, JopaSuka;
#            uses Nahui;
#            """
    data_reader = StrReader(stmt)
    lexer = ProgLangLexer(data_reader=data_reader,
                          specification=SPECIFICATION,
                          skip_kind=SKIP_KIND,
                          keyword_kind=KEYWORD_KIND,
                          id_kind=ID_KIND,
                          keywords=KEYWORDS,
                          multitokens=MULTITOKENS,
                          case_sensitive=CASE_SENSITIVE)
    # t0 = time()
    # try:
    #     for token in lexer.tokens():
    #         print(f"{lexer.num_line}:{lexer.num_column}: {token}")
    # except UnexceptedLexError as err:
    #     print(err)
    # print("lexical analyze: ", time() - t0, " sec")
    # print()

    stab_filename = STAB_FILENAME
    parser = SParser(lexer=lexer,
                     tokens=TOKENS,
                     goal_nterm=GOAL_NTERM,
                     end_term=END_TERM,
                     empty_term=EMPTY_TERM,

                     parsing_of_rules=RULES)
    print(parser.rules)
    parser.create_sparse_tab()
    t0 = time()
    node = parser.parse()
    print("parsing time: ", time() - t0, " sec")
    print(node)