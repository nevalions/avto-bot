from __future__ import annotations

from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.config import user, password, host, port, db_name

DATABASE_URL = f"postgresql+asyncpg://{user}:{password}@{host}:{str(port)}/{db_name}"


class Database:
    def __init__(self, db_url):
        self.engine = create_async_engine(db_url, future=True)
        self.async_session = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )


class Base(DeclarativeBase):
    pass
