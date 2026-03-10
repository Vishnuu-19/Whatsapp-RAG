from rag.ingestion.vectordb import VectorDB
from backend.services.source_service import (
    deactivate_source,
    reactivate_source,
    delete_source
)

vectordb = VectorDB()

def deactivate(source_id):
    deactivate_source(source_id)

def reactivate(source_id):
    reactivate_source(source_id)

def delete(source_id):
    vectordb.collection.delete( where={"source":source_id})

    delete_source(source_id)

    return {"deleted_source": source_id}