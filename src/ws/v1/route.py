from fastapi import APIRouter, WebSocket
import src.lib.clients.openai as openai
from src.schemas.agent_schema import AgentResponse

router = APIRouter()
client = openai.OpenAIClient()


@router.websocket("/ws/health")
async def websocket_health_ws(ws: WebSocket):
    await ws.accept()
    await ws.send_json({"message": "WebSocket health connected"})
    await ws.close()


# TODO: viseme/fonemes, ffmpeg and 1.25 speed for audio
@router.websocket("/ws/agent")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()

    while True:
        data = await ws.receive_text()
        print(f"User said: {data}")

        response = await client.create_response(data)

        await ws.send_json(
            AgentResponse(
                text=response.answer, 
                audio_base64=response.audio_base64
            ).model_dump()
        )
