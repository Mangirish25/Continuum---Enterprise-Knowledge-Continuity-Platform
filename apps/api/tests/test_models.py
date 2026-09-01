import pytest
from sqlalchemy import create_engine
from apps.api.app.repositories.models import (
    Base,
    Organization,
    Department,
    Team,
    User,
    Role,
    UserRole,
    Skill,
    UserSkill,
    Project,
    ProjectMember,
    ProjectDependency,
    Asset,
    KnowledgeDocument,
    KnowledgeChunk,
    Integration,
    ExternalObject,
    SyncRun,
    Handover,
    HandoverTask,
    HandoverApproval,
    OwnershipTransfer,
    AccessAction,
    RiskAssessment,
    Notification,
    AuditEvent,
    AuditVerification,
)

EXPECTED_TABLES = {
    "organizations",
    "departments",
    "teams",
    "users",
    "roles",
    "user_roles",
    "skills",
    "user_skills",
    "projects",
    "project_members",
    "project_dependencies",
    "assets",
    "knowledge_documents",
    "knowledge_chunks",
    "integrations",
    "external_objects",
    "sync_runs",
    "handovers",
    "handover_tasks",
    "handover_approvals",
    "ownership_transfers",
    "access_actions",
    "risk_assessments",
    "notifications",
    "audit_events",
    "audit_verifications",
}


def test_all_26_models_registered_in_metadata():
    """Verify all 26 required tables from docs/DATABASE.md §2 exist in Base.metadata."""
    registered_tables = set(Base.metadata.tables.keys())
    assert registered_tables == EXPECTED_TABLES
    assert len(registered_tables) == 26


def test_tenant_isolation_organization_id_present():
    """Security test: spot-check that every tenant-owned model has an organization_id column."""
    for table_name, table in Base.metadata.tables.items():
        if table_name == "organizations":
            continue
        assert "organization_id" in table.columns, f"Table {table_name} missing mandatory organization_id column!"


def test_audit_event_exact_fields():
    """Verify audit_events contains the exact 16 fields listed in docs/DATABASE.md §8."""
    audit_table = Base.metadata.tables["audit_events"]
    expected_fields = {
        "event_id",
        "sequence",
        "organization_id",
        "timestamp",
        "actor_type",
        "actor_id",
        "action_type",
        "entity_type",
        "entity_id",
        "old_state_hash",
        "new_state_hash",
        "request_id",
        "correlation_id",
        "metadata",
        "previous_hash",
        "current_hash",
    }
    actual_fields = set(audit_table.columns.keys())
    assert actual_fields == expected_fields


def test_knowledge_metadata_fields():
    """Verify knowledge_documents and knowledge_chunks preserve docs/DATABASE.md §6 metadata fields."""
    doc_table = Base.metadata.tables["knowledge_documents"]
    chunk_table = Base.metadata.tables["knowledge_chunks"]

    expected_doc_fields = {
        "id", "organization_id", "project_id", "title", "source_type", "source_url",
        "source_version", "checksum", "classification", "owner_id", "allowed_roles",
        "allowed_groups", "allowed_users", "acl_version", "parser_version",
        "chunking_version", "embedding_model", "created_at", "updated_at"
    }
    expected_chunk_fields = {
        "id", "organization_id", "document_id", "chunk_index", "content", "source_type",
        "source_url", "checksum", "classification", "allowed_roles", "allowed_groups",
        "allowed_users", "parser_version", "chunking_version", "embedding_model", "created_at"
    }

    assert expected_doc_fields.issubset(set(doc_table.columns.keys()))
    assert expected_chunk_fields.issubset(set(chunk_table.columns.keys()))


def test_external_object_uniqueness_constraint():
    """Verify external_objects model includes the unique constraint per docs/DATABASE.md §5."""
    ext_table = Base.metadata.tables["external_objects"]
    unique_constraint_names = [uc.name for uc in ext_table.constraints if hasattr(uc, "columns")]
    assert "uq_external_object_ident" in unique_constraint_names


def test_models_create_all_smoke_test():
    """Integration test: verify all ORM models can create schema tables in SQLite in-memory without errors."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    assert len(Base.metadata.tables) == 26
