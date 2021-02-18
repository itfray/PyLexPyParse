from .ilexer import ILexer, Token, LexerError, UnknownLexemeError, IStrReader
import re


class Lexer(ILexer):
    __data_reader: IStrReader
    __specification: list

    def __init__(self, **kwargs):
        self.data_reader = kwargs.get("data_reader", None)
        self.__specification = kwargs.get("specification", [])                  # [('KIND', '[A-Za-z]', (lambda: ...))]

    def tokens(self):
        if self.__data_reader is None: return
        if not self.__data_reader.has_data(): return
        self.__data_reader.reset()

        size_data = 128
        max_size_data = 128

        callbacks = {kind: procs for kind, reg, procs in self.__specification}
        token_regex = re.compile("|".join("(?P<%s>%s)" % (kind, reg) for kind, reg, procs in self.__specification))

        data = self.__data_reader.read(size_data)
        pos = 0
        while True:
            mtch = token_regex.match(data, pos, len(data))
            if mtch is None:
                if self.__data_reader.has_data():
                    data += self.__data_reader.read(size_data)
                    continue
                break
            kind = mtch.lastgroup
            value = mtch.group()
            for callback in callbacks[kind]:
                callback()
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
        self.__specification = value

    @property
    def data_reader(self)-> IStrReader:
        return self.__data_reader

    @data_reader.setter
    def data_reader(self, value: IStrReader)-> None:
        self.__data_reader = value