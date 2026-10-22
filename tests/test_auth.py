import pytest
from fastapi.testclient import TestClient

import database
import main


@pytest.fixture
def client(tmp_path, monkeypatch):
    test_database = tmp_path / "test_auth.db"
    monkeypatch.setattr(database, "DATABASE_PATH", test_database)

    monkeypatch.setenv(
        "JWT_SECRET_KEY",
        "chave-segura-exclusiva-para-testes-automatizados",
    )

    database.initialize_database()

    with TestClient(main.app) as test_client:
        yield test_client


def test_register_user(client):
    response = client.post(
        "/auth/register",
        json={
            "email": "usuario@example.com",
            "password": "SenhaForte123",
        },
    )

    assert response.status_code == 201
    assert response.json()["email"] == "usuario@example.com"
    assert "id" in response.json()
    assert "created_at" in response.json()
    assert "password" not in response.json()
    assert "password_hash" not in response.json()


def test_reject_duplicate_email(client):
    payload = {
        "email": "usuario@example.com",
        "password": "SenhaForte123",
    }

    first_response = client.post("/auth/register", json=payload)

    second_response = client.post(
        "/auth/register",
        json={
            "email": " USUARIO@example.com ",
            "password": "OutraSenha123",
        },
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 409


def test_login_returns_bearer_token(client):
    client.post(
        "/auth/register",
        json={
            "email": "usuario@example.com",
            "password": "SenhaForte123",
        },
    )

    response = client.post(
        "/auth/login",
        json={
            "email": "usuario@example.com",
            "password": "SenhaForte123",
        },
    )

    assert response.status_code == 200
    assert isinstance(response.json()["access_token"], str)
    assert response.json()["access_token"]
    assert response.json()["token_type"] == "bearer"


def test_login_rejects_wrong_password(client):
    client.post(
        "/auth/register",
        json={
            "email": "usuario@example.com",
            "password": "SenhaForte123",
        },
    )

    response = client.post(
        "/auth/login",
        json={
            "email": "usuario@example.com",
            "password": "SenhaErrada123",
        },
    )

    assert response.status_code == 401


def test_login_rejects_unknown_email(client):
    response = client.post(
        "/auth/login",
        json={
            "email": "inexistente@example.com",
            "password": "SenhaForte123",
        },
    )

    assert response.status_code == 401
