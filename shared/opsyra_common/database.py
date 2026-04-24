from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from opsyra_common.config import get_shared_settings


class Base(DeclarativeBase):
    pass


_settings = get_shared_settings()
engine = create_engine(_settings.database_url, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_database() -> None:
    from opsyra_common import models  # noqa: F401

    Base.metadata.create_all(bind=engine)
