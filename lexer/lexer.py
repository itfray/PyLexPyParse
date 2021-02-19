from .ilexer import (ILexer, Token, LexerError, UnknownLexemeError,
                     NoneDataReaderError, IStrReader)
import re


class Lexer(ILexer):
    """
    Lexer is lexical analyzer for strings analyzing
    """
    DEFAULT_SIZE_READ_DATA = 256         # default size one portion of read data
    __data_reader: IStrReader            # reader of string data
    __specification: list                # lexical specification. Example: [('KIND', '[Regex]', (func, ...)), ...]
    __token_regex: None                  # compiled specification in regex
    __token_procs: dict                  # dictionary of callback procedures from specification
    __size_read_data: int                # size one portion of read data
    __num_line = 1                       # current processed line
    __num_column = 1                     # current processed column

    def __init__(self, **kwargs):
        self.data_reader = kwargs.get("data_reader", None)
        self.size_read_data = kwargs.get("size_read_data", self.DEFAULT_SIZE_READ_DATA)
        self.specification = kwargs.get("specification", [])

    def tokens(self):
        if self.__data_reader is None:                                # checks data reader
            raise NoneDataReaderError("Data reader is None!!!")

        self.__data_reader.reset()                                     # resets data reader in init state
        data = self.__data_reader.read(self.size_read_data)            # reads portion of data
        if len(data) == 0 or len(self.specification) == 0:
            return

        self.__num_line = 1
        self.__num_column = 1

        pos = 0                          # set current pos in data
        endpos = -1                      # pos newline character or end pos of portion data
        while True:
            if pos >= endpos:
                endpos = data.find('\n', endpos + 1, len(data))                  # try find newline character
                if endpos == -1:
                    next_data = self.__data_reader.read(self.size_read_data)     # try find newline in next portion
                    if len(next_data) > 0:
                        data += next_data
                        endpos = data.find('\n', pos + 1, len(data))
                    if endpos == -1:                                             # if still can't find newline
                        endpos = len(data) - 1                                   # set in end of data

            mtch = self.__token_regex.match(data, pos, endpos + 1)               # find matches of lexeme
            if mtch is None:
                next_data = self.__data_reader.read(self.size_read_data)         # try read yet portion of data
                if len(next_data) > 0:
                    data += next_data
                    continue
                break

            kind = mtch.lastgroup                       # define kind and value of lexeme
            value = mtch.group()
            for proc in self.__token_procs[kind]:       # call all callback functions for lexeme
                proc()
            yield Token(kind, value)

            pos = mtch.end()                            # set new pos
            if pos >= self.size_read_data:              # remove processed portion of data
                data = data[pos:]
                endpos -= pos
                pos = 0

        if pos < len(data):
            raise UnknownLexemeError(f"Unknown symbol '{data[pos]}'"\
                                     f" in line {self.__num_line} in column {self.__num_column}!!!")

    @property
    def num_line(self):
        return self.__num_line

    @property
    def num_column(self):
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
    def specification(self)-> list:
        """
        Get lexical specification
        :return: list of lexical specification. Example: [('KIND', '[Regex]', (func, ...)), ...]
        """
        return self.__specification.copy()

    @specification.setter
    def specification(self, value: list)-> None:
        """
        Set lexical specification
        :param value: list of lexical specification. Example: [('KIND', '[Regex]', (func, ...)), ...]
        :return: None
        """
        if value is None: return
        self.__specification = value.copy()
        # compile specification in regex
        self.__token_regex = re.compile("|".join("(?P<%s>%s)" % (kind, reg)
                                                 for kind, reg, _ in self.__specification))
        # prepare dict with callback functions
        self.__token_procs = {kind: procs for kind, _, procs in self.__specification}

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