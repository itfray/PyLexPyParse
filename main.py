from sparser.sparser import SParser, first_term


'⊥'

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
print(first_term(rules, lambda ch: ch.islower(), "S'"))