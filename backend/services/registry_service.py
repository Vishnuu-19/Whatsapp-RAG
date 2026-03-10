import json
import os
from datetime import datetime

REGISTRY_PATH = "backend/registry.json"

def load_registry():
    if not os.path.exists(REGISTRY_PATH):
        return []
    with open(REGISTRY_PATH, "r") as r:
        return json.load(r)
    
def save_registry(data):
    with open(REGISTRY_PATH, "w") as f:
        json.dump(data, f, indent=2)
    
def add_source(source_id, chunk_count):
    registry = load_registry()
    registry .append({
        "source_id": source_id,
        "upload_time": datetime.now().isoformat(),
        "chunk_count": chunk_count,
        "active": True
    })
    save_registry(registry)

def list_sources():
    return load_registry()

def deactivate_source(source_id):
    registry = load_registry()
    for item in registry:
        if item["source_id"] == source_id:
            item["active"]= False
    save_registry(registry)

def reactivate_source(source_id):
    registry = load_registry()
    for item in registry:
        if item["source_id"] == source_id:
            item["active"]= True
    save_registry(registry)

def delete_source(source_id):
    registry= load_registry()
    registry = [item for item in registry if item["source_id"]!=source_id]
    save_registry(registry)