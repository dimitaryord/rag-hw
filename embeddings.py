import requests
import os

API_URL = os.environ.get("SFR_EMBEDDING_API_URL")
headers = {
	"Accept" : "application/json",
	"Authorization": f"Bearer {os.environ.get("HUGGING_FACE_ACCESS_TOKEN")}",
	"Content-Type": "application/json" 
}

def sfr_query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

def create_embedding(text: str):
	payload = {
		"inputs": text,
		"parameters": {}
	}
	
	return sfr_query(payload)
	
	