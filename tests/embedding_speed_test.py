import time
import random
from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"

# load model
print("Loading model...")
model = SentenceTransformer(MODEL_NAME)

# generate synthetic messages
NUM_MESSAGES = 10000
messages = [f"This is test message number {i}" for i in range(NUM_MESSAGES)]

print(f"\nTesting with {NUM_MESSAGES} messages\n")

# -------------------------
# Test 1: Individual encoding
# -------------------------
start = time.time()

embeddings = []
for msg in messages:
    emb = model.encode(msg)
    embeddings.append(emb)

end = time.time()

print("Individual encoding time:", round(end - start, 2), "seconds")


# -------------------------
# Test 2: Full batch encoding
# -------------------------
start = time.time()

embeddings = model.encode(messages)

end = time.time()

print("Full batch encoding time:", round(end - start, 2), "seconds")


# -------------------------
# Test 3: Custom batch sizes
# -------------------------
batch_sizes = [32, 64, 128, 256, 512, 1000]

for batch_size in batch_sizes:

    start = time.time()

    embeddings = []

    for i in range(0, len(messages), batch_size):
        batch = messages[i:i + batch_size]
        emb = model.encode(batch)
        embeddings.extend(emb)

    end = time.time()

    print(f"Batch size {batch_size}: {round(end - start, 2)} seconds")