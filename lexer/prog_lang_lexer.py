from .lexer import Lexer


class ProgLangLexer(Lexer):
    skip_kind: str
    id_kind: str
    keyword_kind: str
    __keywords: tuple

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.skip_kind = kwargs.get("skip_kind", "")
        self.id_kind = kwargs.get("id_kind", "")
        self.keyword_kind = kwargs.get("keyword_kind", "")
        self.keywords = kwargs.get("keywords", ())

    def tokens(self):
        for token in super().tokens():
            if token.kind == self.skip_kind:
                continue
            elif token.kind == self.id_kind:
                if token.value in self.keywords:
                    token.kind = self.keyword_kind
            yield token

    @property
    def keywords(self)-> tuple:
        return self.__keywords

    @keywords.setter
    def keywords(self, value: tuple)-> None:
        if value is None:
            raise ValueError('keywords can not be None!!!')
        self.__keywords = value