from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from apps.api.app.core.exceptions import (
    AppError,
    ConflictError,
    NotFoundError,
    ValidationError,
)
from apps.api.app.repositories.models.asset import Asset
from apps.api.app.repositories.models.project import Project
from apps.api.app.repositories.models.user import User


class AssetRepository:
    """Data-access layer for asset metadata.

    Note on storage boundary:
    This repository manages asset metadata rows only. Actual file binary contents,
    file uploads, and object-storage interactions (MinIO/S3) are handled by separate
    storage services and are intentionally out of scope for this repository.

    Every query is explicitly scoped by organization_id to enforce multi-tenant isolation
    at the repository boundary (docs/DATABASE.md §3, REQ-S001).
    """

    _UNSET = object()

    def __init__(self, db: Session) -> None:
        self.db = db

    def create_asset(
        self,
        organization_id: uuid.UUID,
        name: str,
        asset_type: str,
        project_id: Optional[uuid.UUID] = None,
        owner_id: Optional[uuid.UUID] = None,
        asset_metadata: Optional[Dict[str, Any]] = None,
    ) -> Asset:
        """Create a new asset metadata record scoped to an organization."""
        clean_name = name.strip() if name else ""
        if not clean_name:
            raise ValidationError("Asset name cannot be empty.")

        clean_type = asset_type.strip() if asset_type else ""
        if not clean_type:
            raise ValidationError("Asset type cannot be empty.")

        if project_id is not None:
            project = (
                self.db.execute(
                    select(Project).where(
                        Project.id == project_id,
                        Project.organization_id == organization_id,
                    )
                )
                .scalars()
                .first()
            )
            if not project:
                raise NotFoundError(f"Project '{project_id}' not found.")

        if owner_id is not None:
            owner = (
                self.db.execute(
                    select(User).where(
                        User.id == owner_id,
                        User.organization_id == organization_id,
                    )
                )
                .scalars()
                .first()
            )
            if not owner:
                raise NotFoundError(f"Owner user '{owner_id}' not found.")

        asset = Asset(
            organization_id=organization_id,
            project_id=project_id,
            name=clean_name,
            asset_type=clean_type,
            owner_id=owner_id,
            asset_metadata=asset_metadata,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )

        try:
            self.db.add(asset)
            self.db.commit()
            self.db.refresh(asset)
            return asset
        except IntegrityError as exc:
            self.db.rollback()
            raise ConflictError("Failed to create asset due to a database constraint violation.") from exc
        except SQLAlchemyError as exc:
            self.db.rollback()
            raise AppError("Failed to create asset due to an internal database error.") from exc

    def get_asset_by_id(self, organization_id: uuid.UUID, asset_id: uuid.UUID) -> Asset:
        """Retrieve an asset by ID, scoped to the caller's organization.

        Raises NotFoundError if the asset does not exist OR if it belongs to another
        organization, ensuring cross-org existence information is never leaked.
        """
        try:
            asset = (
                self.db.execute(
                    select(Asset).where(
                        Asset.id == asset_id,
                        Asset.organization_id == organization_id,
                    )
                )
                .scalars()
                .first()
            )
        except SQLAlchemyError as exc:
            raise AppError("Database error occurred while retrieving asset.") from exc

        if not asset:
            raise NotFoundError(f"Asset '{asset_id}' not found.")
        return asset

    def list_assets(
        self,
        organization_id: uuid.UUID,
        project_id: Optional[uuid.UUID] = None,
        owner_id: Optional[uuid.UUID] = None,
        asset_type: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Asset]:
        """List assets belonging to an organization, with optional filtering and pagination."""
        if skip < 0:
            raise ValidationError("skip must be non-negative.")
        if limit <= 0 or limit > 1000:
            raise ValidationError("limit must be between 1 and 1000.")

        query = select(Asset).where(Asset.organization_id == organization_id)

        if project_id is not None:
            query = query.where(Asset.project_id == project_id)
        if owner_id is not None:
            query = query.where(Asset.owner_id == owner_id)
        if asset_type is not None:
            query = query.where(Asset.asset_type == asset_type.strip())

        query = query.order_by(Asset.created_at.desc()).offset(skip).limit(limit)

        try:
            return list(self.db.execute(query).scalars().all())
        except SQLAlchemyError as exc:
            raise AppError("Database error occurred while listing assets.") from exc

    def update_asset(
        self,
        organization_id: uuid.UUID,
        asset_id: uuid.UUID,
        name: Optional[str] = None,
        asset_type: Optional[str] = None,
        project_id: Any = _UNSET,
        owner_id: Any = _UNSET,
        asset_metadata: Optional[Dict[str, Any]] = None,
    ) -> Asset:
        """Update an asset's metadata, scoped to caller's organization."""
        asset = self.get_asset_by_id(organization_id, asset_id)

        if name is not None:
            clean_name = name.strip()
            if not clean_name:
                raise ValidationError("Asset name cannot be empty.")
            asset.name = clean_name

        if asset_type is not None:
            clean_type = asset_type.strip()
            if not clean_type:
                raise ValidationError("Asset type cannot be empty.")
            asset.asset_type = clean_type

        if project_id is not self._UNSET:
            if project_id is not None:
                project = (
                    self.db.execute(
                        select(Project).where(
                            Project.id == project_id,
                            Project.organization_id == organization_id,
                        )
                    )
                    .scalars()
                    .first()
                )
                if not project:
                    raise NotFoundError(f"Project '{project_id}' not found.")
            asset.project_id = project_id

        if owner_id is not self._UNSET:
            if owner_id is not None:
                owner = (
                    self.db.execute(
                        select(User).where(
                            User.id == owner_id,
                            User.organization_id == organization_id,
                        )
                    )
                    .scalars()
                    .first()
                )
                if not owner:
                    raise NotFoundError(f"Owner user '{owner_id}' not found.")
            asset.owner_id = owner_id

        if asset_metadata is not None:
            asset.asset_metadata = asset_metadata

        asset.updated_at = datetime.now(timezone.utc)

        try:
            self.db.commit()
            self.db.refresh(asset)
            return asset
        except IntegrityError as exc:
            self.db.rollback()
            raise ConflictError("Failed to update asset due to a database constraint violation.") from exc
        except SQLAlchemyError as exc:
            self.db.rollback()
            raise AppError("Failed to update asset due to an internal database error.") from exc

    def delete_asset(self, organization_id: uuid.UUID, asset_id: uuid.UUID) -> None:
        """Permanently delete an asset record, scoped to organization."""
        asset = self.get_asset_by_id(organization_id, asset_id)

        try:
            self.db.delete(asset)
            self.db.commit()
        except SQLAlchemyError as exc:
            self.db.rollback()
            raise AppError("Failed to delete asset.") from exc
