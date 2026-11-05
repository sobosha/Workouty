from sqlalchemy import create_engine

from app.config import settings

from sqlalchemy.orm import Session

engine = create_engine(settings.DATABASE_URL)


def get_db_session() -> Session:
    """Get a database session."""
    with Session(engine) as session:
        yield session