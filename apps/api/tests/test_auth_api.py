from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from apps.api.app.core.database import get_db
from apps.api.app.main import app
from apps.api.app.repositories.models import Base

# Setup in-memory SQLite database for API testing
test_engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
Base.metadata.create_all(bind=test_engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_login_success():
    """Verify valid credentials login returns 200 with access and refresh tokens."""
    payload = {
        "email": "admin@example.com",
        "password": "adminpassword",
    }
    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"
    assert data["expires_in"] > 0


def test_login_invalid_credentials():
    """Verify invalid password returns structured 401 AuthenticationError."""
    payload = {
        "email": "admin@example.com",
        "password": "wrongpassword!",
    }
    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 401
    data = response.json()
    assert data["error"]["code"] == "AUTHENTICATION_ERROR"
    assert "Invalid credentials" in data["error"]["message"]


def test_login_unknown_user():
    """Verify non-existent user returns structured 401 AuthenticationError."""
    payload = {
        "email": "nonexistent@example.com",
        "password": "somepassword",
    }
    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 401
    data = response.json()
    assert data["error"]["code"] == "AUTHENTICATION_ERROR"


def test_refresh_token_success():
    """Verify valid refresh token issues a new access token pair."""
    # 1. Login to get refresh token
    login_resp = client.post("/api/v1/auth/login", json={
        "email": "dev@example.com",
        "password": "password",
    })
    refresh_token = login_resp.json()["refresh_token"]

    # 2. Call refresh endpoint
    refresh_resp = client.post("/api/v1/auth/refresh", json={"refresh_token": refresh_token})
    assert refresh_resp.status_code == 200
    refreshed_data = refresh_resp.json()
    assert "access_token" in refreshed_data
    assert "refresh_token" in refreshed_data


def test_refresh_token_invalid_or_expired():
    """Verify invalid or tampered refresh token returns 401."""
    response = client.post("/api/v1/auth/refresh", json={"refresh_token": "invalid.jwt.token"})
    assert response.status_code == 401
    data = response.json()
    assert data["error"]["code"] == "AUTHENTICATION_ERROR"


def test_logout_endpoint():
    """Verify logout endpoint invalidates client session state."""
    # Login
    login_resp = client.post("/api/v1/auth/login", json={
        "email": "dev@example.com",
        "password": "password",
    })
    token = login_resp.json()["access_token"]

    # Call logout
    logout_resp = client.post(
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert logout_resp.status_code == 200
    assert logout_resp.json()["status"] == "ok"


def test_full_auth_e2e_path():
    """E2E flow test: login -> use access token -> refresh token -> logout."""
    # Step 1: Login
    login_resp = client.post("/api/v1/auth/login", json={
        "email": "admin@example.com",
        "password": "adminpassword",
    })
    assert login_resp.status_code == 200
    tokens = login_resp.json()
    access_token = tokens["access_token"]
    refresh_token = tokens["refresh_token"]

    # Step 2: Use token on logout (protected route)
    protected_resp = client.post(
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert protected_resp.status_code == 200

    # Step 3: Test access denied without token
    no_token_resp = client.post("/api/v1/auth/logout")
    assert no_token_resp.status_code == 401

    # Step 4: Refresh token
    refresh_resp = client.post("/api/v1/auth/refresh", json={"refresh_token": refresh_token})
    assert refresh_resp.status_code == 200
    new_access_token = refresh_resp.json()["access_token"]

    # Step 5: Use new access token
    protected_resp_2 = client.post(
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {new_access_token}"},
    )
    assert protected_resp_2.status_code == 200
