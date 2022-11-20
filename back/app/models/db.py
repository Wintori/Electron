from typing import AsyncIterator

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import DeclarativeMeta

from back.config.settings import Settings
from back.lib.db_acessor import DatabaseAccessor

Base: DeclarativeMeta = declarative_base()

settings = Settings()
database_accessor = DatabaseAccessor(db_settings=settings.db_settings)


async def get_async_session() -> AsyncIterator[AsyncSession]:
    async with database_accessor.get_session() as session:
        yield session


def init_db(engine) -> None:
    Base.metadata.create_all(bind=engine)
