from .isparser import ISParser, Node, NoneLexerError, ILexer


class Rule:
    """
    Rule is rule of grammar of language
    """
    key: str                             # key of rule, string
    __value: tuple                       # value of rule, set of strings
    def __init__(self, key, *value):
        self.key = key
        self.value = value

    @property
    def value(self)-> tuple:
        """
        Get value
        :return: value, tuple of strings
        """
        return self.__value

    @value.setter
    def value(self, val: tuple)-> None:
        """
        Set value
        :param val: value, tuple of strings
        :return: None
        """
        if val is None:
            raise ValueError("Value must be not is None!!!")
        self.__value = val

    def __eq__(self, other):
        return self.key == other.key and self.value == other.value

    def __ne__(self, other):
        return not self == other

    def __copy__(self):
        return Rule(self.key, *self.value)

    def __str__(self):
        return self.key + " -> " + " ".join(self.value)

    def __repr__(self):
        return f"Rules(key='{self.key}', value={self.value})"


class LR0Point:
    """
    LR0Point is LR0-point of grammar of language
    """
    __rule: Rule                           # rule of grammar
    __iptr: int                            # position of pointer ● in value of rule
    def __init__(self, **kwargs):
        self.rule = kwargs.get("rule", None)
        self.iptr = kwargs.get("iptr", -1)

    @property
    def rule(self)-> Rule:
        """
        Get rule
        :return: rule of grammar
        """
        return self.__rule

    @rule.setter
    def rule(self, value: Rule)-> None:
        """
        Set rule
        :param value: rule of grammar
        :return: None
        """
        self.__rule = value
        self.__iptr = -1                   # reset pointer

    @property
    def iptr(self)-> int:
        """
        Get position of pointer ● in value of rule.
        :return:
            -1 - reseted pointer
            0..n-1 - position in value of rule
            n - in end of rule
        """
        if not self.rule is None and \
           self.__iptr > len(self.rule.value):      # fix value of iptr
            self.__iptr = len(self.rule.value)
        return self.__iptr

    @iptr.setter
    def iptr(self, value: int)-> None:
        """
        Set position of pointer ● in value of rule.
        :param value: int position
        :return: None
        """
        if self.rule is None:
            self.iptr = -1
        elif value < -1:
            self.__iptr = -1
        elif value > len(self.rule.value):
            self.__iptr = len(self.rule.value)
        else:
            self.__iptr = value

    def __eq__(self, other):
        return self.rule == other.rule and self.iptr == other.iptr

    def __ne__(self, other):
        return not self == other

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
    """
    LR1Point is LR1-point of grammar of language
    """
    __lookahead: list                   # terminal symbols of lookahead
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__lookahead = kwargs.get("lookahead", [])

    @property
    def lookahead(self)-> list:
        """
        Get list of terminal symbols of lookahead
        :return: list of strings
        """
        return self.__lookahead

    @lookahead.setter
    def lookahead(self, value: list)-> None:
        """
        Set list of terminal symbols of lookahead
        :param value: list of strings
        :return: None
        """
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

    def __eq__(self, other):
        return super().__eq__(other) and self.lookahead == other.lookahead

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return f"LR1Point(rule={self.rule}, iptr={self.iptr}, lookahead={self.lookahead})"


class LRState:
    """
    LRState is state of LR state machine
    """
    __lrpoints: list                        # LR-points of LR-state
    __goto: dict                            # transitions in other states

    def __init__(self, **kwargs):
        self.lrpoints = kwargs.get('lrpoints', [])
        self.goto = kwargs.get('goto', {})

    @property
    def lrpoints(self)-> list:
        """
        Get LR-points
        :return: list of LR-points
        """
        return self.__lrpoints

    @lrpoints.setter
    def lrpoints(self, value: list)-> None:
        """
        Set LR-points
        :param value: list of LR-points
        :return: None
        """
        if value is None:
            raise ValueError("lrpoints must be not is None!!!")
        self.__lrpoints = value

    @property
    def goto(self)-> dict:
        """
        Get transitions in other states.
        key - symbol for transition
        value - new state
        :return: dictionary of transitions
        """
        return self.__goto

    @goto.setter
    def goto(self, value: dict)-> None:
        """
        Set transitions in other states.
        :param value: dictionary of transitions
        :return: None
        """
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


def first_term(rules: list, terminal_func, value: str)-> list:
    """
    Calculate set of FIRST(value) for specified value.
    FIRST(A) - the set of terminal characters that begin
    strings derived from 'A'
    :param rules: rules of grammar
    :param terminal_func: predicate for definition terminal symbols
    :param value: symbol who need calulate set of FIRST(...)
    :return: list of terminal symbols
    """
    ans = []                    # list of found terminal symbols
    queue = []
    queue.append(value)
    while len(queue) > 0:       # breadth-first search (BFS)
        val = queue.pop(0)
        if terminal_func(val):
            ans.append(val)     # add terminal
        else:
            for rule in rules:
                if rule.key == val:
                    if len(rule.value) > 0:
                        queue.append(rule.value[0])   # add new symbol for check
    return ans

def closure_LR1(rules: list, terminal_func, lrpoint: LR1Point)-> list:
    """
    Calculate set of CLOSURE(...) for specified LR-point.
    CLOSURE(I) - closing LR-points.
    if [A -> α●Bβ, a] is included in CLOSURE(I)
    and there is rule [B -> γ], then in CLOSURE(I)
    append [B -> ●γ, b] for each terminal b ∈ FIRST(βa).
    :param rules: rules of grammar
    :param terminal_func: predicate for definition terminal symbols
    :param lrpoint: LR-point who need calulate set of CLOSURE(...)
    :return: list of LR-points for LR-state
    """
    lrpoints = []                   # CLOSURE(...), list of LR-points
    queue = []
    lrpoints.append(lrpoint)
    queue.append(lrpoint)
    while len(queue) > 0:           # breadth-first search (BFS)
        lrpoint = queue.pop(0)
        iptr = lrpoint.iptr
        rule = lrpoint.rule
        if iptr < 0 or iptr > len(rule.value) - 1:
            continue
        B = rule.value[iptr]                          # calculate B
        b = rule.value[iptr + 1] \
            if iptr < len(rule.value) - 1 else ''     # calculate β
        firstb = first_term(rules, terminal_func, b)  # calculate FIRST(β)
        if len(firstb) == 0:
            firstb += lrpoint.lookahead               # calculate FIRST(a)
        for rule in rules:
            if B == rule.key:
                lrp = LR1Point(rule=rule, iptr=0, lookahead=firstb)   # add rule [B -> ●γ, FIRST(βa)]
                queue.append(lrp)
                lrpoints.append(lrp)                  # add rule [B -> ●γ, b]
    return lrpoints

def goto_LR1Point(rules: list, terminal_func, lrpoints: list, value: str)-> LR1Point:
    """
    Calculate LR-point for GOTO-transition by specified value.
    GOTO_LR1Point([..., [A -> α●Xβ, a], ...], X) = [A -> αX●β, a].
    GOTO(I, X) - set of transitions, I - LR-state,
    X - symbol for transition.
    if [A -> α●Xβ, a] in CLOSURE(Ii) then
    GOTO(Ii, X) = CLOSURE([A -> αX●β, a]).
    :param rules: rules of grammar
    :param terminal_func: predicate for definition terminal symbols
    :param lrpoints: list of LR1-points
    :param value: symbol for transition
    :return: LR1-point
    """
    for lrpoint in lrpoints:                # check all LR-points
        iptr = lrpoint.iptr
        rule = lrpoint.rule
        lookahead = lrpoint.lookahead
        if iptr < 0 or iptr > len(rule.value) - 1:
            continue
        B = rule.value[iptr]
        if value == B:
            return LR1Point(rule=rule, iptr=iptr + 1, lookahead=lookahead)
    return None

def create_LR1States(rules: list, term_func, lrpoint: LR1Point)-> list:
    """
    Create all LR-states of LR state machine by LR-point with goal symbol
    :param rules: rules of grammar
    :param term_func: predicate for definition terminal symbols
    :param lrpoint: LR1-point who need calulate LR-states
    :return: list of all LR-states of LR state machine
    """
    lrpt = lrpoint
    lrst = LRState()                                      # LR-state I0
    lrst.lrpoints = closure_LR1(rules, term_func, lrpt)   # calculate CLOSURE(I0)
    used_lrpoints = []
    lrstates = []                        # all LR-states
    queue = []
    lrstates.append(lrst)                # add I0
    queue.append((lrpt, lrst))           # add I0 for processing
    used_lrpoints.append((lrpt, lrst))
    while len(queue) > 0:
        curr_lrp, curr_lrst = queue.pop(0)
        for lrpoint in curr_lrst.lrpoints:
            rule = lrpoint.rule
            iptr = lrpoint.iptr
            if iptr < 0 or iptr > len(rule.value) - 1:      # if after ● there is a symbol
                continue
            B = rule.value[iptr]
            # calculate LR1-point fot GOTO-transition
            new_lrp = goto_LR1Point(rules, term_func, curr_lrst.lrpoints, B)
            if new_lrp is None:
                continue
            new_lrst = None
            for lrp, lrst in used_lrpoints:     # find LR-state for GOTO LR-point
                if lrp == new_lrp:              # if LR-state is already created
                    new_lrp = lrp
                    new_lrst = lrst
                    break
            if new_lrst is None:                # create new LR-state
                new_lrst = LRState()
                new_lrst.lrpoints = closure_LR1(rules, term_func, new_lrp)
                used_lrpoints.append((new_lrp, new_lrst))
                queue.append((new_lrp, new_lrst))          # add Ii for processing
                lrstates.append(new_lrst)                  # add Ii
            curr_lrst.goto[B] = new_lrst                   # set transition
    return lrstates


class SParser(ISParser):
    DEFAULT_GOAL_NTERM = ''
    DEFAULT_END_TERM = '⊥'
    __rules: list                                    # rules of grammar
    __tokens: tuple                                  # tokens
    goal_nterm: str
    end_term: str
    __lrstates: list                                 # LR-states of LR state machine
    def __init__(self, **kwargs):
        self.lexer = kwargs.get("lexer", None)
        self.rules = kwargs.get("rules", [])
        self.tokens = kwargs.get("tokens", ())
        self.goal_nterm = kwargs.get("goal_nterm", self.DEFAULT_GOAL_NTERM)
        self.end_term = kwargs.get("end_term", self.DEFAULT_END_TERM)

    def parse(self) -> Node:
        if lexer is None:
            raise NoneLexerError("Lexer is None!!!")

    def is_terminal(self, value: str)-> bool:
        """
        Predicate for definition terminal symbols of grammar
        :param value: symbol for check
        :return: result of check
        """
        if value in self.__tokens:
            return True
        elif len(value) > 0 and value[0] == "'" \
             and value[len(value) - 1] == "'":
            return True
        elif value == self.end_term:
            return True
        else:
            return False

    @property
    def lexer(self)-> ILexer:
        """
        Get lexer
        :return: lexer
        """
        return self.__lexer

    @lexer.setter
    def lexer(self, value: ILexer)-> None:
        """
        Set lexer
        :param value: lexer
        :return: None
        """
        self.__lexer = value

    def create_lrstates(self)-> None:
        """
        Create all LR-states of LR state machine
        :return: None
        """
        rule = None
        for r in self.__rules:
            if r.key == self.goal_nterm:
                rule = r
                break
        if rule is None:
            if len(self.__rules) > 0:
                rule = self.__rules[0]
            else:
                return
        goal_rule = Rule(rule.key + "'", rule.key)
        self.__rules = [goal_rule] + self.__rules
        lrpt = LR1Point(rule=goal_rule, iptr=0, lookahead=[self.end_term])
        self.__lrstates = create_LR1States(self.__rules, self.is_terminal, lrpt)

    @property
    def tokens(self)-> tuple:
        """
        Get lexemes of language
        :return:
        """
        return self.__tokens

    @tokens.setter
    def tokens(self, value: tuple)-> None:
        """
        Set lexemes of language
        :param value: list of lexemes
        :return: None
        """
        if value is None:
            raise ValueError("Rules must be not None!!!")
        self.__tokens = value

    @property
    def rules(self)-> list:
        """
        Get rules of grammar as
        [Rule(key='...', value=(val1, val2, ...)), ...]
        :return:
        """
        return self.__rules

    @rules.setter
    def rules(self, value: tuple)-> None:
        """
        Sets rules of grammar.
        :param value: list of grammar rules
        :return: None
        """
        if value is None:
            raise ValueError("Rules must be not None!!!")
        self.__rules = value

    def parse_rules_from(self, specification: str)-> None:
        self.__rules = self.parse_rules(specification)

    @staticmethod
    def parse_rules(specification: str)-> list:
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
        return rules
