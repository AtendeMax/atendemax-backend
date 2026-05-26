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

## LINK DO JIRA

https://projetosana.atlassian.net/jira/software/projects/FLOW/boards/100/backlog?atlOrigin=eyJpIjoiYjBhYjI4ZmNlMmU5NDA3MzllNzQ0YzBmYTBhMmE4ZDUiLCJwIjoiaiJ9

## PROJETO 03 — Sistema de Atendimento (Fila de Espera)

### Sobre

O **AtendeMax** simula um sistema de atendimento com fila de espera. Este repositório contém o **backend** em Python, responsável por gerenciar a fila em memória usando a estrutura de dados **Fila (FIFO)**.

---

## Como executar

### Pré-requisitos

- Python 3.10 ou superior
- Git

### Instalação

1. Clone o repositório:

```bash
git clone <url-do-repositorio>
cd AtendeMax
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

### Swagger (documentação interativa)

Acesse no navegador:

http://127.0.0.1:8000/docs

---

## Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/` | Healthcheck — verifica se a API está online |
| POST | `/clientes` | Cadastra cliente e adiciona à fila |
| GET | `/fila` | Retorna total e lista de clientes com posição |

### Exemplo — cadastrar cliente

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
  "message": "Cliente adicionado à fila com sucesso"
}
```

Tipos aceitos: `normal` ou `preferencial`.

### Exemplo — consultar fila

**GET** `/fila`

```json
{
  "total": 2,
  "clientes": [
    {
      "id": 1,
      "nome": "Ana",
      "tipo": "normal",
      "posicao": 1
    },
    {
      "id": 2,
      "nome": "Bruno",
      "tipo": "preferencial",
      "posicao": 2
    }
  ]
}
```

A posição `1` representa o primeiro da fila.

---

## Estrutura do projeto

```
AtendeMax/
├── main.py              # API FastAPI
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
- GET `/fila` retorna total e posições corretas
- Nome vazio retorna erro 422
- Tipo inválido retorna erro 422
- Swagger acessível em `/docs`
