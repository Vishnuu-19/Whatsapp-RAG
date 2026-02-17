from query_parser import QueryParser
from retriever import Retriever

class Search:
    def __init__(self, known_senders, collection_name, persist_dir):
        self.parser = QueryParser(known_senders)
        self.retriever = Retriever(
            collection_name = collection_name,
            persist_dir = persist_dir
        )

    def run(self, user_query: str, top_k: int=10):
        parsed= self.parser.parse(user_query)
        results = self.retriever.search(
            semantic_query=parsed["semantic_query"],
            sender_id=parsed["sender_id"],
            top_k=top_k
        )
    
        return {
            "parsed_query": parsed,
            "results": results
        }