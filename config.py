from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import os
from sqlalchemy.orm import mapped_column, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from pgvector.sqlalchemy import Vector

connection_string = os.environ.get("DATABASE_URL")

engine = create_async_engine(
    connection_string, connect_args={"sslmode": "require"}, pool_recycle=300
)

Base = declarative_base()

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    dataset_id = Column(String)
    chunk = Column(String)
    embedding = mapped_column(Vector(1024))

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
