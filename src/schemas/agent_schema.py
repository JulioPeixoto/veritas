from pydantic import BaseModel


class AgentResponse(BaseModel):
    text: str
    audio_base64: str
