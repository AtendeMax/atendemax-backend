import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.models.cliente import ClienteCreate, ClienteResponse
from backend.services.fila_service import adicionar_cliente, obter_fila

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # Domínios que podem acessar a API
    allow_credentials=True,      # Permite cookies e autenticação
    allow_methods=["*"],         # Métodos HTTP permitidos (GET, POST, etc.)
    allow_headers=["*"],         # Cabeçalhos permitidos
)

@app.get("/")
def home():
    return {"status": "ok"}

@app.post("/cliente", response_model=ClienteResponse)
def criar_cliente(dados_cliente: ClienteCreate):
    return adicionar_cliente(dados_cliente)


@app.get("/fila", response_model=list[ClienteResponse])
def listar_fila():
    return obter_fila()
