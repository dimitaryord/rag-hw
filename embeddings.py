from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from models import Document
import numpy as np
import os

import aiohttp
import asyncio

API_URL = os.environ.get("EMBEDDING_API_URL")
headers = {
	"Accept" : "application/json",
	"Authorization": f"Bearer {os.environ.get('HUGGING_FACE_ACCESS_TOKEN')}",
	"Content-Type": "application/json" 
}

async def model_query(payload):
	async with aiohttp.ClientSession() as session:
		async with session.post(API_URL, headers=headers, json=payload) as response:
			return await response.json()

async def create_embedding(text: str):
	payload = {
		"inputs": text,
		"parameters": {}
	}
	
	embedding = await model_query(payload)
	embedding_array = np.array(embedding)
	if embedding_array.ndim > 1:
		embedding_array = embedding_array.flatten()
	return embedding_array


async def insert_chunks_to_documents(chunks, dataset_id, db: AsyncSession):
    batch_size = 100
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i+batch_size]
        documents = [
            Document(
                dataset_id=dataset_id,
                chunk=chunk,
                embedding=await create_embedding(chunk)
            )
            for chunk in batch
        ]
        db.add_all(documents)
        await db.flush()
    await db.commit()