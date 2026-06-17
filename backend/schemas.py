from pydantic import BaseModel
from typing import Any


class ReglaIn(BaseModel):
    texto: str
    schema_vars: dict[str, str]


class PostulantesIn(BaseModel):
    postulantes: list[dict[str, Any]]


class EvaluarOut(BaseModel):
    ranking: list[dict[str, Any]]
    no_elegibles: list[dict[str, Any]]
