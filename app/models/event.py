from datetime import datetime
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from app.models.sensor import AlarmState


class SensorAlarmEvent(BaseModel):
    event_id: UUID = Field(default_factory=uuid4)
    sensor_id: str
    building_id: str
    previous_state: AlarmState
    new_state: AlarmState
    value: float
    timestamp: datetime
