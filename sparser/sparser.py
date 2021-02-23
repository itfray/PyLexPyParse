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

    def __copy__(self):
        return Rule(self.key, *self.value)

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
        if not self.rule is None and \
           self.__iptr > len(self.rule.value):
            self.__iptr = len(self.rule.value)
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


class LRState:
    __lrpoints: list
    __goto: dict

    def __init__(self, **kwargs):
        self.lrpoints = kwargs.get('lrpoints', [])
        self.goto = kwargs.get('goto', {})

    @property
    def lrpoints(self)-> list:
        return self.__lrpoints

    @lrpoints.setter
    def lrpoints(self, value: list)-> None:
        if value is None:
            raise ValueError("lrpoints must be not is None!!!")
        self.__lrpoints = value

    @property
    def goto(self)-> dict:
        return self.__goto

    @goto.setter
    def goto(self, value: dict)-> None:
        if value is None:
            raise ValueError("goto must be not is None!!!")
        self.__goto = value

    def __str__(self):
        ans = "["
        for i in range(len(self.lrpoints)):
            ans += str(self.lrpoints[i])
            if i < len(self.lrpoints) - 1:
                ans += ", "
        ans += "]"
        if len(self.goto) > 0:
            ans += "\n{ "
            for key in self.goto:
                ans += key + "; "
            ans += "}"
        return ans

def first_term(rules: tuple, terminal_func, value: str)-> list:
    vals = []
    queue = []
    queue.append(value)
    while len(queue) > 0:
        val = queue.pop(0)
        if terminal_func(val):
            vals.append(val)
        else:
            for rule in rules:
                if rule.key == val:
                    if len(rule.value) > 0:
                        queue.append(rule.value[0])
    return vals


def closure_LR1(rules: tuple, terminal_func, lrpoint: LR1Point)-> list:
    lrpoints = []
    queue = []
    lrpoints.append(lrpoint)
    queue.append(lrpoint)
    while len(queue) > 0:
        lrpoint = queue.pop(0)
        iptr = lrpoint.iptr
        rule = lrpoint.rule
        if iptr < 0 or iptr > len(rule.value) - 1:
            continue
        B = rule.value[iptr]
        b = rule.value[iptr + 1] if iptr < len(rule.value) - 1 else ''
        firstb = first_term(rules, terminal_func, b)
        if len(firstb) == 0:
            firstb += lrpoint.lookahead
        for rule in rules:
            if B == rule.key:
                lrp = LR1Point(rule=rule, iptr=0, lookahead=firstb)
                queue.append(lrp)
                lrpoints.append(lrp)
    return lrpoints


def goto_LR1(rules: list, terminal_func, lrpoints: list, value: str)-> LRState:
    new_lrstate = None
    for lrpoint in lrpoints:
        iptr = lrpoint.iptr
        rule = lrpoint.rule
        lookahead = lrpoint.lookahead
        if iptr < 0 or iptr > len(rule.value) - 1:
            continue
        B = rule.value[iptr]
        if value == B:
            new_lrstate = LRState()
            lrp = LR1Point(rule=rule, iptr=iptr + 1, lookahead=lookahead)
            new_lrstate.lrpoints = closure_LR1(rules, terminal_func, lrp)
            break
    return new_lrstate


class SParser(ISParser):
    __rules: tuple                                   # rules of grammar
    __tokens: tuple                                  # tokens
    def __init__(self, **kwargs):
        self.lexer = kwargs.get("lexer", None)
        self.rules = kwargs.get("rules", ())
        self.tokens = kwargs.get("tokens", ())

    def parse(self) -> Node:
        if lexer is None:
            raise NoneLexerError("Lexer is None!!!")

    def is_terminal(self, value: str)-> bool:
        if value in self.__tokens:
            return True
        elif len(value) > 0 and value[0] == "'" \
             and value[len(value) - 1] == "'":
            return True
        else:
            return False

    @property
    def lexer(self)-> ILexer:
        return self.__lexer

    @lexer.setter
    def lexer(self, value: ILexer)-> None:
        self.__lexer = value

    @property
    def tokens(self)-> tuple:
        return self.__tokens

    @tokens.setter
    def tokens(self, value: tuple)-> None:
        if value is None:
            raise ValueError("Rules must be not None!!!")
        self.__tokens = value

    @property
    def rules(self)-> tuple:
        """
        Get rules of grammar as
        (Rule(key='...', value=(val1, val2, ...)), ...)
        :return:
        """
        return tuple(rule.__copy__() for rule in self.__rules)

    @rules.setter
    def rules(self, value: tuple)-> None:
        """
        Sets rules of grammar.
        :param value: list of grammar rules
        :return: None
        """
        if value is None:
            raise ValueError("Rules must be not None!!!")
        self.__rules = tuple(rule.__copy__() for rule in value)

    def parse_rules_from(self, specification: str)-> None:
        self.__rules = self.parse_rules(specification)

    @staticmethod
    def parse_rules(specification: str)-> tuple:
        """
        Parses and sets rules of grammar.
        from:   key1 -> val1 val2 ... |
                        val1 val2 ... |
                        ...;
                key2 -> val1 val2 ... |
                        val1 val2 ... |
                        ...;
        to: (Rule(key='...', value=(val1, val2, ...)), ...)
        :param specification: string of grammar rules
        :return: None
        """
        rules = []
        for requir in specification.split(';\n'):
            key, values = requir.split('->', 1)
            key = key.strip()
            values = values.split('|\n')
            for value in values:
                rule = Rule(key, *[val for val in value.strip().split(' ')])
                rules.append(rule)
        return tuple(rules)
