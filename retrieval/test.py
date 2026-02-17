from pipeline import pipeline

KNOWN_SENDERS = {
    "Sathi Pandu -600": "user_001",
    "Vishnu": "user_002"
}

# pipeline = Search(
#     known_senders=KNOWN_SENDERS,
#     collection_name="whatsapp_chunks",
#     persist_dir="vector_store"
# )

rag = pipeline(
    known_senders=KNOWN_SENDERS,
    collection_name="whatsapp_chunks",
    persist_dir="vector_store"
)

query = "What was discussed about gift?"

# response = pipeline.run(query, top_k=10)

# print("Parsed Query:")
# print(response["parsed_query"])

# print("\nRetrieved Chunks:")
# for r in response["results"]:
#     print(r["sender_id"], "->", r["text"])

result = rag.run(query,top_k=10)

print("\nAnswer\n")
print(result["answer"])
