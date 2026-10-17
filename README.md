# Task Manager API

API REST para gerenciamento de tarefas, desenvolvida com Python e FastAPI, com persistência de dados em SQLite e testes automatizados.

## Tecnologias utilizadas

- Python
- FastAPI
- SQLite
- Pydantic
- Pytest
- HTTPX

## Funcionalidades

- Criar tarefas.
- Listar todas as tarefas.
- Consultar uma tarefa pelo ID.
- Atualizar tarefas existentes.
- Excluir tarefas.
- Validar os dados recebidos.
- Armazenar tarefas em banco de dados SQLite.
- Executar testes automatizados dos endpoints.

## Requisitos

- Python instalado.
- Git instalado.

## Como executar o projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/sousa2210/task-manager-api.git
cd task-manager-api
```

### 2. Criar o ambiente virtual

No Windows PowerShell:

```powershell
python -m venv .venv
```

### 3. Ativar o ambiente virtual

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

http://127.0.0.1:8000/docs

A documentação permite testar os endpoints diretamente pelo navegador.

## Endpoints

| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/` | Verificar se a API está funcionando |
| GET | `/health` | Verificar a saúde da aplicação |
| POST | `/tasks` | Criar uma tarefa |
| GET | `/tasks` | Listar tarefas |
| GET | `/tasks/{task_id}` | Consultar uma tarefa |
| PUT | `/tasks/{task_id}` | Atualizar uma tarefa |
| DELETE | `/tasks/{task_id}` | Excluir uma tarefa |

## Exemplo de criação de tarefa

Requisição `POST /tasks`:

```json
{
  "title": "Estudar Python",
  "description": "Praticar desenvolvimento de APIs",
  "completed": false
}
```

## Executar os testes

Com o ambiente virtual ativado, execute:

```powershell
python -m pytest -v
```

Os testes verificam a criação, listagem, atualização e exclusão de tarefas, além da validação de entradas e do tratamento de tarefas inexistentes.

## Banco de dados

O projeto utiliza SQLite para armazenar as tarefas. O banco de dados é inicializado automaticamente pela aplicação.

## Autor

Vinicio Sousa

GitHub: https://github.com/sousa2210
