import abc
from lexer import ILexer


class Node:
    value = None
    __nodes: list
    def __init__(self, **kwargs):
        self.value = kwargs.get('value', None)
        nodes = kwargs.get('nodes', None)
        self.__nodes = [] if nodes is None else [node for node in nodes]

    @property
    def nodes(self)-> list:
        return self.__nodes


class IParser(abc.ABC):
    def parse(self)-> Node:
        """
        :return:
        """

    @property
    @abc.abstractmethod
    def lexer(self)-> ILexer:
        """
        :return:
        """

    @lexer.setter
    @abc.abstractmethod
    def lexer(self, value: ILexer)-> None:
        """
        :param value:
        :return:
        """