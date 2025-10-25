from typing import Any, Dict

from fastapi import APIRouter, File, Form, HTTPException, Query, UploadFile

from src.api.exceptions.store_excpetions import InvalidFormatExceptionResponse
from src.schemas.store_schema import DocsIndexingRequest
from src.services.store_service import StoreService

store_service = StoreService()

router = APIRouter(prefix="", tags=["Store"])


@router.post(
    "/store/docs/indexing",
    status_code=204,
    responses={400: {"model": InvalidFormatExceptionResponse}},
)
async def index_document_in_vector_store(
    file: UploadFile = File(..., description="Arquivo para indexação"),
    name: str = Form("", description="Nome do documento"),
    description: str = Form("", description="Descrição do documento"),
):
    request_data = DocsIndexingRequest(name=name, description=description)
    result = await store_service.indexa_documento(file, request_data)
    return result


@router.get(
    "/store/docs/search",
    status_code=200,
    responses={400: {"model": InvalidFormatExceptionResponse}},
)
async def search_docs(
    query: str = Query(..., description="Texto de busca", min_length=1),
    limit: int = Query(5, description="Número máximo de resultados", ge=1, le=20),
):
    try:
        results = await store_service.search_docs(query, limit)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na busca: {str(e)}")


@router.get(
    "/store/docs/search/context",
    status_code=200,
    response_model=Dict[str, Any],
)
async def search_docs_with_context(
    query: str = Query(..., description="Texto de busca", min_length=1),
    limit: int = Query(5, description="Número máximo de resultados", ge=1, le=10),
):
    try:
        results = await store_service.search_docs_with_context(query, limit)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na busca: {str(e)}")
