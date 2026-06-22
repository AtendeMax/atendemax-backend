# AtendeMax

## INTEGRANTES

- Ana Clara Silvestre
- Caio Victor Santos Valentim
- Adilson Valtim de Almeida Júnior

## BACKEND

- FastAPI
- Python 3

## FRONTEND

- HTML, JavaScript e Bootstrap
- Repositório separado — roda em `http://127.0.0.1:5500`

## LINK DO JIRA

https://projetosana.atlassian.net/jira/software/projects/FLOW/boards/100/backlog?atlOrigin=eyJpIjoiYjBhYjI4ZmNlMmU5NDA3MzllNzQ0YzBmYTBhMmE4ZDUiLCJwIjoiaiJ9

## PROJETO 03 — Sistema de Atendimento (Fila de Espera)

### Etapa 04 — Busca e ordenação

Funcionalidades implementadas no histórico (`GET /historico`):

- **Ordenação por data e hora:** registros retornados do mais recente para o mais antigo, usando `sorted()` com `horario_conclusao` ou `horario_inicio`.
- **Busca por nome:** filtro parcial via query string `?nome=...` (case-insensitive), integrado ao campo de filtro do frontend.

### Sobre

O **AtendeMax** simula um sistema de atendimento com fila de espera. Este repositório contém o **backend** em Python, responsável por gerenciar a fila em memória usando a estrutura de dados **Fila (FIFO)**.

A API expõe os endpoints consumidos pelo frontend: cadastro, fila ativa, chamar próximo, cancelar, concluir atendimento e histórico.

---

## Como executar

### Pré-requisitos

- Python 3.10 ou superior
- Git

### Instalação

1. Clone o repositório:

```bash
git clone <url-do-repositorio>
cd AtendeMax-backend
```

2. Crie e ative o ambiente virtual:

```bash
python -m venv venv
```

**Windows:**

```bash
venv\Scripts\activate
```

**Linux/Mac:**

```bash
source venv/bin/activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

### Execução

Suba a API com:

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Ou:

```bash
python main.py
```

A API ficará disponível em: http://127.0.0.1:8000

### Integração com o frontend

O frontend deve estar rodando em `http://127.0.0.1:5500` (ex.: `python -m http.server 5500`). O CORS da API já está configurado para essa origem.

### Swagger (documentação interativa)

Acesse no navegador:

http://127.0.0.1:8000/docs

---

## Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/` | Healthcheck — verifica se a API está online |
| GET | `/fila` | Retorna clientes aguardando ou em atendimento |
| POST | `/clientes` | Cadastra cliente e adiciona à fila |
| POST | `/fila/chamar` | Chama o próximo cliente da fila |
| DELETE | `/clientes/{id}` | Cancela cliente aguardando |
| POST | `/atendimentos/{id}/concluir` | Finaliza atendimento em andamento |
| GET | `/historico` | Retorna histórico ordenado por data/hora, com filtros opcionais |

### Ciclo de vida do cliente

```
aguardando  →  POST /clientes
     │
     ├── POST /fila/chamar  →  em_atendimento
     │                              │
     │                              └── POST /atendimentos/{id}/concluir  →  concluido
     │
     └── DELETE /clientes/{id}  →  cancelado
```

Registros `concluido` e `cancelado` aparecem em `GET /historico`. Apenas `aguardando` e `em_atendimento` aparecem em `GET /fila`.

### Regras de negócio

- Clientes **preferencial** entram na frente dos **normal** (FIFO dentro de cada grupo).
- Apenas **um** cliente pode estar `em_atendimento` por vez.
- Cancelamento permitido somente para status `aguardando`.
- Conclusão permitida somente para status `em_atendimento`.
- Timestamps em ISO 8601 UTC (ex.: `2026-06-09T14:00:00Z`).

---

## Exemplos

### Cadastrar cliente

**POST** `/clientes`

```json
{
  "nome": "João Silva",
  "tipo": "normal"
}
```

**Resposta (201):**

```json
{
  "message": "Cliente adicionado à fila com sucesso.",
  "cliente": {
    "id": 1,
    "nome": "João Silva",
    "tipo": "normal",
    "status": "aguardando",
    "posicao": 1,
    "horario_inicio": null,
    "horario_conclusao": null
  }
}
```

Tipos aceitos: `normal` ou `preferencial`.

### Consultar fila

**GET** `/fila`

```json
{
  "total": 2,
  "clientes": [
    {
      "id": 1,
      "nome": "Ana",
      "tipo": "preferencial",
      "status": "aguardando",
      "posicao": 1,
      "horario_inicio": null,
      "horario_conclusao": null
    },
    {
      "id": 2,
      "nome": "Bruno",
      "tipo": "normal",
      "status": "em_atendimento",
      "posicao": 2,
      "horario_inicio": "2026-06-09T14:00:00Z",
      "horario_conclusao": null
    }
  ]
}
```

A posição `1` representa o primeiro da fila.

### Chamar próximo

**POST** `/fila/chamar`

**Resposta (200):**

```json
{
  "message": "Próximo cliente chamado com sucesso.",
  "cliente": {
    "id": 1,
    "nome": "Ana",
    "tipo": "preferencial",
    "status": "em_atendimento",
    "posicao": 1,
    "horario_inicio": "2026-06-09T14:00:00Z",
    "horario_conclusao": null
  }
}
```

Erros comuns: **404** (fila vazia), **409** (já existe cliente em atendimento).

### Cancelar cliente

**DELETE** `/clientes/1`

**Resposta (200):**

```json
{
  "message": "Cliente cancelado com sucesso.",
  "cliente": null
}
```

### Concluir atendimento

**POST** `/atendimentos/1/concluir`

**Resposta (200):**

```json
{
  "message": "Atendimento concluído com sucesso.",
  "cliente": null
}
```

### Consultar histórico

O histórico é retornado **ordenado por data e hora** (mais recente primeiro), usando `horario_conclusao` ou, na ausência dele, `horario_inicio`.

**GET** `/historico`

**GET** `/historico?tipo=preferencial`

**GET** `/historico?status=concluido`

**GET** `/historico?nome=joao`

**GET** `/historico?tipo=normal&status=cancelado&nome=maria`

Filtros disponíveis:

| Parâmetro | Descrição |
|-----------|-----------|
| `tipo` | `normal` ou `preferencial` |
| `status` | `concluido` ou `cancelado` |
| `nome` | Busca parcial por nome (sem diferenciar maiúsculas/minúsculas) |

```json
{
  "total": 1,
  "clientes": [
    {
      "id": 1,
      "nome": "João Silva",
      "tipo": "normal",
      "status": "concluido",
      "posicao": null,
      "horario_inicio": "2026-06-09T14:00:00Z",
      "horario_conclusao": "2026-06-09T14:15:00Z"
    }
  ]
}
```

### Teste rápido com curl

```bash
curl -X POST http://127.0.0.1:8000/clientes \
  -H "Content-Type: application/json" \
  -d '{"nome":"Maria","tipo":"preferencial"}'

curl http://127.0.0.1:8000/fila

curl -X POST http://127.0.0.1:8000/fila/chamar \
  -H "Content-Type: application/json"

curl -X POST http://127.0.0.1:8000/atendimentos/1/concluir \
  -H "Content-Type: application/json"

curl "http://127.0.0.1:8000/historico?status=concluido"

curl "http://127.0.0.1:8000/historico?nome=maria"
```

---

## Estrutura do projeto

```
AtendeMax-backend/
├── main.py              # API FastAPI e rotas
├── requirements.txt
├── estruturas/
│   └── fila.py          # Estrutura de dados Fila (FIFO)
├── models/
│   └── cliente.py       # Models Pydantic
└── services/
    └── fila_service.py  # Lógica de negócio
```

---

## Testes realizados

- GET `/` retorna status ok
- POST `/clientes` cadastra cliente com sucesso (201)
- GET `/fila` retorna total, posições, status e horários
- POST `/fila/chamar` promove próximo respeitando prioridade preferencial
- POST `/fila/chamar` retorna 409 quando já há cliente em atendimento
- POST `/fila/chamar` retorna 404 quando não há clientes aguardando
- DELETE `/clientes/{id}` cancela cliente aguardando e move para histórico
- POST `/atendimentos/{id}/concluir` finaliza atendimento com `horario_conclusao`
- GET `/historico` retorna registros ordenados por data/hora (mais recente primeiro)
- GET `/historico` aceita filtros `tipo`, `status` e busca por `nome`
- Nome vazio retorna erro 422
- Tipo inválido retorna erro 422
- Swagger acessível em `/docs`
- CORS habilitado para o frontend em `http://127.0.0.1:5500`
