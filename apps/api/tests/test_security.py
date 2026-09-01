from datetime import timedelta
import uuid
from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient
import pytest

from apps.api.app.core.config import Settings
from apps.api.app.core.exceptions import AuthenticationError, AuthorizationError, setup_exception_handlers
from apps.api.app.core.security import (
    AuthenticatedUser,
    PermissionChecker,
    create_access_token,
    create_refresh_token,
    decode_token,
    get_authenticated_user_from_token,
    get_current_user,
    hash_password,
    require_organization,
    require_permission,
    require_project_member,
    require_role,
    verify_password,
)


def test_password_hashing_and_verification():
    """Verify plain password hashing and verification logic."""
    raw_password = "SecretPassword123!"
    hashed = hash_password(raw_password)

    assert hashed != raw_password
    assert verify_password(raw_password, hashed) is True
    assert verify_password("WrongPassword!", hashed) is False


def test_jwt_issue_and_decode_valid_token():
    """Verify access and refresh token creation and payload claim extraction."""
    user_id = uuid.uuid4()
    org_id = uuid.uuid4()

    token = create_access_token(
        subject=user_id,
        organization_id=org_id,
        roles=["admin", "member"],
        permissions=["read", "write"],
        is_superuser=False,
        mfa_verified=True,
    )

    auth_user = get_authenticated_user_from_token(token)
    assert auth_user.user_id == user_id
    assert auth_user.organization_id == org_id
    assert auth_user.roles == ["admin", "member"]
    assert auth_user.permissions == ["read", "write"]
    assert auth_user.is_superuser is False
    assert auth_user.mfa_verified is True
    assert auth_user.amr == ["pwd", "mfa"]

    # Refresh token check
    refresh_token = create_refresh_token(subject=user_id, organization_id=org_id)
    payload = decode_token(refresh_token, expected_type="refresh")
    assert payload["sub"] == str(user_id)
    assert payload["type"] == "refresh"


def test_expired_token_raises_typed_401():
    """Verify expired token raises typed AuthenticationError (401)."""
    user_id = uuid.uuid4()
    org_id = uuid.uuid4()

    token = create_access_token(
        subject=user_id,
        organization_id=org_id,
        expires_delta=timedelta(seconds=-10),  # expired 10 seconds ago
    )

    with pytest.raises(AuthenticationError) as exc_info:
        decode_token(token)

    assert exc_info.value.status_code == 401
    assert exc_info.value.code == "AUTHENTICATION_ERROR"
    assert "expired" in exc_info.value.message.lower()


def test_tampered_token_raises_typed_401():
    """Verify tampered JWT signature raises typed AuthenticationError (401)."""
    user_id = uuid.uuid4()
    org_id = uuid.uuid4()
    token = create_access_token(subject=user_id, organization_id=org_id)
    tampered_token = token[:-5] + "XXXXX"

    with pytest.raises(AuthenticationError) as exc_info:
        decode_token(tampered_token)

    assert exc_info.value.status_code == 401
    assert exc_info.value.code == "AUTHENTICATION_ERROR"


def test_wrong_token_type_raises_typed_401():
    """Verify passing refresh token to access token decoder raises typed AuthenticationError (401)."""
    refresh_token = create_refresh_token(subject=uuid.uuid4(), organization_id=uuid.uuid4())

    with pytest.raises(AuthenticationError) as exc_info:
        decode_token(refresh_token, expected_type="access")

    assert exc_info.value.status_code == 401
    assert "Expected 'access'" in exc_info.value.message


def test_rbac_organization_boundary_check():
    """Verify organization boundary enforcement logic."""
    org_a = uuid.uuid4()
    org_b = uuid.uuid4()
    user_id = uuid.uuid4()

    user = AuthenticatedUser(user_id=user_id, organization_id=org_a, roles=["member"])

    # Matching org -> allowed
    require_organization(user, org_a)

    # Mismatched org -> raises 403
    with pytest.raises(AuthorizationError) as exc_info:
        require_organization(user, org_b)

    assert exc_info.value.status_code == 403

    # Superuser -> allowed across all orgs
    superuser = AuthenticatedUser(user_id=user_id, organization_id=org_a, is_superuser=True)
    require_organization(superuser, org_b)


def test_rbac_role_and_permission_checks():
    """Verify role and permission checks."""
    user = AuthenticatedUser(
        user_id=uuid.uuid4(),
        organization_id=uuid.uuid4(),
        roles=["editor"],
        permissions=["edit_asset"],
    )

    # Role check
    require_role(user, "editor")
    require_role(user, ["admin", "editor"])

    with pytest.raises(AuthorizationError):
        require_role(user, "admin")

    # Permission check
    require_permission(user, "edit_asset")

    with pytest.raises(AuthorizationError):
        require_permission(user, "delete_asset")


def test_rbac_project_membership_check():
    """Verify project membership check."""
    user_id = uuid.uuid4()
    other_user_id = uuid.uuid4()
    user = AuthenticatedUser(user_id=user_id, organization_id=uuid.uuid4())

    # User is in member list
    require_project_member(user, [other_user_id, user_id])

    # User is not in member list
    with pytest.raises(AuthorizationError):
        require_project_member(user, [other_user_id])


def test_security_secret_validation_in_viva_prod_mode():
    """Verify viva/prod mode fails fast if JWT_SECRET_KEY is missing or set to default."""
    with pytest.raises(Exception):
        Settings(APP_MODE="viva", JWT_SECRET_KEY="dev_secret_key_change_in_production")

    with pytest.raises(Exception):
        Settings(APP_MODE="prod", JWT_SECRET_KEY=None)


def test_protected_fastapi_route_integration():
    """Integration test: FastAPI app endpoint protected with Bearer token & PermissionChecker."""
    app = FastAPI()
    setup_exception_handlers(app)

    @app.get("/api/v1/protected")
    def protected_route(
        user: AuthenticatedUser = Depends(PermissionChecker(required_roles=["admin"])),
    ):
        return {"status": "ok", "user_id": str(user.user_id)}

    client = TestClient(app)

    # 1. Missing Bearer token -> 401
    resp = client.get("/api/v1/protected")
    assert resp.status_code == 401
    assert resp.json()["error"]["code"] == "AUTHENTICATION_ERROR"

    # 2. Token without required 'admin' role -> 403
    user_id = uuid.uuid4()
    org_id = uuid.uuid4()
    member_token = create_access_token(user_id, org_id, roles=["member"])

    resp_forbidden = client.get(
        "/api/v1/protected",
        headers={"Authorization": f"Bearer {member_token}"},
    )
    assert resp_forbidden.status_code == 403
    assert resp_forbidden.json()["error"]["code"] == "AUTHORIZATION_ERROR"

    # 3. Valid token with 'admin' role -> 200
    admin_token = create_access_token(user_id, org_id, roles=["admin"])
    resp_success = client.get(
        "/api/v1/protected",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert resp_success.status_code == 200
    assert resp_success.json()["user_id"] == str(user_id)
