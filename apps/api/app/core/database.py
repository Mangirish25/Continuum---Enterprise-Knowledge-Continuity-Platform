from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from apps.api.app.core.config import settings

engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db():
    """Dependency for obtaining a database session in FastAPI routes."""
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
