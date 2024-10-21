from dotenv import load_dotenv
load_dotenv()

from PyPDF2 import PdfReader
from docx import Document as DocxDocument
import json
import pandas as pd
import mammoth
from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from schemas import IngestData, RetrieveData, DeleteData
from io import BytesIO
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
from models import Document
from utils import pdf_splitter, txt_splitter, md_splitter, json_splitter
import aiohttp
from embeddings import create_embedding, insert_chunks_to_documents
import os

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

from fastapi import HTTPException, Request

async def verify_token(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return JSONResponse(status_code=401, content={"detail": "Invalid or missing Authorization header"})
    token = auth_header.split(" ")[1]
    if token != ACCESS_TOKEN:
        return JSONResponse(status_code=401, content={"detail": "Invalid access token"})

app = FastAPI()

@app.middleware("http")
async def authentication_middleware(request: Request, call_next):
    if request.url.path not in ["/docs", "/openapi.json"]:
        await verify_token(request)
    response = await call_next(request)
    return response

@app.post("/ingest")
async def ingest(request: IngestData, db: AsyncSession = Depends(get_db)):
    ingested_files = 0

    for file in request.files:
        file_text = ""
        file_extension = file.split(".")[-1]


        async with aiohttp.ClientSession() as aio_session:
            async with aio_session.get(file) as response:
                content = await response.read()
                buffer = BytesIO(content)
                buffer.seek(0)

        match file_extension:
            case "pdf":
                pdf_reader = PdfReader(buffer)
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text = page.extract_text()
                    file_text += text + "\n"
            case "docx":
                docx_reader = DocxDocument(buffer)
                for paragraph in docx_reader.paragraphs:
                    file_text += paragraph.text + "\n"
            case "doc":
                result = mammoth.convert_to_markdown(buffer)
                file_text = result.value
            case "csv":
                df = pd.read_csv(buffer)
                file_text = df.to_string()
            case "json":
                json_data = json.load(buffer)
                file_text = json.dumps(json_data, indent=2)
            case _:
                file_text = buffer.read().decode("utf-8")

        match file_extension:
            case "pdf":
                chunks = pdf_splitter.split_text(file_text)
            case "docx":
                chunks = pdf_splitter.split_text(file_text)
            case "doc":
                chunks = md_splitter.split_text(file_text)
            case "json":
                chunks = json_splitter.split_text(file_text)
            case _:
                chunks = txt_splitter.split_text(file_text)

        ingested_files += 1

        await insert_chunks_to_documents(chunks, request.datasetId, db)
        

    return JSONResponse(
        status_code=200,
        content={
            "message": "Files successfully ingested and stored in the vector database",
            "ingestedFiles": ingested_files,
            "datasetId": request.datasetId
        }
    )


@app.post("/retrieve")
async def retrieve(request: RetrieveData, db: AsyncSession = Depends(get_db)):
    embedding = await create_embedding(request.prompt)
    print(f"Embedding: {embedding}")

    k = 3
    query = (
        select(Document)
        .where(Document.dataset_id == request.datasetId)
        .order_by(Document.embedding.cosine_distance(embedding.tolist()))
        .limit(k)
    )

    results = await db.execute(query)
    documents = results.scalars().all()

    serialized_results = [
        {
            "chunk": document.chunk,
        }
        for document in documents
    ]

    return JSONResponse(
        status_code=200,
        content={
            "prompt": request.prompt,
            "datasetId": request.datasetId,
            "results": serialized_results
        }
    )


@app.delete("/delete")
async def delete(request: DeleteData, db: AsyncSession = Depends(get_db)):
    await db.execute(
        delete(Document)
        .where(Document.dataset_id == request.datasetId)
    )
    await db.commit()

    return JSONResponse(
        status_code=200,
        content={
            "message": "Dataset deleted successfully",
            "datasetId": request.datasetId
        }
    )