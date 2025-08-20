from fastapi import FastAPI
from src.http import router

app = FastAPI(title="Veritas", version="0.1.0")

app.include_router(router)
