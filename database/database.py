from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config import get_settings

settings = get_settings()

engine = create_async_engine(settings.database_url, echo=False)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)
