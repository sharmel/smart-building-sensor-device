from fastapi import FastAPI
from app.api.health import router as health_router
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.api.debug import router as debug_router
from app.api.event import router as event_router

settings = get_settings()

configure_logging(settings.log_level)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

app.include_router(health_router)
app.include_router(debug_router)
app.include_router(event_router)


@app.get("/")
async def root():
    return {
        "service": settings.app_name,
        "version": settings.app_version,
    }
