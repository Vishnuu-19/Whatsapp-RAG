# import json
from rag.retrieval.pipeline import pipeline
from backend.services.registry_service import list_sources


# # load registry
# with open("backend/registry.json") as f:
#     registry = json.load(f)

registry = list_sources()

active_sources = [
    item["source_id"]
    for item in registry
    if item["active"] == 1
]

print("Active sources:", active_sources)

rag = pipeline(
    known_senders={},
    collection_name="whatsapp_chunks",
    persist_dir="vector_store"
)

result = rag.run(
    user_query="",
    sources=active_sources
)

print(result["retrieved_chunks"])