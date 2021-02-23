from sparser.sparser import SParser, first_term, closure_LR1, goto_LR1point,\
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