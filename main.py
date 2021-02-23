from sparser.sparser import SParser, first_term, closure_LR1, goto_LR1,\
                            Rule, LR1Point, LRState



RULES = """
         S' -> S;
         S -> C C;
         C -> c C |
              d
        """
TOKENS = ('c', 'd')

parser = SParser(tokens=TOKENS)
parser.parse_rules_from(RULES)
print(parser.rules)

rules = SParser.parse_rules(RULES)
terminal_func = lambda ch: ch.islower()
lrstate = LRState()
lrstate.lrpoints = closure_LR1(rules, terminal_func,
                               LR1Point(rule=Rule("S'", 'S'),
                                        iptr=0, lookahead=['⊥',]))
print(lrstate)
print()

new_lrstate = goto_LR1(rules, terminal_func, lrstate.lrpoints, "d")
print(new_lrstate)