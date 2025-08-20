from fastapi import APIRouter
from fastapi.datastructures import UploadFile

router = APIRouter(prefix="", tags=["Vector Store"])

@router.post("/vector_store")
async def adiciona_documento(file: UploadFile):
    return {"message": "Hello, World!"}