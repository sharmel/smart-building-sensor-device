from fastapi import APIRouter, Depends, HTTPException, Query

from app.core.exceptions import OutOfOrderReadingError
from app.schemas.requests import SensorReadingRequest
from app.schemas.responses import (
    AcceptedResponse,
    SensorResponse,
)
from app.services.sensor_service import SensorService

from .dependencies import get_sensor_service

router = APIRouter(
    prefix="/sensors",
    tags=["Sensors"],
)


@router.post(
    "/readings",
    response_model=AcceptedResponse,
    status_code=202,
)
async def ingest_reading(
    request: SensorReadingRequest,
    service: SensorService = Depends(get_sensor_service),
):
    await service.ingest(request)
    return AcceptedResponse()


@router.get(
    "/{sensor_id}",
    response_model=SensorResponse,
)
async def get_sensor(
    sensor_id: str,
    service: SensorService = Depends(get_sensor_service),
):
    sensor = await service.get_sensor(sensor_id)

    if sensor is None:
        raise HTTPException(
            status_code=404,
            detail="Sensor not found",
        )

    return SensorResponse.model_validate(sensor)


@router.get(
    "",
    response_model=list[SensorResponse],
)
async def list_sensors(
    sensor_type: str | None = Query(default=None),
    building_id: str | None = Query(default=None),
    alarm: bool | None = Query(default=None),
    service: SensorService = Depends(get_sensor_service),
):
    return await service.list_sensors(
        sensor_type,
        building_id,
        alarm,
    )
