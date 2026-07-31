from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from app.models.sensor import SensorType


class SensorReadingRequest(BaseModel):
    sensor_id: str = Field(..., min_length=1)
    building_id: str = Field(..., min_length=1)
    sensor_type: SensorType
    value: float
    timestamp: datetime

    @field_validator("value")
    @classmethod
    def validate_value(cls, value: float) -> float:
        if value < 0:
            raise ValueError("Sensor value cannot be negative")
        return value
