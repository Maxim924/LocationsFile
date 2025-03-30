from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from settings import settings

async_engine = create_async_engine(settings.ASYNC_DATABASE_URL, pool_recycle=3600)
async_session = async_sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

async def async_get_session():
    session = async_session()
    try:
        yield session
    finally:
        await session.close()

#Сессия для тестов
engine = create_engine(settings.DATABASE_URL, pool_size=100, max_overflow=0)
Session = sessionmaker(
    engine,
    autocommit=False,
    autoflush=False,
)
def get_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()

Base = declarative_base()
metadata = MetaData(schema="public")
