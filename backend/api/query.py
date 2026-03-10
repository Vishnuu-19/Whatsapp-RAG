from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from backend.services.query_service import run_query

router = APIRouter()

class QueryRequest(BaseModel):
    question:str
    sources:List[str]

@router.post("/")
def query(request: QueryRequest):
    answer = run_query(request.question, request.sources)
    return {"answer": answer}

