from typing import List

from pydantic import BaseModel, Field


class SearchLinksResponse(BaseModel):
    filename: str = Field(..., description="Nome do CSV salvo em data/")
    total_links: int = Field(..., description="Quantidade de links coletados")
    path: str = Field(..., description="Caminho completo do arquivo gerado")


class EtlResponse(BaseModel):
    filename: str = Field(..., description="Arquivo de entrada em data/")
    processed: int = Field(..., description="Total de links lidos do CSV")
    output_dir: str = Field(..., description="Diretório onde os CSVs por artigo são salvos")


class FileItem(BaseModel):
    name: str = Field(..., description="Nome do arquivo")
    size: int = Field(..., description="Tamanho em bytes")
    modified: str = Field(..., description="Data/hora da última modificação em ISO8601")
    path: str = Field(..., description="Caminho completo do arquivo")


class ListFilesResponse(BaseModel):
    links: List[FileItem] = Field(default_factory=list, description="Arquivos em data/")
    scraped: List[FileItem] = Field(default_factory=list, description="Arquivos em data/scraping/search/")


class DeleteFileResponse(BaseModel):
    deleted: str = Field(..., description="Arquivo removido")
    kind: str = Field(..., description="Categoria: links ou scraped")

