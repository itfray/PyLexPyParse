from sparser.sparser import SParser, CellSParseTab, SParseTab


GOAL_NTERM = "S'"
END_TERM = '⊥'
RULES = """
         S' -> S;
         S -> C C;
         C -> c C |
              d
        """
TOKENS = ('c', 'd')

parser = SParser(tokens=TOKENS, goal_nterm=GOAL_NTERM, end_term=END_TERM)
parser.parse_rules_from(RULES)
parser.create_sparse_tab()
print(parser.rules)