from .ilexer import (ILexer, Token, LexerError, UnknownLexemeError,
                     NoneDataReaderError, IStrReader)
import re


class Lexer(ILexer):
    """
    Lexer is lexical analyzer for strings analyzing
    """
    DEFAULT_SIZE_READ_DATA = 256         # default size one portion of read data
    __data_reader: IStrReader            # reader of string data
    __specification: tuple                # lexical specification. Example: (('KIND','[Regex]'),...)
    __token_regex: None                  # compiled specification in regex
    __size_read_data: int                # size one portion of read data
    __num_line = 1                       # current processed line
    __num_column = 1                     # current processed column

    def __init__(self, **kwargs):
        self.data_reader = kwargs.get("data_reader", None)
        self.size_read_data = kwargs.get("size_read_data", self.DEFAULT_SIZE_READ_DATA)
        self.specification = kwargs.get("specification", ())

    def tokens(self):
        if self.__data_reader is None:                                # checks data reader
            raise NoneDataReaderError("Data reader is None!!!")

        self.__data_reader.reset()                                     # resets data reader in init state
        data = self.__data_reader.read(self.size_read_data)            # reads portion of data
        if len(data) == 0 or len(self.specification) == 0:
            return

        self.__num_line = 1             # number of line
        self.__num_column = 1           # number of column
        newline_flag = False            # endpos is newline character?
        start_line = -1                 # position start line

        pos = 0                          # set current pos in data
        endpos = -1                      # pos newline character or end pos of portion data
        while True:
            if pos >= endpos + 1:
                if newline_flag:
                    self.__num_line += 1
                    start_line = pos - 1
                endpos = data.find('\n', endpos + 1, len(data))                  # try find newline character
                if endpos == -1:
                    next_data = self.__data_reader.read(self.size_read_data)     # try find newline in next portion
                    if len(next_data) > 0:
                        data += next_data
                        endpos = data.find('\n', pos + 1, len(data))
                    if endpos == -1:                                             # if still can't find newline
                        endpos = len(data) - 1                                   # set in end of data
                newline_flag = data[endpos] == '\n'

            mtch = self.__token_regex.match(data, pos, endpos + 1)               # find matches of lexeme
            if mtch is None:
                next_data = self.__data_reader.read(self.size_read_data)         # try read yet portion of data
                if len(next_data) > 0:
                    data += next_data
                    continue
                break

            self.__num_column = mtch.start() - start_line

            kind = mtch.lastgroup                       # define kind and value of lexeme
            value = mtch.group()
            yield Token(kind, value)                    # return token

            pos = mtch.end()                            # set new pos
            if pos >= self.size_read_data:              # remove processed portion of data
                data = data[pos:]
                endpos -= pos
                pos = 0

        if pos < len(data):
            self.__num_column += 1
            raise UnknownLexemeError(f"Unexcepted character '{data[pos]}'" +
                                     f" in line {self.__num_line} in column {self.__num_column}!!!")

    @property
    def num_line(self):
        """
        Get number of current processed line
        :return: number of line
        """
        return self.__num_line

    @property
    def num_column(self):
        """
        Get number of current processed column
        :return: number of column
        """
        return self.__num_column

    @property
    def size_read_data(self)-> int:
        """
        Get size read data
        :return: size one portion of read data
        """
        return self.__size_read_data

    @size_read_data.setter
    def size_read_data(self, value: int)-> None:
        """
        Set size read data
        :param value: size one portion of read data
        :return: None
        """
        if value < 1:
            raise ValueError('Size read data value must be greater 0!!!')
        self.__size_read_data = value

    @property
    def specification(self)-> tuple:
        """
        Get lexical specification
        :return: tuple of lexical specification. Example: (('KIND','[Regex]'),...)
        """
        return self.__specification

    @specification.setter
    def specification(self, value: tuple)-> None:
        """
        Set lexical specification
        :param value: tuple of lexical specification
        :return: None
        """
        if value is None:
            raise ValueError("specification must be is not None!!!")
        self.__specification = value
        # compile specification in regex
        self.__token_regex = re.compile("|".join("(?P<%s>%s)" % rule for rule in self.__specification))

    @property
    def data_reader(self)-> IStrReader:
        """
        Get data reader
        :return: data reader with type of IStrReder
        """
        return self.__data_reader

    @data_reader.setter
    def data_reader(self, value: IStrReader)-> None:
        """
        Set data reader
        :param value: data reader with type of IStrReder
        :return: None
        """
        self.__data_reader = value