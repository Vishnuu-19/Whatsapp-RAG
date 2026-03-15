import os
import time
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

    print(f"Ingestion started for {file_name}")
    start = time.time()
    print("parsing started")
    messages = parse_whatsapp_chat(file_path,file_name)
    print("Parsing time:", time.time() - start)

    start = time.time()
    print("chunking started")
    chunks = create_chunks(messages, file_name)
    print("Chunking time:", time.time() - start)

    texts = [chunk["text"] for chunk in chunks]

    start = time.time()
    print("embedding started")
    embeddings = embedder.encode(texts)
    print("Embedding time:", time.time() - start)

    metadatas = []
    ids = []

    for chunk in chunks:
        ids.append(chunk["chunk_id"])
        metadatas.append({
            "source": file_name,
            "chunk_id": chunk["chunk_id"],
            "sender_id": chunk["sender_id"],
            "start_time": chunk["start_time"].isoformat(),
            "end_time": chunk["end_time"].isoformat(),
            "message_count": chunk["message_count"]
        })

    vectordb = VectorDB(COLLECTION_NAME, PERSIST_DIR)

    start = time.time()
    print("inserting into vectordb")
    BATCH_SIZE = 2000

    for i in range(0, len(texts), BATCH_SIZE):
        batch_texts = texts[i:i+BATCH_SIZE]
        batch_ids = ids[i:i+BATCH_SIZE]
        batch_metadata = metadatas[i:i+BATCH_SIZE]

        batch_embeddings = embedder.encode(batch_texts)

        vectordb.upsert(
            ids=batch_ids,
            documents=batch_texts,
            embeddings=batch_embeddings,
            metadatas=batch_metadata
        )

    print("Vector insert time:", time.time() - start)
    
    add_source(file_name, len(chunks))

    return{
        "file": upload_file.filename,
        "chunks_added": len(chunks)
    }
