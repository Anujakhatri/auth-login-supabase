import os

os.environ.setdefault("SUPABASE_URL", "https://test-project.supabase.co")
os.environ.setdefault("SUPABASE_KEY", "test-anon-key")

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_public_info() -> None:
    response = client.get("/public/info")
    assert response.status_code == 200


def test_protected_route_requires_bearer_token() -> None:
    response = client.get("/protected/profile")
    assert response.status_code == 401
    assert response.json()["detail"] == "A valid Bearer token is required."


def test_openapi_contains_auth_routes() -> None:
    paths = app.openapi()["paths"]
    assert "/auth/signup" in paths
    assert "/auth/login" in paths
    assert "/auth/logout" in paths
