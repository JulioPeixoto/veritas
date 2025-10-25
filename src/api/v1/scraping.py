from fastapi import APIRouter, Query

from src.schemas.scraping_schema import (
    DeleteFileResponse,
    EtlResponse,
    ListFilesResponse,
    SearchLinksResponse,
)
from src.services.scraping_service import ScrapingService

router = APIRouter(prefix="", tags=["Scraping"])
service = ScrapingService()


@router.post("/scraping/urls", status_code=200, response_model=SearchLinksResponse)
async def scraping_urls(
    query: str = Query(..., min_length=1, description="Termo de busca"),
    limit: int = Query(
        10, ge=1, le=100, description="Quantidade máxima de links a coletar (1–100)"
    ),
    gl: str = Query("br", description="Código de país (gl), ex: br, us"),
    hl: str = Query("pt", description="Idioma (hl), ex: pt, en"),
    engine: str = Query(
        "google_news", description="Engine do SerpAPI; use google_news para notícias"
    ),
    when: str | None = Query(None, description="Janela de tempo, ex: 24h, 7d"),
):
    """
    Busca e armazena URLs de notícias relacionadas ao termo informado, utilizando SerpAPI.

    Este endpoint consulta a SerpAPI (usando o mecanismo definido em 'engine', por padrão 'google_news'),
    coletando links de notícias relevantes conforme critérios definidos pelos parâmetros. Os links encontrados
    são salvos em um arquivo CSV na pasta 'data/'.

    Parâmetros:
        query (str): Termo de busca para pesquisar notícias.
        limit (int): Quantidade máxima de links a coletar (1-100).
        gl (str): País dos resultados (ex.: 'br', 'us').
        hl (str): Idioma dos resultados (ex.: 'pt', 'en').
        engine (str): Motor de busca na SerpAPI; 'google_news' (padrão).
        when (str | None): Intervalo de tempo opcional (ex: '24h', '7d').

    Retorno:
        SearchLinksResponse: Dicionário com:
            - filename (str): Nome do arquivo CSV salvo.
            - total_links (int): Total de links coletados.
            - path (str): Caminho completo do CSV salvo.

    Exceções:
        HTTPException 400: Se parâmetros obrigatórios forem inválidos (query ou limit).
        HTTPException 404: Se nenhum link for encontrado.
        Exception: Para falhas inesperadas na requisição ou escrita de arquivos.

    Exemplo de uso:
        >>> POST /scraping/urls
            {{
                "query": "inteligência artificial",
                "limit": 10,
                "gl": "br",
                "hl": "pt",
                "engine": "google_news"
            }}
        Resposta:
            {{
                "filename": "links_inteligencia_artificial_20251025_203010.csv",
                "total_links": 10,
                "path": "data/links_inteligencia_artificial_20251025_203010.csv"
            }}
    """
    result = service.search_links(
        query=query, limit=limit, gl=gl, hl=hl, engine=engine, when=when
    )
    return result


@router.post("/scraping/etl", status_code=200, response_model=EtlResponse)
async def scraping_etl(
    filename: str = Query(
        ..., description="Nome do CSV gerado pela busca, localizado em data/"
    )
):
    """
    Executa ETL (Extract, Transform, Load) sobre arquivo CSV gerado pelo scraping.

    Este endpoint processa o arquivo CSV informado, realizando etapas de extração, transformação e carregamento dos dados,
    retornando estatísticas e status do processamento.

    Parâmetros:
        filename (str): Nome do arquivo CSV disponível em data/.

    Retorna:
        dict: Dicionário com informações do ETL como número de registros processados, erros, e status final.

    Exceções:
        FileNotFoundError: Se o arquivo não existir.
        ValueError: Se o formato estiver inválido.
        Exception: Para erros no processamento.

    Exemplo de uso:
        >>> POST /scraping/etl?filename=meuarquivo.csv
        Resposta: {{ "status": "concluído", "registrosProcessados": 200 }}
    """
    return service.etl(filename)


@router.get("/scraping/files", status_code=200, response_model=ListFilesResponse)
async def list_files(
    kind: str = Query(
        "all",
        description="Tipo de listagem: links (data/), scraped (data/scraping/search/) ou all",
    )
):
    """
    Lista arquivos de scraping disponíveis para consulta ou processamento.

    Permite listar arquivos gerados pelo processo de scraping, podendo filtrar por tipos.

    Parâmetros:
        kind (str): Define tipo da listagem: 'links', 'scraped' ou 'all'.

    Retorna:
        ListFilesResponse: Modelo contendo nomes e tipos de arquivos existentes.

    Exceções:
        ValueError: Se o tipo informado não existir.

    Exemplo de uso:
        >>> GET /scraping/files?kind=scraped
        Resposta: {{ "arquivos": ["arquivo1.csv", "arquivo2.csv"] }}
    """
    return service.list_files(kind)


@router.delete("/scraping/files", status_code=200, response_model=DeleteFileResponse)
async def delete_file(
    kind: str = Query(..., description="Categoria do arquivo: links ou scraped"),
    filename: str = Query(..., description="Nome do arquivo a remover (apenas nome)"),
):
    """
    Remove arquivo específico gerado pelo scraping.

    Permite excluir um arquivo de resultados brutos (links) ou de dados processados (scraped).

    Parâmetros:
        kind (str): Categoria do arquivo ('links' ou 'scraped').
        filename (str): Nome do arquivo a ser removido (apenas nome, sem path).

    Retorna:
        DeleteFileResponse: Modelo indicando sucesso ou falha na remoção.

    Exceções:
        FileNotFoundError: Se o arquivo não for encontrado.
        Exception: Para erros na exclusão do arquivo.

    Exemplo de uso:
        >>> DELETE /scraping/files?kind=links&filename=antigo.csv
        Resposta: {{ "status": "removido" }}
    """
    return service.delete_file(kind, filename)
