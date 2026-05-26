# AtendeMax

## INTEGRANTES

- Ana Clara Silvestre
- Caio Victor Santos Valentim

## BACKEND 

- FastApi

## FRONTEND

- html, Javascript e bootstrap

## LINK DO JIRA

https://projetosana.atlassian.net/jira/software/projects/FLOW/boards/100/backlog?atlOrigin=eyJpIjoiYjBhYjI4ZmNlMmU5NDA3MzllNzQ0YzBmYTBhMmE4ZDUiLCJwIjoiaiJ9

## PROJETO 03 — Sistema de Atendimento (Fila de Espera)

### Sobre

O **AtendeMax** simula um sistema de atendimento com fila de espera, como em clínicas ou agências bancárias. Este repositório concentra o **backend**, desenvolvido integralmente em **Python**, responsável pelo gerenciamento da fila, prioridades e histórico de atendimentos.

### Requisitos funcionais

| Funcionalidade | Descrição |
|---|---|
| Cadastro de clientes | Registrar cliente com **nome** e **tipo de atendimento** (normal ou preferencial) |
| Entrada na fila | Adicionar cliente à fila de espera após o cadastro |
| Chamada do próximo | Chamar o próximo cliente, respeitando a prioridade (preferencial à frente do normal) |
| Status da fila | Exibir a situação atual da fila, incluindo a posição de cada cliente |
| Histórico | Registrar atendimentos concluídos em uma lista de histórico |
| Cancelamento | Cancelar atendimento e remover o cliente da fila |

### Funcionalidades previstas (a definir em aula)

| Funcionalidade | Descrição |
|---|---|
| Ordenação do histórico | Ordenar atendimentos concluídos por data e hora |
| Busca por nome | Localizar clientes no histórico pelo nome |
| Busca por senha | Localização rápida de cliente por número de senha utilizando **tabela hash** |