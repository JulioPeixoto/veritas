from fastapi import APIRouter
from .v1.health import router as health_router
from .v1.vector_store import router as vector_store_router


router = APIRouter(prefix="/api/v1")

router.include_router(health_router)
router.include_router(vector_store_router)

__all__ = ["router"]
