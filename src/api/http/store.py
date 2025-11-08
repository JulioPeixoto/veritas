from typing import List

from fastapi import APIRouter, File, HTTPException, Query, UploadFile

from src.api.exceptions.store_excpetions import InvalidFormatExceptionResponse
from src.schemas.store_schema import (DocsIndexingResponse, SearchDocsResponse,
                                      SearchDocsWithContextResponse)
from src.services.store_service import StoreService

store_service = StoreService()

router = APIRouter(prefix="", tags=["Store"])


@router.post(
    "/store/docs/indexing",
    status_code=200,
    response_model=DocsIndexingResponse,
    responses={400: {"model": InvalidFormatExceptionResponse}},
)
async def index_documents_in_vector_store(
    files: List[UploadFile] = File(
        ..., description="Selecione múltiplos arquivos (Ctrl+Click ou Cmd+Click)"
    ),
):
    """
    Indexa múltiplos documentos no vector store, processando cada arquivo individualmente.

    Este endpoint recebe uma lista de arquivos e os processa um por um, gerando embeddings
    para cada documento e armazenando-os no vector store para busca por similaridade.
    O nome de cada documento é automaticamente extraído do nome do arquivo.

    **Como selecionar múltiplos arquivos:**
    - No Swagger UI: Clique em "Choose Files" e selecione múltiplos arquivos usando Ctrl+Click (Windows/Linux) ou Cmd+Click (Mac)
    - Via cURL: Use múltiplos parâmetros -F "files=@arquivo1.pdf" -F "files=@arquivo2.docx"
    - Via código: Envie uma lista de arquivos no campo 'files'

    Parâmetros:
        files (List[UploadFile]): Lista de arquivos para indexação (PDF, DOCX, TXT, HTML, MD).

    Retorna:
        DocsIndexingResponse: Estatísticas do processamento incluindo número de arquivos,
        chunks criados e caracteres processados.

    Exceções:
        HTTPException 400: Se algum arquivo tiver formato inválido.
        HTTPException 500: Para erros durante o processamento.

    Exemplo de uso:
        >>> POST /store/docs/indexing
        Files: [documento1.pdf, documento2.docx, documento3.txt]

        Resposta:
        {
            "processed_files": 3,
            "results": [...],
            "total_chunks": 45,
            "total_characters": 12500
        }
    """
    result = await store_service.indexa_documentos(files)
    return result


@router.get(
    "/store/docs/search",
    status_code=200,
    response_model=SearchDocsResponse,
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
    response_model=SearchDocsWithContextResponse,
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
