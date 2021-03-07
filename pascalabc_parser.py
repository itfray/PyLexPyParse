
GOAL_NTERM = "program"
END_TERM = '⊥'
EMPTY_TERM = 'ε'
RULES = """
        program -> section_prgrname section_uses sub_sections section_program;


        sub_sections -> sub_sections sub_section| 
                        ε;
        

        sub_section -> section_var |
                       section_const |
                       section_type |
                       section_label;
        

        section_prgrname -> 'program' ID ';' |
                            'unit' ID ';' |
                             ε;
                

        section_uses -> section_uses uses |
                        ε;
        uses -> 'uses' list_ids ';';
        list_ids -> list_ids ',' ID |
                    ID;


        section_var -> 'var' decls;
        decls -> decls decl |
                 decl;
        list_exprs -> list_exprs ',' expr |
                      expr;
        decl -> list_ids ':' ID ';' |
                ID ':' ID ':=' expr ';' |
                ID ':' ID '=' expr ';' |
                ID ':=' expr ';' |
                '(' list_ids ')' ':=' '(' list_exprs ')' ';';


        section_const -> 'const';


        section_type -> 'type';


        section_label -> 'label';
        

        section_program -> block '.';
        block -> 'begin' stmts 'end';
        stmts -> stmts stmt |
                 ε;
        stmt -> ';';
        expr -> ID |
                NUM
        """
RULES = """
        program -> section_prgrname section_uses section_program;
        

        section_prgrname -> 'program' ID ';' |
                            'unit' ID ';' |
                             ε;
                

        section_uses -> section_uses uses |
                        ε;
        uses -> 'uses' list_ids ';';
        list_ids -> list_ids ',' ID |
                    ID;
        
        
        section_program -> block '.';
        block -> 'begin' stmts 'end';
        stmts -> stmts stmt |
                 ε;
        stmt -> ';'
        """
TOKENS = ('ID', 'NUM',)
STAB_FILENAME = "pascalabc_stab.prstab"


if __name__ == "__main__":
    from time import time
    from str_reader.file_reader import FileStrReader
    from lexer.prog_lang_lexer import ProgLangLexer, UnexceptedLexError
    from sparser.sparser import SParser
    from pascalabc_lexer import (CASE_SENSITIVE, SKIP_KIND,
                                 SPECIFICATION, ID_KIND,
                                 KEYWORD_KIND, KEYWORDS,
                                 MULTITOKENS)

    code_filename = "pascal_code.pas"
    data_reader = FileStrReader(code_filename, buffering=1024, encoding='utf-8-sig')
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
    print()

    stab_filename = STAB_FILENAME
    parser = SParser(lexer=lexer,
                     tokens=TOKENS,
                     goal_nterm=GOAL_NTERM,
                     end_term=END_TERM,
                     empty_term=EMPTY_TERM,
                     parsing_of_rules=RULES)
    print(parser.rules)
    print()
    parser.create_sparse_tab()
    t0 = time()
    node = parser.parse()
    print("parsing time: ", time() - t0, " sec")
    print(node)