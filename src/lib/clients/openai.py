import base64
from typing import List

import pydantic
from langchain_openai import OpenAIEmbeddings
from openai import AsyncOpenAI

from src.config import settings


class AudioResponse(pydantic.BaseModel):
    answer: str
    audio_base64: str


class OpenAIClient:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small", 
            api_key=settings.openai_api_key
        )

    async def create_answer(self, data: str) -> str:
        response = await self.client.chat.completions.create(
            model="gpt-4o-mini", messages=[{"role": "user", "content": data}]
        )
        answer = response.choices[0].message.content
        return answer

    async def create_audio(self, data: str) -> str:
        speech = await self.client.audio.speech.create(
            model="gpt-4o-mini-tts", voice="ash", input=data
        )
        audio_bytes = speech.read()
        audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
        return audio_base64

    async def create_response(self, data: str) -> AudioResponse:
        answer = await self.create_answer(data)
        audio_base64 = await self.create_audio(answer)
        return AudioResponse(answer=answer, audio_base64=audio_base64)

    async def create_embedding(self, text: str) -> List[float]:
        """
        Gera embedding vetorial para um texto usando OpenAI.
        
        Args:
            text: Texto para gerar embedding
            
        Returns:
            Lista de floats representando o vetor embedding
        """
        response = await self.client.embeddings.create(
            model="text-embedding-3-small",
            input=text.strip()
        )
        return response.data[0].embedding

    async def semantic_search_query_expansion(self, user_input: str) -> str:
        """
        Expande e otimiza a query do usuário para busca vetorial.
        
        Analisa todo o input do usuário e gera uma versão expandida
        que melhora a recuperação de documentos relevantes.
        
        Args:
            user_input: Input original do usuário
            
        Returns:
            Query expandida e otimizada para busca vetorial
        """
        expansion_prompt = f"""Analise a seguinte pergunta do usuário e expanda-a para melhorar a busca vetorial:

Pergunta original: "{user_input}"

Sua tarefa:
1. Identifique os conceitos-chave e termos importantes
2. Adicione sinônimos e termos relacionados relevantes
3. Inclua variações linguísticas (plural/singular, verbos relacionados)
4. Mantenha o contexto de Aracaju, clima e prevenção quando aplicável
5. Retorne apenas a query expandida, sem explicações

Query expandida:"""

        response = await self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": expansion_prompt}],
            temperature=0.3,
            max_tokens=150
        )
        
        expanded_query = response.choices[0].message.content
        return expanded_query.strip() if expanded_query else user_input

    async def vector_search_with_expansion(self, user_input: str) -> tuple[str, List[float]]:
        """
        Método principal para busca vetorial com expansão de query.
        
        Processa todo o user input, expande a query e gera embedding
        otimizado para busca vetorial.
        
        Args:
            user_input: Input completo do usuário
            
        Returns:
            Tupla com (query_expandida, embedding_vector)
        """
        # Expande a query para melhor recuperação
        expanded_query = await self.semantic_search_query_expansion(user_input)
        
        # Gera embedding da query expandida
        embedding_vector = await self.create_embedding(expanded_query)
        
        return expanded_query, embedding_vector
