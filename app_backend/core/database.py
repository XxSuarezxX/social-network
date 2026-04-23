from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from core.config import settings

class Base(DeclarativeBase):
    pass

engine = create_async_engine(settings.database_url, future=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_db():
    db = async_session()
    try:
        yield db
    finally:
        await db.close()