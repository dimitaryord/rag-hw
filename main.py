from dotenv import load_dotenv
load_dotenv()

from PyPDF2 import PdfReader
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from schemas import IngestData, RetrieveData, DeleteData
from io import BytesIO
from sqlalchemy import select
from config import Session, Document
from utils import pdf_splitter, txt_splitter
import aiohttp
from embeddings import create_embedding, insert_chunks_to_documents

app = FastAPI()


@app.post("/ingest")
async def ingest(request: IngestData):
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
            case _:
                file_text = buffer.read().decode("utf-8")

        match file_extension:
            case "pdf":
                chunks = pdf_splitter.split_text(file_text)
            case _:
                chunks = txt_splitter.split_text(file_text)

        ingested_files += 1

        for i, chunk in enumerate(chunks):
            print(f"Chunk {i+1}:\n{chunk}\n")

        await insert_chunks_to_documents(chunks, request.datasetId)
        

    return JSONResponse(
        status_code=200,
        content={
            "message": "Files successfully ingested and stored in the vector database",
            "ingestedFiles": ingested_files,
            "datasetId": request.datasetId
        }
    )


@app.post("/retrieve")
async def retrieve(request: RetrieveData):
    embedding = create_embedding(request.query)

    async with Session() as session:
        k = 3
        similarity_threshold = 0.7
        query = (
            await session.scalars(
                select(Document)
                .where(Document.dataset_id == request.datasetId)
                .order_by(Document.embedding.cosine_distance(embedding.tolist()) < similarity_threshold)
                .limit(k)
            )
        )

        serialized_results = [
            {
                "chunk": document.chunk,
            }
            for document in query
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
async def delete(request: DeleteData):
    async with Session() as session:
        await session.execute(
            delete(Document)
            .where(Document.dataset_id == request.datasetId)
        )
        await session.commit()

    return JSONResponse(
        status_code=200,
        content={
            "message": "Dataset deleted successfully",
            "datasetId": request.datasetId
        }
    )