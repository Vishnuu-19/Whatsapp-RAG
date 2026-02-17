from typing import Dict, List

class QueryParser:
    def __init__(self,known_sender: Dict[str,str]):
        self.known_senders = known_sender

    def parse(self,query)-> Dict:
        query_lower=query.lower()

        detected_sender_id = None
        detected_sender_name = None

        for name, sender_id in self.known_senders.items():
            if name.lower() in query_lower:
                detected_sender_id = sender_id
                detected_sender_name = name
                break

        semantic_query = query
        if detected_sender_name:
            semantic_query = semantic_query.replace(detected_sender_name.lower(), "")

        semantic_query = semantic_query.strip()

        return {
            "original_query": query,
            "semantic_query": semantic_query,
            "sender_id": detected_sender_id,
            "sender_name": detected_sender_name
        }
    