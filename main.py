from sparser.sparser import SParser, Rule, LR0Point, LR1Point


RULES = ("""
         E: E + T
         """,
         """
         T: T * F |
            T / F |
            F
         """,
         """
         F: (E) |
             id
         """)

parser = SParser()
parser.rules = RULES
print(parser.rules)

rule = Rule('E', 'E', '+', 'T')
print(rule)
lrpoint = LR1Point(rule=rule, iptr=1, lookahead='⊥')
print(lrpoint)