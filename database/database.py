import contextlib
from pathlib import Path
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from sqlalchemy.sql import Select
from sqlalchemy.engine import ChunkedIteratorResult

try:
    from utils.decorators import utils
    from settings.config import config
    from loggers.logger import logger
    from database.models import Base, User, UserSchema
except ImportError as ie:
    exit(f'{ie} :: {Path(__file__).resolve()}')


class Database:
    def __init__(self):
        self._engine: AsyncEngine = create_async_engine(
            url=config.DB_CONNECT['postgres'].format(user=config.DB_USER, password=config.DB_PASS)
        )
        self.session_factory: sessionmaker[AsyncSession] = sessionmaker(
            bind=self._engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    @contextlib.asynccontextmanager
    async def init(self, _: FastAPI) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        yield
        await self._engine.dispose()

    @contextlib.asynccontextmanager
    async def get_session(self) -> AsyncSession:
        async with self.session_factory() as session:
            try:
                yield session
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()

    @utils.async_exception
    async def get_user(self, email: str) -> UserSchema:
        async with self.get_session() as session:
            query: Select = select(User).filter_by(email=email)
            result: ChunkedIteratorResult = await session.execute(statement=query)
            user = result.scalars().first()
            return UserSchema.model_validate(user) if user else None

    @utils.async_exception
    async def add_user(self, email: str, password: str = None) -> int:
        async with self.get_session() as session:
            new_user: User = User(email=email)

            if password:
                new_user.password = password

            session.add(new_user)
            await session.commit()
            return new_user.id


db: Database = Database()
