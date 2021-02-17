from lexer import Token, ILexer
from str_reader import IStrReader
from str_reader.str_reader import StrReader
from str_reader.file_reader import FileStrReader


class Lexer(ILexer):
    __data_reader: IStrReader

    def __init__(self, data_reader: IStrReader):
        super().__init__()
        self.data_reader = data_reader

    def reset(self) -> None:
        pass

    def token(self) -> Token:
        return Token("", "")

    @property
    def data_reader(self)-> IStrReader:
        return self.__data_reader

    @data_reader.setter
    def data_reader(self, value: IStrReader)-> None:
        self.__data_reader = value


if __name__ == "__main__":
    lexer = Lexer(StrReader())
    print(lexer.data_reader)
    lexer.data_reader = FileStrReader()
    print(lexer.data_reader)