from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api import ingest, query, sources

app = FastAPI(title="Whatsapp RAG Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingest.router, prefix="/ingest", tags=["Ingest"])
app.include_router(query.router, prefix="/query",tags=["Query"])
app.include_router(sources.router, prefix="/sources",tags=["Sources"])