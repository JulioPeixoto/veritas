from fastapi import APIRouter, File, UploadFile, Form
from src.schemas.docs_schema import DocsIndexingRequest
from src.services.docs_service import DocsService
from src.http.exceptions.docs_excpetions import InvalidFormatExceptionResponse
from fastapi import Query

docs_service = DocsService()

router = APIRouter(prefix="", tags=["Docs"])


@router.post(
    "/docs/indexing",
    status_code=204,
    responses={400: {"model": InvalidFormatExceptionResponse}},
)
async def indexa_documento_no_vector_store(
    file: UploadFile = File(...),
    name: str = Form(""),
    description: str = Form(""),
):
    request_data = DocsIndexingRequest(name=name, description=description)
    return await docs_service.indexa_documento(file, request_data)


@router.get(
    "/docs/search",
    status_code=200,
    responses={400: {"model": InvalidFormatExceptionResponse}},
)
async def search_docs(
    query: str = Query(...),
):
    return await docs_service.search_docs(query)