from pydantic import BaseModel, StringConstraints, ConfigDict
from typing import Annotated, Literal

class ClienteCreate(BaseModel):
    nome: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=255)]
    tipo: Literal["normal", "preferencial"]

class ClienteResponse(BaseModel):
    id: int
    nome: str
    tipo: str
    posicao_fila: int

    model_config = ConfigDict(from_attributes=True)

'''a = ClienteCreate(nome="João Silva", tipo="preferencial")
print(a)
b = ClienteResponse(id=1, nome="João Silva", tipo="preferencial", posicao_fila=1)
print(b)'''