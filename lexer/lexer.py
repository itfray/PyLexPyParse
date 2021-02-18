from .ilexer import (ILexer, Token, LexerError, UnknownLexemeError,
                     NoneDataReaderError, IStrReader)
import re


class Lexer(ILexer):
    __data_reader: IStrReader
    __specification: list
    __token_regex: None
    __token_procs: dict

    def __init__(self, **kwargs):
        self.data_reader = kwargs.get("data_reader", None)
        self.specification = kwargs.get("specification", [])                  # [('KIND', '[A-Za-z]', (lambda: ...))]

    def tokens(self):
        if self.__data_reader is None:
            raise NoneDataReaderError("Data reader is None!!!")

        self.__data_reader.reset()
        if not self.__data_reader.has_data() or len(self.specification) == 0:
            return

        size_data = 256
        max_size_data = 1024

        data = self.__data_reader.read(size_data)
        pos = 0
        while True:
            mtch = self.__token_regex.match(data, pos, len(data))
            if mtch is None:
                if self.__data_reader.has_data():
                    data += self.__data_reader.read(size_data)
                    continue
                break
            kind = mtch.lastgroup
            value = mtch.group()
            for proc in self.__token_procs[kind]:
                proc()
            yield Token(kind, value)
            pos = mtch.end()
            if pos + 1 >= max_size_data:
                data = data[pos:]
                pos = 0

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