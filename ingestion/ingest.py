import json 
from embedder import Embedder
from vectordb import VectorDB

CHUNKS_PATH = "data/chunks/chunks.json"
COLLECTION_NAME = "whatsapp_chunks"
PERSIST_DIR = "../vector_store"
BATCH_SIZE = 64

def load_chunks(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
    
def normalize_text(text):
    return " ".join(text.strip().split())

def build_metadata(chunk):
    return{
        "chunk_id":chunk["chunk_id"],
        "sender_id": chunk["sender_id"],
        "start_time": chunk["start_time"],
        "end_time": chunk["end_time"],
        "message_count": chunk["message_count"]
    }

def batchify(data, batch_size):
    for i in range(0, len(data), batch_size):
        yield data[i:i+batch_size]

def main():
    chunks = load_chunks(CHUNKS_PATH)
    embedder = Embedder()
    vectordb = VectorDB(COLLECTION_NAME, PERSIST_DIR)

    for batch in batchify(chunks, BATCH_SIZE):
        texts = [normalize_text(c["text"]) for c in batch]
        ids = [c["chunk_id"] for c in batch]
        metadatas = [build_metadata(c) for c in batch]

        embeddings = embedder.encode(texts)

        vectordb.upsert(ids,texts, metadatas, embeddings)
    
    # vectordb.persist()
    print("Ingestion complete")
    print("Total vectors: ", vectordb.count())

if __name__=="__main__":
    main()