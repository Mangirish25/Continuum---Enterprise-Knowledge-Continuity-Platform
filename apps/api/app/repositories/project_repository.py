from datetime import datetime, timezone
from typing import List, Optional
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
from apps.api.app.repositories.models.project import Project, ProjectDependency, ProjectMember
from apps.api.app.repositories.models.user import User


class ProjectRepository:
    """Data-access layer for projects, members, and dependencies.

    Every query is explicitly scoped by organization_id to enforce multi-tenant isolation
    at the repository boundary (docs/DATABASE.md §3, REQ-S001).
    """

    def __init__(self, db: Session) -> None:
        self.db = db

    # -------------------------------------------------------------------------
    # Project CRUD
    # -------------------------------------------------------------------------

    def create_project(
        self,
        organization_id: uuid.UUID,
        name: str,
        key: str,
        description: Optional[str] = None,
        owner_id: Optional[uuid.UUID] = None,
        status: str = "active",
    ) -> Project:
        """Create a new project scoped to the given organization."""
        if not name or not name.strip():
            raise ValidationError("Project name cannot be empty.")
        if not key or not key.strip():
            raise ValidationError("Project key cannot be empty.")

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

        existing = (
            self.db.execute(
                select(Project).where(
                    Project.organization_id == organization_id,
                    Project.key == key,
                )
            )
            .scalars()
            .first()
        )
        if existing:
            raise ConflictError(f"Project with key '{key}' already exists in this organization.")

        project = Project(
            organization_id=organization_id,
            name=name.strip(),
            key=key.strip(),
            description=description,
            owner_id=owner_id,
            status=status,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )

        try:
            self.db.add(project)
            self.db.commit()
            self.db.refresh(project)
            return project
        except IntegrityError as exc:
            self.db.rollback()
            raise ConflictError("Failed to create project due to a database constraint violation.") from exc
        except SQLAlchemyError as exc:
            self.db.rollback()
            raise AppError("Failed to create project due to an internal database error.") from exc

    def get_project_by_id(self, organization_id: uuid.UUID, project_id: uuid.UUID) -> Project:
        """Get a project by ID, scoped to the caller's organization.

        Raises NotFoundError if the project doesn't exist OR if it belongs to another
        organization, ensuring cross-org existence information is never leaked.
        """
        try:
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
        except SQLAlchemyError as exc:
            raise AppError("Database error occurred while retrieving project.") from exc

        if not project:
            raise NotFoundError(f"Project '{project_id}' not found.")
        return project

    def get_project_by_key(self, organization_id: uuid.UUID, key: str) -> Optional[Project]:
        """Get a project by key within an organization, or None if not found."""
        try:
            return (
                self.db.execute(
                    select(Project).where(
                        Project.key == key,
                        Project.organization_id == organization_id,
                    )
                )
                .scalars()
                .first()
            )
        except SQLAlchemyError as exc:
            raise AppError("Database error occurred while retrieving project by key.") from exc

    def list_projects(
        self,
        organization_id: uuid.UUID,
        status: Optional[str] = None,
        owner_id: Optional[uuid.UUID] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Project]:
        """List projects belonging to an organization, with optional filtering and pagination."""
        if skip < 0:
            raise ValidationError("skip must be non-negative.")
        if limit <= 0 or limit > 1000:
            raise ValidationError("limit must be between 1 and 1000.")

        query = select(Project).where(Project.organization_id == organization_id)
        if status is not None:
            query = query.where(Project.status == status)
        if owner_id is not None:
            query = query.where(Project.owner_id == owner_id)

        query = query.order_by(Project.created_at.desc()).offset(skip).limit(limit)

        try:
            return list(self.db.execute(query).scalars().all())
        except SQLAlchemyError as exc:
            raise AppError("Database error occurred while listing projects.") from exc

    def update_project(
        self,
        organization_id: uuid.UUID,
        project_id: uuid.UUID,
        name: Optional[str] = None,
        key: Optional[str] = None,
        description: Optional[str] = None,
        owner_id: Optional[uuid.UUID] = None,
        status: Optional[str] = None,
    ) -> Project:
        """Update a project's metadata, scoped to the caller's organization."""
        project = self.get_project_by_id(organization_id, project_id)

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
            project.owner_id = owner_id

        if key is not None and key.strip() != project.key:
            clean_key = key.strip()
            if not clean_key:
                raise ValidationError("Project key cannot be empty.")
            existing = (
                self.db.execute(
                    select(Project).where(
                        Project.organization_id == organization_id,
                        Project.key == clean_key,
                        Project.id != project_id,
                    )
                )
                .scalars()
                .first()
            )
            if existing:
                raise ConflictError(f"Project with key '{clean_key}' already exists in this organization.")
            project.key = clean_key

        if name is not None:
            clean_name = name.strip()
            if not clean_name:
                raise ValidationError("Project name cannot be empty.")
            project.name = clean_name
        if description is not None:
            project.description = description
        if status is not None:
            project.status = status

        project.updated_at = datetime.now(timezone.utc)

        try:
            self.db.commit()
            self.db.refresh(project)
            return project
        except IntegrityError as exc:
            self.db.rollback()
            raise ConflictError("Failed to update project due to a database constraint violation.") from exc
        except SQLAlchemyError as exc:
            self.db.rollback()
            raise AppError("Failed to update project due to an internal database error.") from exc

    def soft_delete_project(
        self,
        organization_id: uuid.UUID,
        project_id: uuid.UUID,
        status: str = "archived",
    ) -> Project:
        """Soft delete a project by marking its status as archived or deleted."""
        project = self.get_project_by_id(organization_id, project_id)
        project.status = status
        project.updated_at = datetime.now(timezone.utc)

        try:
            self.db.commit()
            self.db.refresh(project)
            return project
        except SQLAlchemyError as exc:
            self.db.rollback()
            raise AppError("Failed to soft-delete project.") from exc

    def hard_delete_project(self, organization_id: uuid.UUID, project_id: uuid.UUID) -> None:
        """Permanently delete a project and its cascades, scoped to organization."""
        project = self.get_project_by_id(organization_id, project_id)

        try:
            self.db.delete(project)
            self.db.commit()
        except SQLAlchemyError as exc:
            self.db.rollback()
            raise AppError("Failed to hard-delete project.") from exc

    # -------------------------------------------------------------------------
    # Membership operations against project_members
    # -------------------------------------------------------------------------

    def add_member(
        self,
        organization_id: uuid.UUID,
        project_id: uuid.UUID,
        user_id: uuid.UUID,
        role: str = "member",
    ) -> ProjectMember:
        """Add a member to a project within the same organization."""
        self.get_project_by_id(organization_id, project_id)

        user = (
            self.db.execute(
                select(User).where(
                    User.id == user_id,
                    User.organization_id == organization_id,
                )
            )
            .scalars()
            .first()
        )
        if not user:
            raise NotFoundError(f"User '{user_id}' not found.")

        existing = (
            self.db.execute(
                select(ProjectMember).where(
                    ProjectMember.organization_id == organization_id,
                    ProjectMember.project_id == project_id,
                    ProjectMember.user_id == user_id,
                )
            )
            .scalars()
            .first()
        )
        if existing:
            raise ConflictError(f"User '{user_id}' is already a member of project '{project_id}'.")

        member = ProjectMember(
            organization_id=organization_id,
            project_id=project_id,
            user_id=user_id,
            role=role,
            joined_at=datetime.now(timezone.utc),
        )

        try:
            self.db.add(member)
            self.db.commit()
            self.db.refresh(member)
            return member
        except IntegrityError as exc:
            self.db.rollback()
            raise ConflictError("Failed to add project member due to constraint violation.") from exc
        except SQLAlchemyError as exc:
            self.db.rollback()
            raise AppError("Failed to add project member.") from exc

    def get_member(
        self,
        organization_id: uuid.UUID,
        project_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> ProjectMember:
        """Retrieve a project member record."""
        self.get_project_by_id(organization_id, project_id)

        member = (
            self.db.execute(
                select(ProjectMember).where(
                    ProjectMember.organization_id == organization_id,
                    ProjectMember.project_id == project_id,
                    ProjectMember.user_id == user_id,
                )
            )
            .scalars()
            .first()
        )
        if not member:
            raise NotFoundError(f"User '{user_id}' is not a member of project '{project_id}'.")
        return member

    def list_members(
        self,
        organization_id: uuid.UUID,
        project_id: uuid.UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> List[ProjectMember]:
        """List all members of a project."""
        self.get_project_by_id(organization_id, project_id)

        if skip < 0:
            raise ValidationError("skip must be non-negative.")
        if limit <= 0 or limit > 1000:
            raise ValidationError("limit must be between 1 and 1000.")

        query = (
            select(ProjectMember)
            .where(
                ProjectMember.organization_id == organization_id,
                ProjectMember.project_id == project_id,
            )
            .order_by(ProjectMember.joined_at.asc())
            .offset(skip)
            .limit(limit)
        )

        try:
            return list(self.db.execute(query).scalars().all())
        except SQLAlchemyError as exc:
            raise AppError("Database error occurred while listing project members.") from exc

    def update_member_role(
        self,
        organization_id: uuid.UUID,
        project_id: uuid.UUID,
        user_id: uuid.UUID,
        role: str,
    ) -> ProjectMember:
        """Update the role of a project member."""
        if not role or not role.strip():
            raise ValidationError("Role cannot be empty.")

        member = self.get_member(organization_id, project_id, user_id)
        member.role = role.strip()

        try:
            self.db.commit()
            self.db.refresh(member)
            return member
        except SQLAlchemyError as exc:
            self.db.rollback()
            raise AppError("Failed to update project member role.") from exc

    def remove_member(
        self,
        organization_id: uuid.UUID,
        project_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> None:
        """Remove a member from a project."""
        member = self.get_member(organization_id, project_id, user_id)

        try:
            self.db.delete(member)
            self.db.commit()
        except SQLAlchemyError as exc:
            self.db.rollback()
            raise AppError("Failed to remove project member.") from exc

    # -------------------------------------------------------------------------
    # Dependency operations against project_dependencies
    # -------------------------------------------------------------------------

    def add_dependency(
        self,
        organization_id: uuid.UUID,
        project_id: uuid.UUID,
        depends_on_project_id: uuid.UUID,
        dependency_type: str = "blocks",
    ) -> ProjectDependency:
        """Record a dependency of one project on another within the same organization."""
        if project_id == depends_on_project_id:
            raise ValidationError("A project cannot depend on itself.")

        # Ensure both projects exist and belong to the same organization
        self.get_project_by_id(organization_id, project_id)
        self.get_project_by_id(organization_id, depends_on_project_id)

        existing = (
            self.db.execute(
                select(ProjectDependency).where(
                    ProjectDependency.organization_id == organization_id,
                    ProjectDependency.project_id == project_id,
                    ProjectDependency.depends_on_project_id == depends_on_project_id,
                )
            )
            .scalars()
            .first()
        )
        if existing:
            raise ConflictError(
                f"Dependency from project '{project_id}' to '{depends_on_project_id}' already exists."
            )

        dependency = ProjectDependency(
            organization_id=organization_id,
            project_id=project_id,
            depends_on_project_id=depends_on_project_id,
            dependency_type=dependency_type,
            created_at=datetime.now(timezone.utc),
        )

        try:
            self.db.add(dependency)
            self.db.commit()
            self.db.refresh(dependency)
            return dependency
        except IntegrityError as exc:
            self.db.rollback()
            raise ConflictError("Failed to add project dependency due to constraint violation.") from exc
        except SQLAlchemyError as exc:
            self.db.rollback()
            raise AppError("Failed to add project dependency.") from exc

    def list_dependencies(
        self,
        organization_id: uuid.UUID,
        project_id: uuid.UUID,
    ) -> List[ProjectDependency]:
        """List all dependencies of a project (projects this project depends on)."""
        self.get_project_by_id(organization_id, project_id)

        try:
            return list(
                self.db.execute(
                    select(ProjectDependency)
                    .where(
                        ProjectDependency.organization_id == organization_id,
                        ProjectDependency.project_id == project_id,
                    )
                    .order_by(ProjectDependency.created_at.asc())
                )
                .scalars()
                .all()
            )
        except SQLAlchemyError as exc:
            raise AppError("Database error occurred while listing project dependencies.") from exc

    def list_dependents(
        self,
        organization_id: uuid.UUID,
        project_id: uuid.UUID,
    ) -> List[ProjectDependency]:
        """List all dependents of a project (projects that depend on this project)."""
        self.get_project_by_id(organization_id, project_id)

        try:
            return list(
                self.db.execute(
                    select(ProjectDependency)
                    .where(
                        ProjectDependency.organization_id == organization_id,
                        ProjectDependency.depends_on_project_id == project_id,
                    )
                    .order_by(ProjectDependency.created_at.asc())
                )
                .scalars()
                .all()
            )
        except SQLAlchemyError as exc:
            raise AppError("Database error occurred while listing project dependents.") from exc

    def remove_dependency(
        self,
        organization_id: uuid.UUID,
        project_id: uuid.UUID,
        depends_on_project_id: uuid.UUID,
    ) -> None:
        """Remove a recorded dependency between two projects."""
        self.get_project_by_id(organization_id, project_id)

        dependency = (
            self.db.execute(
                select(ProjectDependency).where(
                    ProjectDependency.organization_id == organization_id,
                    ProjectDependency.project_id == project_id,
                    ProjectDependency.depends_on_project_id == depends_on_project_id,
                )
            )
            .scalars()
            .first()
        )
        if not dependency:
            raise NotFoundError(
                f"Dependency from project '{project_id}' to '{depends_on_project_id}' not found."
            )

        try:
            self.db.delete(dependency)
            self.db.commit()
        except SQLAlchemyError as exc:
            self.db.rollback()
            raise AppError("Failed to remove project dependency.") from exc
