"""Initial schema creation

Revision ID: 0001
Revises: 
Create Date: 2026-09-01 10:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '0001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. organizations
    op.create_table(
        'organizations',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('slug', sa.String(length=255), nullable=False),
        sa.Column('settings', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
        sa.UniqueConstraint('slug')
    )

    # 2. departments
    op.create_table(
        'departments',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('organization_id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('code', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_departments_organization_id'), 'departments', ['organization_id'], unique=False)

    # 3. teams
    op.create_table(
        'teams',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('organization_id', sa.UUID(), nullable=False),
        sa.Column('department_id', sa.UUID(), nullable=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['department_id'], ['departments.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_teams_department_id'), 'teams', ['department_id'], unique=False)
    op.create_index(op.f('ix_teams_organization_id'), 'teams', ['organization_id'], unique=False)

    # 4. users
    op.create_table(
        'users',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('organization_id', sa.UUID(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('full_name', sa.String(length=255), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('is_superuser', sa.Boolean(), nullable=False),
        sa.Column('external_identity_provider', sa.String(length=50), nullable=True),
        sa.Column('external_identity_id', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_organization_id'), 'users', ['organization_id'], unique=False)

    # 5. roles
    op.create_table(
        'roles',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('organization_id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.String(length=255), nullable=True),
        sa.Column('permissions', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_roles_organization_id'), 'roles', ['organization_id'], unique=False)

    # 6. user_roles
    op.create_table(
        'user_roles',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('organization_id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('role_id', sa.UUID(), nullable=False),
        sa.Column('assigned_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_roles_organization_id'), 'user_roles', ['organization_id'], unique=False)
    op.create_index(op.f('ix_user_roles_role_id'), 'user_roles', ['role_id'], unique=False)
    op.create_index(op.f('ix_user_roles_user_id'), 'user_roles', ['user_id'], unique=False)

    # 7. skills
    op.create_table(
        'skills',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('organization_id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('category', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_skills_organization_id'), 'skills', ['organization_id'], unique=False)

    # 8. user_skills
    op.create_table(
        'user_skills',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('organization_id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('skill_id', sa.UUID(), nullable=False),
        sa.Column('proficiency_level', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['skill_id'], ['skills.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_skills_organization_id'), 'user_skills', ['organization_id'], unique=False)
    op.create_index(op.f('ix_user_skills_skill_id'), 'user_skills', ['skill_id'], unique=False)
    op.create_index(op.f('ix_user_skills_user_id'), 'user_skills', ['user_id'], unique=False)

    # 9. projects
    op.create_table(
        'projects',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('organization_id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('key', sa.String(length=50), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('owner_id', sa.UUID(), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_projects_key'), 'projects', ['key'], unique=False)
    op.create_index(op.f('ix_projects_organization_id'), 'projects', ['organization_id'], unique=False)
    op.create_index(op.f('ix_projects_owner_id'), 'projects', ['owner_id'], unique=False)

    # 10. project_members
    op.create_table(
        'project_members',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('organization_id', sa.UUID(), nullable=False),
        sa.Column('project_id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('role', sa.String(length=50), nullable=False),
        sa.Column('joined_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_project_members_organization_id'), 'project_members', ['organization_id'], unique=False)
    op.create_index(op.f('ix_project_members_project_id'), 'project_members', ['project_id'], unique=False)
    op.create_index(op.f('ix_project_members_user_id'), 'project_members', ['user_id'], unique=False)

    # 11. project_dependencies
    op.create_table(
        'project_dependencies',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('organization_id', sa.UUID(), nullable=False),
        sa.Column('project_id', sa.UUID(), nullable=False),
        sa.Column('depends_on_project_id', sa.UUID(), nullable=False),
        sa.Column('dependency_type', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['depends_on_project_id'], ['projects.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_project_dependencies_depends_on_project_id'), 'project_dependencies', ['depends_on_project_id'], unique=False)
    op.create_index(op.f('ix_project_dependencies_organization_id'), 'project_dependencies', ['organization_id'], unique=False)
    op.create_index(op.f('ix_project_dependencies_project_id'), 'project_dependencies', ['project_id'], unique=False)

    # 12. assets
    op.create_table(
        'assets',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('organization_id', sa.UUID(), nullable=False),
        sa.Column('project_id', sa.UUID(), nullable=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('asset_type', sa.String(length=50), nullable=False),
        sa.Column('owner_id', sa.UUID(), nullable=True),
        sa.Column('asset_metadata', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_assets_organization_id'), 'assets', ['organization_id'], unique=False)
    op.create_index(op.f('ix_assets_owner_id'), 'assets', ['owner_id'], unique=False)
    op.create_index(op.f('ix_assets_project_id'), 'assets', ['project_id'], unique=False)

    # 13. knowledge_documents
    op.create_table(
        'knowledge_documents',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('organization_id', sa.UUID(), nullable=False),
        sa.Column('project_id', sa.UUID(), nullable=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('source_type', sa.String(length=50), nullable=False),
        sa.Column('source_url', sa.String(length=512), nullable=True),
        sa.Column('source_version', sa.String(length=100), nullable=True),
        sa.Column('checksum', sa.String(length=64), nullable=True),
        sa.Column('classification', sa.String(length=50), nullable=True),
        sa.Column('owner_id', sa.UUID(), nullable=True),
        sa.Column('allowed_roles', sa.JSON(), nullable=True),
        sa.Column('allowed_groups', sa.JSON(), nullable=True),
        sa.Column('allowed_users', sa.JSON(), nullable=True),
        sa.Column('acl_version', sa.String(length=50), nullable=True),
        sa.Column('parser_version', sa.String(length=50), nullable=True),
        sa.Column('chunking_version', sa.String(length=50), nullable=True),
        sa.Column('embedding_model', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_knowledge_documents_organization_id'), 'knowledge_documents', ['organization_id'], unique=False)
    op.create_index(op.f('ix_knowledge_documents_owner_id'), 'knowledge_documents', ['owner_id'], unique=False)
    op.create_index(op.f('ix_knowledge_documents_project_id'), 'knowledge_documents', ['project_id'], unique=False)

    # 14. knowledge_chunks
    op.create_table(
        'knowledge_chunks',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('organization_id', sa.UUID(), nullable=False),
        sa.Column('document_id', sa.UUID(), nullable=False),
        sa.Column('chunk_index', sa.Integer(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('source_type', sa.String(length=50), nullable=True),
        sa.Column('source_url', sa.String(length=512), nullable=True),
        sa.Column('checksum', sa.String(length=64), nullable=True),
        sa.Column('classification', sa.String(length=50), nullable=True),
        sa.Column('allowed_roles', sa.JSON(), nullable=True),
        sa.Column('allowed_groups', sa.JSON(), nullable=True),
        sa.Column('allowed_users', sa.JSON(), nullable=True),
        sa.Column('parser_version', sa.String(length=50), nullable=True),
        sa.Column('chunking_version', sa.String(length=50), nullable=True),
        sa.Column('embedding_model', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['document_id'], ['knowledge_documents.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_knowledge_chunks_document_id'), 'knowledge_chunks', ['document_id'], unique=False)
    op.create_index(op.f('ix_knowledge_chunks_organization_id'), 'knowledge_chunks', ['organization_id'], unique=False)

    # 15. integrations
    op.create_table(
        'integrations',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('organization_id', sa.UUID(), nullable=False),
        sa.Column('provider', sa.String(length=50), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('config', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_integrations_organization_id'), 'integrations', ['organization_id'], unique=False)

    # 16. external_objects
    op.create_table(
        'external_objects',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('organization_id', sa.UUID(), nullable=False),
        sa.Column('integration_id', sa.UUID(), nullable=False),
        sa.Column('external_identifier', sa.String(length=255), nullable=False),
        sa.Column('external_version', sa.String(length=100), nullable=True),
        sa.Column('object_type', sa.String(length=50), nullable=False),
        sa.Column('payload', sa.JSON(), nullable=True),
        sa.Column('synced_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['integration_id'], ['integrations.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('integration_id', 'external_identifier', 'external_version', name='uq_external_object_ident')
    )
    op.create_index(op.f('ix_external_objects_external_identifier'), 'external_objects', ['external_identifier'], unique=False)
    op.create_index(op.f('ix_external_objects_integration_id'), 'external_objects', ['integration_id'], unique=False)
    op.create_index(op.f('ix_external_objects_organization_id'), 'external_objects', ['organization_id'], unique=False)

    # 17. sync_runs
    op.create_table(
        'sync_runs',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('organization_id', sa.UUID(), nullable=False),
        sa.Column('integration_id', sa.UUID(), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('stats', sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(['integration_id'], ['integrations.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_sync_runs_integration_id'), 'sync_runs', ['integration_id'], unique=False)
    op.create_index(op.f('ix_sync_runs_organization_id'), 'sync_runs', ['organization_id'], unique=False)

    # 18. handovers
    op.create_table(
        'handovers',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('organization_id', sa.UUID(), nullable=False),
        sa.Column('project_id', sa.UUID(), nullable=True),
        sa.Column('departing_user_id', sa.UUID(), nullable=False),
        sa.Column('successor_user_id', sa.UUID(), nullable=True),
        sa.Column('state', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['departing_user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['successor_user_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_handovers_departing_user_id'), 'handovers', ['departing_user_id'], unique=False)
    op.create_index(op.f('ix_handovers_organization_id'), 'handovers', ['organization_id'], unique=False)
    op.create_index(op.f('ix_handovers_project_id'), 'handovers', ['project_id'], unique=False)
    op.create_index(op.f('ix_handovers_successor_user_id'), 'handovers', ['successor_user_id'], unique=False)

    # 19. handover_tasks
    op.create_table(
        'handover_tasks',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('organization_id', sa.UUID(), nullable=False),
        sa.Column('handover_id', sa.UUID(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['handover_id'], ['handovers.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_handover_tasks_handover_id'), 'handover_tasks', ['handover_id'], unique=False)
    op.create_index(op.f('ix_handover_tasks_organization_id'), 'handover_tasks', ['organization_id'], unique=False)

    # 20. handover_approvals
    op.create_table(
        'handover_approvals',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('organization_id', sa.UUID(), nullable=False),
        sa.Column('handover_id', sa.UUID(), nullable=False),
        sa.Column('approver_id', sa.UUID(), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('comments', sa.Text(), nullable=True),
        sa.Column('decided_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['approver_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['handover_id'], ['handovers.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_handover_approvals_approver_id'), 'handover_approvals', ['approver_id'], unique=False)
    op.create_index(op.f('ix_handover_approvals_handover_id'), 'handover_approvals', ['handover_id'], unique=False)
    op.create_index(op.f('ix_handover_approvals_organization_id'), 'handover_approvals', ['organization_id'], unique=False)

    # 21. ownership_transfers
    op.create_table(
        'ownership_transfers',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('organization_id', sa.UUID(), nullable=False),
        sa.Column('handover_id', sa.UUID(), nullable=True),
        sa.Column('asset_id', sa.UUID(), nullable=True),
        sa.Column('from_user_id', sa.UUID(), nullable=False),
        sa.Column('to_user_id', sa.UUID(), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('transferred_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['asset_id'], ['assets.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['from_user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['handover_id'], ['handovers.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['to_user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ownership_transfers_asset_id'), 'ownership_transfers', ['asset_id'], unique=False)
    op.create_index(op.f('ix_ownership_transfers_from_user_id'), 'ownership_transfers', ['from_user_id'], unique=False)
    op.create_index(op.f('ix_ownership_transfers_handover_id'), 'ownership_transfers', ['handover_id'], unique=False)
    op.create_index(op.f('ix_ownership_transfers_organization_id'), 'ownership_transfers', ['organization_id'], unique=False)
    op.create_index(op.f('ix_ownership_transfers_to_user_id'), 'ownership_transfers', ['to_user_id'], unique=False)

    # 22. access_actions
    op.create_table(
        'access_actions',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('organization_id', sa.UUID(), nullable=False),
        sa.Column('handover_id', sa.UUID(), nullable=True),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('action_type', sa.String(length=50), nullable=False),
        sa.Column('target_system', sa.String(length=100), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('executed_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['handover_id'], ['handovers.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_access_actions_handover_id'), 'access_actions', ['handover_id'], unique=False)
    op.create_index(op.f('ix_access_actions_organization_id'), 'access_actions', ['organization_id'], unique=False)
    op.create_index(op.f('ix_access_actions_user_id'), 'access_actions', ['user_id'], unique=False)

    # 23. risk_assessments
    op.create_table(
        'risk_assessments',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('organization_id', sa.UUID(), nullable=False),
        sa.Column('project_id', sa.UUID(), nullable=True),
        sa.Column('asset_id', sa.UUID(), nullable=True),
        sa.Column('bus_factor_score', sa.Float(), nullable=True),
        sa.Column('kcs_score', sa.Float(), nullable=True),
        sa.Column('risk_level', sa.String(length=50), nullable=False),
        sa.Column('details', sa.JSON(), nullable=True),
        sa.Column('assessed_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['asset_id'], ['assets.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_risk_assessments_asset_id'), 'risk_assessments', ['asset_id'], unique=False)
    op.create_index(op.f('ix_risk_assessments_organization_id'), 'risk_assessments', ['organization_id'], unique=False)
    op.create_index(op.f('ix_risk_assessments_project_id'), 'risk_assessments', ['project_id'], unique=False)

    # 24. notifications
    op.create_table(
        'notifications',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('organization_id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('is_read', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_notifications_organization_id'), 'notifications', ['organization_id'], unique=False)
    op.create_index(op.f('ix_notifications_user_id'), 'notifications', ['user_id'], unique=False)

    # 25. audit_events
    op.create_table(
        'audit_events',
        sa.Column('event_id', sa.UUID(), nullable=False),
        sa.Column('sequence', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('organization_id', sa.UUID(), nullable=False),
        sa.Column('timestamp', sa.DateTime(timezone=True), nullable=False),
        sa.Column('actor_type', sa.String(length=50), nullable=False),
        sa.Column('actor_id', sa.String(length=255), nullable=True),
        sa.Column('action_type', sa.String(length=100), nullable=False),
        sa.Column('entity_type', sa.String(length=100), nullable=False),
        sa.Column('entity_id', sa.String(length=255), nullable=True),
        sa.Column('old_state_hash', sa.String(length=64), nullable=True),
        sa.Column('new_state_hash', sa.String(length=64), nullable=True),
        sa.Column('request_id', sa.String(length=255), nullable=True),
        sa.Column('correlation_id', sa.String(length=255), nullable=True),
        sa.Column('metadata', sa.JSON(), nullable=True),
        sa.Column('previous_hash', sa.String(length=64), nullable=True),
        sa.Column('current_hash', sa.String(length=64), nullable=False),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('event_id')
    )
    op.create_index(op.f('ix_audit_events_action_type'), 'audit_events', ['action_type'], unique=False)
    op.create_index(op.f('ix_audit_events_entity_type'), 'audit_events', ['entity_type'], unique=False)
    op.create_index(op.f('ix_audit_events_organization_id'), 'audit_events', ['organization_id'], unique=False)
    op.create_index(op.f('ix_audit_events_sequence'), 'audit_events', ['sequence'], unique=True)
    op.create_index(op.f('ix_audit_events_timestamp'), 'audit_events', ['timestamp'], unique=False)

    # 26. audit_verifications
    op.create_table(
        'audit_verifications',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('organization_id', sa.UUID(), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('last_verified_event_id', sa.UUID(), nullable=True),
        sa.Column('verified_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('details', sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(['last_verified_event_id'], ['audit_events.event_id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_audit_verifications_organization_id'), 'audit_verifications', ['organization_id'], unique=False)


def downgrade() -> None:
    # Drop tables in exact reverse dependency order
    op.drop_index(op.f('ix_audit_verifications_organization_id'), table_name='audit_verifications')
    op.drop_table('audit_verifications')

    op.drop_index(op.f('ix_audit_events_timestamp'), table_name='audit_events')
    op.drop_index(op.f('ix_audit_events_sequence'), table_name='audit_events')
    op.drop_index(op.f('ix_audit_events_organization_id'), table_name='audit_events')
    op.drop_index(op.f('ix_audit_events_entity_type'), table_name='audit_events')
    op.drop_index(op.f('ix_audit_events_action_type'), table_name='audit_events')
    op.drop_table('audit_events')

    op.drop_index(op.f('ix_notifications_user_id'), table_name='notifications')
    op.drop_index(op.f('ix_notifications_organization_id'), table_name='notifications')
    op.drop_table('notifications')

    op.drop_index(op.f('ix_risk_assessments_project_id'), table_name='risk_assessments')
    op.drop_index(op.f('ix_risk_assessments_organization_id'), table_name='risk_assessments')
    op.drop_index(op.f('ix_risk_assessments_asset_id'), table_name='risk_assessments')
    op.drop_table('risk_assessments')

    op.drop_index(op.f('ix_access_actions_user_id'), table_name='access_actions')
    op.drop_index(op.f('ix_access_actions_organization_id'), table_name='access_actions')
    op.drop_index(op.f('ix_access_actions_handover_id'), table_name='access_actions')
    op.drop_table('access_actions')

    op.drop_index(op.f('ix_ownership_transfers_to_user_id'), table_name='ownership_transfers')
    op.drop_index(op.f('ix_ownership_transfers_organization_id'), table_name='ownership_transfers')
    op.drop_index(op.f('ix_ownership_transfers_handover_id'), table_name='ownership_transfers')
    op.drop_index(op.f('ix_ownership_transfers_from_user_id'), table_name='ownership_transfers')
    op.drop_index(op.f('ix_ownership_transfers_asset_id'), table_name='ownership_transfers')
    op.drop_table('ownership_transfers')

    op.drop_index(op.f('ix_handover_approvals_organization_id'), table_name='handover_approvals')
    op.drop_index(op.f('ix_handover_approvals_handover_id'), table_name='handover_approvals')
    op.drop_index(op.f('ix_handover_approvals_approver_id'), table_name='handover_approvals')
    op.drop_table('handover_approvals')

    op.drop_index(op.f('ix_handover_tasks_organization_id'), table_name='handover_tasks')
    op.drop_index(op.f('ix_handover_tasks_handover_id'), table_name='handover_tasks')
    op.drop_table('handover_tasks')

    op.drop_index(op.f('ix_handovers_successor_user_id'), table_name='handovers')
    op.drop_index(op.f('ix_handovers_project_id'), table_name='handovers')
    op.drop_index(op.f('ix_handovers_organization_id'), table_name='handovers')
    op.drop_index(op.f('ix_handovers_departing_user_id'), table_name='handovers')
    op.drop_table('handovers')

    op.drop_index(op.f('ix_sync_runs_organization_id'), table_name='sync_runs')
    op.drop_index(op.f('ix_sync_runs_integration_id'), table_name='sync_runs')
    op.drop_table('sync_runs')

    op.drop_index(op.f('ix_external_objects_organization_id'), table_name='external_objects')
    op.drop_index(op.f('ix_external_objects_integration_id'), table_name='external_objects')
    op.drop_index(op.f('ix_external_objects_external_identifier'), table_name='external_objects')
    op.drop_table('external_objects')

    op.drop_index(op.f('ix_integrations_organization_id'), table_name='integrations')
    op.drop_table('integrations')

    op.drop_index(op.f('ix_knowledge_chunks_organization_id'), table_name='knowledge_chunks')
    op.drop_index(op.f('ix_knowledge_chunks_document_id'), table_name='knowledge_chunks')
    op.drop_table('knowledge_chunks')

    op.drop_index(op.f('ix_knowledge_documents_project_id'), table_name='knowledge_documents')
    op.drop_index(op.f('ix_knowledge_documents_owner_id'), table_name='knowledge_documents')
    op.drop_index(op.f('ix_knowledge_documents_organization_id'), table_name='knowledge_documents')
    op.drop_table('knowledge_documents')

    op.drop_index(op.f('ix_assets_project_id'), table_name='assets')
    op.drop_index(op.f('ix_assets_owner_id'), table_name='assets')
    op.drop_index(op.f('ix_assets_organization_id'), table_name='assets')
    op.drop_table('assets')

    op.drop_index(op.f('ix_project_dependencies_project_id'), table_name='project_dependencies')
    op.drop_index(op.f('ix_project_dependencies_organization_id'), table_name='project_dependencies')
    op.drop_index(op.f('ix_project_dependencies_depends_on_project_id'), table_name='project_dependencies')
    op.drop_table('project_dependencies')

    op.drop_index(op.f('ix_project_members_user_id'), table_name='project_members')
    op.drop_index(op.f('ix_project_members_project_id'), table_name='project_members')
    op.drop_index(op.f('ix_project_members_organization_id'), table_name='project_members')
    op.drop_table('project_members')

    op.drop_index(op.f('ix_projects_owner_id'), table_name='projects')
    op.drop_index(op.f('ix_projects_organization_id'), table_name='projects')
    op.drop_index(op.f('ix_projects_key'), table_name='projects')
    op.drop_table('projects')

    op.drop_index(op.f('ix_user_skills_user_id'), table_name='user_skills')
    op.drop_index(op.f('ix_user_skills_skill_id'), table_name='user_skills')
    op.drop_index(op.f('ix_user_skills_organization_id'), table_name='user_skills')
    op.drop_table('user_skills')

    op.drop_index(op.f('ix_skills_organization_id'), table_name='skills')
    op.drop_table('skills')

    op.drop_index(op.f('ix_user_roles_user_id'), table_name='user_roles')
    op.drop_index(op.f('ix_user_roles_role_id'), table_name='user_roles')
    op.drop_index(op.f('ix_user_roles_organization_id'), table_name='user_roles')
    op.drop_table('user_roles')

    op.drop_index(op.f('ix_roles_organization_id'), table_name='roles')
    op.drop_table('roles')

    op.drop_index(op.f('ix_users_organization_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')

    op.drop_index(op.f('ix_teams_organization_id'), table_name='teams')
    op.drop_index(op.f('ix_teams_department_id'), table_name='teams')
    op.drop_table('teams')

    op.drop_index(op.f('ix_departments_organization_id'), table_name='departments')
    op.drop_table('departments')

    op.drop_table('organizations')
