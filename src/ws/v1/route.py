from fastapi import APIRouter, WebSocket
import src.lib.openai as openai

router = APIRouter()
client = openai.OpenAIClient()


@router.websocket("/ws/health")
async def websocket_health_ws(ws: WebSocket):
    await ws.accept()
    await ws.send_json({"message": "WebSocket health connected"})
    await ws.close()

@router.websocket("/ws/agent")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()

    while True:
        data = await ws.receive_text()
        print(f"User said: {data}")

        response = await client.create_response(data)

        await ws.send_json(
            {"text": response.answer, "audio_base64": response.audio_base64}
        )
