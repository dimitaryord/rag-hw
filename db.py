from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
import os

connection_string = os.environ.get("DATABASE_URL")

engine = create_async_engine(url=connection_string, pool_pre_ping=True, pool_size=5, pool_recycle=300, echo=True, connect_args={
    "sslmode": "require",
    "keepalives": 1,
    "keepalives_idle": 30,
    "keepalives_interval": 10,
    "keepalives_count": 5
})
Session = async_sessionmaker(bind=engine, expire_on_commit=False)

async def get_db():
    async with Session() as session:
        yield session

class Base(DeclarativeBase):
    pass
