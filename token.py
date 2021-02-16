from typing import NamedTuple


class Token(NamedTuple):
    """
    Token is class for tokenization of data
    """
    kind: str
    value: str