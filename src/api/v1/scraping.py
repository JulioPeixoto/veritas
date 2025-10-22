from typing import Dict

from fastapi import APIRouter, Query

from src.services.scraping_service import ScrapingService
from src.schemas.scraping_schema import (
    DeleteFileResponse,
    EtlResponse,
    ListFilesResponse,
    SearchLinksResponse,
)

router = APIRouter(prefix="", tags=["Scraping"])
service = ScrapingService()


@router.post("/scraping/search", status_code=200, response_model=SearchLinksResponse)
async def scraping_search(
    query: str = Query(..., min_length=1, description="Termo de busca"),
    limit: int = Query(10, ge=1, le=100, description="Quantidade máxima de links a coletar (1–100)"),
    gl: str = Query("br", description="Código de país (gl), ex: br, us"),
    hl: str = Query("pt", description="Idioma (hl), ex: pt, en"),
    engine: str = Query("google_news", description="Engine do SerpAPI; use google_news para notícias"),
    when: str | None = Query(None, description="Janela de tempo, ex: 24h, 7d"),
):
    result = service.search_links(query=query, limit=limit, gl=gl, hl=hl, engine=engine, when=when)
    return result


@router.post("/scraping/etl", status_code=200, response_model=EtlResponse)
async def scraping_etl(
    filename: str = Query(..., description="Nome do CSV gerado pela busca, localizado em data/")
) -> Dict[str, str | int]:
    return service.etl(filename)


@router.get("/scraping/files", status_code=200, response_model=ListFilesResponse)
async def list_files(
    kind: str = Query("all", description="Tipo de listagem: links (data/), scraped (data/scraping/search/) ou all")
):
    return service.list_files(kind)


@router.delete("/scraping/files", status_code=200, response_model=DeleteFileResponse)
async def delete_file(
    kind: str = Query(..., description="Categoria do arquivo: links ou scraped"),
    filename: str = Query(..., description="Nome do arquivo a remover (apenas nome)"),
):
    return service.delete_file(kind, filename)
