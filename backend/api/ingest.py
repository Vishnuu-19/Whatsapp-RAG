from fastapi import APIRouter, UploadFile, File
from typing import List
from backend.services.ingestion_service import ingest_file

router = APIRouter()

@router.post("/")
async def ingest(files: List[UploadFile] = File(..., description="Upload WhatsApp chat files")):
    
    results = []

    for file in files:
        result = await ingest_file(file)
        results.append(result)

    return {"status": "completed", "results": results}