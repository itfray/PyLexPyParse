from .isparser import ISParser, Node, NoneLexerError, ILexer


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