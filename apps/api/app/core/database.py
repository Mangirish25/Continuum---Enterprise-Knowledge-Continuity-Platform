from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from apps.api.app.core.config import settings

engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    echo=(settings.APP_MODE == "dev"),
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """Provide transactional database session dependency."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
