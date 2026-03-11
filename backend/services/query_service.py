import json
from rag.retrieval.pipeline import pipeline

COLLECTION_NAME = "whatsapp_chunks"
PERSIST_DIR = "vector_store"
with open("data/processed/sender_map.json", "r", encoding="utf-8") as f:
    KNOWN_SENDERS = json.load(f)

rag_pipeline = pipeline(
    known_senders=KNOWN_SENDERS,
    collection_name=COLLECTION_NAME,
    persist_dir=PERSIST_DIR
)

def run_query(question, sources):
    result = rag_pipeline.run(
        user_query=question,
        sources= sources,
        top_k = 5
    )

    return{
        "parsed_query": result["parsed_query"],
        "answer": result["answer"],
        "retrieved_chunks":result["retrieved_chunks"]
    }