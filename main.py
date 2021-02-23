from sparser.sparser import SParser, Rule, LR0Point, LR1Point, LRState


'⊥'

RULES = """
         S' -> S;
         S -> CC;
         C -> cC |
              d |
              ID
        """
TOKENS = ('ID',)

parser = SParser(tokens=TOKENS)
parser.parse_rules_from(RULES)
print(parser.rules)
print(parser.is_terminal("ID"))