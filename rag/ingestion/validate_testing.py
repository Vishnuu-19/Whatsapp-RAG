import chromadb
from chromadb.config import Settings

COLLECTION_NAME = "whatsapp_chunks"
PERSIST_DIR = "vector_store"

# client = chromadb.Client(
#     Settings(persist_directory = PERSIST_DIR)
# )
client = chromadb.PersistentClient(path=PERSIST_DIR)

collection = client.get_collection(COLLECTION_NAME)

print("Total vectors in DB:", collection.count())

results = collection.query(
    query_texts=["planing discussion"],
    n_results = 5
)

print("\nSample Retrieval Result: ")
for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
    print(meta["sender_id"], "->", doc)