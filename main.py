from sparser.sparser import SParser


GOAL_NTERM = 'S'
END_TERM = '⊥'
RULES = """
         S -> C C;
         C -> c C |
              d
        """
TOKENS = ('c', 'd')

parser = SParser(tokens=TOKENS, goal_nterm=GOAL_NTERM, end_term=END_TERM)
parser.parse_rules_from(RULES)
parser.create_lrstates()
print(parser.rules)