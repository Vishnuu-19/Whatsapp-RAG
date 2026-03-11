import chromadb

# Path where your ChromaDB vector store is persisted
PERSIST_DIR = "vector_store"

# Connect to the database
client = chromadb.PersistentClient(path=PERSIST_DIR)

# Get all collections
collections = client.list_collections()

print("Collections in Vector DB:")
for col in collections:
    print("-", col.name)
    print(col.count())