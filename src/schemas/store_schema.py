from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class DocsType(str, Enum):
    PDF = "pdf"
    DOCX = "docx"
    TXT = "txt"
    HTML = "html"
    MD = "md"


class DocumentIndexResult(BaseModel):
    message: str
    filename: str
    document_name: str
    file_type: str
    chunks_created: int
    characters_processed: int
    chunk_size_used: int
    preview: str


class DocsIndexingResponse(BaseModel):
    processed_files: int
    results: List[DocumentIndexResult]
    total_chunks: int
    total_characters: int
    errors: Optional[List[str]] = None


class SearchDocResult(BaseModel):
    rank: int
    content: str
    filename: str
    document_name: str
    document_type: str
    chunk: str
    preview: str
    content_length: int
    metadata: Dict[str, Any]


class SearchDocsResponse(BaseModel):
    results: List[SearchDocResult]


class ContextStats(BaseModel):
    total_characters: int
    estimated_tokens: int
    chunks_included: int


class SearchDocsWithContextResponse(BaseModel):
    query: str
    found_documents: int
    results: List[SearchDocResult]
    context: str
    context_stats: ContextStats
