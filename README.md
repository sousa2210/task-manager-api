# Task Manager API

API REST para gerenciamento de tarefas, desenvolvida com Python e FastAPI. O projeto utiliza SQLite, autenticação JWT, hash de senhas com Argon2 e testes automatizados com Pytest.

O objetivo é demonstrar conhecimentos práticos em desenvolvimento backend, APIs REST, autenticação, autorização, SQL, validação de dados e testes automatizados.

## Tecnologias

- Python 3.13
- FastAPI
- SQLite
- Pydantic
- JWT com PyJWT
- Argon2 com pwdlib
- Pytest e HTTPX
- Git e GitHub

## Funcionalidades

### Autenticação e segurança
- Cadastro de usuários.
- Login com e-mail e senha.
- Senhas armazenadas com hash Argon2.
- Tokens de acesso JWT com validade de 30 minutos.
- Proteção dos endpoints de tarefas.
- Isolamento das tarefas por usuário.

### Gerenciamento de tarefas
- Criar, listar, consultar, atualizar e excluir tarefas.
- Atualização completa com PUT e parcial com PATCH.
- Filtro por status de conclusão.
- Pesquisa por título.
- Paginação com limit e offset.
- Validação de dados e tratamento de erros.

## Requisitos

- Python 3.13 ou compatível.
- Git.

## Como executar

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

A aplicação precisa da variável de ambiente `JWT_SECRET_KEY` para assinar e validar tokens.

No PowerShell, gere uma chave aleatória e configure-a na sessão atual:

```powershell
$env:JWT_SECRET_KEY = python -c "import secrets; print(secrets.token_urlsafe(48))"
```

Não compartilhe essa chave nem a publique no GitHub. Se reiniciar o terminal, configure a variável novamente. Em produção, use um gerenciador de segredos ou uma configuração segura equivalente.

### 5. Iniciar a API

```powershell
python -m uvicorn main:app --reload
```

A API estará disponível em:

- API: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

O banco SQLite é inicializado automaticamente quando a aplicação inicia.

## Autenticação

### Cadastrar usuário

`POST /auth/register`

Exemplo de corpo JSON:

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
2. Execute o login em `POST /auth/login` e copie o `access_token`.
3. Clique em **Authorize**.
4. Informe o token conforme solicitado pela interface e confirme.
5. Execute os endpoints de tarefas.

Não é necessário incluir o prefixo `Bearer ` manualmente se a interface solicitar apenas o token; siga o formato exibido pelo Swagger.

## Endpoints

| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/` | Verificar se a API está funcionando |
| GET | `/health` | Verificar a saúde da aplicação |
| POST | `/auth/register` | Cadastrar usuário |
| POST | `/auth/login` | Fazer login e obter token |
| POST | `/tasks` | Criar tarefa autenticada |
| GET | `/tasks` | Listar e filtrar tarefas do usuário |
| GET | `/tasks/{task_id}` | Consultar tarefa do usuário |
| PUT | `/tasks/{task_id}` | Atualizar tarefa do usuário |
| PATCH | `/tasks/{task_id}` | Atualizar parcialmente |
| DELETE | `/tasks/{task_id}` | Excluir tarefa do usuário |

## Exemplos de tarefas

Os exemplos a seguir pressupõem que você já fez login e autorizou a requisição com o token JWT.

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

- `GET /tasks?completed=true`
- `GET /tasks?completed=false`

### Pesquisar por título

`GET /tasks?search=Python`

É possível combinar os filtros:

`GET /tasks?completed=false&search=Python&limit=10&offset=0`

### Consultar, atualizar e excluir

- `GET /tasks/1`
- `PUT /tasks/1`
- `PATCH /tasks/1`
- `DELETE /tasks/1`

Substitua `1` pelo ID da tarefa. O usuário autenticado só pode acessar as próprias tarefas.

## Testes automatizados

Com o ambiente virtual ativado, execute:

```powershell
python -m pytest -v
```

Na última execução registrada, os **31 testes passaram**, cobrindo autenticação, operações CRUD, validações, filtros, paginação e isolamento entre usuários.

## Segurança e dados locais

- Configure `JWT_SECRET_KEY` por variável de ambiente.
- Não publique chaves secretas, arquivos `.env`, bancos de dados ou backups locais.
- Os arquivos locais do SQLite são excluídos do versionamento pelo `.gitignore`.
- Para produção, avalie também HTTPS, limitação de tentativas de login, política de renovação de tokens, migrações de banco e gestão segura de segredos.

## Autor

**Vinicio Sousa**

- GitHub: https://github.com/sousa2210
- Repositório: https://github.com/sousa2210/task-manager-api
