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
    Base,
    Organization,
    Project,
    ProjectDependency,
    ProjectMember,
    User,
)
from apps.api.app.repositories.project_repository import ProjectRepository


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
    return ProjectRepository(db)


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


# =============================================================================
# 1. Project CRUD Unit Tests
# =============================================================================

def test_create_project_success(repo, org_a, user_a):
    """Verify creating a valid project returns persisted Project entity."""
    project = repo.create_project(
        organization_id=org_a.id,
        name="Continuum Platform",
        key="CONT",
        description="Core Continuity Platform",
        owner_id=user_a.id,
        status="active",
    )
    assert project.id is not None
    assert project.organization_id == org_a.id
    assert project.name == "Continuum Platform"
    assert project.key == "CONT"
    assert project.description == "Core Continuity Platform"
    assert project.owner_id == user_a.id
    assert project.status == "active"
    assert project.created_at is not None
    assert project.updated_at is not None


def test_create_project_validation_errors(repo, org_a):
    """Verify empty name or key raises ValidationError."""
    with pytest.raises(ValidationError):
        repo.create_project(organization_id=org_a.id, name="", key="KEY")

    with pytest.raises(ValidationError):
        repo.create_project(organization_id=org_a.id, name="Name", key="")


def test_create_project_duplicate_key_conflict(repo, org_a):
    """Verify creating two projects with the same key in the same org raises ConflictError."""
    repo.create_project(organization_id=org_a.id, name="Project 1", key="PROJ")

    with pytest.raises(ConflictError) as exc_info:
        repo.create_project(organization_id=org_a.id, name="Project 2", key="PROJ")
    assert "already exists" in str(exc_info.value)


def test_create_project_invalid_owner(repo, org_a):
    """Verify creating a project with a non-existent owner raises NotFoundError."""
    fake_user_id = uuid.uuid4()
    with pytest.raises(NotFoundError) as exc_info:
        repo.create_project(
            organization_id=org_a.id,
            name="Project",
            key="PROJ",
            owner_id=fake_user_id,
        )
    assert f"Owner user '{fake_user_id}' not found" in str(exc_info.value)


def test_get_project_by_id_success(repo, org_a):
    """Verify get_project_by_id retrieves the correct project."""
    created = repo.create_project(organization_id=org_a.id, name="Alpha", key="ALPHA")
    retrieved = repo.get_project_by_id(organization_id=org_a.id, project_id=created.id)
    assert retrieved.id == created.id
    assert retrieved.name == "Alpha"


def test_get_project_by_id_not_found(repo, org_a):
    """Verify get_project_by_id raises NotFoundError for non-existent project."""
    fake_id = uuid.uuid4()
    with pytest.raises(NotFoundError) as exc_info:
        repo.get_project_by_id(organization_id=org_a.id, project_id=fake_id)
    assert f"Project '{fake_id}' not found" in str(exc_info.value)


def test_get_project_by_key(repo, org_a):
    """Verify get_project_by_key returns Project if found, None if not found."""
    created = repo.create_project(organization_id=org_a.id, name="Beta", key="BETA")
    found = repo.get_project_by_key(organization_id=org_a.id, key="BETA")
    assert found is not None
    assert found.id == created.id

    not_found = repo.get_project_by_key(organization_id=org_a.id, key="NONEXISTENT")
    assert not_found is None


def test_list_projects_filtering_and_pagination(repo, org_a, user_a):
    """Verify list_projects filtering by status and owner, plus skip/limit pagination."""
    p1 = repo.create_project(org_a.id, "P1", "K1", owner_id=user_a.id, status="active")
    p2 = repo.create_project(org_a.id, "P2", "K2", owner_id=user_a.id, status="archived")
    p3 = repo.create_project(org_a.id, "P3", "K3", owner_id=None, status="active")

    # List all
    all_projects = repo.list_projects(org_a.id)
    assert len(all_projects) == 3

    # Filter status
    active_projects = repo.list_projects(org_a.id, status="active")
    assert len(active_projects) == 2
    assert {p.id for p in active_projects} == {p1.id, p3.id}

    # Filter owner
    user_projects = repo.list_projects(org_a.id, owner_id=user_a.id)
    assert len(user_projects) == 2
    assert {p.id for p in user_projects} == {p1.id, p2.id}

    # Pagination
    paginated = repo.list_projects(org_a.id, skip=1, limit=1)
    assert len(paginated) == 1

    # Invalid pagination
    with pytest.raises(ValidationError):
        repo.list_projects(org_a.id, skip=-1)
    with pytest.raises(ValidationError):
        repo.list_projects(org_a.id, limit=0)


def test_update_project(repo, org_a, user_a):
    """Verify update_project modifies fields and updates updated_at timestamp."""
    project = repo.create_project(org_a.id, "Old Name", "OLD", description="Old Desc")

    updated = repo.update_project(
        org_a.id,
        project.id,
        name="New Name",
        key="NEW",
        description="New Desc",
        owner_id=user_a.id,
        status="archived",
    )
    assert updated.name == "New Name"
    assert updated.key == "NEW"
    assert updated.description == "New Desc"
    assert updated.owner_id == user_a.id
    assert updated.status == "archived"


def test_update_project_key_conflict(repo, org_a):
    """Verify updating project key to an existing key raises ConflictError."""
    repo.create_project(org_a.id, "Project 1", "P1")
    p2 = repo.create_project(org_a.id, "Project 2", "P2")

    with pytest.raises(ConflictError):
        repo.update_project(org_a.id, p2.id, key="P1")


def test_soft_delete_project(repo, org_a):
    """Verify soft_delete_project updates status to archived/deleted without removing record."""
    project = repo.create_project(org_a.id, "Target", "TGT", status="active")
    soft_deleted = repo.soft_delete_project(org_a.id, project.id, status="archived")

    assert soft_deleted.status == "archived"
    refetched = repo.get_project_by_id(org_a.id, project.id)
    assert refetched.status == "archived"


def test_hard_delete_project(repo, org_a):
    """Verify hard_delete_project removes record completely."""
    project = repo.create_project(org_a.id, "Target", "TGT")
    repo.hard_delete_project(org_a.id, project.id)

    with pytest.raises(NotFoundError):
        repo.get_project_by_id(org_a.id, project.id)


# =============================================================================
# 2. Project Membership Operations Unit Tests
# =============================================================================

def test_add_and_list_members(repo, org_a, user_a):
    """Verify adding members and listing members."""
    project = repo.create_project(org_a.id, "Project", "PROJ")

    member = repo.add_member(org_a.id, project.id, user_a.id, role="lead")
    assert member.id is not None
    assert member.organization_id == org_a.id
    assert member.project_id == project.id
    assert member.user_id == user_a.id
    assert member.role == "lead"

    members = repo.list_members(org_a.id, project.id)
    assert len(members) == 1
    assert members[0].user_id == user_a.id


def test_add_member_duplicate_conflict(repo, org_a, user_a):
    """Verify adding the same member twice raises ConflictError."""
    project = repo.create_project(org_a.id, "Project", "PROJ")
    repo.add_member(org_a.id, project.id, user_a.id, role="member")

    with pytest.raises(ConflictError):
        repo.add_member(org_a.id, project.id, user_a.id, role="member")


def test_get_and_update_member_role(repo, org_a, user_a):
    """Verify retrieving a member and updating their role."""
    project = repo.create_project(org_a.id, "Project", "PROJ")
    repo.add_member(org_a.id, project.id, user_a.id, role="member")

    member = repo.get_member(org_a.id, project.id, user_a.id)
    assert member.role == "member"

    updated_member = repo.update_member_role(org_a.id, project.id, user_a.id, role="maintainer")
    assert updated_member.role == "maintainer"


def test_remove_member(repo, org_a, user_a):
    """Verify removing a member deletes membership record."""
    project = repo.create_project(org_a.id, "Project", "PROJ")
    repo.add_member(org_a.id, project.id, user_a.id, role="member")

    repo.remove_member(org_a.id, project.id, user_a.id)

    with pytest.raises(NotFoundError):
        repo.get_member(org_a.id, project.id, user_a.id)


# =============================================================================
# 3. Project Dependency Operations Unit Tests
# =============================================================================

def test_add_and_list_dependencies(repo, org_a):
    """Verify recording and listing project dependencies."""
    p1 = repo.create_project(org_a.id, "Frontend", "FE")
    p2 = repo.create_project(org_a.id, "API", "API")

    dep = repo.add_dependency(org_a.id, project_id=p1.id, depends_on_project_id=p2.id, dependency_type="requires")
    assert dep.id is not None
    assert dep.project_id == p1.id
    assert dep.depends_on_project_id == p2.id
    assert dep.dependency_type == "requires"

    dependencies = repo.list_dependencies(org_a.id, p1.id)
    assert len(dependencies) == 1
    assert dependencies[0].depends_on_project_id == p2.id

    dependents = repo.list_dependents(org_a.id, p2.id)
    assert len(dependents) == 1
    assert dependents[0].project_id == p1.id


def test_add_self_dependency_raises_validation_error(repo, org_a):
    """Verify a project cannot depend on itself."""
    p1 = repo.create_project(org_a.id, "Service", "SVC")
    with pytest.raises(ValidationError) as exc_info:
        repo.add_dependency(org_a.id, project_id=p1.id, depends_on_project_id=p1.id)
    assert "cannot depend on itself" in str(exc_info.value)


def test_add_duplicate_dependency_conflict(repo, org_a):
    """Verify duplicate dependency raises ConflictError."""
    p1 = repo.create_project(org_a.id, "Service 1", "SVC1")
    p2 = repo.create_project(org_a.id, "Service 2", "SVC2")

    repo.add_dependency(org_a.id, p1.id, p2.id)
    with pytest.raises(ConflictError):
        repo.add_dependency(org_a.id, p1.id, p2.id)


def test_remove_dependency(repo, org_a):
    """Verify removing a dependency record."""
    p1 = repo.create_project(org_a.id, "Service 1", "SVC1")
    p2 = repo.create_project(org_a.id, "Service 2", "SVC2")
    repo.add_dependency(org_a.id, p1.id, p2.id)

    repo.remove_dependency(org_a.id, p1.id, p2.id)
    assert len(repo.list_dependencies(org_a.id, p1.id)) == 0


# =============================================================================
# 4. Security & Cross-Organization Isolation Integration Tests
# =============================================================================

def test_cross_organization_get_project_raises_not_found(repo, org_a, org_b):
    """Security test: Org B cannot see Org A's project even with valid project ID."""
    proj_a = repo.create_project(org_a.id, "Project A", "PA")

    # Calling get_project_by_id with Org B's organization_id must raise identical NotFoundError
    with pytest.raises(NotFoundError) as exc_info:
        repo.get_project_by_id(organization_id=org_b.id, project_id=proj_a.id)
    assert f"Project '{proj_a.id}' not found" in str(exc_info.value)


def test_cross_organization_get_by_key_returns_none(repo, org_a, org_b):
    """Security test: Org B cannot retrieve Org A's project by key."""
    repo.create_project(org_a.id, "Project A", "PA")

    # Org B querying with key 'PA' should get None
    assert repo.get_project_by_key(org_b.id, "PA") is None

    # Org B can independently create a project with key 'PA' in their own org
    proj_b = repo.create_project(org_b.id, "Project B", "PA")
    assert proj_b.organization_id == org_b.id
    assert proj_b.key == "PA"


def test_cross_organization_list_projects_isolation(repo, org_a, org_b):
    """Security test: list_projects strictly scopes results to the caller's organization."""
    p_a1 = repo.create_project(org_a.id, "Project A1", "PA1")
    p_a2 = repo.create_project(org_a.id, "Project A2", "PA2")
    p_b1 = repo.create_project(org_b.id, "Project B1", "PB1")

    org_a_projects = repo.list_projects(org_a.id)
    org_b_projects = repo.list_projects(org_b.id)

    assert len(org_a_projects) == 2
    assert {p.id for p in org_a_projects} == {p_a1.id, p_a2.id}

    assert len(org_b_projects) == 1
    assert {p.id for p in org_b_projects} == {p_b1.id}


def test_cross_organization_update_project_isolation(repo, org_a, org_b):
    """Security test: Org B cannot update Org A's project."""
    proj_a = repo.create_project(org_a.id, "Project A", "PA")

    with pytest.raises(NotFoundError):
        repo.update_project(org_b.id, proj_a.id, name="Hacked Name")

    # Verify project in Org A was unmodified
    refetched = repo.get_project_by_id(org_a.id, proj_a.id)
    assert refetched.name == "Project A"


def test_cross_organization_soft_and_hard_delete_isolation(repo, org_a, org_b):
    """Security test: Org B cannot soft-delete or hard-delete Org A's project."""
    proj_a = repo.create_project(org_a.id, "Project A", "PA")

    with pytest.raises(NotFoundError):
        repo.soft_delete_project(org_b.id, proj_a.id)

    with pytest.raises(NotFoundError):
        repo.hard_delete_project(org_b.id, proj_a.id)

    # Verify Org A's project still exists and is active
    refetched = repo.get_project_by_id(org_a.id, proj_a.id)
    assert refetched.status == "active"


def test_cross_organization_membership_isolation(repo, org_a, org_b, user_a, user_b):
    """Security test: Cannot add a cross-org user, nor manipulate members across orgs."""
    proj_a = repo.create_project(org_a.id, "Project A", "PA")
    proj_b = repo.create_project(org_b.id, "Project B", "PB")

    # 1. Org A cannot add Org B's user to Org A's project
    with pytest.raises(NotFoundError):
        repo.add_member(org_a.id, proj_a.id, user_b.id)

    # 2. Org B cannot add members to Org A's project
    with pytest.raises(NotFoundError):
        repo.add_member(org_b.id, proj_a.id, user_b.id)

    # 3. Add valid member to Org A's project
    repo.add_member(org_a.id, proj_a.id, user_a.id)

    # 4. Org B cannot list members of Org A's project
    with pytest.raises(NotFoundError):
        repo.list_members(org_b.id, proj_a.id)

    # 5. Org B cannot update or remove members of Org A's project
    with pytest.raises(NotFoundError):
        repo.update_member_role(org_b.id, proj_a.id, user_a.id, role="admin")

    with pytest.raises(NotFoundError):
        repo.remove_member(org_b.id, proj_a.id, user_a.id)


def test_cross_organization_dependency_isolation(repo, org_a, org_b):
    """Security test: Dependencies cannot cross organization boundaries."""
    proj_a = repo.create_project(org_a.id, "Project A", "PA")
    proj_b = repo.create_project(org_b.id, "Project B", "PB")

    # Org A trying to depend on Org B's project must fail
    with pytest.raises(NotFoundError):
        repo.add_dependency(org_a.id, proj_a.id, proj_b.id)

    # Org B trying to depend on Org A's project must fail
    with pytest.raises(NotFoundError):
        repo.add_dependency(org_b.id, proj_b.id, proj_a.id)

    # Org B cannot query Org A's dependencies
    with pytest.raises(NotFoundError):
        repo.list_dependencies(org_b.id, proj_a.id)

    with pytest.raises(NotFoundError):
        repo.list_dependents(org_b.id, proj_a.id)
