from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from .models import SQLModel

db_filename = "fastapi_1.db"
sqlite_url = f"sqlite+aiosqlite:///src/{db_filename}"

connect_args = {"check_same_thread": False}

engine = create_async_engine(
    url=sqlite_url, connect_args=connect_args, echo=True, future=True
)

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
