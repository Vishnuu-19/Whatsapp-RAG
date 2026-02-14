import chromadb
from chromadb.config import Settings

class VectorDB:
    def __init__(self, collection_name, persist_dir):
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection(name=collection_name)

    def upsert(self, ids, documents, metadatas, embeddings):
        self.collection.upsert(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=embeddings
        )
    
    def count(self):
        return self.collection.count()
    
    # def persist(self):
    #     self.client.persist()