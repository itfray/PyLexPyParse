from lexer import Token, ILexer
from str_reader import IStrReader
import enum


class LexerState(enum.Enum):
    H = enum.auto()
    NUM = enum.auto()
    ID = enum.auto()
    DLM = enum.auto()
    ASN = enum.auto()
    END = enum.auto()
    ERR = enum.auto()


class Lexer(ILexer):
    __data_reader: IStrReader
    __state: LexerState
    __tokener = None

    def __init__(self, **kwargs):
        super().__init__()
        self.data_reader = kwargs.get("data_reader", None)
        self.keywords = kwargs.get("keywords", tuple())
        self.delims = kwargs.get("delims", tuple())
        self.__state = LexerState.H

    def reset(self) -> None:
        pass

    def token(self) -> Token:
        if self.__tokener is None:
            raise
        for token in self.__tokener:
            return token

    def __tokens(self):
        c = self.__data_reader.read(1)
        if len(c) == 0:
            yield Token("", "")
            raise EOFError("No more tokens!!!")

        while not self.__state in (LexerState.ERR, LexerState.END):
            if not self.data_reader.has_data():
                raise SyntaxError("Not found END symbol in string data!!!")
            if self.__state == LexerState.H:
                 if c.isdigit():
                     self.__state = LexerState.NUM


        while True:
            yield Token("", "")
            raise EOFError("No more tokens!!!")

        return Token("", "")

    @property
    def data_reader(self)-> IStrReader:
        return self.__data_reader

    @data_reader.setter
    def data_reader(self, value: IStrReader)-> None:
        self.__data_reader = value


if __name__ == "__main__":
    from str_reader.str_reader import StrReader
    from str_reader.file_reader import FileStrReader

    lexer = Lexer(data_reader=StrReader())
    print(lexer.data_reader)
    lexer.data_reader = FileStrReader()
    print(lexer.data_reader)