import logging
from typing import List, Optional
import uuid
from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session

from apps.api.app.core.config import settings
from apps.api.app.core.database import get_db
from apps.api.app.core.exceptions import AuthenticationError
from apps.api.app.core.security import (
    AuthenticatedUser,
    create_access_token,
    create_refresh_token,
    decode_token,
    get_current_user,
    hash_password,
    verify_password,
)
from apps.api.app.repositories.models.user import User

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    """Schema for login credentials request."""
    email: str = Field(..., json_schema_extra={"example": "admin@example.com"})
    password: str = Field(..., json_schema_extra={"example": "password123"})
    organization_id: Optional[uuid.UUID] = Field(None, description="Optional target organization ID")


class TokenResponse(BaseModel):
    """Schema for JWT token response."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = Field(description="Access token validity in seconds")


class RefreshTokenRequest(BaseModel):
    """Schema for refreshing access token."""
    refresh_token: str = Field(..., description="Valid JWT refresh token")


class LogoutResponse(BaseModel):
    """Schema for logout response."""
    status: str = "ok"
    message: str = "Successfully logged out."


# Dev mode fallback credentials
DEV_DEMO_USERS = {
    "admin@example.com": {
        "user_id": uuid.UUID("00000000-0000-0000-0000-000000000001"),
        "organization_id": uuid.UUID("00000000-0000-0000-0000-000000000010"),
        "password_hash": hash_password("adminpassword"),
        "roles": ["admin"],
        "permissions": ["read", "write", "admin"],
        "is_superuser": True,
    },
    "dev@example.com": {
        "user_id": uuid.UUID("00000000-0000-0000-0000-000000000002"),
        "organization_id": uuid.UUID("00000000-0000-0000-0000-000000000010"),
        "password_hash": hash_password("password"),
        "roles": ["member"],
        "permissions": ["read"],
        "is_superuser": False,
    },
}


@router.post("/login", response_model=TokenResponse)
def login(
    body: LoginRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    """Authenticate user credentials and return access + refresh tokens."""
    user = None
    try:
        user = db.query(User).filter(User.email == body.email).first()
    except Exception as exc:
        logger.debug("Database query skipped or unavailable during auth attempt: %s", exc)

    if user:
        if not user.is_active:
            logger.warning("Failed login attempt for disabled user: email=%s client=%s", body.email, request.client.host if request.client else "unknown")
            raise AuthenticationError("Account is disabled.")

        roles = [ur.role.name for ur in user.user_roles] if user.user_roles else ["member"]
        user_id = user.id
        org_id = user.organization_id
        is_superuser = user.is_superuser
        permissions = ["read", "write"]
    elif settings.APP_MODE == "dev" and body.email in DEV_DEMO_USERS:
        dev_user = DEV_DEMO_USERS[body.email]
        if not verify_password(body.password, dev_user["password_hash"]):
            logger.warning("Failed login attempt (invalid dev password): email=%s", body.email)
            raise AuthenticationError("Invalid credentials.")
        user_id = dev_user["user_id"]
        org_id = body.organization_id or dev_user["organization_id"]
        roles = dev_user["roles"]
        permissions = dev_user["permissions"]
        is_superuser = dev_user["is_superuser"]
    else:
        logger.warning("Failed login attempt (user not found): email=%s", body.email)
        raise AuthenticationError("Invalid credentials.")

    access_token = create_access_token(
        subject=user_id,
        organization_id=org_id,
        roles=roles,
        permissions=permissions,
        is_superuser=is_superuser,
    )
    refresh_token = create_refresh_token(
        subject=user_id,
        organization_id=org_id,
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(body: RefreshTokenRequest):
    """Re-issue access token using a valid refresh token."""
    payload = decode_token(body.refresh_token, expected_type="refresh")

    user_id = payload["sub"]
    org_id = payload["org_id"]

    new_access_token = create_access_token(
        subject=user_id,
        organization_id=org_id,
        roles=["member"],
    )
    new_refresh_token = create_refresh_token(
        subject=user_id,
        organization_id=org_id,
    )

    return TokenResponse(
        access_token=new_access_token,
        refresh_token=new_refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


@router.post("/logout", response_model=LogoutResponse)
def logout(current_user: AuthenticatedUser = Depends(get_current_user)):
    """Logout current user session. Refresh tokens are stateless by design."""
    logger.info("User logged out: user_id=%s org_id=%s", current_user.user_id, current_user.organization_id)
    return LogoutResponse(status="ok", message="Successfully logged out.")
