from datetime import datetime

from src.config import settings
from src.lib.clients.openai import OpenAIClient
from src.schemas.chat_schema import ChatRequest, ChatResponse, DocumentContext
from src.services.store_service import StoreService


class ChatService:
    def __init__(self, db_file: str = settings.path_db_file):
        self.store_service = StoreService(db_file=db_file)
        self.openai_client = OpenAIClient()

    async def chat(self, request: ChatRequest) -> ChatResponse:
        expanded_query, _ = await self.openai_client.vector_search_with_expansion(
            request.prompt
        )

        search_response = await self.store_service.search_docs_with_context(
            query=expanded_query, limit=5
        )

        if not search_response.results:
            search_response = await self.store_service.search_docs_with_context(
                query=request.prompt, limit=5
            )

        context_docs = []
        for result in search_response.results:
            context_docs.append(
                DocumentContext(
                    content=result.content,
                    filename=result.filename,
                    document_name=result.document_name,
                    chunk=result.chunk,
                    relevance_score=1.0 / result.rank,
                )
            )

        if search_response.context:
            system_prompt = """Você é um assistente especializado em informações sobre Aracaju, clima e prevenção.

INSTRUÇÕES IMPORTANTES:
1. Use as informações disponíveis no contexto fornecido
2. Extraia e sintetize dados relevantes dos documentos
3. Combine informações
4. Responda apenas o escopo que foi solicitado
"""
            user_message = f"""CONTEXTO DOS DOCUMENTOS:
{search_response.context}

PERGUNTA: {request.prompt}

INSTRUÇÃO: Analise todo o contexto acima e forneça uma resposta útil e prática. Extraia todas as informações relevantes disponíveis, incluindo medidas preventivas, números de emergência, bairros afetados, e orientações específicas mencionadas nos documentos."""

            full_prompt = f"{system_prompt}\n\n{user_message}"
        else:
            full_prompt = f"Pergunta: {request.prompt}\n\nResposta: Não encontrei informações relevantes na base de conhecimento para responder sua pergunta."

        if search_response.context:
            output = await self.openai_client.create_answer(full_prompt)
        else:
            output = "Não encontrei informações relevantes na base de conhecimento para responder sua pergunta."

        estimated_tokens = (
            len(full_prompt.split()) + len(output.split())
            if search_response.context
            else 0
        )

        return ChatResponse(
            output=output,
            timestamp=datetime.now(),
            context_used=context_docs,
            total_tokens_estimated=estimated_tokens,
            expanded_query=expanded_query,
        )
