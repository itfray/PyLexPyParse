from lexer import Token, ILexer, LexerError, UnknownLexemeError
from str_reader import IStrReader
import enum


class Lexer(ILexer):
    __data_reader: IStrReader
    __num_line: int
    __num_column: int

    class LexerState(enum.Enum):
        H = enum.auto()
        NUM = enum.auto()
        ID = enum.auto()
        DLM = enum.auto()
        ASN = enum.auto()
        END = enum.auto()
        ERR = enum.auto()

    def __init__(self, **kwargs):
        super().__init__()
        self.data_reader = kwargs.get("data_reader", None)

        self.KEYWORD, self.DELIM, self.OPASN, self.NUMBER, self.ID = range(0, 5)
        self.tables = {
            self.KEYWORD: ('IF', 'THEN', 'ELSE'),
            self.DELIM: (';', '(', ')'),
            self.OPASN: (":=",),
            self.NUMBER: [],
            self.ID: []
        }
        self.kinds = {
            self.KEYWORD: "KEYWORD",
            self.DELIM: "DELIM",
            self.OPASN: "OPASN",
            self.NUMBER: "NUMBER",
            self.ID: "ID"
        }

    def __getch(self)-> str:
        self.__num_column += 1
        return self.__data_reader.read()

    def tokens(self):
        LexerState = self.LexerState
        if self.__data_reader is None:
            return
        self.__data_reader.reset()

        self.__num_line = 1
        self.__num_column = 1
        getch = self.__getch
        ch = getch()
        if len(ch) == 0:
            return

        buf = ""
        state = LexerState.H
        while len(ch) > 0 and state != LexerState.ERR:
            if state == LexerState.H:
                if ch.isdigit():
                    state = LexerState.NUM
                    buf += ch
                    ch = getch()
                elif ch == "_" or ch.isalpha():
                    state = LexerState.ID
                    buf += ch
                    ch = getch()
                elif ch == ":":
                    state = LexerState.ASN
                    buf += ch
                    ch = getch()
                elif ch.isspace():
                    if ch == '\n':
                        self.__num_line += 1
                        self.__num_column = 1
                    ch = getch()
                    continue
                else:
                    state = LexerState.DLM
            elif state == LexerState.NUM:
                if ch.isdigit():
                    buf += ch
                    ch = getch()
                else:
                    if buf not in self.tables[self.NUMBER]:
                        self.tables[self.NUMBER].append(buf)
                    yield Token(self.kinds[self.NUMBER], buf)
                    buf = ""
                    state = LexerState.H
            elif state == LexerState.ID:
                if ch == "_" or ch.isalpha() or ch.isalpha():
                    buf += ch
                    ch = getch()
                else:
                    if buf in self.tables[self.KEYWORD]:
                        yield Token(self.kinds[self.KEYWORD], buf)
                    else:
                        if buf not in self.tables[self.ID]:
                            self.tables[self.ID].append(buf)
                        yield Token(self.kinds[self.ID], buf)
                    buf = ""
                    state = LexerState.H
            elif state == LexerState.ASN:
                if ch == "=":
                    buf += ch
                    yield Token(self.kinds[self.OPASN], buf)
                    buf = ""
                    state = LexerState.H
                    ch = getch()
                else:
                    state = LexerState.ERR
            elif state == LexerState.DLM:
                if ch in self.tables[self.DELIM]:
                    yield Token(self.kinds[self.DELIM], ch)
                    buf = ""
                    state = LexerState.H
                    ch = getch()
                else:
                    state = LexerState.ERR

        if state == LexerState.ERR:
            raise UnknownLexemeError("Unknown symbol: " + ch + f" in line {self.__num_line}:{self.__num_column}")


    @property
    def data_reader(self)-> IStrReader:
        return self.__data_reader

    @data_reader.setter
    def data_reader(self, value: IStrReader)-> None:
        self.__data_reader = value


if __name__ == "__main__":
    from str_reader.str_reader import StrReader

    statement = """
    a := 1;
    b := (2);
    IF (a) THEN 
        a := 0;
    ELSE
        b := 0;
    """

    lexer = Lexer(data_reader=StrReader(statement))
    for token in lexer.tokens():
        print(token)

    print()