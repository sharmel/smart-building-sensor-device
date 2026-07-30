from datetime import datetime
from enum import Enum
from pydantic import BaseModel


class SensorType(str, Enum):
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    CO2 = "co2"
    SMOKE = "smoke"
    MOTION = "motion"


class AlarmState(str, Enum):
    NORMAL = "NORMAL"
    ALARM = "ALARM"


class Sensor(BaseModel):
    sensor_id: str
    building_id: str
    sensor_type: SensorType
    value: float
    timestamp: datetime
    alarm_state: AlarmState = AlarmState.NORMAL
