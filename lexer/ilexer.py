import abc
from str_reader import IStrReader


class Token:
    """
    Token is class for tokenization of data
    """
    kind: str
    value: str
    def __init__(self, kind = "", value = ""):
        self.kind = kind
        self.value = value

    def __str__(self)-> str:
        return f"Token(kind='{self.kind}'; value='{self.value}')"

    def __repr__(self):
        return self.__str__()


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
    def num_line(self):
        """
        Get number of current processed line
        :return: number of line
        """

    @property
    def num_column(self):
        """
        Get number of current processed column
        :return: number of column
        """

    @property
    @abc.abstractmethod
    def size_read_data(self)-> int:
        """
        Get size read data
        :return: size one portion of read data
        """

    @size_read_data.setter
    @abc.abstractmethod
    def size_read_data(self, value: int)-> None:
        """
        Set size read data
        :param value: size one portion of read data
        :return: None
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


class NoneDataReaderError(LexerError):
    """
     NoneDataReaderError is class of errors for lexical analyzer ILexer
     Raise when lexer's data reader not found (is None).
    """
    def __init__(self, *args):
        super().__init__(*args)


class UnexceptedLexError(LexerError):
    """
     UnexceptedLexError is class of lexical errors for lexical analyzer ILexer.
     Raise when Lexer meet unexcepted lexeme.
    """
    def __init__(self, data, num_line, num_column, *args):
        super().__init__(*args)
        self.data = data
        self.num_line = num_line
        self.num_column = num_column