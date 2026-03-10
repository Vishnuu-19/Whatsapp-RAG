from rag.retrieval.pipeline import pipeline

COLLECTION_NAME = "whatsapp_chunks"
PERSIST_DIR = "vector_store"
KNOWN_SENDERS = "data/processed/sender_map.json"

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
        "chunks":result["chunks"]
    }