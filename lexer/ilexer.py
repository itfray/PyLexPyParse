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
    def tokens(self):
        """
        Peforms search lexemes in string data
        :return: tokenized parts of data i.e. tokens
        """

    @property
    @abc.abstractmethod
    def data_reader(self)-> IStrReader:
        """
        Property for work with string data reader
        :return: string data reader IStrReader
        """

    @data_reader.setter
    @abc.abstractmethod
    def data_reader(self, value: IStrReader)-> None:
        """
        Property.setter for work with string data reader
        :param value: string reader IStrReader
        :return: None
        """


class LexerError(Exception):
    """
     LexerError is class of errors for lexical analyzer ILexer
    """
    def __init__(self, *args):
        self.args = args


class UnknownLexemeError(LexerError):
    """
     UnknownLexemeError is class of lexical errors for lexical analyzer ILexer.
     Raise when Lexer meet unknown lexeme.
    """
    def __init__(self, *args):
        super().__init__(*args)


class NoneDataReaderError(LexerError):
    """
     NoneDataReaderError is class of errors for lexical analyzer ILexer
     Raise when lexer's data reader not found (is None).
    """
    def __init__(self, *args):
        super().__init__(*args)