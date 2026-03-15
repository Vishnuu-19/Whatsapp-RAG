# import json
# import os
# from datetime import datetime

# REGISTRY_PATH = "backend/registry.json"

# def load_registry():
#     if not os.path.exists(REGISTRY_PATH):
#         return []
#     with open(REGISTRY_PATH, "r") as r:
#         return json.load(r)
    
# def save_registry(data):
#     with open(REGISTRY_PATH, "w") as f:
#         json.dump(data, f, indent=2)
    
# def add_source(source_id, chunk_count):
#     registry = load_registry()
#     registry .append({
#         "source_id": source_id,
#         "upload_time": datetime.now().isoformat(),
#         "chunk_count": chunk_count,
#         "active": True
#     })
#     save_registry(registry)

# def list_sources():
#     return load_registry()

# def deactivate_source(source_id):
#     registry = load_registry()
#     for item in registry:
#         if item["source_id"] == source_id:
#             item["active"]= False
#     save_registry(registry)

# def reactivate_source(source_id):
#     registry = load_registry()
#     for item in registry:
#         if item["source_id"] == source_id:
#             item["active"]= True
#     save_registry(registry)

# def delete_source(source_id):
#     registry= load_registry()
#     registry = [item for item in registry if item["source_id"]!=source_id]
#     save_registry(registry)

from datetime import datetime
from backend.services.db import get_connection

def load_registry():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("select * from sources")
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]

def add_source(source_id, chunk_count):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO sources
        (source_id, chunk_count, active, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (
            source_id,
            chunk_count,
            1,
            datetime.now().isoformat(),
        ),
    )
    conn.commit()
    conn.close()

def list_sources():
    return load_registry()

def deactivate_source(source_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "update sources set active=0 where source_id = ?",
        (source_id,),
    )
    conn.commit()
    conn.close()

def reactivate_source(source_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "update sources set active=1 where source_id = ?",
        (source_id,),
    )
    conn.commit()
    conn.close()

def delete_source(source_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "delete from sources where source_id = ?",
        (source_id,),
    )
    conn.commit()
    conn.close()