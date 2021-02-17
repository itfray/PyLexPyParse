import abc
from typing import NamedTuple
from str_reader import IStrReader


class Token(NamedTuple):
    """
    Token is class for tokenization of data
    """
    kind: str
    value: str


class ILexer(abc.ABC):
    """
    ILexer is interface of lexical analyzer for strings analyzing
    """
    @abc.abstractmethod
    def token(self)-> Token:
        """
        Peforms search lexeme in string data
        :return: tokenized part of data i.e. token
        """
        pass

    @abc.abstractmethod
    def reset(self)-> None:
        """
        Reset lexer in init state of analyzing
        :return: None
        """
        pass

    @abc.abstractproperty
    def data_reader(self)-> IStrReader:
        """
        Property for work with string data reader
        :return: string data reader IStrReader
        """
        pass