# Task Manager API

API REST para gerenciamento de tarefas, desenvolvida com **Python e FastAPI**, com autenticação JWT, controle de acesso por usuário e persistência de dados em bancos relacionais.

O projeto utiliza **SQLite no ambiente local** e **PostgreSQL em produção**, com deploy realizado no Render e banco hospedado no Neon.

O objetivo é demonstrar conhecimentos práticos em desenvolvimento Backend, construção de APIs REST, autenticação, autorização, integração com bancos de dados, validação de dados e testes automatizados.

## Demonstração

- **API em produção:** https://task-manager-api-vinicio.onrender.com/
- **Documentação Swagger:** https://task-manager-api-vinicio.onrender.com/docs
- **Documentação ReDoc:** https://task-manager-api-vinicio.onrender.com/redoc
- **Repositório GitHub:** https://github.com/sousa2210/task-manager-api

## Tecnologias

- Python 3.13
- FastAPI
- Pydantic
- SQLite — desenvolvimento local
- PostgreSQL — produção
- Neon — hospedagem do banco PostgreSQL
- Render — hospedagem da API
- PyJWT — autenticação por tokens
- Argon2 com pwdlib — hash de senhas
- Psycopg — conexão com PostgreSQL
- Pytest e HTTPX — testes automatizados
- Docker e Docker Compose
- Git e GitHub

## Funcionalidades

### Autenticação e segurança

- Cadastro de usuários.
- Login com e-mail e senha.
- Senhas armazenadas com hash Argon2.
- Tokens JWT com validade de 30 minutos.
- Proteção dos endpoints de tarefas.
- Isolamento dos dados por usuário autenticado.

### Gerenciamento de tarefas

- Criar, listar, consultar, atualizar e excluir tarefas.
- Atualização completa com PUT e parcial com PATCH.
- Filtro por status de conclusão.
- Pesquisa por título.
- Paginação com limit e offset.
- Validação de dados e tratamento de erros.

### Banco de dados

- Persistência local com SQLite.
- PostgreSQL em ambiente de produção.
- Integração com Neon.
- Suporte a diferentes bancos por configuração de ambiente.

## Arquitetura e implantação

A aplicação utiliza uma configuração que permite trabalhar com diferentes bancos de dados:

| Ambiente | Banco de dados | Hospedagem |
|---|---|---|
| Desenvolvimento | SQLite | Local |
| Produção | PostgreSQL | Neon |
| API em produção | FastAPI | Render |

A conexão com o PostgreSQL é configurada pela variável de ambiente `DATABASE_URL`.

A chave utilizada para assinar os tokens JWT é configurada por `JWT_SECRET_KEY`.

As credenciais não devem ser armazenadas diretamente no código-fonte.

## Requisitos

- Python 3.13 ou compatível.
- Git.

## Como executar localmente

### 1. Clonar o repositório

```bash
git clone https://github.com/sousa2210/task-manager-api.git
cd task-manager-api
```

### 2. Criar e ativar o ambiente virtual

No Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Instalar as dependências

```powershell
python -m pip install -r requirements.txt
```

### 4. Configurar a chave JWT

No PowerShell:

```powershell
$env:JWT_SECRET_KEY = python -c "import secrets; print(secrets.token_urlsafe(48))"
```

Não compartilhe essa chave nem a publique no GitHub.

### 5. Iniciar a API

```powershell
python -m uvicorn main:app --reload
```

A aplicação estará disponível em:

- API: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

O banco SQLite é inicializado automaticamente quando a aplicação inicia.

## Autenticação

### Cadastrar usuário

`POST /auth/register`

```json
{
  "email": "usuario@example.com",
  "password": "SenhaForte123"
}
```

O cadastro retorna os dados públicos do usuário, sem a senha ou seu hash.

### Fazer login

`POST /auth/login`

```json
{
  "email": "usuario@example.com",
  "password": "SenhaForte123"
}
```

A resposta contém um `access_token` e o tipo `bearer`.

### Autorizar requisições

Os endpoints `/tasks` exigem autenticação.

No Swagger UI:

1. Execute o cadastro em `POST /auth/register`.
2. Faça login em `POST /auth/login`.
3. Copie o `access_token`.
4. Clique em **Authorize**.
5. Informe o token conforme solicitado pela interface.
6. Execute os endpoints protegidos.

## Endpoints

| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/` | Verificar funcionamento da API |
| GET | `/health` | Verificar saúde da aplicação |
| POST | `/auth/register` | Cadastrar usuário |
| POST | `/auth/login` | Autenticar usuário |
| POST | `/tasks` | Criar tarefa |
| GET | `/tasks` | Listar tarefas do usuário |
| GET | `/tasks/{task_id}` | Consultar tarefa |
| PUT | `/tasks/{task_id}` | Atualizar tarefa |
| PATCH | `/tasks/{task_id}` | Atualizar parcialmente |
| DELETE | `/tasks/{task_id}` | Excluir tarefa |

## Exemplos de utilização

Os exemplos pressupõem que o usuário já esteja autenticado.

### Criar tarefa

`POST /tasks`

```json
{
  "title": "Estudar Python",
  "description": "Praticar desenvolvimento de APIs",
  "completed": false
}
```

### Listar tarefas com paginação

`GET /tasks?limit=5&offset=0`

- `limit`: quantidade máxima de resultados, de 1 a 100.
- `offset`: quantidade de registros ignorados.

### Filtrar por conclusão

```text
GET /tasks?completed=true
GET /tasks?completed=false
```

### Pesquisar por título

```text
GET /tasks?search=Python
```

Os filtros podem ser combinados:

```text
GET /tasks?completed=false&search=Python&limit=10&offset=0
```

### Consultar, atualizar e excluir

```text
GET /tasks/1
PUT /tasks/1
PATCH /tasks/1
DELETE /tasks/1
```

O usuário autenticado só pode acessar e modificar suas próprias tarefas.

## Testes automatizados

O projeto utiliza Pytest e HTTPX para validar o funcionamento da aplicação.

Para executar:

```powershell
python -m pytest -v
```

**Resultado da última execução: 31 testes aprovados.**

Os testes contemplam:

- Cadastro e autenticação de usuários.
- Validação de credenciais.
- Proteção das rotas.
- Isolamento entre usuários.
- Operações CRUD de tarefas.
- Atualizações completas e parciais.
- Validação de dados.
- Filtros, pesquisa e paginação.
- Tratamento de erros.

## Executando com Docker

### Pré-requisitos

- Docker Desktop instalado e em execução.
- Git instalado.

### Configuração

Crie um arquivo `.env` na raiz do projeto com uma chave JWT aleatória:

```powershell
$key = python -c "import secrets; print(secrets.token_urlsafe(48))"
"JWT_SECRET_KEY=$key" | Set-Content -Encoding ascii .env
```

Não compartilhe a chave secreta nem publique o arquivo `.env`.

### Iniciar a aplicação

```powershell
docker compose up --build -d
```

Verificar os contêineres:

```powershell
docker compose ps
```

A documentação estará disponível em:

http://localhost:8000/docs

### Comandos úteis

Visualizar logs:

```powershell
docker compose logs -f api
```

Reiniciar a API:

```powershell
docker compose restart api
```

Parar os contêineres:

```powershell
docker compose down
```

O banco de dados utiliza o volume persistente configurado no Docker Compose. O comando `docker compose down -v` também remove os volumes e pode apagar os dados armazenados.

## Segurança

- Senhas protegidas com Argon2.
- Autenticação baseada em JWT.
- Controle de acesso por usuário.
- Credenciais configuradas por variáveis de ambiente.
- Arquivos locais e informações sensíveis excluídos do versionamento.

## Autor

**Vinicio Sousa**

- GitHub: https://github.com/sousa2210
- Projeto: https://github.com/sousa2210/task-manager-api