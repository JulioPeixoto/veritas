from fastapi import APIRouter, HTTPException

from src.schemas.chat_schema import ChatRequest, ChatResponse
from src.services.chat_service import ChatService

router = APIRouter(prefix="", tags=["Chat"])
chat_service = ChatService()


@router.post("/chat", status_code=200, response_model=ChatResponse)
async def chat_with_rag(request: ChatRequest):
    """
    Realiza uma consulta usando RAG (Retrieval-Augmented Generation) na base de conhecimento.

    Este endpoint recebe uma pergunta do usuário, busca informações relevantes no vector store
    e gera uma resposta contextualizada usando IA generativa.

    Parâmetros:
        request (ChatRequest): Objeto contendo o prompt/pergunta do usuário.

    Retorna:
        ChatResponse: Resposta gerada com contexto, timestamp e metadados.

    Exceções:
        HTTPException 400: Se o prompt estiver vazio ou inválido.
        HTTPException 500: Para erros durante o processamento.

    Exemplo de uso:
        >>> POST /chat
        {
            "prompt": "Hoje está chovendo muito em Aracaju, há risco de alagamento no bairro São José?"
        }

        Resposta:
        {
            "output": "Sim, o bairro São José é uma das áreas afetadas por alagamentos...",
            "timestamp": "2024-10-25T14:30:00",
            "context_used": [...],
            "total_tokens_estimated": 150
        }
    """
    try:
        response = await chat_service.chat(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no processamento: {str(e)}")
