
import pytest
from fastapi.testclient import TestClient

import database
import main


@pytest.fixture
def client(tmp_path, monkeypatch):
    test_database = tmp_path / "test_ownership.db"
    monkeypatch.setattr(database, "DATABASE_PATH", test_database)

    monkeypatch.setenv(
        "JWT_SECRET_KEY",
        "chave-segura-exclusiva-para-testes-automatizados",
    )

    database.initialize_database()

    with TestClient(main.app) as test_client:
        yield test_client


def criar_usuario_e_obter_token(client, email):
    response = client.post(
        "/auth/register",
        json={
            "email": email,
            "password": "SenhaForte123",
        },
    )
    assert response.status_code == 201

    response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": "SenhaForte123",
        },
    )
    assert response.status_code == 200

    return response.json()["access_token"]


def test_tasks_requires_authentication(client):
    response = client.get("/tasks")

    assert response.status_code == 401


def test_user_cannot_access_another_users_task(client):
    # Cria dois usuários independentes.
    token_a = criar_usuario_e_obter_token(
        client, "usuario_a@example.com"
    )
    token_b = criar_usuario_e_obter_token(
        client, "usuario_b@example.com"
    )

    # O usuário A cria uma tarefa.
    client.headers.update(
        {"Authorization": f"Bearer {token_a}"}
    )

    creation = client.post(
        "/tasks",
        json={
            "title": "Tarefa privada do usuário A",
            "description": "Não deve ser acessível pelo usuário B",
            "completed": False,
        },
    )

    assert creation.status_code == 201
    task_id = creation.json()["id"]

    # O usuário B tenta acessar a tarefa do usuário A.
    client.headers.update(
        {"Authorization": f"Bearer {token_b}"}
    )

    listing = client.get("/tasks")
    assert listing.status_code == 200
    assert listing.json() == []

    detail = client.get(f"/tasks/{task_id}")
    assert detail.status_code == 404

    update = client.put(
        f"/tasks/{task_id}",
        json={
            "title": "Tentativa de alteração",
            "description": "Não deve funcionar",
            "completed": True,
        },
    )
    assert update.status_code == 404

    partial_update = client.patch(
        f"/tasks/{task_id}",
        json={"title": "Tentativa de alteração"},
    )
    assert partial_update.status_code == 404

    deletion = client.delete(f"/tasks/{task_id}")
    assert deletion.status_code == 404

    # Confirma que a tarefa continua acessível pelo dono.
    client.headers.update(
        {"Authorization": f"Bearer {token_a}"}
    )

    original_task = client.get(f"/tasks/{task_id}")
    assert original_task.status_code == 200
    assert original_task.json()["title"] == (
        "Tarefa privada do usuário A"
    )
