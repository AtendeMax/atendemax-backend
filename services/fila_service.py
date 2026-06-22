from datetime import datetime, timezone

from estruturas.fila import Fila
from models.cliente import ClienteCreate, ClienteResponse, FilaResponse

fila_atual = Fila()
historico: list[dict] = []
contador_id = 1


def _agora_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _para_response(cliente: dict, posicao: int | None = None) -> ClienteResponse:
    return ClienteResponse(
        id=cliente["id"],
        nome=cliente["nome"],
        tipo=cliente["tipo"],
        status=cliente["status"],
        posicao=posicao,
        horario_inicio=cliente.get("horario_inicio"),
        horario_conclusao=cliente.get("horario_conclusao"),
    )


def _buscar_na_fila(cliente_id: int) -> dict | None:
    for cliente in fila_atual.listar():
        if cliente["id"] == cliente_id:
            return cliente
    return None


def adicionar_cliente(dados_cliente: ClienteCreate) -> ClienteResponse:
    global contador_id

    cliente = {
        "id": contador_id,
        "nome": dados_cliente.nome,
        "tipo": dados_cliente.tipo,
        "status": "aguardando",
        "horario_inicio": None,
        "horario_conclusao": None,
    }
    contador_id += 1

    itens = fila_atual.listar()

    if dados_cliente.tipo == "preferencial":
        posicao_insercao = 0
        for indice, item in enumerate(itens):
            if item["tipo"] == "preferencial":
                posicao_insercao = indice + 1
            else:
                break
        fila_atual.inserir_em(posicao_insercao, cliente)
        return _para_response(cliente, posicao_insercao + 1)

    fila_atual.enqueue(cliente)
    return _para_response(cliente, len(itens) + 1)


def obter_fila() -> FilaResponse:
    clientes = [
        _para_response(cliente, indice)
        for indice, cliente in enumerate(fila_atual.listar(), start=1)
    ]
    return FilaResponse(total=len(clientes), clientes=clientes)


def chamar_proximo() -> ClienteResponse:
    itens = fila_atual.listar()

    if any(cliente["status"] == "em_atendimento" for cliente in itens):
        raise ValueError("Já existe um cliente em atendimento.")

    proximo = next(
        (cliente for cliente in itens if cliente["status"] == "aguardando"),
        None,
    )
    if proximo is None:
        raise LookupError("Não há clientes aguardando na fila.")

    proximo["status"] = "em_atendimento"
    proximo["horario_inicio"] = _agora_iso()

    posicao = itens.index(proximo) + 1
    return _para_response(proximo, posicao)


def cancelar_cliente(cliente_id: int) -> None:
    cliente = _buscar_na_fila(cliente_id)
    if cliente is None:
        raise LookupError("Cliente não encontrado.")

    if cliente["status"] != "aguardando":
        raise ValueError("Apenas clientes aguardando podem ser cancelados.")

    cliente["status"] = "cancelado"
    historico.append(cliente)
    fila_atual.remover_por_id(cliente_id)


def concluir_atendimento(cliente_id: int) -> None:
    cliente = _buscar_na_fila(cliente_id)
    if cliente is None:
        raise LookupError("Cliente não encontrado.")

    if cliente["status"] != "em_atendimento":
        raise ValueError("Cliente não está em atendimento.")

    cliente["status"] = "concluido"
    cliente["horario_conclusao"] = _agora_iso()
    historico.append(cliente)
    fila_atual.remover_por_id(cliente_id)


def _chave_data_hora(cliente: dict) -> str:
    return cliente.get("horario_conclusao") or cliente.get("horario_inicio") or ""


def obter_historico(
    tipo: str | None = None,
    status: str | None = None,
    nome: str | None = None,
) -> FilaResponse:
    clientes_filtrados = historico

    if tipo is not None:
        clientes_filtrados = [
            cliente for cliente in clientes_filtrados if cliente["tipo"] == tipo
        ]

    if status is not None:
        clientes_filtrados = [
            cliente for cliente in clientes_filtrados if cliente["status"] == status
        ]

    if nome is not None:
        termo = nome.strip().lower()
        if termo:
            clientes_filtrados = [
                cliente
                for cliente in clientes_filtrados
                if termo in cliente["nome"].lower()
            ]

    clientes_filtrados = sorted(
        clientes_filtrados,
        key=_chave_data_hora,
        reverse=True,
    )

    clientes = [_para_response(cliente) for cliente in clientes_filtrados]
    return FilaResponse(total=len(clientes), clientes=clientes)
