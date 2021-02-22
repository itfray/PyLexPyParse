from .isparser import ISParser, Node, NoneLexerError, ILexer


class Rule:
    key: str
    __value: tuple
    def __init__(self, key, *value):
        self.key = key
        self.value = value

    @property
    def value(self)-> tuple:
        return self.__value

    @value.setter
    def value(self, val: tuple)-> None:
        if val is None:
            raise ValueError("Value must be not is None!!!")
        self.__value = val

    def __str__(self):
        return self.key + " -> " + " ".join(self.value)

    def __repr__(self):
        return f"Rules(key='{self.key}', value={self.value})"


class LR0Point:
    __rule: Rule
    __iptr: int
    def __init__(self, **kwargs):
        self.rule = kwargs.get("rule", None)
        self.iptr = kwargs.get("iptr", -1)

    @property
    def rule(self)-> Rule:
        return self.__rule

    @rule.setter
    def rule(self, value: Rule)-> None:
        self.__rule = value
        self.__iptr = -1

    @property
    def iptr(self)-> int:
        return self.__iptr

    @iptr.setter
    def iptr(self, value: int)-> None:
        if self.rule is None:
            self.iptr = -1
        elif value < -1:
            self.__iptr = -1
        elif value > len(self.rule.value):
            self.__iptr = len(self.rule.value)
        else:
            self.__iptr = value

    def __str__(self):
        if self.rule is None:
            return ""
        elif self.iptr < 0:
            return self.rule.__str__()
        else:
            ans = self.rule.key + " -> "
            for i in range(len(self.rule.value)):
                if i == self.iptr:
                    ans += "●"
                ans += self.rule.value[i]
                if i < len(self.rule.value) - 1:
                    ans += " "
            if self.iptr == len(self.rule.value):
                ans += "●"
        return ans

    def __repr__(self):
        return f"LR0Point(rule={self.rule}, iptr={self.iptr})"


class LR1Point(LR0Point):
    __lookahead: list
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__lookahead = kwargs.get("lookahead", [])

    @property
    def lookahead(self)-> list:
        return self.__lookahead

    @lookahead.setter
    def lookahead(self, value: list)-> None:
        if value is None:
            raise ValueError("Lookahead must be not is None!!!")
        self.__lookahead = value

    def __str__(self):
        ans = "[" + super().__str__() + ", "
        for i in range(len(self.lookahead)):
            ans += self.lookahead[i]
            if i < len(self.lookahead) - 1:
                ans += '/'
        ans += "]"
        return ans

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