from openai import OpenAI
import base64
from src.config import settings
import pydantic


class AudioResponse(pydantic.BaseModel):
    answer: str
    audio_base64: str


class OpenAIClient:
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)

    def create_answer(self, data: str) -> str:
        response = self.client.chat.completions.create(
            model="gpt-4o-mini", messages=[{"role": "user", "content": data}]
        )
        answer = response.choices[0].message.content
        return answer

    def create_audio(self, data: str) -> str:
        speech = self.client.audio.speech.create(
            model="gpt-4o-mini-tts", voice="alloy", input=data
        )
        audio_bytes = speech.read()
        audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
        return audio_base64

    def create_response(self, data: str) -> AudioResponse:
        answer = self.create_answer(data)
        audio_base64 = self.create_audio(answer)
        return AudioResponse(answer, audio_base64)
