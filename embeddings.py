from config import Session, Document
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


async def insert_chunks_to_documents(chunks: list[str], dataset_id: str):
	async with Session() as session:
		tasks = []
		for chunk in chunks:
			tasks.append(asyncio.create_task(process_chunks(chunk, dataset_id, session)))
			
		await asyncio.gather(*tasks)
		await session.commit()
			

async def process_chunks(chunk: str, dataset_id: str, session):
	embedding = await create_embedding(chunk)
	document = Document(chunk=chunk, embedding=embedding, dataset_id=dataset_id)
	session.add(document)
