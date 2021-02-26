import abc
from lexer import ILexer


class Node:
    value = None                        # node value
    parent = None                       # parent node
    __childs: list                      # child nodes
    def __init__(self, **kwargs):
        self.parent = kwargs.get('parent', None)
        self.value = kwargs.get('value', None)
        childs = kwargs.get('childs', None)
        self.__childs = [] if childs is None else [child for child in childs]

    @property
    def childs(self)-> list:
        """
        Get list child nodes
        :return:
        """
        return self.__childs


class ISParser(abc.ABC):
    """
    IParser is interface of syntax analyzer
    """
    @abc.abstractmethod
    def parse(self)-> Node:
        """
        Parses tokens and constructs parse tree
        :return: root of parse tree
        """

    @property
    @abc.abstractmethod
    def lexer(self)-> ILexer:
        """
        Get lexer
        :return: lexer
        """

    @lexer.setter
    @abc.abstractmethod
    def lexer(self, value: ILexer)-> None:
        """
        Set lexer
        :param value: lexer
        :return: None
        """


class SParserError(Exception):
    """
     ParserError is class of errors for syntax analyzer IParser
    """
    def __init__(self, *args):
        self.args = args


class NoneLexerError(SParserError):
    """
     NoneLexerError is class of errors for syntax analyzer IParser
     Raise when sparser's lexer not found (is None).
    """
    def __init__(self, *args):
        super().__init__(*args)


class ParseSyntaxError(SParserError):
    """
     ParseSyntaxError is class of errors for syntax analyzer IParser.
     Raise when sparser gets error in syntax analyze.
    """
    def __init__(self, **kwargs):
        super().__init__(kwargs.get("message", ""))
        self.lexeme = kwargs.get("lexeme", "")
        self.num_line = kwargs.get("num_line", -1)
        self.num_column = kwargs.get("num_column", -1)