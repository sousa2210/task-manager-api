# Task Manager API

API REST para gerenciamento de tarefas, desenvolvida com Python e FastAPI. O projeto utiliza SQLite para persistência de dados e Pytest para testes automatizados.

O objetivo é demonstrar conhecimentos práticos em desenvolvimento de APIs, operações CRUD, validação de dados, consultas SQL, tratamento de erros e testes automatizados.

## Tecnologias utilizadas

- **Python 3.13** — linguagem de programação.
- **FastAPI** — construção da API REST.
- **SQLite** — banco de dados relacional.
- **Pydantic** — validação dos dados.
- **Pytest** — testes automatizados.
- **HTTPX** — suporte aos testes das requisições HTTP.
- **Git e GitHub** — versionamento e hospedagem do código.

## Funcionalidades

- Criar tarefas.
- Listar tarefas com paginação.
- Consultar uma tarefa pelo ID.
- Atualizar tarefas completamente com PUT.
- Atualizar campos específicos com PATCH.
- Excluir tarefas.
- Filtrar tarefas pelo status de conclusão.
- Pesquisar tarefas pelo título.
- Combinar filtros de pesquisa e status.
- Validar os dados recebidos.
- Armazenar informações em um banco de dados SQLite.
- Testar os endpoints automaticamente com Pytest.

## Requisitos

- Python instalado.
- Git instalado.
- Terminal PowerShell ou equivalente.

## Como executar o projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/sousa2210/task-manager-api.git
cd task-manager-api
```

### 2. Criar o ambiente virtual

```powershell
python -m venv .venv
```

### 3. Ativar o ambiente virtual

No Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Instalar as dependências

```powershell
python -m pip install -r requirements.txt
```

### 5. Iniciar a API

```powershell
python -m uvicorn main:app --reload
```

A API estará disponível em:

http://127.0.0.1:8000

### 6. Acessar a documentação interativa

Com a aplicação em execução, acesse:

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

A documentação interativa permite consultar os endpoints e realizar requisições diretamente pelo navegador.

## Endpoints

| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/` | Verificar se a API está funcionando |
| GET | `/health` | Verificar a saúde da aplicação |
| POST | `/tasks` | Criar uma tarefa |
| GET | `/tasks` | Listar e filtrar tarefas |
| GET | `/tasks/{task_id}` | Consultar uma tarefa pelo ID |
| PUT | `/tasks/{task_id}` | Atualizar uma tarefa |
| PATCH | `/tasks/{task_id}` | Atualizar campos específicos |
| DELETE | `/tasks/{task_id}` | Excluir uma tarefa |

## Exemplos de utilização

Os exemplos abaixo utilizam a URL local `http://127.0.0.1:8000`.

### Criar uma tarefa

Requisição `POST /tasks`:

```json
{
  "title": "Estudar Python",
  "description": "Praticar desenvolvimento de APIs",
  "completed": false
}
```

### Listar tarefas

Requisição:

```http
GET /tasks
```

### Paginação

Listar até cinco tarefas, começando pelo primeiro resultado:

```http
GET /tasks?limit=5&offset=0
```

- `limit`: quantidade máxima de tarefas retornadas, entre 1 e 100.
- `offset`: quantidade de registros ignorados antes de iniciar a listagem.

### Filtrar por status

Listar somente tarefas concluídas:

```http
GET /tasks?completed=true
```

Listar somente tarefas pendentes:

```http
GET /tasks?completed=false
```

### Pesquisar pelo título

Pesquisar tarefas cujo título contenha a palavra `Python`:

```http
GET /tasks?search=Python
```

### Combinar filtros

Pesquisar tarefas pendentes que contenham `Python` no título:

```http
GET /tasks?completed=false&search=Python&limit=10&offset=0
```

### Consultar uma tarefa específica

```http
GET /tasks/1
```

Substitua `1` pelo ID da tarefa desejada.

### Atualizar uma tarefa parcialmente

Exemplo de requisição `PATCH /tasks/1`:

```json
{
  "completed": true
}
```

O PATCH permite atualizar apenas os campos desejados, sem precisar enviar todos os dados da tarefa.

### Excluir uma tarefa

```http
DELETE /tasks/1
```

Substitua `1` pelo ID da tarefa que deseja excluir.

## Testes automatizados

Para executar os testes, mantenha o ambiente virtual ativado e execute:

```powershell
python -m pytest -v
```

A suíte de testes verifica operações CRUD, validação de entradas, atualização parcial, paginação, filtros, pesquisa por título e tratamento de tarefas inexistentes.

**Status atual:** 23 testes aprovados na última execução.

## Banco de dados

O projeto utiliza SQLite para armazenar as tarefas. O banco de dados é inicializado pela aplicação, e o arquivo do banco local é excluído do versionamento por meio do `.gitignore`.

## Autor

**Vinicio Sousa**

GitHub: https://github.com/sousa2210

Repositório: https://github.com/sousa2210/task-manager-api
