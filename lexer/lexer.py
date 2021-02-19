from .ilexer import (ILexer, Token, LexerError, UnknownLexemeError,
                     NoneDataReaderError, IStrReader)
import re


class Lexer(ILexer):
    __data_reader: IStrReader
    __specification: list
    __token_regex: None
    __token_procs: dict
    __num_line = 1
    __num_column = 1

    def __init__(self, **kwargs):
        self.data_reader = kwargs.get("data_reader", None)
        self.specification = kwargs.get("specification", [])                  # [('KIND', '[A-Za-z]', (lambda: ...,))]

    def tokens(self):
        if self.__data_reader is None:
            raise NoneDataReaderError("Data reader is None!!!")

        self.__data_reader.reset()
        size_data = 256
        data = self.__data_reader.read(size_data)
        if len(data) == 0 or len(self.specification) == 0:
            return

        self.__num_line = 1
        self.__num_column = 1
        start_line = 0
        newline = False

        pos = 0
        endpos = data.find('\n', pos, len(data))
        newline = endpos != -1
        while True:
            if endpos == -1:
                next_data = self.__data_reader.read(size_data)
                if len(next_data) > 0:
                    data += next_data
                    endpos = data.find('\n', pos + 1, len(data))
                    newline = endpos != -1
            if endpos == -1:
                endpos = len(data) - 1
            mtch = self.__token_regex.match(data, pos, endpos + 1)
            if mtch is None:
                next_data = self.__data_reader.read(size_data)
                if len(next_data) > 0:
                    data += next_data
                    continue
                break
            kind = mtch.lastgroup
            value = mtch.group()
            for proc in self.__token_procs[kind]:
                proc()
            yield Token(kind, value)
            pos = mtch.end()
            self.__num_column = pos - start_line
            if pos >= size_data:
                data = data[pos:]
                endpos -= pos
                pos = 0
            if pos >= endpos:
                if newline:
                    self.__num_line += 1
                    start_line = pos - 1
                endpos = data.find('\n', pos + 1, len(data))
                newline = endpos != -1

        if pos < len(data):
            raise UnknownLexemeError(f"Unknown symbol '{data[pos]}'"\
                                     f" in line {self.__num_line} in column {self.__num_column}!!!")

    @property
    def _num_line(self):
        return self.__num_line

    @property
    def _num_column(self):
        return self.__num_column

    @property
    def specification(self)-> list:
        return self.__specification

    @specification.setter
    def specification(self, value: list)-> None:
        if value is None: return
        self.__specification = value.copy()
        self.__token_regex = re.compile("|".join("(?P<%s>%s)" % (kind, reg) for kind, reg, _ in self.__specification))
        self.__token_procs = {kind: procs for kind, _, procs in self.__specification}

    @property
    def data_reader(self)-> IStrReader:
        return self.__data_reader

    @data_reader.setter
    def data_reader(self, value: IStrReader)-> None:
        self.__data_reader = value