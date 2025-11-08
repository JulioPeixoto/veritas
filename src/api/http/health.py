from fastapi import APIRouter
from fastapi.responses import RedirectResponse

router = APIRouter(prefix="")


@router.get("/")
async def root():
    return RedirectResponse(url="/docs")


@router.get("/health")
async def health():
    return {"status": "ok"}
