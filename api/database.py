"""Database layer — SQLAlchemy + asyncpg + Row Level Security.

Multi-tenant PostgreSQL with:
- Async engine (asyncpg)
- Row Level Security (RLS) for tenant isolation
- Connection pooling
- Migration support (Alembic-ready)
"""

from __future__ import annotations

import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

try:
    from sqlalchemy.ext.asyncio import (
        AsyncSession,
        async_sessionmaker,
        create_async_engine,
    )
    from sqlalchemy.orm import DeclarativeBase

    HAS_SQLALCHEMY = True
except ImportError:
    HAS_SQLALCHEMY = False
    AsyncSession = None  # type: ignore
    async_sessionmaker = None  # type: ignore
    create_async_engine = None  # type: ignore

    class DeclarativeBase:  # type: ignore
        pass

# ─── Configuration ──────────────────────────────────────────────

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://juraregel:juraregel@localhost:5432/juraregel",
)

# ─── Engine ────────────────────────────────────────────────────

if HAS_SQLALCHEMY:
    engine = create_async_engine(
        DATABASE_URL,
        echo=False,
        pool_size=20,
        max_overflow=10,
        pool_pre_ping=True,
    )

    async_session_factory = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
else:
    engine = None
    async_session_factory = None


# ─── Base ──────────────────────────────────────────────────────


class Base(DeclarativeBase):
    """Base class for all ORM models."""

    pass


# ─── Session Management ────────────────────────────────────────


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Get a database session with automatic cleanup."""
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def set_tenant_context(session: AsyncSession, tenant_id: str) -> None:
    """Set the current tenant for RLS policies."""
    await session.execute(
        __import__("sqlalchemy").text("SET LOCAL app.current_org = :tenant_id"),
        {"tenant_id": tenant_id},
    )


async def init_database() -> None:
    """Create all tables (development only — use Alembic in production)."""
    if HAS_SQLALCHEMY and engine:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


async def close_database() -> None:
    """Close the database engine."""
    if HAS_SQLALCHEMY and engine:
        await engine.dispose()
