from .lexer import Lexer, UnexceptedLexError, NoneDataReaderError
import re
from collections import namedtuple


# Multitoken - is lexeme that consist of one or more lines.
# MultiTokenBounds is tuple of boundary lexemes of multitoken.
# Consist of start lexeme and end lexeme.
MultiTokenBounds = namedtuple('MultiTokenBounds', "start end")

# MultiTokenBound is tuple of boundaty lexeme of multitoken.
# Consist of lexeme value and lexeme regular expression.
MultiTokenBound = namedtuple('MultiTokenBound', "value regex")


class ProgLangLexer(Lexer):
    """
    ProgLangLexer is lexical analyzer of programming language for strings analyzing
    """
    skip_kind: str                              # kind of lexeme that need skip
    id_kind: str                                # kind of lexeme that is identifier
    keyword_kind: str                           # kind of lexeme taht is keyword
    __keywords: tuple                           # keywords of programming language
    case_sensitive: bool                        # is case sensitive?
    __multitokens: dict                         # multitokens of programming language
    __multiregexs: dict                         # compiled regural expressions of multitokens

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.skip_kind = kwargs.get("skip_kind", "")
        self.id_kind = kwargs.get("id_kind", "")
        self.keyword_kind = kwargs.get("keyword_kind", "")
        self.keywords = kwargs.get("keywords", ())
        self.case_sensitive = kwargs.get("case_sensitive", True)
        self.multitokens = kwargs.get("multitokens", dict())

    def _tokens(self):
        """
        Peforms search lexemes in string data
        :return: tokenized parts of data i.e. tokens
        :raise: UnexceptedLexError
        """
        total_regex = self._Lexer__token_regex                              # get total compiled regex
        token_gen = super()._tokens()                                        # get tokens generator
        try:
            while True:
                token = next(token_gen)                                     # get token
                if token.kind == self.skip_kind:
                    token = None                                            # skip token
                elif token.kind == self.id_kind:
                    if not self.case_sensitive:
                        token.value = token.value.lower()
                    if token.value in self.__keywords:                       # token is identifier or keyword?
                        token.kind = self.keyword_kind
                elif token.kind in self.__multitokens:                       # token is multitoken?
                    kind = token.kind
                    bounds = self.__multitokens[kind]                        # get bounds of multitoken
                    if token.value != bounds.start.value:
                        msg = f"Unexcepted character '{token.value}'" + \
                              f" in line {self.num_line} in column {self.num_column}!!!"
                        raise UnexceptedLexError(token.value, self.num_line, self.num_column, msg)
                    yield token
                    self._Lexer__token_regex = self.__multiregexs[kind]      # set compiled regex for multitoken
                    while token.value != bounds.end.value:                   # get values of multitoken
                        token = next(token_gen)
                        token.kind = kind
                        yield token
                    self._Lexer__token_regex = total_regex                   # comeback total regex
                    token = None
                if not token is None:
                    yield token
        except StopIteration:
            pass
        finally:
            self._Lexer__token_regex = total_regex                           # comeback total regex

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
        :raise: ValueError
        """
        if value is None:
            raise ValueError('keywords can not be None!!!')
        self.__keywords = value

    @property
    def multitokens(self)-> dict:
        """
        Get multitokens of programming language.
        Dictionary of multitokens is example:
        {
            'KIND_MULTI_TOKEN': MultiTokenBounds(start = MultiTokenBound(value='...', regex='...'),
                                                 end = MultiTokenBound(value='...', regex='...')),
            ...,
        }
        :return: dict of multitokens
        """
        return self.__multitokens.copy()

    @multitokens.setter
    def multitokens(self, value: dict)-> None:
        """
        Set multitokens of programming language.
        :param value: dict of multitokens
        :return: None
        :raise: ValueError
        """
        if value is None:
            raise ValueError('multitokens can not be None!!!')
        self.__multitokens = value
        self.__multiregexs = dict()
        for kind in self.__multitokens:                             # compile regex of multitokens
            regex = self.__multitokens[kind].end.regex
            self.__multiregexs[kind] = re.compile('((%s)|([^%s]+))' % (regex, regex))