from dataclasses import dataclass
from enum import Enum, auto


class TipoToken(Enum):
    SI = auto()
    ENTONCES = auto()
    ELEGIBLE = auto()
    Y = auto()
    O = auto()
    NO = auto()
    IDENT = auto()
    NUMERO = auto()
    TEXTO = auto()
    BOOL = auto()
    LT = auto()
    LE = auto()
    GT = auto()
    GE = auto()
    EQ = auto()
    NE = auto()
    LPAREN = auto()
    RPAREN = auto()
    EOF = auto()


@dataclass
class Token:
    tipo: TipoToken
    valor: object
    pos: int
