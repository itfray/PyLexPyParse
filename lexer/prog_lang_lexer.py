from .lexer import Lexer
import re
from collections import namedtuple


MultiTokenBounds = namedtuple('MultiTokenBounds', "start end")
MultiTokenBound = namedtuple('MultiTokenBound', "value regex")


class ProgLangLexer(Lexer):
    """
    ProgLangLexer is lexical analyzer of programming language for strings analyzing
    """
    skip_kind: str                              # kind of lexeme that need skip
    id_kind: str                                # kind of lexeme that is identifier
    keyword_kind: str                           # kind of lexeme taht is keyword
    __keywords: tuple                           # keywords of programming language
    case_sensitive: bool
    __multitokens: dict                         # {'KIND': (start=(value='...', regex='...'), end=(...)), ...}
    __multiregexs: dict

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.skip_kind = kwargs.get("skip_kind", "")
        self.id_kind = kwargs.get("id_kind", "")
        self.keyword_kind = kwargs.get("keyword_kind", "")
        self.keywords = kwargs.get("keywords", ())
        self.case_sensitive = kwargs.get("case_sensitive", True)
        self.multitokens = kwargs.get("multitokens", dict())            # re.compile(r'(?P<>.+)')

    def tokens(self):
        total_regex = self._Lexer__token_regex
        token_gen = super().tokens()
        try:
            while True:
                token = next(token_gen)
                if token.kind == self.skip_kind:
                    token = None                                            # skip token
                elif token.kind == self.id_kind:
                    if not self.case_sensitive:
                        token.value = token.value.lower()
                    if token.value in self.__keywords:                       # check identifier or keyword
                        token.kind = self.keyword_kind
                elif token.kind in self.__multitokens:
                    kind = token.kind
                    bounds = self.__multitokens[kind]
                    if token.value != bounds.start.value and \
                       bounds.start.value != bounds.end.value:
                        raise UnknownLexemeError(f"Unexcepted character '{token.value}'" +
                                                 f" in line {self.num_line} in column {self.num_column}!!!")
                    yield token
                    self._Lexer__token_regex = self.__multiregexs[kind]
                    while token.value != bounds.end.value:
                        token = next(token_gen)
                        token.kind = kind
                        yield token
                    self._Lexer__token_regex = total_regex
                    token = None
                if not token is None:
                    yield token
        except StopIteration:
            self._Lexer__token_regex = total_regex

    @property
    def keywords(self)-> tuple:
        """
        Get keywords of programming language
        :return: tuple of keywords
        """
        return self.__keywords

    @keywords.setter
    def keywords(self, value: tuple)-> None:
        """
        Set keywords of programming language
        :param value: tuple of keywords
        :return: None
        """
        if value is None:
            raise ValueError('keywords can not be None!!!')
        self.__keywords = value

    @property
    def multitokens(self)-> dict:
        return self.__multitokens.copy()

    @multitokens.setter
    def multitokens(self, value: dict)-> None:
        if value is None:
            raise ValueError('multitokens can not be None!!!')
        self.__multitokens = value
        self.__multiregexs = dict()
        for kind in self.__multitokens:
            regex = self.__multitokens[kind].end.regex
            self.__multiregexs[kind] = re.compile('((%s)|([^%s]+))' % (regex, regex))