import struct
import random
import time
from lexer import ILexer, Token
from .isparser import (ISParser, Node, SParserError,
                       NoneLexerError, ParseSyntaxError)


def merge_ranges(*rngs):
    """
    Merge ranges
    :param rngs: list of ranges
    :return: value from range
    """
    for rng in rngs:
        for e in rng:
            yield e


def range_objs(*objs):
    """
    Create range of objects
    :param objs: list of objects
    :return: string from list of objects
    """
    for obj in objs:
        yield obj


class Rule:
    """
    Rule is rule of grammar of language
    """
    key: object                              # key of rule
    __value: tuple                           # value of rule
    def __init__(self, key = None, *value):
        self.key = key
        self.value = value

    @property
    def value(self)-> tuple:
        """
        Get value
        :return: value, tuple of values
        """
        return self.__value

    @value.setter
    def value(self, val: tuple)-> None:
        """
        Set value
        :param val: value, tuple of values
        :return: None
        :raise: ValueError
        """
        if val is None:
            raise ValueError("Value must be not is None!!!")
        self.__value = val

    def __eq__(self, other):
        return self.key == other.key and self.value == other.value

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return str(self.key) + " -> " + " ".join(str(val) for val in self.value)

    def __repr__(self):
        return f"Rules(key={str(self.key)}, value={self.value})"

    def to_tuple(self)-> tuple:
        return (self.key, *self.value)


class IndRule(Rule):
    """
    IndRule is rule of grammar of language with index
    """
    index: int                        # index of rule
    def __init__(self, key = None, *value):
        super().__init__(key, *value)
        self.index = 0


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
            ans = str(self.rule.key) + " -> "
            for i in range(len(self.rule.value)):
                if i == self.iptr:
                    ans += "●"
                ans += str(self.rule.value[i])
                if i < len(self.rule.value) - 1:
                    ans += " "
            if self.iptr == len(self.rule.value):
                ans += "●"
        return ans

    def __repr__(self):
        return f"LR0Point(rule={self.rule}, iptr={self.iptr})"

    def to_tuple(self)-> tuple:
        if self.rule is None:
            return None
        return (self.rule.key, *self.rule.value, self.iptr)


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
        :raise: ValueError
        """
        if value is None:
            raise ValueError("Lookahead must be not is None!!!")
        self.__lookahead = value

    def __str__(self):
        ans = "[" + super().__str__() + ", "
        for i in range(len(self.lookahead)):
            ans += str(self.lookahead[i])
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

    def to_tuple(self)-> tuple:
        if self.rule is None:
            return None
        return (self.rule.key, *self.rule.value, self.iptr, *self.lookahead)


class LRState:
    """
    LRState is state of LR state machine
    """
    index: int                              # index of LR-state
    __lrpoints: list                        # LR-points of LR-state
    __goto: dict                            # transitions in other states
    __rgoto: dict                           # reverse transitions in other states
    def __init__(self, **kwargs):
        self.lrpoints = kwargs.get('lrpoints', [])
        self.goto = kwargs.get('goto', {})
        self.rgoto = kwargs.get('rgoto', {})
        self.index = kwargs.get('index', 0)

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
        :raise: ValueError
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
        :raise: ValueError
        """
        if value is None:
            raise ValueError("goto must be not is None!!!")
        self.__goto = value

    @property
    def rgoto(self)-> dict:
        """
        Get reverse transitions in other states.
        key - symbol for transition
        value - new state
        :return: dictionary of reverse transitions
        """
        return self.__rgoto

    @rgoto.setter
    def rgoto(self, value: dict)-> None:
        """
        Set reverse transitions in other states.
        :param value: dictionary of reverse transitions
        :return: None
        :raise: ValueError
        """
        if value is None:
            raise ValueError("rgoto must be not is None!!!")
        self.__rgoto = value

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
                ans += str(key) + "; "
            ans += "}"
        if len(self.rgoto) > 0:
            ans += "\nr{ "
            for key in self.rgoto:
                ans += str(key) + "; "
            ans += "}"
        return ans


def first_term(rules: list, terminal_func, value)-> list:
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
    checked_rules = set()
    while len(queue) > 0:       # breadth-first search (BFS)
        val = queue.pop(0)
        if terminal_func(val):
            ans.append(val)     # add terminal
        else:
            for rule in rules:
                if rule.key == val and \
                   rule.to_tuple() not in checked_rules:
                    if len(rule.value) > 0:
                        queue.append(rule.value[0])   # add new symbol for check
                        checked_rules.add(rule.to_tuple())
    return ans

def closure_LR1(rules: list, terminal_func, entry_lrps: list)-> list:
    """
    Calculate set of CLOSURE(...) for specified LR-points.
    CLOSURE(I) - closing LR-points.
    if [A -> α●Bβ, a] is included in CLOSURE(I)
    and there is rule [B -> γ], then in CLOSURE(I)
    append [B -> ●γ, b] for each terminal b ∈ FIRST(βa).
    :param rules: rules of grammar
    :param terminal_func: predicate for definition terminal symbols
    :param entry_lrps: list of LR-points who need calulate set of CLOSURE(...)
    :return: list of LR-points for LR-state
    """
    lrpoints = {}                   # CLOSURE(...), list of LR-points
    queue = []                      # processing queue
    for lrpoint in entry_lrps:      # add all entry LR-points
        lrpoints[lrpoint.to_tuple()] = lrpoint
        queue.append(lrpoint)
    while len(queue) > 0:           # breadth-first search (BFS)
        lrpoint = queue.pop(0)
        iptr = lrpoint.iptr
        rule = lrpoint.rule
        if iptr < 0 or iptr > len(rule.value) - 1:
            continue
        B = rule.value[iptr]                            # calculate B
        b = rule.value[iptr + 1] \
            if iptr < len(rule.value) - 1 else None     # calculate β
        firstb = first_term(rules, terminal_func, b)    # calculate FIRST(β)
        if len(firstb) == 0:
            firstb += lrpoint.lookahead                 # calculate FIRST(a)
        for rule in rules:
            if B == rule.key:
                new_lrp = LR1Point(rule=rule, iptr=0, lookahead=firstb)  # add rule [B -> ●γ, FIRST(βa)]
                if new_lrp.to_tuple() not in lrpoints:                   # if lrpoints not have new_lrp
                    queue.append(new_lrp)
                    lrpoints[new_lrp.to_tuple()] = new_lrp               # add rule [B -> ●γ, b]
    return [lrpoints[key_lrp] for key_lrp in lrpoints]

def goto_LR1Point(lrpoints: list, value)-> list:
    """
    Calculate LR-points for GOTO-transition by specified value.
    GOTO_LR1Point([..., [A -> α●Xβ, a], ...], X) = [[A -> αX●β, a], ...]
    GOTO(I, X) - set of transitions, I - LR-state,
    X - symbol for transition.
    if [A -> α●Xβ, a] in CLOSURE(Ii) then
    GOTO(Ii, X) = CLOSURE([[A -> αX●β, a], ...]).
    :param rules: rules of grammar
    :param terminal_func: predicate for definition terminal symbols
    :param lrpoints: list of LR1-points
    :param value: symbol for transition
    :return: list of GOTO LR1-points
    """
    goto_lrps = []
    for lrpoint in lrpoints:                # check all LR-points
        iptr = lrpoint.iptr
        rule = lrpoint.rule
        lookahead = lrpoint.lookahead
        if iptr < 0 or iptr > len(rule.value) - 1:
            continue
        B = rule.value[iptr]
        if value == B:
            goto_lrps += [LR1Point(rule=rule, iptr=iptr + 1, lookahead=lookahead)]
    return goto_lrps

def create_LR1States(rules: list, term_func, start_lrp: LR1Point)-> list:
    """
    Create all LR-states of LR state machine by LR-point with goal symbol
    :param rules: rules of grammar
    :param term_func: predicate for definition terminal symbols
    :param start_lrp: LR1-point who need calulate LR-states
    :return: list of all LR-states of LR state machine
    """
    index = 0
    lrpts = [start_lrp]
    lrst = LRState(index=index)                            # LR-state I0
    lrst.lrpoints = closure_LR1(rules, term_func, lrpts)   # calculate CLOSURE(I0)
    created_lrsts = {}                    # all created LR-states and LR-points with that they were created
    queue = []                            # queue of LR-states processing
    ans_lrsts = []
    ans_lrsts.append(lrst)
    lrst_key = tuple(lrp.to_tuple() for lrp in lrpts)
    created_lrsts[lrst_key] = lrst        # add I0 how created
    queue.append(lrst)                    # add I0 for processing
    while len(queue) > 0:
        curr_lrst = queue.pop(0)
        goto_symbols = set()
        for lrpoint in curr_lrst.lrpoints:
            rule = lrpoint.rule
            iptr = lrpoint.iptr
            if iptr < 0 or iptr > len(rule.value) - 1:      # if after ● there is a symbol
                continue
            B = rule.value[iptr]
            goto_symbols.add(B)
        for B in goto_symbols:
            new_lrps = goto_LR1Point(curr_lrst.lrpoints, B)  # get LR1-points for GOTO-transition
            if len(new_lrps) == 0:
                continue
            lrst_key = tuple(lrp.to_tuple() for lrp in new_lrps)
            new_lrst = created_lrsts.get(lrst_key, None)
            if new_lrst is None:                     # create new LR-state
                index += 1
                new_lrst = LRState(index=index)
                new_lrst.lrpoints = closure_LR1(rules, term_func, new_lrps)
                queue.append(new_lrst)                # add Ii for processing
                created_lrsts[lrst_key] = new_lrst    # add Ii how created
                ans_lrsts.append(new_lrst)
            curr_lrst.goto[B] = new_lrst              # set transition
            refs = new_lrst.rgoto.get(B, [])          # set reverse transition
            refs.append(curr_lrst)
            new_lrst.rgoto[B] = refs
    return ans_lrsts

def can_merge_LR1_states(lrst1: LRState, lrst2: LRState)-> bool:
    """
    Check can merge first LR1-state and second LR1-state?
    :param lrst1: LR1-state
    :param lrst2: LR1-state
    :return: bool
    """
    if len(lrst1.lrpoints) == len(lrst2.lrpoints):
        for k in range(len(lrst1.lrpoints)):
            lrp1 = lrst1.lrpoints[k]
            lrp2 = lrst2.lrpoints[k]
            if lrp1.iptr != lrp2.iptr or \
               lrp1.rule != lrp2.rule:       # check pointers ● and rules
                return False
        return True
    return False

def merge_LR1_states(lrst1: LRState, lrst2: LRState)-> LRState:
    """
    Merge first LR1-state and second LR1-state
    :param lrst1: LR1-state
    :param lrst2: LR1-state
    :return: new LR1-state
    """
    new_lrst = LRState()                        # create new LR-state
    for k in range(len(lrst1.lrpoints)):        # merge LR1-points
        lrp1 = lrst1.lrpoints[k]
        lrp2 = lrst2.lrpoints[k]
        lrp = LR1Point(rule=lrp1.rule, iptr=lrp1.iptr,
                       lookahead=lrp1.lookahead + lrp2.lookahead)
        new_lrst.lrpoints.append(lrp)

    for key in lrst1.goto:                        # add all goto transitions from lrst1
        lrst = lrst1.goto[key]
        new_lrst.goto[key] = lrst                 # add goto transition
        lrst.rgoto[key].remove(lrst1)             # fix rgoto transition in other states
        lrst.rgoto[key].append(new_lrst)

    for key in lrst2.goto:                        # add all goto transitions from lrst2
        lrst = lrst2.goto[key]
        if new_lrst.goto.get(key, None) is None:
            new_lrst.goto[key] = lrst             # add goto transition
        lrst.rgoto[key].remove(lrst2)             # fix rgoto transition in other states
        lrst.rgoto[key].append(new_lrst)

    new_lrst.rgoto = {key: lrst1.rgoto[key].copy()  # add all rgoto transitions from lrst1
                      for key in lrst1.rgoto}
    for key in lrst2.rgoto:                         # add all rgoto transitions from lrst2
        refs = new_lrst.rgoto.get(key, [])
        for lrst1 in lrst2.rgoto[key]:              # add rgoto transitions excluding duplicates
            add_flag = True
            for lrst2 in refs:
                if lrst1 is lrst2:
                    add_flag = False
                    break
            if add_flag:
                refs.append(lrst1)
        new_lrst.rgoto[key] = refs

    for key in new_lrst.rgoto:                 # fix goto transitions in other states
        for lrst in new_lrst.rgoto[key]:
            lrst.goto[key] = new_lrst
    return new_lrst

def states_LR1_to_LALR1(lrstates: list)-> list:
    """
    Transform list of LR1-states to LALR1-states.
    :param lrstates: list of LR1-states
    :return: None
    """
    lrstates = lrstates.copy()
    pos_i = 0
    pos_j = len(lrstates) - 1
    # merge all LR-states with common core
    while pos_i < len(lrstates) - 1:
        merge_flag = False
        for i in range(pos_i, len(lrstates)):
            pos_i = i
            if pos_j == len(lrstates) - 1:
                pos_j = i + 1
            for j in range(pos_j, len(lrstates)):
                pos_j = j
                if i != j and\
                   can_merge_LR1_states(lrstates[i], lrstates[j]):
                    new_lrst = merge_LR1_states(lrstates[pos_i], lrstates[pos_j])
                    lrstates[pos_i] = new_lrst
                    lrstates.pop(pos_j)
                    pos_j -= 1
                    merge_flag = True
                    break
            if merge_flag:
                break
    for i in range(len(lrstates)):              # fix indices in LR-states
        lrstates[i].index = i
    return lrstates


class CellSParseTab:
    """
    CellSParseTab is cell for SParse table
    """
    vDEF: int                                           # default value
    EMP: int                                            # empty action
    ACC: int                                            # accept action
    RUL: int                                            # apply rule action
    SHF: int                                            # shift action
    GOTO: int                                           # goto action
    EMP, ACC, RUL, SHF, GOTO = range(0, 5)              # values of cell action
    vDEF = 0                                            # values of cell value
    action: int                                         # cell action
    value: int                                          # cell value
    def __init__(self, **kwargs):
        self.action = kwargs.get("action", self.EMP)
        self.value = kwargs.get("value", self.vDEF)

    def __str__(self):
        cond =  True
        if self.action == self.ACC:
            ans = 'acc'
            cond = False
        elif self.action == self.RUL:
            ans = 'r'
        elif self.action == self.SHF:
            ans = 's'
        elif self.action == self.GOTO:
            ans = ''
        else:
            ans = ''
            cond = False
        if cond:
            ans += str(self.value)
        return ans

    def __repr__(self):
        return f"CellSParseTab(action={self.action}, value={self.value})"


class SParseTab:
    """
    SParseTab is table of parsing or
    сanonical matrix of syntax analysis.
    """
    __headers: dict                                 # headers of table
    __content: list                                 # matrix
    def __init__(self, **kwargs):
        self.__headers = dict()
        self.__content = []
        self.headers = kwargs.get('headers', ())
        self.create(kwargs.get('rows', 0))

    def create(self, rows: int)-> None:
        """
        Create matrix by count of row and count of columns.
        Count of columns equal count of headers.
        :param rows: count of rows
        :return: None
        """
        self.clear()
        for i in range(rows):
            self.__content.append([CellSParseTab() for i in range(len(self.__headers))])

    def clear(self)-> None:
        self.__content.clear()

    def cell_ind(self, irow: int, icol: int)-> CellSParseTab:
        """
        Get cell by index of row and index of column
        :param irow: index of row
        :param icol: index of column
        :return: cell
        """
        return self.__content[irow][icol]

    def cell_hdr(self, irow: int, ncol)-> CellSParseTab:
        """
        Get cell by index of row and name of column
        :param irow: index of row
        :param ncol: key of column
        :return: cell
        """
        return self.__content[irow][self.__headers[ncol]]

    @property
    def headers(self)-> tuple:
        """
        Get headers
        :return: tuple of headers
        """
        return tuple(hdr for hdr in self.__headers)

    @headers.setter
    def headers(self, value)-> None:
        """
        Set headers
        :param value: list of headers
        :return: None
        """
        self.__headers.clear()
        ind = 0
        for e in value:
            self.__headers[e] = ind
            ind += 1

    @property
    def rows(self)-> int:
        """
        Count of matrix rows
        :return: count of rows
        """
        return len(self.__content)

    @property
    def columns(self)-> int:
        """
        Count of matrix columns
        :return: count of columns
        """
        if len(self.__content) > 0:
            return len(self.__content[0])
        else:
            return 0


def create_sparse_tab(rules: list, lrstates: list,
                      term_func, goal_nterm, end_term)-> SParseTab:
    """
    Create SParse table.
    Creating by next rules:
        1) if [A -> α●aβ, b] included in Ii and GOTO(Ii,a) = Ij then
        SPARSE_TAB[i,a] = 'sj' (SHIFT j)
        2) if [A -> α●, a] included in Ii and A != S' then
        SPARSE_TAB[i,a] = 'rj' (APPLY RULE j)
        3) if [S' -> S●, end] included in Ii then
        SPARSE_TAB[i,end] = 'acc' (ACCEPT)
        4) if [A -> α●Bβ, b] included in Ii and GOTO(Ii,B) = Ij then
        SPARSE_TAB[i,B] = 'j' (GOTO j)
    :param rules: rules of grammar
    :param lrstates: LR-states of LR state machine
    :param term_func: predicate for definition terminal symbols
    :param goal_nterm: goal nterminal of grammar
    :param end_term: end terminal of grammar
    :return: SParse table
    """
    if len(lrstates) == 0:
        return
    headers = set()
    for lrstate in lrstates:         # get all symbols of transitions
        for key in lrstate.goto:
            headers.add(key)
    headers.add(end_term)
    sparse_tab = SParseTab(headers=headers,         # init matrix
                           rows=len(lrstates))
    for i in range(len(lrstates)):
        for lrpoint in lrstates[i].lrpoints:
            if lrpoint.iptr == -1:
                continue
            elif lrpoint.iptr == len(lrpoint.rule.value):     # if [A -> α●, a]
                if lrpoint.rule.key == goal_nterm:                               # if [S' -> S●, end]
                    cell = cell = sparse_tab.cell_hdr(i, lrpoint.lookahead[0])
                    cell.action = cell.ACC                                       # set ACCEPT
                else:
                    for s in lrpoint.lookahead:
                        cell = cell = sparse_tab.cell_hdr(i, s)
                        cell.action = cell.RUL                       # set APPLY RULE i
                        cell.value = lrpoint.rule.index
            else:                                                    # if [A -> α●γβ, b]
                a = lrpoint.rule.value[lrpoint.iptr]
                cell = sparse_tab.cell_hdr(i, a)
                new_lrst = lrstates[i].goto.get(a, None)
                if new_lrst is None:
                    continue
                if term_func(a):                   # if [A -> α●aβ, b]
                    cell.action = cell.SHF         # set SHIFT i
                else:
                    cell.action = cell.GOTO        # set GOTO i
                cell.value = new_lrst.index        # else [A -> α●Bβ, b], set GOTO i
    return sparse_tab


class NoneSParseTabErr(SParserError):
    """
     NoneSParseTabErr is class of errors for syntax analyzer SParser.
     Raise when parser's parsing table not found (is None).
    """
    def __init__(self, *args):
        super().__init__(*args)


class UncorrectSParseTabErr(SParserError):
    """
    UncorrectSParseTabErr is class of errors for syntax analyzer SParser.
    Raise when parser meet inconsistency of the table with the grammar rules.
    """
    def __init__(self, *args):
        super().__init__(*args)


class EmptyRulesError(SParserError):
    """
     EmptyRulesError is class of errors for syntax analyzer SParser.
     Raise when parser's parsing rules not found (list rules is empty).
    """
    def __init__(self, *args):
        super().__init__(*args)


class ReadingSTabFileErr(SParserError):
    """
     ReadingSTabFileErr is class of errors for syntax analyzer SParser.
     Raise when happens reading error of file with SParseTable and rules.
    """
    def __init__(self, *args):
        super().__init__(*args)


class SParser(ISParser):
    SID_BYTES = 8
    MAX_SID = 2 ** (8 * SID_BYTES) - 1
    DEFAULT_TERM_SEGREG = ("'", "'")        # default terminal segregation
    DEFAULT_EXT_GOAL_SIGN = "'"             # default sign for designation extended goal
    DEFAULT_END_TERM = '⊥'                  # default end terminal
    DEFAULT_EMPTY_TERM = 'ε'                # default empty terminal
    FILE_KEYWORD_IN_START = "SPARSER"
    FILE_KEYWORD_BEFORE_RULES = "RULES"
    FILE_KEYWORD_BEFORE_HEADERS = "HDRS"
    FILE_KEYWORD_BEFORE_TABLE = "STAB"
    __sid2symbol_tab: dict
    __symbol2sid_tab: dict
    __rules: list                           # rules of grammar
    __tokens: tuple                         # tokens
    __goal_nterm: int                       # goal nterminal symbol
    __end_term: int                         # end terminal symbol
    __empty_term: int                       # empty terminal symbol
    __term_segreg: tuple                    # terminal segregation
    __ext_goal_sign: str                    # sign for designation extended goal
    __sparse_tab: SParseTab                 # parsing table

    def __init__(self, **kwargs):
        self.__init_symbols_tab()
        self.__rules = list()
        self.__tokens = tuple()
        self.__goal_nterm = None
        self.__end_term = None
        self.__empty_term = None
        self.__sparse_tab = None
        self.lexer = kwargs.get("lexer", None)
        self.term_segreg = kwargs.get("term_segreg", self.DEFAULT_TERM_SEGREG)
        self.__ext_goal_sign = self.DEFAULT_EXT_GOAL_SIGN
        tokens = kwargs.get("tokens", None)
        if not tokens is None:
            self.tokens = tokens
        rules = kwargs.get("rules", None)
        if not rules is None:
            self.rules = rules
        specification = kwargs.get("parsing_of_rules", None)
        if not specification is None and len(self.__rules) == 0:
            self.parse_rules(specification)
        self.end_term = kwargs.get("end_term", self.DEFAULT_END_TERM)
        self.empty_term = kwargs.get("empty_term", self.DEFAULT_EMPTY_TERM)
        goal_nterm = kwargs.get("goal_nterm", None)
        if not goal_nterm is None:
            self.goal_nterm = goal_nterm

    def __init_symbols_tab(self):
        self.__symbol2sid_tab = {}
        self.__sid2symbol_tab = {}

    def __clear_symbols_tab(self):
        self.__sid2symbol_tab.clear()
        self.__symbol2sid_tab.clear()

    def __add_symbol_to_tab(self, symbol: str):
        if symbol not in self.__symbol2sid_tab:
            min_sid = 0
            if len(self.__sid2symbol_tab) == self.MAX_SID - min_sid + 1:
                raise MemoryError('Symbol table in SParser is full!!!')
            new_sid = lambda: random.randint(min_sid, self.MAX_SID)
            sid = new_sid()
            while sid in self.__sid2symbol_tab:
                sid = new_sid()
            self.__symbol2sid_tab[symbol] = sid
            self.__sid2symbol_tab[sid] = symbol

    def __del_symbol_frm_tab(self, symbol: str):
        if symbol in self.__symbol2sid_tab:
            sid = self.__symbol2sid_tab[symbol]
            self.__symbol2sid_tab.pop(symbol)
            self.__sid2symbol_tab.pop(sid)

    def __del_sid_frm_tab(self, sid: int):
        if sid in self.__sid2symbol_tab:
            symbol = self.__sid2symbol_tab[sid]
            self.__sid2symbol_tab.pop(sid)
            self.__symbol2sid_tab.pop(symbol)

    def symbol2sid_tab(self):
        return self.__symbol2sid_tab.copy()

    def sid2symbol_tab(self):
        return self.__sid2symbol_tab.copy()

    def symbol(self, sid: int) -> str:
        return self.__sid2symbol_tab.get(sid, None)

    def sid(self, symbol: str) -> int:
        return self.__symbol2sid_tab.get(symbol, None)

    def has_sparse_tab(self)-> bool:
        """
        Has Parser SParseTable?
        :return: True or False
        """
        if not self.__sparse_tab is None:
            return self.__sparse_tab.rows > 0
        return False

    def has_rules(self)-> bool:
        """
        Has Parser rules?
        :return: True or False
        """
        return len(self.__rules) > 0

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

    @property
    def term_segreg(self)-> tuple:
        """
        Get terminal segregation.
        Terminal segregation need
        that define terminal symbols.
        Example: if term_segreg = ("'", "'")
        then "'t'" is terminal symbol.
        :return: tuple of symbols
                 for terminal segregation
        """
        return self.__term_segreg

    @term_segreg.setter
    def term_segreg(self, value: tuple)-> None:
        """
        Set terminal segregation.
        :param value: tuple of symbols
                      for terminal segregation
        :return: None
        """
        self.__term_segreg = tuple(str(value[i]) for i in range(2))

    def clear_tokens(self):
        for sid_tok in self.__tokens:
            self.__del_sid_frm_tab(sid_tok)
        self.__tokens = tuple()

    @property
    def tokens(self)-> tuple:
        """
        Get lexemes of language
        :return:
        """
        return tuple(self.__sid2symbol_tab[sid_tok] for sid_tok in self.__tokens)

    @tokens.setter
    def tokens(self, value: tuple)-> None:
        """
        Set lexemes of language
        :param value: list of lexemes
        :return: None
        :raise: ValueError
        """
        if value is None:
            raise ValueError("Rules must be not None!!!")
        self.clear_tokens()
        tokens = []
        for token in value:
            self.__add_symbol_to_tab(token)
            tokens.append(self.__symbol2sid_tab[token])
        self.__tokens = tuple(tokens)

    def clear_rules(self):
        for rule in self.__rules:
            self.__del_sid_frm_tab(rule.key)
            for val in rule.value:
                self.__del_sid_frm_tab(val)
        self.__rules.clear()

    @property
    def rules(self) -> list:
        """
        Get rules of grammar.
        :return: list of grammar rules
        """
        rules = []
        for ind_rule in self.__rules:
            rule = Rule()
            rule.key = self.__sid2symbol_tab[ind_rule.key]
            rule.value = tuple(self.__sid2symbol_tab[val] for val in ind_rule.value)
            rules.append(rule)
        return rules

    @rules.setter
    def rules(self, value: list) -> None:
        """
        Set rules of grammar.
        :param value: list of grammar rules
        :return: None
        :raise: ValueError
        """
        if value is None:
            raise ValueError("Rules must be not None!!!")
        self.clear_rules()
        index = 0
        for rule in value:
            ind_rule = IndRule()
            ind_rule.index = index
            self.__add_symbol_to_tab(rule.key)
            ind_rule.key = self.__symbol2sid_tab[rule.key]
            ind_rule_value = []
            for val in rule.value:
                self.__add_symbol_to_tab(val)
                ind_rule_value.append(self.__symbol2sid_tab[val])
            ind_rule.value = tuple(ind_rule_value)
            self.__rules.append(ind_rule)

    def parse_rules(self, specification: str) -> None:
        """
        Parses and sets rules of grammar.
        :param specification: string of grammar rules
        :return: None
        """
        self.clear_rules()
        index = 0
        for requir in specification.split(';\n'):
            key, values = requir.split('->', 1)
            key = key.strip()
            self.__add_symbol_to_tab(key)
            values = values.strip().split('|\n')
            for value in values:
                rule = IndRule()
                rule.index = index
                rule.key = self.__symbol2sid_tab[key]
                rule_value = []
                for val in value.strip().split(' '):
                    self.__add_symbol_to_tab(val)
                    rule_value.append(self.__symbol2sid_tab[val])
                rule.value = tuple(rule_value)
                self.__rules.append(rule)
                index += 1

    @property
    def goal_nterm(self)-> str:
        return self.symbol(self.__goal_nterm)

    @goal_nterm.setter
    def goal_nterm(self, value: str)-> None:
        self.__del_sid_frm_tab(self.__goal_nterm)
        self.__add_symbol_to_tab(value)
        self.__goal_nterm = self.__symbol2sid_tab[value]

    @property
    def end_term(self) -> str:
        return self.symbol(self.__end_term)

    @end_term.setter
    def end_term(self, value: str) -> None:
        self.__del_sid_frm_tab(self.__end_term)
        self.__add_symbol_to_tab(value)
        self.__end_term = self.__symbol2sid_tab[value]

    @property
    def empty_term(self) -> str:
        return self.symbol(self.__empty_term)

    @empty_term.setter
    def empty_term(self, value: str) -> None:
        self.__del_sid_frm_tab(self.__empty_term)
        self.__add_symbol_to_tab(value)
        self.__empty_term = self.__symbol2sid_tab[value]

    def __is_terminal(self, value: int)-> bool:
        """
        Predicate for definition terminal symbols of grammar
        :param value: symbol for check
        :return: result of check
        """
        if value == self.__end_term:
            return True
        elif value == self.__empty_term:
            return True
        elif value in self.__tokens:
            return True
        else:
            svalue = self.__sid2symbol_tab.get(value, None)
            if not svalue is None:
                if len(svalue) > 1 and\
                   svalue[0] == self.term_segreg[0] and\
                   svalue[-1] == self.term_segreg[-1]:
                    return True
        return False

    def create_sparse_tab(self)-> None:
        """
        Creates parsing table for parser
        :return: None
        """
        rule = None
        if not self.symbol(self.__goal_nterm) is None:
            for r in self.__rules:              # find goal rule
                if r.key == self.__goal_nterm:
                    rule = r
                    break
        if rule is None:
            if len(self.__rules) > 0:
                rule = self.__rules[0]
            else:
                raise EmptyRulesError("List of rules is empty!!!")
        goal_nterm = self.__sid2symbol_tab[rule.key] + self.__ext_goal_sign
        self.__add_symbol_to_tab(goal_nterm)
        goal_nterm = self.__symbol2sid_tab[goal_nterm]
        end_term = self.__end_term
        goal_rule = IndRule(goal_nterm, rule.key)
        goal_rule.index = -1
        ext_rules = [goal_rule] + self.__rules.copy()                           # create extended grammar
        lrpt = LR1Point(rule=goal_rule, iptr=0, lookahead=[end_term])           # create goal LR1-point
        lrstates = create_LR1States(ext_rules, self.__is_terminal, lrpt)        # create LR1-states of LR1 state machine
        lrstates = states_LR1_to_LALR1(lrstates)                                # transform LR1-states to LALR1-states
        self.__sparse_tab = create_sparse_tab(ext_rules, lrstates,              # create parsing table
                                              self.__is_terminal,
                                              goal_nterm,
                                              end_term)
        self.__del_sid_frm_tab(goal_nterm)

    def parse(self) -> Node:
        """
        Parses tokens and constructs parse tree
        :return: root of parse tree
        :raises: NoneLexerError, NoneSParseTabErr,
                EmptyRulesError, ParseSyntaxError,
                UncorrectSParseTabErr
        """
        if self.lexer is None:
            raise NoneLexerError("Lexer is None!!!")
        elif self.__sparse_tab is None:
            raise NoneSParseTabErr("Parsing table is None!!!")
        elif len(self.__rules) == 0:
            raise EmptyRulesError("List of rules is empty!!!")
        st_stack = [0]         # stack of states
        buf = []               # buffer tokens and nodes
        root = None            # root of parse tree
        empty_kind, end_kind = range(-2, 0)
        # create token generator
        # add end terminal how end token
        gen_token = merge_ranges(self.lexer.tokens(),
                      range_objs(Token(end_kind, end_kind)))
        curr_gen_token = gen_token
        token = next(curr_gen_token)            # generate first token
        last_lex = ""                           # last looked lexeme
        flag = token.kind != end_kind           # if there is still tokens
        added_empty = False
        while flag:
            if token.kind == end_kind:               # transform token to sid_term
                sid_term = self.__end_term
            elif token.kind == empty_kind:
                sid_term = self.__empty_term
            else:
                last_lex = self.lexer.lexemes[token.kind][token.value]
                nline_lex = self.lexer.num_line
                ncol_lex = self.lexer.num_column
                sid_term = self.__symbol2sid_tab.get(self.lexer.kinds[token.kind], None)
                if sid_term is None:
                    term = self.term_segreg[0] + \
                           self.lexer.lexemes[token.kind][token.value] + \
                           self.term_segreg[-1]
                    try:
                        sid_term = self.__symbol2sid_tab[term]
                    except KeyError:
                        msg = f"Unexcepted '{last_lex}' in line {nline_lex} in column {ncol_lex}!!!"
                        raise ParseSyntaxError(lexeme=last_lex, num_line=nline_lex,
                                               num_column=ncol_lex, message=msg)
            try:
                # get cell of matrix of syntax analysis
                cell = self.__sparse_tab.cell_hdr(st_stack[-1], sid_term)
            except KeyError:
                raise UncorrectSParseTabErr(f"'{self.__sid2symbol_tab[sid_term]}' " +
                                            "not found in the SParseTable!!!")
            if cell.action == cell.SHF:
                added_empty = False
                st_stack.append(cell.value)    # go to a new state
                buf.append(Node(value=token))  # shift token in buffer
                try:
                    token = next(curr_gen_token)        # generate new token
                except StopIteration:
                    raise UncorrectSParseTabErr(f"Last looked cell in the " +
                          f"SParseTable [{st_stack[-2]}]['{self.__sid2symbol_tab[sid_term]}']")
            elif cell.action == cell.RUL:
                added_empty = False
                rule = self.__rules[cell.value]  # roll up by rule
                if len(rule.value) > 1:
                    ibuf = len(buf) - len(rule.value)  # index of first element for roll up
                    childs = []
                    child = None
                    for i in range(len(rule.value)):
                        child = buf.pop(ibuf)
                        st_stack.pop(-1)
                        if not child.value is None and\
                           child.value.kind == empty_kind:
                            continue
                        childs.append(child)
                    if len(childs) > 1:
                        node = Node()
                        for child in childs:                # add elements as child nodes
                            node.childs.append(child)
                            child.parent = node
                        buf.append(node)                    # replace elements to new node
                    elif len(childs) == 1:
                        buf.append(childs[0])                # replace elements to new node
                    else:
                        buf.append(child)
                else:
                    st_stack.pop(-1)
                try:
                    cell = self.__sparse_tab.cell_hdr(st_stack[-1], rule.key)
                    if cell.action != cell.GOTO:
                        raise UncorrectSParseTabErr(f"Action of cell [{st_stack[-2]}]" +
                                                    f"['{self.__sid2symbol_tab[sid_term]}'] must be GOTO!!!")
                except KeyError:
                    raise UncorrectSParseTabErr(f"'{self.__sid2symbol_tab[rule.key]}' " +
                                                "not found in the SParseTable!!!")
                st_stack.append(cell.value)  # go to new state
                if buf[-1].kind is None:
                    buf[-1].kind = rule.key
            elif cell.action == cell.ACC:
                root = buf[-1]  # set root
                return root
            else:
                if added_empty:
                    msg = f"Unexcepted '{last_lex}' in line {nline_lex} in column {ncol_lex}!!!"
                    raise ParseSyntaxError(lexeme=last_lex, num_line=nline_lex,
                                           num_column=ncol_lex, message=msg)
                else:
                    added_empty = True
                    curr_gen_token = merge_ranges(range_objs(token), gen_token)
                    token = Token(empty_kind, empty_kind)
        return root

    def write_stab_to_file(self, filename: str, buffering = -1)-> None:
        """
        Write rules and SParseTable to file
        :param filename: path to file
        :return: None
        :raises: NoneSParseTabErr, NoneSParseTabErr,
                EmptyRulesError
        """
        if self.__sparse_tab is None:
            raise NoneSParseTabErr("Parsing table is None!!!")
        elif self.__sparse_tab.rows == 0:
            raise NoneSParseTabErr("Parsing table is empty!!!")
        elif len(self.__rules) == 0:
            raise EmptyRulesError("List of rules is empty!!!")
        with open(filename, 'wb', buffering) as file:
            data = self.FILE_KEYWORD_IN_START.encode()
            file.write(struct.pack(f'<{len(data)}s', data))              # write "SPARSER"
            file.write(struct.pack('<Q', len(self.__symbol2sid_tab)))    # write count symbols
            for symbol in self.__symbol2sid_tab:                         # write table of symbols
                sid = self.__symbol2sid_tab[symbol]
                bsymbol = symbol.encode()
                file.write(struct.pack(f'<I{len(bsymbol)}sQ', len(bsymbol), bsymbol, sid))

            data = self.FILE_KEYWORD_BEFORE_RULES.encode()
            file.write(struct.pack(f'<{len(data)}s', data))                  # write "RULES"
            count_rules = len(self.__rules)
            file.write(struct.pack(f'<I', count_rules))                      # write count rules
            for i in range(count_rules):
                file.write(struct.pack(f'<Q', self.__rules[i].key))          # write key
                file.write(struct.pack('<I', len(self.__rules[i].value)))    # write count of values in rule
                for val in self.__rules[i].value:                            # write values
                    file.write(struct.pack(f'<Q', val))

            file.write(struct.pack('<Q', self.__end_term))        # write end term
            file.write(struct.pack('<Q', self.__empty_term))      # write empty term
            file.write(struct.pack('<Q', len(self.__tokens)))     # write count tokens
            for sid_token in self.__tokens:                       # write tokens
                file.write(struct.pack('<Q', sid_token))

            for i in range(2):                                    # write term segreg
                btseg = self.__term_segreg[i].encode()
                file.write(struct.pack(f'<I{len(btseg)}s', len(btseg), btseg))

            data = self.FILE_KEYWORD_BEFORE_HEADERS.encode()
            file.write(struct.pack(f'<{len(data)}s', data))    # write "HDRS"
            hdrs = self.__sparse_tab.headers
            file.write(struct.pack(f'<I', len(hdrs)))          # write count of hdrs
            for hdr in hdrs:                                   # write headers
                file.write(struct.pack(f'<Q', hdr))

            data = self.FILE_KEYWORD_BEFORE_TABLE.encode()
            file.write(struct.pack(f'<{len(data)}s', data))            # write "TAB"
            file.write(struct.pack(f'<I', self.__sparse_tab.rows))     # write count of rows
            for i in range(self.__sparse_tab.rows):                    # write sparse table
                for j in range(self.__sparse_tab.columns):
                    cell = self.__sparse_tab.cell_ind(i, j)
                    file.write(struct.pack(f'<BI', cell.action, cell.value))

    def read_stab_from_file(self, filename: str, buffering = -1)-> None:
        """
        Read rules and SParseTable from file
        :param filename: path to file
        :return: None
        :raise: ReadingSTabFileErr
        """
        read_err_msg = "Uncorrect format of file that contain SParseTable!!!"
        def search_keyword(file, keyword: str, err_msg: str)-> None:
            count_bytes = len(keyword.encode())
            data = struct.unpack(f'<{count_bytes}s', file.read(count_bytes))[0]
            if data.decode() != keyword:
                raise ReadingSTabFileErr(err_msg + " Not found " + keyword + " keyword!!!")

        try:
            with open(filename, 'rb', buffering) as file:
                search_keyword(file, self.FILE_KEYWORD_IN_START, read_err_msg)   # read "SPARSER"
                count_symbols = struct.unpack('<Q', file.read(8))[0]             # read count symbols
                self.__symbol2sid_tab.clear()
                self.__sid2symbol_tab.clear()
                for i in range(count_symbols):                                   # read table of symbols
                    len_symbol = struct.unpack('<I', file.read(4))[0]
                    symbol = struct.unpack(f'<{len_symbol}s', file.read(len_symbol))[0]
                    sid = struct.unpack(f'<Q', file.read(8))[0]
                    symbol = symbol.decode()
                    self.__symbol2sid_tab[symbol] = sid
                    self.__sid2symbol_tab[sid] = symbol

                search_keyword(file, self.FILE_KEYWORD_BEFORE_RULES, read_err_msg)  # read "RULES"
                count_rules = struct.unpack('<I', file.read(4))[0]                  # read count rules
                self.__rules.clear()
                for irule in range(count_rules):                                    # read rules
                    rule = IndRule()
                    rule.index = irule
                    rule.key = struct.unpack('<Q', file.read(8))[0]                 # read rule key
                    count_vals = struct.unpack('<I', file.read(4))[0]               # read count of values
                    vals = []
                    for ival in range(count_vals):                                  # read rule values
                        val = struct.unpack(f'<Q', file.read(8))[0]
                        vals.append(val)
                    rule.value = tuple(vals)
                    self.__rules.append(rule)

                self.__end_term = struct.unpack('<Q', file.read(8))[0]              # read end term
                self.__empty_term = struct.unpack('<Q', file.read(8))[0]            # read empty term
                len_tokens = struct.unpack('<Q', file.read(8))[0]                   # read count of tokens
                tokens = []
                for i in range(len_tokens):                                         # read tokens
                    sid_token = struct.unpack('<Q', file.read(8))[0]
                    tokens.append(sid_token)
                self.__tokens = tuple(tokens)

                term_segreg = []
                for i in range(2):                                                  # read term segreg
                    len_tseg = struct.unpack('<I', file.read(4))[0]
                    tseg = struct.unpack(f'<{len_tseg}s', file.read(len_tseg))[0].decode()
                    term_segreg.append(tseg)
                self.__term_segreg = tuple(term_segreg)

                search_keyword(file, self.FILE_KEYWORD_BEFORE_HEADERS, read_err_msg)  # read "HDRS"
                count_hdrs = struct.unpack('<I', file.read(4))[0]                     # read count of headers
                hdrs = []
                for i in range(count_hdrs):                                           # read hdrs
                    hdr = struct.unpack('<Q', file.read(8))[0]
                    hdrs.append(hdr)

                search_keyword(file, self.FILE_KEYWORD_BEFORE_TABLE, read_err_msg)  # read "TAB"
                count_rows = struct.unpack(f'<I', file.read(4))[0]                  # read count of rows
                sparse_tab = SParseTab(headers=hdrs, rows=count_rows)
                for i in range(sparse_tab.rows):                                    # read SParseTable
                    for j in range(sparse_tab.columns):
                        cell = sparse_tab.cell_ind(i, j)
                        cell.action, cell.value = struct.unpack('<BI', file.read(5))
                self.__sparse_tab = sparse_tab
        except struct.error as err:
            self.__sparse_tab = None
            raise ReadingSTabFileErr(read_err_msg + f" struct.error: {err}")


def print_sparse_tab(parser: SParser, size_cell = 6):
    tab = parser._SParser__sparse_tab
    print('+' + ('-' * size_cell + '+') * (len(tab.headers) + 1))
    print(f"|{' ':^{size_cell}}|", end="")
    for hdr in tab.headers:
        print(f"{str(parser.symbol(hdr)):^{size_cell}}|", end="")
    print()
    print('+' + ('-'*size_cell + '+') * (len(tab.headers) + 1))
    irow = 0
    for row in tab._SParseTab__content:
        print(f"|{str(irow):^{size_cell}}|", end="")
        for e in row:
            print(f"{str(e):^{size_cell}}|", end="")
        print()
        irow += 1
    print('+' + ('-' * size_cell + '+') * (len(tab.headers) + 1))


# if __name__ == "__main__":
#     print('start test1...')
#     GOAL_NTERM = "S"
#     END_TERM = '⊥'
#     EMPTY_TERM = 'ε'
#     RULES = """
#              S -> C C;
#              C -> c C |
#                   d
#             """
#     TOKENS = ('c', 'd')
#     parser = SParser(tokens=TOKENS,
#                      goal_nterm=GOAL_NTERM,
#                      end_term=END_TERM,
#                      empty_term=EMPTY_TERM,
#                      parsing_of_rules=RULES)
#     parser.create_sparse_tab()
#     tab = parser._SParser__sparse_tab
#     print(f"count rows: {tab.rows}")
#     print(f"count cols: {tab.columns}")
#     print_sparse_tab(parser)
#     print("end test1...")
#
#     print()
#
#     print("start test2...")
#     GOAL_NTERM = "E"
#     END_TERM = '⊥'
#     EMPTY_TERM = 'ε'
#     RULES = """
#              E -> E '+' T |
#                   E '-' T |
#                   T;
#              T -> T '*' F |
#                   T '/' F |
#                   F;
#              F -> '(' E ')' |
#                   ID
#             """
#     TOKENS = ('ID',)
#     parser = SParser(tokens=TOKENS,
#                      goal_nterm=GOAL_NTERM,
#                      end_term=END_TERM,
#                      empty_term=EMPTY_TERM,
#                      parsing_of_rules=RULES)
#     parser.create_sparse_tab()
#     tab = parser._SParser__sparse_tab
#     print(f"count rows: {tab.rows}")
#     print(f"count cols: {tab.columns}")
#     print_sparse_tab(parser)
#     print('end test2...')
#
#     """
#     ANSWERS:
#
#     TEST1:
#     count rows: 7
#     count cols: 5
#     +------+------+------+------+------+------+
#     |      |  d   |  ⊥   |  S   |  C   |  c   |
#     +------+------+------+------+------+------+
#     |  0   |  s4  |      |  1   |  2   |  s3  |
#     |  1   |      | acc  |      |      |      |
#     |  2   |  s4  |      |      |  5   |  s3  |
#     |  3   |  s4  |      |      |  6   |  s3  |
#     |  4   |  r2  |  r2  |      |      |  r2  |
#     |  5   |      |  r0  |      |      |      |
#     |  6   |  r1  |  r1  |      |      |  r1  |
#     +------+------+------+------+------+------+
#
#     TEST2:
#     count rows: 16
#     count cols: 11
#     +------+------+------+------+------+------+------+------+------+------+------+------+
#     |      |  E   |  F   | '-'  | '*'  |  ID  | '+'  |  ⊥   | ')'  |  T   | '/'  | '('  |
#     +------+------+------+------+------+------+------+------+------+------+------+------+
#     |  0   |  1   |  3   |      |      |  s5  |      |      |      |  2   |      |  s4  |
#     |  1   |      |      |  s7  |      |      |  s6  | acc  |      |      |      |      |
#     |  2   |      |      |  r2  |  s8  |      |  r2  |  r2  |  r2  |      |  s9  |      |
#     |  3   |      |      |  r5  |  r5  |      |  r5  |  r5  |  r5  |      |  r5  |      |
#     |  4   |  10  |  3   |      |      |  s5  |      |      |      |  2   |      |  s4  |
#     |  5   |      |      |  r7  |  r7  |      |  r7  |  r7  |  r7  |      |  r7  |      |
#     |  6   |      |  3   |      |      |  s5  |      |      |      |  11  |      |  s4  |
#     |  7   |      |  3   |      |      |  s5  |      |      |      |  12  |      |  s4  |
#     |  8   |      |  13  |      |      |  s5  |      |      |      |      |      |  s4  |
#     |  9   |      |  14  |      |      |  s5  |      |      |      |      |      |  s4  |
#     |  10  |      |      |  s7  |      |      |  s6  |      | s15  |      |      |      |
#     |  11  |      |      |  r0  |  s8  |      |  r0  |  r0  |  r0  |      |  s9  |      |
#     |  12  |      |      |  r1  |  s8  |      |  r1  |  r1  |  r1  |      |  s9  |      |
#     |  13  |      |      |  r3  |  r3  |      |  r3  |  r3  |  r3  |      |  r3  |      |
#     |  14  |      |      |  r4  |  r4  |      |  r4  |  r4  |  r4  |      |  r4  |      |
#     |  15  |      |      |  r6  |  r6  |      |  r6  |  r6  |  r6  |      |  r6  |      |
#     +------+------+------+------+------+------+------+------+------+------+------+------+
#     """