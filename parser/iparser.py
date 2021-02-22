import abc
from lexer import ILexer


class Node:
    value = None                        # node value
    parent: Node                        # parent node
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


class IParser(abc.ABC):
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