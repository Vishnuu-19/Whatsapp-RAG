from sentence_transformers import SentenceTransformer
import chromadb

class Retriever:
    def __init__(self, collection_name: str, persist_dir: str , embedding_model: str = "all-MiniLM-L6-V2"):
        self.embedder = SentenceTransformer(embedding_model)
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_collection(collection_name)

    def search(self, semantic_query:str, sender_id: str=None, top_k=10):
        query_embedding = self.embedder.encode(semantic_query).tolist()

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        retrieved = []
        for doc,meta, dist in zip(documents, metadatas, distances):
            if sender_id and meta["sender_id"] !=sender_id:
                continue
            retrieved.append({
                "chunk_id":meta["chunk_id"],
                "sender_id": meta["sender_id"],
                "text": doc,
                "score": 1 - dist
            })

        return retrieved