import pytest
from fastapi.testclient import TestClient

import database
import main


@pytest.fixture
def client(tmp_path, monkeypatch):
    # Usa um banco temporário exclusivo para cada teste.
    test_database = tmp_path / "test_tasks.db"

    monkeypatch.setattr(database, "DATABASE_PATH", test_database)

    database.initialize_database()

    with TestClient(main.app) as test_client:
        yield test_client


def test_create_and_list_tasks(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Estudar Python",
            "description": "Aprender testes automatizados",
            "completed": False,
        },
    )

    assert response.status_code == 201
    assert response.json()["title"] == "Estudar Python"

    list_response = client.get("/tasks")

    assert list_response.status_code == 200
    assert len(list_response.json()) == 1



def test_reject_title_with_only_spaces(client):
    response = client.post(
        "/tasks",
        json={"title": "   "}
    )

    assert response.status_code == 422


def test_reject_empty_title(client):
    response = client.post(
        "/tasks",
        json={"title": ""}
    )

    assert response.status_code == 422


def test_update_task(client):
    create_response = client.post(
        "/tasks",
        json={"title": "Tarefa original"},
    )
    task_id = create_response.json()["id"]

    response = client.put(
        f"/tasks/{task_id}",
        json={
            "title": "Tarefa atualizada",
            "description": "Alterada pelo teste",
            "completed": True,
        },
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Tarefa atualizada"
    assert response.json()["completed"] is True


def test_delete_task(client):
    create_response = client.post(
        "/tasks",
        json={"title": "Tarefa para excluir"},
    )
    task_id = create_response.json()["id"]

    delete_response = client.delete(f"/tasks/{task_id}")

    assert delete_response.status_code == 204

    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404


def test_task_not_found(client):
    response = client.get("/tasks/9999")

    assert response.status_code == 404
