import os
import pytest
from alembic.config import Config
from alembic import command
from sqlalchemy import create_engine, inspect


def test_alembic_upgrade_downgrade_cycle(tmp_path):
    """Integration test: Verify upgrade -> downgrade -> upgrade cycle against SQLite database."""
    db_file = tmp_path / "test_migration.db"
    db_url = f"sqlite:///{db_file}"

    # Setup Alembic Config pointing to repository alembic.ini
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    alembic_ini_path = os.path.join(repo_root, "alembic.ini")

    alembic_cfg = Config(alembic_ini_path)
    alembic_cfg.set_main_option("sqlalchemy.url", db_url)
    alembic_cfg.set_main_option("script_location", os.path.join(repo_root, "migrations"))

    # 1. Run upgrade to head
    command.upgrade(alembic_cfg, "head")

    engine = create_engine(db_url)
    inspector = inspect(engine)
    tables_after_upgrade = set(inspector.get_table_names())

    # Exclude alembic_version tracking table
    created_tables = tables_after_upgrade - {"alembic_version"}
    assert len(created_tables) == 26, f"Expected 26 tables created, got {len(created_tables)}: {created_tables}"

    # Spot check specific critical tables
    assert "organizations" in created_tables
    assert "users" in created_tables
    assert "audit_events" in created_tables
    assert "knowledge_documents" in created_tables

    # 2. Run downgrade to base
    command.downgrade(alembic_cfg, "base")

    inspector_after_downgrade = inspect(engine)
    tables_after_downgrade = set(inspector_after_downgrade.get_table_names()) - {"alembic_version"}
    assert len(tables_after_downgrade) == 0, f"Expected 0 tables remaining after downgrade, got: {tables_after_downgrade}"

    # 3. Idempotency test: Run upgrade head again
    command.upgrade(alembic_cfg, "head")

    inspector_after_second_upgrade = inspect(engine)
    tables_after_second_upgrade = set(inspector_after_second_upgrade.get_table_names()) - {"alembic_version"}
    assert len(tables_after_second_upgrade) == 26
