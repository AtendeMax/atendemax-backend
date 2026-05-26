from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from models.cliente import ClienteCreate, FilaResponse
from services.fila_service import adicionar_cliente, obter_fila

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def healthcheck():
    return {"status": "ok"}


@app.post("/clientes", status_code=status.HTTP_201_CREATED)
def criar_cliente(dados_cliente: ClienteCreate):
    adicionar_cliente(dados_cliente)
    return {"message": "Cliente adicionado à fila com sucesso"}


@app.get("/fila", response_model=FilaResponse)
def listar_fila():
    return obter_fila()

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000)