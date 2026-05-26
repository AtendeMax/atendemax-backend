from structures.fila import Fila
from models.cliente import ClienteCreate, ClienteResponse

fila_atual = Fila()
contador_id = 1

def adicionar_cliente(dados_cliente: ClienteCreate) -> ClienteResponse:
