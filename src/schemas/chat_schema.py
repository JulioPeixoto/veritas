from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    prompt: str = Field(..., min_length=1, description="Pergunta ou prompt do usuário")


class DocumentContext(BaseModel):
    content: str
    filename: str
    document_name: str
    chunk: str
    relevance_score: float


class ChatResponse(BaseModel):
    output: str = Field(..., description="Resposta gerada pelo modelo")
    timestamp: datetime = Field(default_factory=datetime.now, description="Data e hora da resposta")
    context_used: List[DocumentContext] = Field(default_factory=list, description="Documentos utilizados como contexto")
    total_tokens_estimated: Optional[int] = Field(None, description="Estimativa de tokens utilizados")
    expanded_query: Optional[str] = Field(None, description="Query expandida usada na busca vetorial")
