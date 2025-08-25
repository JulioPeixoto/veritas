from fastapi import APIRouter, File, UploadFile, Form, Query, HTTPException
from src.schemas.docs_schema import DocsIndexingRequest
from src.services.docs_service import DocsService
from src.http.exceptions.docs_excpetions import InvalidFormatExceptionResponse
from typing import List, Dict, Any

docs_service = DocsService()

router = APIRouter(prefix="", tags=["Docs"])

@router.post(
    "/docs/indexing",
    status_code=204,
    responses={400: {"model": InvalidFormatExceptionResponse}},
)
async def indexa_documento_no_vector_store(
    file: UploadFile = File(..., description="Arquivo para indexação"),
    name: str = Form("", description="Nome do documento"),
    description: str = Form("", description="Descrição do documento"),
):
    request_data = DocsIndexingRequest(name=name, description=description)
    result = await docs_service.indexa_documento(file, request_data)
    return result


@router.get(
    "/docs/search",
    status_code=200,
    responses={400: {"model": InvalidFormatExceptionResponse}},
)
async def search_docs(
    query: str = Query(..., description="Texto de busca", min_length=1),
    limit: int = Query(5, description="Número máximo de resultados", ge=1, le=20),
):
    try:
        results = await docs_service.search_docs(query, limit)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na busca: {str(e)}")


@router.get(
    "/docs/search/context",
    status_code=200,
    response_model=Dict[str, Any],
)
async def search_docs_with_context(
    query: str = Query(..., description="Texto de busca", min_length=1),
    limit: int = Query(5, description="Número máximo de resultados", ge=1, le=10),
):
    try:
        results = await docs_service.search_docs_with_context(query, limit)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na busca: {str(e)}")