
GOAL_NTERM = "program"
END_TERM = '⊥'
EMPTY_TERM = 'ε'
RULES = """
        program -> section_prgrname section_uses sub_sections block '.';


        sub_sections -> sub_sections sub_section |
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


        section_var -> 'var' vars;
        vars -> vars var ';' |
                var ';';
        var -> var_decl |
               vars_decl |
               var_decl '=' expr |
               var_decl ':=' expr |
               ID ':=' expr |
               '(' list_ids2 ')' ':=' expr;
        list_ids2 -> list_ids ',' ID;
        
        vars_decl -> list_ids2 ':' var_type;
        var_decl -> ID ':' var_type;
        
        var_type -> '(' list_var_types2 ')' |
                    range |
                    'array' 'of' var_type |
                    'array' '[' arr_inds ']' 'of' var_type |
                    ID;
        list_var_types ->  list_var_types ',' var_type |
                           var_type;
        list_var_types2 -> list_var_types ',' var_type;
        
        arr_inds -> arr_rngs |
                    arr_commas;
        arr_rngs -> arr_rngs ',' range |
                    range;
        arr_commas -> arr_commas ',' |
                      ',';


        section_const -> 'const' consts;
        consts -> consts const ';' |
                  const ';';
        const -> ID '=' expr |
                 var_decl '=' expr;
                 

        section_type -> 'type';


        section_label -> 'label' labels ';';
        labels -> labels ',' label |
                  label;
        label -> ID |
                 NUM;


        block -> 'begin' stmts 'end';
        stmts -> stmts ';' stmt |
                 stmt;
        stmt -> inner_var |
                asgn |
                block |
                if |
                case |
                for |
                loop |
                foreach |
                ε;
        
        if -> 'if' expr 'then' stmt |
              'if' expr 'then' stmt 'else' stmt;
        
        inner_var -> 'var' var |
                     '(' list_idvars ')' ':=' expr;
        list_idvars -> list_idvars ',' 'var' ID |
                       'var' ID;
        
        asgn -> ptr ':=' expr |
                ptr '+=' expr |
                ptr '-=' expr |
                ptr '*=' expr |
                ptr '/=' expr |
                '(' list_ptrs ')' ':=' expr;
        list_ptrs -> list_ptrs ',' ptr |
                     ptr;
        
        case -> 'case' expr 'of' case_list 'end' |
                'case' expr 'of' case_list 'else' stmts 'end';
        case_list -> case_list ';' case_element |
                     case_element;
        case_element -> const_expr ':' stmt |
                        ε;
        
        for -> 'for' for_var 'to' expr 'do' stmt |
               'for' for_var 'downto' expr 'do' stmt;
        for_var -> var_decl ':=' expr |
                   ID ':=' expr |
                   'var' ID ':=' expr;
        
        loop -> 'loop' expr 'do' stmt;
        
        foreach -> 'foreach' foreach_var 'in' expr 'do' stmt;
        foreach_var -> ID |
                       'var' ID |
                       var_decl;

        expr -> tuple;
        tuple -> '(' list_exprs ')' |
                 ternar;
        list_exprs -> list_exprs ',' expr |
                      expr;
        ternar -> ternar '?' expr ':' expr |
                  rel;
        rel -> rel '<' add |
               rel '<=' add |
               rel '>' add |
               rel '>=' add |
               rel '<>' add |
               rel '=' add |
               add;
        add -> add '+' mul |
               add '-' mul |
               add 'or' mul |
               add 'xor' mul |
               mul;
        mul -> mul '*' unar |
               mul '/' unar |
               mul 'div' unar |
               mul 'mod' unar |
               mul 'and' unar |
               mul 'shl' unar |
               mul 'shr' unar |
               mul 'as' unar |
               mul 'is' unar |
               unar;
        unar -> '@' ptr |
                'not' ptr |
                '+' ptr |
                '-' ptr |
                'new' ptr |
                ptr;
        ptr -> iter ptr_op |
               iter;
        ptr_op -> ptr_op '^' |
                  ε;
        iter -> sel iter_op |
                sel;
        iter_op -> iter_op '[' slice ']' |
                   iter_op '?[' slice ']' |
                   ε;
        slice -> slice ':' slice |
                 expr |
                 ε;
        sel -> sel '.' ID |
               factor;
        factor -> '(' expr ')' |
                  ID |
                  const_expr;
        
        const_expr -> NUM |
                      STR |
                      range;
                  
        range -> rng_brdr '..' rng_brdr;
        rng_brdr -> NUM |
                    ID |
                    STR
        """
TOKENS = ('ID', 'NUM', 'STR',)
STAB_FILENAME = "pascalabc_stab.prstab"


if __name__ == "__main__":
    from time import time
    import os
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

    parser = SParser(lexer=lexer)
    t0 = time()
    if os.path.exists(STAB_FILENAME) and \
            os.path.isfile(STAB_FILENAME):
        parser.read_stab_from_file(STAB_FILENAME)
        print("sparse table readed")
    else:
        parser.tokens = TOKENS
        parser.goal_nterm = GOAL_NTERM
        parser.end_term = END_TERM
        parser.empty_term = EMPTY_TERM
        parser.parse_rules(RULES)
        parser.create_sparse_tab()
        parser.write_stab_to_file(STAB_FILENAME)
        print("sparse table created")
    print("time for sparse table: ", time() - t0, " sec")
    print()
    print("parser's rules: ")
    for rule in parser.rules:
        print(rule)
    print()
    t0 = time()
    node = parser.parse()
    print("parsing time: ", time() - t0, " sec")
    print(node)