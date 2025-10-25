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
        Use apenas as informações fornecidas no contexto para responder às perguntas. 
        Se a informação não estiver disponível no contexto, diga que não possui essa informação específica.
        Seja preciso, útil e mantenha as respostas focadas no contexto fornecido."""

            user_message = f"""Contexto disponível:
            {search_response.context}

            Pergunta do usuário: {request.prompt}

            Responda com base apenas nas informações do contexto fornecido."""

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
