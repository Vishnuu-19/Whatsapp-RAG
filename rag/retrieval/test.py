from .pipeline import pipeline
import time

import os
os.environ['PYTHONIOENCODING'] = 'utf-8'

KNOWN_SENDERS = {
    "M Vishnu Vardhan": "user_001",
    "Madhu": "user_002"
}

# ============ CHECKPOINT 1: Initialize Pipeline ============
print("=" * 60)
print("CHECKPOINT 1: Initializing RAG Pipeline...")
print("=" * 60)
start_init = time.time()

rag = pipeline(
    known_senders=KNOWN_SENDERS,
    collection_name="whatsapp_chunks",
    persist_dir="vector_store"
)

init_time = time.time() - start_init
print(f"✓ Pipeline initialized in {init_time:.2f}s\n")

# ============ CHECKPOINT 2: Query Setup ============
query = "What was discussed about model?"
print("=" * 60)
print("CHECKPOINT 2: Query Setup")
print("=" * 60)
print(f"Query: '{query}'")
print("=" * 60)
print()

# ============ CHECKPOINT 3: Running RAG Pipeline ============
print("=" * 60)
print("CHECKPOINT 3: Running RAG Pipeline (Retrieval + Generation)...")
print("=" * 60)
start_total = time.time()

result = rag.run(query, top_k=10,sources)

total_time = time.time() - start_total
print(f"✓ RAG Pipeline completed in {total_time:.2f}s\n")

# ============ CHECKPOINT 4: Display Results ============
print("=" * 60)
print("CHECKPOINT 4: Results")
print("=" * 60)
print(f"\nParsed Query: {result['parsed_query']}\n")

print(f"Retrieved {len(result['retrieved_chunks'])} chunks:")
for i, chunk in enumerate(result['retrieved_chunks'], 1):
    print(f"  {i}. [{chunk.get('sender_id', 'Unknown')}]: {chunk.get('text', '')[:60]}...")

print("\nFinal Answer:")
print("-" * 60)
print(result["answer"])
print("-" * 60)

# ============ TIMING SUMMARY ============
print("\n" + "=" * 60)
print("TIMING SUMMARY")
print("=" * 60)
print(f"Pipeline Initialization: {init_time:.2f}s")
print(f"RAG Query Execution:     {total_time:.2f}s")
print(f"Total Time:              {init_time + total_time:.2f}s")
print("=" * 60)
