import os
from rag.chunking.preprocessing import parse_whatsapp_chat
from rag.chunking.chunking import create_chunks
from rag.ingestion.embedder import Embedder
from rag.ingestion.vectordb import VectorDB
from backend.services.registry_service import add_source
from pathlib import Path

RAW_DIR = "data/raw"
COLLECTION_NAME = "whatsapp_chunks"
PERSIST_DIR = "vector_store"

embedder = Embedder()

async def ingest_file(upload_file):
    os.makedirs(RAW_DIR, exist_ok=True)

    file_path = os.path.join(RAW_DIR, upload_file.filename)

    with open(file_path, "wb") as f:
        f.write(await upload_file.read())
    
    file_name = Path(file_path).stem

    messages = parse_whatsapp_chat(file_path,file_name)

    chunks = create_chunks(messages, file_name)

    texts = [chunk["text"] for chunk in chunks]
    embeddings = embedder.encode(texts)

    metadatas = []
    ids = []

    for chunk in chunks:
        ids.append(chunk["chunk_id"])
        metadatas.append({
            "source": upload_file.filename,
            "chunk_id": chunk["chunk_id"],
            "sender_id": chunk["sender_id"],
            "start_time": chunk["start_time"],
            "end_time": chunk["end_time"],
            "message_count": chunk["message_count"]
        })

    vectordb = VectorDB(COLLECTION_NAME, PERSIST_DIR)

    vectordb.upsert(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas
    )
    
    add_source(upload_file.filename, len(chunks))

    return{
        "file": upload_file.filename,
        "chunks_added": len(chunks)
    }
