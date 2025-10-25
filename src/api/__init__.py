from fastapi import APIRouter

from .v1.docs import router as vector_store_router
from .v1.health import router as health_router
from .v1.scraping import router as scraping_router

router = APIRouter(prefix="/api/v1")

router.include_router(health_router)
router.include_router(vector_store_router)
router.include_router(scraping_router)

__all__ = ["router"]
