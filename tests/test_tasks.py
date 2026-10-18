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

    assert set(response.json().keys()) == {
        "id",
        "title",
        "description",
        "completed",
    }
    assert isinstance(response.json()["id"], int)
    assert response.json()["completed"] is False

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
        json={"title": ""},
    )

    assert response.status_code == 422



def test_title_is_trimmed(client):
    response = client.post(
        "/tasks",
        json={"title": "  Estudar Python  "},
    )

    assert response.status_code == 201
    assert response.json()["title"] == "Estudar Python"


def test_reject_title_over_100_characters(client):
    response = client.post(
        "/tasks",
        json={"title": "A" * 101},
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


def test_patch_updates_only_title(client):
    create_response = client.post(
        "/tasks",
        json={
            "title": "Tarefa original",
            "description": "Descrição que deve ser preservada",
            "completed": False,
        },
    )
    task_id = create_response.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={"title": "Novo título"},
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Novo título"
    assert response.json()["description"] == "Descrição que deve ser preservada"
    assert response.json()["completed"] is False


def test_patch_can_set_completed_to_false(client):
    create_response = client.post(
        "/tasks",
        json={
            "title": "Tarefa concluída",
            "completed": True,
        },
    )
    task_id = create_response.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={"completed": False},
    )

    assert response.status_code == 200
    assert response.json()["completed"] is False


def test_patch_task_not_found(client):
    response = client.patch(
        "/tasks/9999",
        json={"title": "Novo título"},
    )

    assert response.status_code == 404


def test_patch_rejects_empty_update(client):
    create_response = client.post(
        "/tasks",
        json={"title": "Tarefa original"},
    )
    task_id = create_response.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={},
    )

    assert response.status_code == 400


def test_patch_rejects_title_with_only_spaces(client):
    create_response = client.post(
        "/tasks",
        json={"title": "Título original"},
    )
    task_id = create_response.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={"title": "   "},
    )

    assert response.status_code == 422


def test_patch_rejects_unknown_field(client):
    create_response = client.post(
        "/tasks",
        json={"title": "Tarefa original"},
    )
    task_id = create_response.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={"priority": "high"},
    )

    assert response.status_code == 422
