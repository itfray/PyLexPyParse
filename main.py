from sparser.sparser import SParser


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