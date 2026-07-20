"""Database layer — SQLAlchemy with multi-backend support.

Supports:
- PostgreSQL (production, with RLS)
- SQLite (development, with aiosqlite)
- File mode (no database — in-memory stores)

Auto-selects backend based on DATABASE_URL environment variable.
If DATABASE_URL is not set, operates in file mode.
"""

from __future__ import annotations

import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

# ─── Configuration ──────────────────────────────────────────────

DATABASE_URL = os.getenv("DATABASE_URL", "")
USE_DATABASE = bool(DATABASE_URL)
IS_POSTGRES = DATABASE_URL.startswith("postgresql") if DATABASE_URL else False
IS_SQLITE = DATABASE_URL.startswith("sqlite") if DATABASE_URL else False

# ─── Imports ──────────────────────────────────────────────────

HAS_SQLALCHEMY = False
AsyncSession = None
async_sessionmaker = None
create_async_engine = None

try:
    from sqlalchemy.ext.asyncio import (
        AsyncSession,
        async_sessionmaker,
        create_async_engine,
    )
    from sqlalchemy.orm import DeclarativeBase

    HAS_SQLALCHEMY = True
except ImportError:
    pass

if not HAS_SQLALCHEMY:

    class DeclarativeBase:
        pass


# ─── Engine ────────────────────────────────────────────────────

engine = None
async_session_factory = None

if HAS_SQLALCHEMY and USE_DATABASE:
    if IS_POSTGRES:
        engine = create_async_engine(
            DATABASE_URL,
            echo=False,
            pool_size=20,
            max_overflow=10,
            pool_pre_ping=True,
        )
    elif IS_SQLITE:
        engine = create_async_engine(
            DATABASE_URL,
            echo=False,
            connect_args={"check_same_thread": False},
        )

    if engine:
        async_session_factory = async_sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )


# ─── Base ──────────────────────────────────────────────────────


class Base(DeclarativeBase):
    """Base class for all ORM models."""

    pass


# ─── Session Management ────────────────────────────────────────


@asynccontextmanager
async def get_session() -> AsyncGenerator:
    """Get a database session with automatic cleanup."""
    if async_session_factory:
        async with async_session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
    else:
        yield None


async def set_tenant_context(session, tenant_id: str) -> None:
    """Set the current tenant for RLS policies (PostgreSQL only)."""
    if IS_POSTGRES and session:
        import sqlalchemy

        await session.execute(
            sqlalchemy.text("SET LOCAL app.current_org = :tenant_id"),
            {"tenant_id": tenant_id},
        )


async def init_database() -> None:
    """Create all tables (development only — use Alembic in production)."""
    if HAS_SQLALCHEMY and USE_DATABASE and engine:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


async def close_database() -> None:
    """Close the database engine."""
    if HAS_SQLALCHEMY and USE_DATABASE and engine:
        await engine.dispose()
