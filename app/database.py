"""Database engine, connection pooling, SQLite PRAGMAs, and session management."""

import sqlite3
from collections.abc import Generator

from sqlalchemy import Engine, create_engine, event
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import settings


class Base(DeclarativeBase):
    """Declarative base class for all SQLAlchemy 2.0 ORM models."""


def set_sqlite_pragma(dbapi_connection, connection_record) -> None:
    """Enforce foreign keys, WAL mode, and busy timeout on every SQLite connection."""
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.execute("PRAGMA journal_mode=WAL;")
        cursor.execute("PRAGMA busy_timeout=5000;")
        cursor.close()


def get_engine_with_pragmas(db_url: str | None = None) -> Engine:
    """Create a SQLAlchemy engine with enforced SQLite PRAGMAs."""
    url = db_url or settings.DB_URL
    connect_args = {}
    if url.startswith("sqlite"):
        connect_args["check_same_thread"] = False

    eng = create_engine(
        url,
        connect_args=connect_args,
        pool_pre_ping=True,
    )
    event.listen(eng, "connect", set_sqlite_pragma)
    return eng


# Default application engine
engine: Engine = get_engine_with_pragmas(settings.DB_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency for obtaining a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db(target_engine: Engine | None = None) -> None:
    """Create all database tables on application startup and apply lightweight migrations."""
    import app.models  # noqa: F401 - Register models with Base.metadata
    eng = target_engine or engine
    Base.metadata.create_all(bind=eng)

    # Safe automated schema migrations for SQLite
    with eng.connect() as conn:
        try:
            # Check if target_repo_id exists on ads table
            res = conn.execute(sqlite3_text if "sqlite3_text" in globals() else __import__("sqlalchemy").text("PRAGMA table_info(ads);")).fetchall()
            col_names = [r[1] for r in res]
            if "target_repo_id" not in col_names and len(col_names) > 0:
                conn.execute(__import__("sqlalchemy").text("ALTER TABLE ads ADD COLUMN target_repo_id INTEGER;"))
                conn.commit()
        except Exception:
            pass


def reset_db(target_engine: Engine | None = None) -> None:
    """Drop and recreate all database tables (for test fixtures)."""
    import app.models  # noqa: F401
    eng = target_engine or engine
    Base.metadata.drop_all(bind=eng)
    Base.metadata.create_all(bind=eng)
