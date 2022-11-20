from collections import OrderedDict
from contextlib import asynccontextmanager
from re import compile
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool


class DatabaseAccessor:
    DEFAULT_ACQUIRE_TIMEOUT: float = 1
    DEFAULT_REFRESH_DELAY: float = 1
    DEFAULT_REFRESH_TIMEOUT: float = 5
    DEFAULT_MASTER_AS_REPLICA_WEIGHT: float = 0.0
    DEFAULT_STOPWATCH_WINDOW_SIZE: int = 128
    SEARCH_HOST_REGEXP = compile(r'host=(.+?)\s')

    def __init__(self, db_settings: dict, statement_cache_size: int = 0):
        self._db_settings = db_settings
        self._dsn = f'postgresql+asyncpg://{self._db_settings.db_user}:{self._db_settings.db_password}' \
                    f'@{self._db_settings.db_url}:{self._db_settings.db_port}/{self._db_settings.db_name}'
        self._session_makers = OrderedDict()
        self._statement_cache_size = statement_cache_size
        self._async_session_maker = None

    async def run(self) -> None:
        await self._set_engine()

    async def _set_engine(self) -> None:
        self._engine = create_async_engine(
            self._dsn,
            pool_pre_ping=True,
            pool_size=self._db_settings.db_pool_size,
            max_overflow=self._db_settings.db_max_overflow,
            # poolclass=NullPool,
            future=True,
            echo=True
        )

    async def init_db(self, Base) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    def _create_session(self) -> None:
        self._async_session_maker = sessionmaker(bind=self._engine, expire_on_commit=False, class_=AsyncSession)

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        self._create_session()
        async with self._async_session_maker() as session:
            yield session

    async def stop(self) -> None:
        await self._engine.dispose()