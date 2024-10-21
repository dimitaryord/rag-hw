from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
import os

connection_string = os.environ.get("DATABASE_URL")

engine = create_async_engine(connection_string, echo=True)
Session = async_sessionmaker(bind=engine, expire_on_commit=False)

async def get_db():
    async with Session() as session:
        yield session

class Base(DeclarativeBase):
    pass
