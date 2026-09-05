from datetime import datetime, timezone
import uuid
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from apps.api.app.core.exceptions import (
    AppError,
    ConflictError,
    NotFoundError,
    ValidationError,
)
from apps.api.app.repositories.models import (
    Asset,
    Base,
    Organization,
    Project,
    User,
)
from apps.api.app.repositories.asset_repository import AssetRepository


@pytest.fixture
def db():
    """Create a fresh in-memory SQLite database session for each test."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = session_factory()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def repo(db):
    return AssetRepository(db)


@pytest.fixture
def org_a(db):
    org = Organization(
        id=uuid.uuid4(),
        name="Acme Corp",
        slug="acme-corp",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    db.add(org)
    db.commit()
    db.refresh(org)
    return org


@pytest.fixture
def org_b(db):
    org = Organization(
        id=uuid.uuid4(),
        name="Beta Inc",
        slug="beta-inc",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    db.add(org)
    db.commit()
    db.refresh(org)
    return org


@pytest.fixture
def user_a(db, org_a):
    user = User(
        id=uuid.uuid4(),
        organization_id=org_a.id,
        email="alice@acme.com",
        full_name="Alice Acme",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def user_b(db, org_b):
    user = User(
        id=uuid.uuid4(),
        organization_id=org_b.id,
        email="bob@beta.com",
        full_name="Bob Beta",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def proj_a(db, org_a, user_a):
    proj = Project(
        id=uuid.uuid4(),
        organization_id=org_a.id,
        name="Project A",
        key="PA",
        owner_id=user_a.id,
        status="active",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    db.add(proj)
    db.commit()
    db.refresh(proj)
    return proj


@pytest.fixture
def proj_b(db, org_b, user_b):
    proj = Project(
        id=uuid.uuid4(),
        organization_id=org_b.id,
        name="Project B",
        key="PB",
        owner_id=user_b.id,
        status="active",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    db.add(proj)
    db.commit()
    db.refresh(proj)
    return proj


# =============================================================================
# 1. Asset CRUD & Filtering Unit Tests
# =============================================================================

def test_create_asset_success(repo, org_a, proj_a, user_a):
    """Verify creating a valid asset with all fields returns persisted Asset."""
    metadata = {"repo_url": "https://github.com/acme/repo", "language": "python"}
    asset = repo.create_asset(
        organization_id=org_a.id,
        name="Core Repo",
        asset_type="repository",
        project_id=proj_a.id,
        owner_id=user_a.id,
        asset_metadata=metadata,
    )
    assert asset.id is not None
    assert asset.organization_id == org_a.id
    assert asset.name == "Core Repo"
    assert asset.asset_type == "repository"
    assert asset.project_id == proj_a.id
    assert asset.owner_id == user_a.id
    assert asset.asset_metadata == metadata
    assert asset.created_at is not None
    assert asset.updated_at is not None


def test_create_asset_minimal(repo, org_a):
    """Verify creating an asset with minimal fields (no project, no owner, no metadata)."""
    asset = repo.create_asset(
        organization_id=org_a.id,
        name="Standalone Service",
        asset_type="service",
    )
    assert asset.id is not None
    assert asset.project_id is None
    assert asset.owner_id is None
    assert asset.asset_metadata is None


def test_create_asset_validation_empty_fields(repo, org_a):
    """Verify empty name or asset_type raises ValidationError."""
    with pytest.raises(ValidationError):
        repo.create_asset(organization_id=org_a.id, name="", asset_type="repository")

    with pytest.raises(ValidationError):
        repo.create_asset(organization_id=org_a.id, name="Name", asset_type="")


def test_create_asset_invalid_project_or_owner(repo, org_a):
    """Verify non-existent project_id or owner_id raises NotFoundError."""
    fake_id = uuid.uuid4()
    with pytest.raises(NotFoundError) as exc_info:
        repo.create_asset(org_a.id, name="Asset", asset_type="db", project_id=fake_id)
    assert f"Project '{fake_id}' not found" in str(exc_info.value)

    with pytest.raises(NotFoundError) as exc_info:
        repo.create_asset(org_a.id, name="Asset", asset_type="db", owner_id=fake_id)
    assert f"Owner user '{fake_id}' not found" in str(exc_info.value)


def test_get_asset_by_id_success(repo, org_a):
    """Verify retrieving an asset by ID."""
    created = repo.create_asset(org_a.id, name="Doc", asset_type="document")
    retrieved = repo.get_asset_by_id(org_a.id, created.id)
    assert retrieved.id == created.id
    assert retrieved.name == "Doc"


def test_get_asset_by_id_not_found(repo, org_a):
    """Verify retrieving a non-existent asset raises NotFoundError."""
    fake_id = uuid.uuid4()
    with pytest.raises(NotFoundError) as exc_info:
        repo.get_asset_by_id(org_a.id, fake_id)
    assert f"Asset '{fake_id}' not found" in str(exc_info.value)


def test_list_assets_filtering_and_pagination(repo, org_a, proj_a, user_a):
    """Verify listing assets with project, owner, type filtering and pagination."""
    a1 = repo.create_asset(org_a.id, "A1", "repo", project_id=proj_a.id, owner_id=user_a.id)
    a2 = repo.create_asset(org_a.id, "A2", "doc", project_id=proj_a.id)
    a3 = repo.create_asset(org_a.id, "A3", "repo", owner_id=user_a.id)
    a4 = repo.create_asset(org_a.id, "A4", "service")

    # List all
    assert len(repo.list_assets(org_a.id)) == 4

    # Filter by project_id
    by_proj = repo.list_assets(org_a.id, project_id=proj_a.id)
    assert len(by_proj) == 2
    assert {a.id for a in by_proj} == {a1.id, a2.id}

    # Filter by owner_id
    by_owner = repo.list_assets(org_a.id, owner_id=user_a.id)
    assert len(by_owner) == 2
    assert {a.id for a in by_owner} == {a1.id, a3.id}

    # Filter by asset_type
    by_type = repo.list_assets(org_a.id, asset_type="repo")
    assert len(by_type) == 2
    assert {a.id for a in by_type} == {a1.id, a3.id}

    # Pagination
    paginated = repo.list_assets(org_a.id, skip=1, limit=2)
    assert len(paginated) == 2

    # Validation on negative skip or invalid limit
    with pytest.raises(ValidationError):
        repo.list_assets(org_a.id, skip=-1)
    with pytest.raises(ValidationError):
        repo.list_assets(org_a.id, limit=0)


def test_update_asset(repo, org_a, proj_a, user_a):
    """Verify updating asset metadata fields."""
    asset = repo.create_asset(org_a.id, "Old Name", "repo")

    updated = repo.update_asset(
        org_a.id,
        asset.id,
        name="New Name",
        asset_type="service",
        project_id=proj_a.id,
        owner_id=user_a.id,
        asset_metadata={"version": "2.0"},
    )
    assert updated.name == "New Name"
    assert updated.asset_type == "service"
    assert updated.project_id == proj_a.id
    assert updated.owner_id == user_a.id
    assert updated.asset_metadata == {"version": "2.0"}

    # Unlink project and owner by setting to None
    unlinked = repo.update_asset(org_a.id, asset.id, project_id=None, owner_id=None)
    assert unlinked.project_id is None
    assert unlinked.owner_id is None


def test_update_asset_validation_empty_fields(repo, org_a):
    """Verify updating with empty name or type raises ValidationError."""
    asset = repo.create_asset(org_a.id, "Asset", "repo")

    with pytest.raises(ValidationError):
        repo.update_asset(org_a.id, asset.id, name="   ")

    with pytest.raises(ValidationError):
        repo.update_asset(org_a.id, asset.id, asset_type="")


def test_delete_asset(repo, org_a):
    """Verify delete_asset permanently removes the asset record."""
    asset = repo.create_asset(org_a.id, "To Delete", "repo")
    repo.delete_asset(org_a.id, asset.id)

    with pytest.raises(NotFoundError):
        repo.get_asset_by_id(org_a.id, asset.id)


# =============================================================================
# 2. Cross-Organization Isolation & Security Tests
# =============================================================================

def test_cross_organization_get_asset_raises_not_found(repo, org_a, org_b):
    """Security test: Org B cannot access Org A's asset even with valid asset ID."""
    asset_a = repo.create_asset(org_a.id, "Asset A", "repo")

    # Calling get_asset_by_id with Org B's ID must raise identical NotFoundError
    with pytest.raises(NotFoundError) as exc_info:
        repo.get_asset_by_id(org_b.id, asset_a.id)
    assert f"Asset '{asset_a.id}' not found" in str(exc_info.value)


def test_cross_organization_list_assets_isolation(repo, org_a, org_b):
    """Security test: list_assets returns only caller's organization assets."""
    a_a1 = repo.create_asset(org_a.id, "A1", "repo")
    a_a2 = repo.create_asset(org_a.id, "A2", "doc")
    a_b1 = repo.create_asset(org_b.id, "B1", "repo")

    org_a_assets = repo.list_assets(org_a.id)
    org_b_assets = repo.list_assets(org_b.id)

    assert len(org_a_assets) == 2
    assert {a.id for a in org_a_assets} == {a_a1.id, a_a2.id}

    assert len(org_b_assets) == 1
    assert {a.id for a in org_b_assets} == {a_b1.id}


def test_cross_organization_update_asset_isolation(repo, org_a, org_b):
    """Security test: Org B cannot update Org A's asset."""
    asset_a = repo.create_asset(org_a.id, "Asset A", "repo")

    with pytest.raises(NotFoundError):
        repo.update_asset(org_b.id, asset_a.id, name="Compromised Name")

    # Verify Org A's asset was untouched
    refetched = repo.get_asset_by_id(org_a.id, asset_a.id)
    assert refetched.name == "Asset A"


def test_cross_organization_delete_asset_isolation(repo, org_a, org_b):
    """Security test: Org B cannot delete Org A's asset."""
    asset_a = repo.create_asset(org_a.id, "Asset A", "repo")

    with pytest.raises(NotFoundError):
        repo.delete_asset(org_b.id, asset_a.id)

    # Verify Org A's asset still exists
    refetched = repo.get_asset_by_id(org_a.id, asset_a.id)
    assert refetched.id == asset_a.id


def test_cross_organization_foreign_project_or_owner_forbidden(repo, org_a, org_b, proj_a, proj_b, user_a, user_b):
    """Security test: Assets cannot link to projects or owners from other organizations."""
    # Org A trying to create asset linked to Org B's project or owner
    with pytest.raises(NotFoundError):
        repo.create_asset(org_a.id, "A", "repo", project_id=proj_b.id)

    with pytest.raises(NotFoundError):
        repo.create_asset(org_a.id, "A", "repo", owner_id=user_b.id)

    # Org B trying to create asset linked to Org A's project or owner
    with pytest.raises(NotFoundError):
        repo.create_asset(org_b.id, "B", "repo", project_id=proj_a.id)

    with pytest.raises(NotFoundError):
        repo.create_asset(org_b.id, "B", "repo", owner_id=user_a.id)

    # Updating asset to link to foreign project or owner
    asset_a = repo.create_asset(org_a.id, "Asset A", "repo")
    with pytest.raises(NotFoundError):
        repo.update_asset(org_a.id, asset_a.id, project_id=proj_b.id)

    with pytest.raises(NotFoundError):
        repo.update_asset(org_a.id, asset_a.id, owner_id=user_b.id)
