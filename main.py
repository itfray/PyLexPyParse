from sparser.sparser import SParser, first_term, closure_LR1, Rule, LR1Point



RULES = """
         S' -> S;
         S -> C C;
         C -> c C |
              d
        """
TOKENS = ('ID',)

# parser = SParser(tokens=TOKENS)
# parser.parse_rules_from(RULES)
# print(parser.rules)

rules = SParser.parse_rules(RULES)
lrpoints = closure_LR1(rules, lambda ch: ch.islower(),
                      LR1Point(rule=Rule("S'", 'S'),
                               iptr=0, lookahead=['⊥',]))

# lrpoints = closure_LR1(rules, lambda ch: ch.islower(),
#                       LR1Point(rule=Rule("S", 'C', 'C'),
#                                iptr=1, lookahead=['⊥',]))

for lrpoint in lrpoints:
    print(lrpoint)