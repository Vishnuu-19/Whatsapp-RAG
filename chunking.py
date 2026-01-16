import numpy as np
import json
from uuid import uuid4
from datetime import timedelta
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity

import os
os.environ["HF_HUB_OFFLINE"] = "1"
from sentence_transformers import SentenceTransformer
embedder = SentenceTransformer("all-MiniLm-L6-v2")
print("Loaded Model completely offline")

TIME_GAP_MINUTES = 30
SIM_THRESHOLD = 0.65
MAX_CHARS = 1500

def check_time_gap(prev_ts, curr_ts, minutes = TIME_GAP_MINUTES):
    return curr_ts-prev_ts>timedelta(minutes = minutes)

def cosine_sim(v1,v2):
    return cosine_similarity(v1.reshape(1,-1), v2.reshape(1,-1))[0][0]

def create_new_chunk(msg,embedding):
    return(
        {
            "chunk_id": str(uuid4()),
            "sender_id": msg["sender_id"],
            "start_time": msg["timestamp"],
            "end_time": msg["timestamp"],
            "message_ids": [msg["message_id"]],
            "texts": [msg["message"].strip()],
            "message_count": 1
        },
        [embedding]
    )

def finalize_chunk(chunk):
    return {
        "chunk_id": chunk["chunk_id"],
        "sender_id": chunk["sender_id"],
        "start_time": chunk["start_time"],
        "end_time": chunk["end_time"],
        "message_ids": chunk["message_ids"],
        "text": "\n".join(chunk["texts"]),
        "message_count": chunk["message_count"]
    }

def write_chunks_json(chunks, output_path: str):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok = True)

    chunks_copy = []
    for chunk in chunks:
        chunk_copy = chunk.copy()
        chunk_copy["start_time"] = chunk_copy["start_time"].isoformat()
        chunk_copy["end_time"] = chunk_copy["end_time"].isoformat()
        chunks_copy.append(chunk_copy)

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(chunks_copy, f, ensure_ascii=False, indent=2)

def create_chunks(messages):
    chunks = []
    current_chunk = None
    current_embedding = []

    for msg in messages:
        msg_text = msg["message"].strip()
        msg_ts = msg["timestamp"]
        msg_sender = msg["sender_id"]

        #embedding
        msg_embedding = embedder.encode( msg_text )

        if current_chunk is None:
            current_chunk = {
                "chunk_id": str(uuid4()),
                "sender_id": msg_sender,
                "start_time": msg_ts,
                "end_time": msg_ts,
                "message_ids": [msg["message_id"]],
                "texts": [msg_text],
                "message_count": 1
            }
            current_embedding = [msg_embedding]
            prev_msg_ts = msg_ts
            continue

        if ( 
            msg_sender != current_chunk["sender_id"] 
            or check_time_gap(prev_msg_ts, msg_ts) 
            or len("".join(current_chunk["texts"]))+ len(msg_text)>MAX_CHARS
        ):
            chunks.append(finalize_chunk(current_chunk))
            current_chunk,current_embedding = create_new_chunk(msg, msg_embedding)
            prev_msg_ts = msg_ts
            continue

        chunk_centroid = np.mean(current_embedding,axis = 0)
        similarity = cosine_sim(msg_embedding,chunk_centroid)

        if similarity< SIM_THRESHOLD:
            chunks.append(finalize_chunk(current_chunk))
            current_chunk,current_embedding = create_new_chunk(msg,msg_embedding)
        else:
            current_chunk["texts"].append(msg_text)
            current_chunk["message_ids"].append(msg["message_id"])
            current_chunk["message_count"]+=1
            current_chunk["end_time"] = msg_ts
            current_embedding.append(msg_embedding)

        prev_msg_ts = msg_ts
    
    if current_chunk:
        chunks.append(finalize_chunk(current_chunk))
    
    write_chunks_json(chunks, "data/chunks/chunks.json")
    
    return chunks

