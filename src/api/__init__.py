from fastapi import APIRouter

from .http.chat import router as chat_router
from .http.health import router as health_router
from .http.scraping import router as scraping_router
from .http.store import router as store_router
from .ws.route import router as ws_router

router = APIRouter(prefix="/api/v1")

router.include_router(health_router)
router.include_router(store_router)
router.include_router(scraping_router)
router.include_router(chat_router)
router.include_router(ws_router)

__all__ = ["router"]
