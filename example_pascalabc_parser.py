
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
        uses -> 'uses' list_sel_id ';';
        list_sel_id -> list_sel_id ',' sel_id |
                       sel_id;


        section_var -> 'var' vars funcs |
                       'var' vars |
                       'var' funcs;
        vars -> vars var ';' |
                var ';';
        var -> var_decl |
               vars_decl |
               var_decl '=' expr |
               var_decl ':=' expr |
               ID ':=' expr |
               '(' list_ids2 ')' ':=' expr;
        list_ids -> list_ids ',' ID |
                    ID;
        list_ids2 -> list_ids ',' ID;
        
        vars_decl -> list_ids2 ':' var_type;
        var_decl -> ID ':' var_type;
        
        var_type -> tuple_type |
                    range |
                    arr_type |
                    set_type |
                    file_type |
                    seq_type |
                    ptr_type |
                    record |
                    func_type |
                    ID;
        list_var_types ->  list_var_types ',' var_type |
                           var_type;
        list_var_types2 -> list_var_types ',' var_type;
        
        arr_type -> 'array' 'of' var_type |
                    'array' '[' arr_inds ']' 'of' var_type;
        arr_inds -> arr_rngs |
                    arr_commas;
        arr_rngs -> arr_rngs ',' range |
                    range;
        arr_commas -> arr_commas ',' |
                      ',';
        
        set_type -> 'set' 'of' var_type;
        
        file_type -> 'file' 'of' var_type |
                     'file' |
                     'text';
                     
        ptr_type -> '^' var_type;
        
        seq_type -> 'sequence' 'of' var_type;
        
        tuple_type -> '(' list_var_types2 ')';
        
        func_type -> 'procedure' func_params |
                     'function' func_params ':' var_type |
                     '(' ')' '->' var_type |
                     var_type '->' var_type |
                     '(' list_var_types2 ')' '->' var_type |
                     '(' ')' '->' '(' ')' |
                     var_type '->' '(' ')' |
                     '(' list_var_types2 ')' '->' '(' ')';
                     
        
        funcs -> funcs func ';' |
                 func ';';
        func -> func_hdr func_body;

        func_hdr -> 'procedure' sel_id func_params |
                    'function' sel_id func_params ':' var_type;
        
        func_body ->  method_body |
                     ';' 'forward' |
                     ';' 'external' STR 'name' STR;
        
        func_params -> '(' list_fparams ')' |
                        '(' ')' |
                        ε;
        list_fparams -> list_fparams1 ';' list_fparams2 |
                        list_fparams1 ';' fparams3 |
                        list_fparams1 |
                        list_fparams2 |
                        fparams3;
        list_fparams1 -> list_fparams1 ';' fparams1 |
                         fparams1;
        list_fparams2 -> list_fparams2 ';' fparams2 |
                         fparams2;
        fparams1 -> 'var' fparams1_decl |
                    'const' fparams1_decl |
                    fparams1_decl;
        fparams2 -> 'var' fparams2_decl |
                   'const' fparams2_decl |
                    fparams2_decl;
        fparams3 -> 'params' fparams3_decl;
        fparams1_decl -> var_decl |
                         vars_decl;
        fparams1_decls -> fparams1_decls ';' fparams1_decl |
                          fparams1_decl;
                          
        fparams2_decl -> var_decl ':=' expr;
        fparams3_decl -> ID ':' 'array' 'of' var_type;
        
        methods -> methods method ';' |
                   method ';';
        method -> method_hdr method_body |
                  prop_hdr prop_body;

        method_hdr -> 'constructor' 'create' func_params |
                      'constructor' func_params |
                      'destructor' 'destroy' |
                       func_hdr;

        method_body -> ';' sub_sections block |
                       ';' block |
                       ':=' expr;
               
        prop_hdr -> 'property' var_decl |
                    'property' ind_prop_decl;
        
        ind_prop_decl -> ID '[' fparams1_decls ']' ':' var_type;
        
        prop_body -> 'read' expr 'write' stmt |
                     'write' stmt 'read' expr |
                     'read' expr |
                     'write' stmt;


        section_const -> 'const' consts;
        consts -> consts const ';' |
                  const ';';
        const -> ID '=' expr |
                 var_decl '=' expr;
                 

        section_type -> 'type' types;
        types -> types type ';' |
                 type ';';
        type -> ID '=' var_type |
                ID '=' class;
        

        section_label -> 'label' labels ';';
        labels -> labels ',' label |
                  label;
        label -> ID |
                 NUM;
                 
                 
        record -> 'record' obj_sections 'end';
        obj_sections -> obj_sections obj_section |
                        ε;
        obj_section -> access_mod obj_section_content |
                       obj_section_content;
        access_mod -> 'public' |
                      'protected' |
                      'private' |
                      'internal';
        obj_section_content -> vars methods |
                               vars |
                               methods;
        class -> class_mods 'class' base_class obj_sections 'end' |
                 class_mods 'class' base_class;
        base_class -> '(' list_sel_id ')' |
                       ε;
        class_mods -> class_mods class_mod |
                      ε;
        class_mod -> 'sealed' |
                     'auto' |
                     'abstract';


        block -> 'begin' stmts 'end';
        stmts -> stmts ';' stmt |
                 stmt;
        stmt -> expr |
                inner_var |
                asgn |
                block |
                if |
                case |
                for |
                loop |
                foreach |
                while |
                repeat |
                with |
                goto |
                break |
                continue |
                exit |
                yield |
                try_except |
                try_finally |
                raise |
                lock |
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
        
        while -> 'while' expr 'do' stmt;
        
        repeat -> 'repeat' stmts 'until' expr;

        with -> 'with' list_ids 'do' stmt;
        
        goto -> 'goto' label;
        
        yield -> 'yield' expr |
                 'yield' 'sequence' expr;
        
        break -> 'break';
        
        continue -> 'continue';
        
        exit -> 'exit';
        
        try_except -> 'try' stmts 'except' stmts 'end' |
                      'try' stmts 'except' except_block 'end';
        except_block -> on_list |
                        on_list 'else' stmts;
        on_list -> on_list ';' on_element |
                   on_element;
        on_element -> 'on' var_decl 'do' stmt |
                      'on' var_type 'do' stmt |
                       ε;

        try_finally -> 'try' stmts 'finally' stmts 'end';
        
        raise -> 'raise' expr;
        
        lock -> 'lock' expr 'do' stmt;


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
        sel -> ptr '.' call_id |
               ptr '.' ID |
               'inherited' call_id |
               'inherited' ID |
               'inherited' |
               factor;
        factor -> '(' expr ')' |
                  ID |
                  call |
                  const_expr;
        
        sel_id -> sel_id '.' ID |
                  ID;
        
        call -> '(' expr ')' '(' optparams ')' |
                 ID '(' optparams ')' |
                 call '(' optparams ')';
        optparams -> list_exprs |
                     ε;
        call_id -> ID '(' optparams ')';
        
        const_expr -> NUM |
                      STR |
                      range;
                  
        range -> rng_brdr '..' rng_brdr;
        rng_brdr -> NUM |
                    ID |
                    STR
        """
TOKENS = ('ID', 'NUM', 'STR',)
STAB_FILENAME = "example_pascalabc_stab.prstab"


if __name__ == "__main__":
    import argparse
    from time import time
    import os
    from str_reader.file_reader import FileStrReader
    from lexer.prog_lang_lexer import ProgLangLexer, UnexceptedLexError
    from sparser.sparser import SParser, ParseSyntaxError
    from work_with_syntax_tree import print_tokens_syntax_tree
    from example_pascalabc_lexer import (CASE_SENSITIVE, SKIP_KIND,
                                 SPECIFICATION, ID_KIND,
                                 KEYWORD_KIND, KEYWORDS,
                                 MULTITOKENS)

    def main(code_filename):
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
        print()
        print_tokens_syntax_tree(parser, lexer, node)

    parser = argparse.ArgumentParser(add_help=True, description="Pascal ABC parser script")

    parser.add_argument(dest='code_file', type=str, help="Specifies file with Pascal ABC code!!!")
    args = parser.parse_args()
    try:
        main(args.code_file)
    except (UnexceptedLexError, ParseSyntaxError, FileNotFoundError) as err:
        print(err)