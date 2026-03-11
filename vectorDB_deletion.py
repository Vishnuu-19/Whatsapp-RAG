import chromadb

PERSIST_DIR = "vector_store"
COLLECTION_NAME = "whatsapp_chunks"

client = chromadb.PersistentClient(path=PERSIST_DIR)

try:
    client.delete_collection(COLLECTION_NAME)
    print(f"Collection '{COLLECTION_NAME}' deleted successfully.")
except Exception as e:
    print("Error deleting collection:", e)

# recreate empty collection so the system can run again
client.get_or_create_collection(name=COLLECTION_NAME)

print("Empty collection recreated.")