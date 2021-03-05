import abc
from str_reader import IStrReader


class Token:
    """
    Token is class for tokenization of data
    """
    kind: object        # token kind
    value: object       # token value
    def __init__(self, kind = None, value = None):
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
    @property
    @abc.abstractmethod
    def kind_ids(self)-> dict:
        """
        Get dict of kinds where
        index is kind and value
        is identifier of kind.
        example: {kind0: kind_id0, ..., kindN: kind_idN}
        :return: dict of kinds
        """

    @property
    @abc.abstractmethod
    def kinds(self)-> list:
        """
        Get list of kinds where
        index is identifier of kind.
        example: [kind0, ..., kindN]
        :return: list of kinds
        """

    @property
    @abc.abstractmethod
    def lexemes(self)-> list:
        """
        Get table of lexemes.
        :return: list of lexemes, grouped by kinds.
                 row index is kind identifier,
                 column index is index of lexeme
                 among lexemes of this kind.
        """

    def tokens(self):
        """
        Peforms search lexemes in string data
        :return: tokenized parts of data i.e. tokens,
                 where kind is index in table of kinds,
                 and kind and value is indexes in table of lexemes
        """
        self.kind_ids.clear()                       # clear tables of kinds
        self.kinds.clear()
        self.lexemes.clear()                        # clear table of lexemes
        for token in self._tokens():
            yield self.new_id_token(token)          # return indexed token

    def new_id_token(self, token: Token)-> Token:
        """
        Create new indexed token.
        Append new kind to dictionary of kinds and
        append new lexeme to table of lexemes.
        :param token: string token, Token(kind, value)
        :return: indexed token, Token(kind_id, value_id)
        """
        if token.kind not in self.kind_ids:
            kind_id = len(self.kind_ids)             # create new kind id
            self.kind_ids[token.kind] = kind_id
            self.kinds.append(token.kind)            # append new kind
            self.lexemes.append([token.value,])      # append new lexeme
            value_id = 0
        else:
            kind_id = self.kind_ids[token.kind]      # return already existing kind id
            try:
                value_id = self.lexemes[kind_id].index(token.value)
            except ValueError:
                self.lexemes[kind_id].append(token.value)    # append new lexeme
                value_id = len(self.lexemes[kind_id]) - 1
        new_token = Token(kind_id, value_id)
        return new_token

    @abc.abstractmethod
    def _tokens(self):
        """
        Peforms search lexemes in string data
        :return: tokenized parts of data i.e. tokens
        """

    @property
    @abc.abstractmethod
    def num_line(self):
        """
        Get number of current processed line
        :return: number of line
        """
        return 0

    @property
    @abc.abstractmethod
    def num_column(self):
        """
        Get number of current processed column
        :return: number of column
        """
        return 0

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