from datetime import datetime, timedelta, timezone
from typing import Any, List, Optional
import uuid
import bcrypt
import jwt
from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field

from apps.api.app.core.config import settings
from apps.api.app.core.exceptions import AuthenticationError, AuthorizationError

# HTTP Bearer scheme for token extraction
bearer_scheme = HTTPBearer(auto_error=False)


class AuthenticatedUser(BaseModel):
    """Data object representing authenticated user identity & claims."""
    user_id: uuid.UUID
    organization_id: uuid.UUID
    roles: List[str] = Field(default_factory=list)
    permissions: List[str] = Field(default_factory=list)
    is_superuser: bool = False
    mfa_verified: bool = False
    amr: List[str] = Field(default_factory=lambda: ["pwd"])


def hash_password(password: str) -> str:
    """Hash plain-text password using bcrypt."""
    pwd_bytes = password.encode("utf-8")[:72]
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify plain password against hashed password using bcrypt."""
    try:
        pwd_bytes = plain_password.encode("utf-8")[:72]
        hash_bytes = hashed_password.encode("utf-8")
        return bcrypt.checkpw(pwd_bytes, hash_bytes)
    except Exception:
        return False


def create_access_token(
    subject: str | uuid.UUID,
    organization_id: str | uuid.UUID,
    roles: Optional[List[str]] = None,
    permissions: Optional[List[str]] = None,
    is_superuser: bool = False,
    mfa_verified: bool = False,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Issue signed JWT access token."""
    now = datetime.now(timezone.utc)
    expire = now + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))

    payload = {
        "sub": str(subject),
        "org_id": str(organization_id),
        "roles": roles or [],
        "permissions": permissions or [],
        "is_superuser": is_superuser,
        "type": "access",
        "mfa_verified": mfa_verified,
        "amr": ["pwd", "mfa"] if mfa_verified else ["pwd"],
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
    }

    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def create_refresh_token(
    subject: str | uuid.UUID,
    organization_id: str | uuid.UUID,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Issue signed JWT refresh token."""
    now = datetime.now(timezone.utc)
    expire = now + (expires_delta or timedelta(days=7))

    payload = {
        "sub": str(subject),
        "org_id": str(organization_id),
        "type": "refresh",
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
    }

    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_token(token: str, expected_type: str = "access") -> dict[str, Any]:
    """Decode and validate a JWT token, raising typed AuthenticationError on any failure."""
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        if payload.get("type") != expected_type:
            raise AuthenticationError(f"Invalid token type. Expected '{expected_type}'.")
        return payload
    except jwt.ExpiredSignatureError:
        raise AuthenticationError("Token has expired.")
    except jwt.PyJWTError:
        raise AuthenticationError("Could not validate authentication credentials.")


def get_authenticated_user_from_token(token: str) -> AuthenticatedUser:
    """Parse JWT token payload into AuthenticatedUser model."""
    payload = decode_token(token, expected_type="access")
    try:
        return AuthenticatedUser(
            user_id=uuid.UUID(payload["sub"]),
            organization_id=uuid.UUID(payload["org_id"]),
            roles=payload.get("roles", []),
            permissions=payload.get("permissions", []),
            is_superuser=payload.get("is_superuser", False),
            mfa_verified=payload.get("mfa_verified", False),
            amr=payload.get("amr", ["pwd"]),
        )
    except (KeyError, ValueError) as exc:
        raise AuthenticationError("Malformed token payload claims.") from exc


# --- Authorization & RBAC Primitives ---

def require_organization(user: AuthenticatedUser, target_org_id: str | uuid.UUID) -> None:
    """Enforce organization boundary access."""
    if user.is_superuser:
        return
    if str(user.organization_id) != str(target_org_id):
        raise AuthorizationError("Access denied for requested organization.")


def require_role(user: AuthenticatedUser, required_roles: List[str] | str) -> None:
    """Enforce role-based access control (RBAC)."""
    if user.is_superuser:
        return
    allowed_roles = [required_roles] if isinstance(required_roles, str) else required_roles
    if not any(r in user.roles for r in allowed_roles):
        raise AuthorizationError(f"User lacks required role: {allowed_roles}.")


def require_permission(user: AuthenticatedUser, required_permission: str) -> None:
    """Enforce specific permission check."""
    if user.is_superuser:
        return
    if required_permission not in user.permissions:
        raise AuthorizationError(f"User lacks required permission: '{required_permission}'.")


def require_project_member(user: AuthenticatedUser, member_user_ids: List[str | uuid.UUID]) -> None:
    """Enforce project/resource membership check."""
    if user.is_superuser:
        return
    str_member_ids = [str(uid) for uid in member_user_ids]
    if str(user.user_id) not in str_member_ids:
        raise AuthorizationError("User is not a member of this resource.")


# --- FastAPI Route Dependencies ---

def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
) -> AuthenticatedUser:
    """FastAPI route dependency to extract and validate Bearer JWT token."""
    if not credentials or not credentials.credentials:
        raise AuthenticationError("Not authenticated. Bearer token missing.")
    return get_authenticated_user_from_token(credentials.credentials)


class PermissionChecker:
    """FastAPI dependency for verifying required roles and permissions."""

    def __init__(
        self,
        required_roles: Optional[List[str]] = None,
        required_permissions: Optional[List[str]] = None,
    ):
        self.required_roles = required_roles or []
        self.required_permissions = required_permissions or []

    def __call__(self, current_user: AuthenticatedUser = Depends(get_current_user)) -> AuthenticatedUser:
        if current_user.is_superuser:
            return current_user

        if self.required_roles:
            require_role(current_user, self.required_roles)

        for perm in self.required_permissions:
            require_permission(current_user, perm)

        return current_user
