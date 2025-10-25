from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from src.api import router
from src.lib.clients.langchain import LangChainClient
from src.ws import router as ws_router

app = FastAPI(title="Veritas", version="0.1.0")


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")


@app.on_event("startup")
async def startup_event():
    LangChainClient().init_db()


app.include_router(router)
app.include_router(ws_router)
