from fastapi import APIRouter, Depends
from app.api.dependencies import get_repository
from app.repositories.base import SensorRepository

router = APIRouter(prefix="/debug", tags=["Debug"])


@router.get("/count")
async def count(
    repository: SensorRepository = Depends(get_repository),
):
    sensors = await repository.list()

    return {"count": len(sensors)}
