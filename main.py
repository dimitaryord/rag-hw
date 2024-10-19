from dotenv import load_dotenv
load_dotenv()

from PyPDF2 import PdfReader
from fastapi import FastAPI
from schemas import IngestData, RetrieveData
from io import BytesIO
from sqlalchemy import create_engine, Column, Integer, String, desc, func, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, mapped_column
from pgvector.sqlalchemy import Vector
from langchain_text_splitters import RecursiveCharacterTextSplitter, TokenTextSplitter
import requests
import os
from embeddings import create_embedding
import numpy as np

connection_string = os.environ.get("DATABASE_URL")

Base = declarative_base()

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    dataset_id = Column(String)
    chunk = Column(String)
    embedding = mapped_column(Vector(1024))

engine = create_engine(
    connection_string, connect_args={"sslmode": "require"}, pool_recycle=300
)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

app = FastAPI()

pdf_separators = [
    "\n\n",
    "\n- ",
    "\n* ",
    "\n• ",
    "\n1. ",
    "\n",
    " ",
    ""
]
pdf_splitter = RecursiveCharacterTextSplitter(separators=pdf_separators, chunk_size=1000, chunk_overlap=200)


@app.post("/ingest")
async def ingest(request: IngestData):
    for file in request.files:
        file_text = ""

        response = requests.get(file)
        buffer = BytesIO(response.content)
        buffer.seek(0)

        pdf_reader = PdfReader(buffer)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            file_text += text + "\n"

        chunks = pdf_splitter.split_text(file_text)

        for i, chunk in enumerate(chunks):
            print(f"Chunk {i+1}:\n{chunk}\n")

        with Session() as session:
            for chunk in chunks:
                embedding = create_embedding(chunk)
                embedding_array = np.array(embedding)
                print(embedding_array.ndim)

                if embedding_array.ndim > 1:
                    embedding_array = embedding_array.flatten()
                document = Document(dataset_id=request.datasetId, chunk=chunk, embedding=embedding_array)
                session.add(document)
            session.commit()
        

    return {"message": "Ingested successfully"}


@app.post("/retrieve")
async def retrieve(request: RetrieveData):
    embedding = create_embedding(request.query)
    embedding_array = np.array(embedding)
    if embedding_array.ndim > 1:
        embedding_array = embedding_array.flatten()

    with Session() as session:
        k = 3
        query = (
            session.scalars(
                select(Document)
                .where(Document.dataset_id == request.datasetId)
                .order_by(Document.embedding.cosine_distance(embedding_array.tolist()))
                .limit(k)
            ).all()
        )

        serialized_results = [
            {
                "id": document.id,
                "dataset_id": document.dataset_id,
                "chunk": document.chunk,
            }
            for document in query
        ]
        return { "message": "Retrieved successfully", "results": serialized_results }