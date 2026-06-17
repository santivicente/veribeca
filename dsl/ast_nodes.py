from dataclasses import dataclass


@dataclass
class Comparacion:
    variable: str
    operador: str
    valor: object


@dataclass
class OpBinaria:
    operador: str
    izquierda: object
    derecha: object


@dataclass
class Negacion:
    expr: object


@dataclass
class Regla:
    condicion: object
