from pydantic import BaseModel
from typing import List

class IngestData(BaseModel):
    files: List[str]
    datasetId: str

class RetrieveData(BaseModel):
    query: str
    datasetId: str