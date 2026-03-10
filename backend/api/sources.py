from fastapi import APIRouter
from backend.services.registry_service import list_sources, delete_source,deactivate_source, reactivate_source

router = APIRouter()

@router.get("/")
def get_sources():
    return list_sources()

@router.post("/{source_id}/deactivate")
def deactivate(source_id:str):
    deactivate_source(source_id)
    return{"status": "deactivated"}

@router.post("/{source_id}/reactivate")
def reactivate(source_id:str):
    reactivate_source(source_id)
    return{"status": "reactivated"}

@router.delete("/{source_id}")
def remove_source(source_id: str):
    return delete_source(source_id)

