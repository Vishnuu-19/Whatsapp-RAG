import os
os.environ["HF_HUB_OFFLINE"] = "1"

from sentence_transformers import SentenceTransformer
SentenceTransformer("all-MiniLM-L6-v2")
print("LOADED COMPLETELY OFFLINE")