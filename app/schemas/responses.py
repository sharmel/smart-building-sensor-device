from datetime import datetime
from pydantic import BaseModel
from app.models.sensor import AlarmState, SensorType


class SensorResponse(BaseModel):
    sensor_id: str
    building_id: str
    sensor_type: SensorType
    value: float
    timestamp: datetime
    alarm_state: AlarmState


class AcceptedResponse(BaseModel):
    accepted: bool = True


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
