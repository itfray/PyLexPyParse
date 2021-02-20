from .lexer import Lexer


class ProgLangLexer(Lexer):
    """
    ProgLangLexer is lexical analyzer of programming language for strings analyzing
    """
    skip_kind: str                                              # kind of lexeme that need skip
    id_kind: str                                                # kind of lexeme that is identifier
    keyword_kind: str                                           # kind of lexeme taht is keyword
    __keywords: tuple                                           # keywords of programming language
    case_sensitive: bool

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.skip_kind = kwargs.get("skip_kind", "")
        self.id_kind = kwargs.get("id_kind", "")
        self.keyword_kind = kwargs.get("keyword_kind", "")
        self.keywords = kwargs.get("keywords", ())
        self.case_sensitive = kwargs.get("case_sensitive", True)

    def tokens(self):
        for token in super().tokens():
            if token.kind == self.skip_kind:
                continue                                            # skip token
            elif token.kind == self.id_kind:
                if not self.case_sensitive:
                    token.value = token.value.lower()
                if token.value in self.keywords:                             # check identifier or keyword
                    token.kind = self.keyword_kind
            yield token                                             # return token

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