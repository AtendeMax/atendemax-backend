from estruturas.fila import Fila
from models.cliente import ClienteCreate, ClienteResponse, FilaResponse

fila_atual = Fila()
contador_id = 1


def adicionar_cliente(dados_cliente: ClienteCreate) -> None:
    global contador_id

    cliente = {
        "id": contador_id,
        "nome": dados_cliente.nome,
        "tipo": dados_cliente.tipo,
    }
    contador_id += 1
    fila_atual.enqueue(cliente)


def obter_fila() -> FilaResponse:
    clientes = [
        ClienteResponse(
            id=cliente["id"],
            nome=cliente["nome"],
            tipo=cliente["tipo"],
            posicao=indice,
        )
        for indice, cliente in enumerate(fila_atual.listar(), start=1)
    ]
    return FilaResponse(total=len(clientes), clientes=clientes)
