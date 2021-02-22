from .isparser import ISParser, Node, NoneLexerError, ILexer


class Rule:
    key: str
    values: tuple
    def __init__(self, key, *vals):
        self.key = key
        self.values = tuple(vals)

    def __str__(self):
        return self.key + " -> " + " ".join(self.values)

    def __repr__(self):
        return f"Rules(key='{self.key}', values={self.values})"


class LR0Point:
    rule: Rule
    iptr: int
    def __init__(self, **kwargs):
        self.rule = kwargs.get("rule", None)
        self.iptr = kwargs.get("iptr", -1)

    def __str__(self):
        ans = self.rule.key + " -> "
        if self.iptr < 0:
            ans += " ".join(self.rule.values)
        else:
            self.iptr = self.iptr \
                if self.iptr <= len(self.rule.values) else len(self.rule.values)
            for i in range(len(self.rule.values)):
                if i == self.iptr:
                    ans += "●"
                ans += self.rule.values[i]
                if i < len(self.rule.values) - 1:
                    ans += " "
            if self.iptr == len(self.rule.values):
                ans += "●"
        return ans

    def __repr__(self):
        return f"LR0Point(rule={self.rule}, iptr={self.iptr})"


class LR1Point(LR0Point):
    lookahead: str
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lookahead = kwargs.get("lookahead", '')

    def __str__(self):
        return f"[{super().__str__()}, {self.lookahead}]"

    def __repr__(self):
        return f"LR1Point(rule={self.rule}, iptr={self.iptr}, lookahead={self.lookahead})"


class SParser(ISParser):
    __rules: dict                                   # rules of grammar
    def __init__(self, **kwargs):
        self.lexer = kwargs.get("lexer", None)

    def parse(self) -> Node:
        if lexer is None:
            raise NoneLexerError("Lexer is None!!!")

    @property
    def lexer(self)-> ILexer:
        return self.__lexer

    @lexer.setter
    def lexer(self, value: ILexer)-> None:
        self.__lexer = value

    @property
    def rules(self)-> dict:
        """
        Get rules of grammar as
        {key1: ((val1, val2, ...), (val1, val2, ...), ...) ...}
        :return:
        """
        return self.__rules.copy()

    @rules.setter
    def rules(self, rules: tuple)-> None:
        """
        Parses and sets rules of grammar.
        from: ('''key1: val1 val2 ... |
                        val1 val2 ... |
                        ...''', ...)
        to: {key1: ((val1, val2, ...), (val1, val2, ...), ...) ...}
        :param rules: list of grammar rules
        :return: None
        """
        self.__rules = dict()
        for rule in rules:
            key, values = rule.split(':', 1)
            key = key.strip()
            values = values.split('|\n')
            vals = []
            for value in values:
                vals.append(tuple(val for val in value.strip().split(' ')))
            vals = tuple(vals)
            self.__rules[key] = vals