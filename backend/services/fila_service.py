from ..classes.fila import Fila
from ..classes.cliente import Cliente
from ..models.cliente import ClienteCreate, ClienteResponse

fila_atual = Fila()
contador_id = 1


def _inserir_na_fila(cliente: Cliente) -> None:
    if cliente.tipo == "preferencial":
        for indice, item in enumerate(fila_atual.listar()):
            if item.tipo == "normal":
                fila_atual.inserir(cliente, indice)
                return
    fila_atual.enqueue(cliente)


def _obter_posicao(cliente_id: int) -> int:
    for indice, cliente in enumerate(fila_atual.listar(), start=1):
        if cliente.id == cliente_id:
            return indice
    return 0


def adicionar_cliente(dados_cliente: ClienteCreate) -> ClienteResponse:
    global contador_id

    cliente_id = contador_id
    contador_id += 1

    novo_cliente = Cliente(
        id=cliente_id,
        nome=dados_cliente.nome,
        tipo=dados_cliente.tipo,
    )
    _inserir_na_fila(novo_cliente)

    return ClienteResponse(
        id=novo_cliente.id,
        nome=novo_cliente.nome,
        tipo=novo_cliente.tipo,
        posicao_fila=_obter_posicao(novo_cliente.id),
    )


def obter_fila() -> list[ClienteResponse]:
    return [
        ClienteResponse(
            id=cliente.id,
            nome=cliente.nome,
            tipo=cliente.tipo,
            posicao_fila=indice,
        )
        for indice, cliente in enumerate(fila_atual.listar(), start=1)
    ]
