from pydantic import BaseModel, field_validator
from typing import Literal


class ClienteCreate(BaseModel):
    nome: str
    tipo: Literal["normal", "preferencial"]

    @field_validator("nome")
    @classmethod
    def validar_nome(cls, valor: str) -> str:
        nome = valor.strip()
        if not nome:
            raise ValueError("Nome não pode ser vazio")
        return nome


class ClienteResponse(BaseModel):
    id: int
    nome: str
    tipo: str
    posicao: int


class FilaResponse(BaseModel):
    total: int
    clientes: list[ClienteResponse]
