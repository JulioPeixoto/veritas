from fastapi import FastAPI

from src.http import router
from src.lib.langchain import LangChainClient

app = FastAPI(title="Veritas", version="0.1.0")


@app.on_event("startup")
async def startup_event():
    LangChainClient().init_db()


app.include_router(router)
