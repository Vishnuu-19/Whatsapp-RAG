from rag.retrieval.search import Search
from rag.retrieval.generator import AnswerGenerator

class pipeline:
    def __init__(self, known_senders, collection_name, persist_dir):
        
        self.search = Search(
            known_senders=known_senders,
            collection_name=collection_name,
            persist_dir=persist_dir
        )

        self.generator = AnswerGenerator()
    
    def run(self, user_query: str, sources=None, top_k = 10):
        retrieval_result = self.search.run(
            user_query= user_query,
            top_k=top_k,
            sources = sources
        )

        retrieved_chunks = retrieval_result["results"]

        answer = self.generator.generate(
            user_query=user_query,
            retrieved_chunks=retrieved_chunks
        )

        return{
            "parsed_query": retrieval_result["parsed_query"],
            "retrieved_chunks": retrieved_chunks,
            "answer":answer
        }