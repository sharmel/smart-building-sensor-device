from fastapi import APIRouter, Depends
from app.core.config import Settings, get_settings

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health(settings: Settings = Depends(get_settings)):
    return {
        "status": "UP",
        "service": settings.app_name,
        "version": settings.app_version,
    }
