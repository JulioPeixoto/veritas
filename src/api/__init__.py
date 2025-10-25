from fastapi import APIRouter

from .v1.chat import router as chat_router
from .v1.health import router as health_router
from .v1.scraping import router as scraping_router
from .v1.store import router as store_router

router = APIRouter(prefix="/api/v1")

router.include_router(health_router)
router.include_router(store_router)
router.include_router(scraping_router)
router.include_router(chat_router)

__all__ = ["router"]
