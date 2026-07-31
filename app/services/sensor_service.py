from datetime import datetime
from app.core.config import Settings
from app.core.exceptions import *
from app.models.event import SensorAlarmEvent
from app.publishers.base import EventPublisher
from app.repositories.base import SensorRepository
from app.schemas.requests import SensorReadingRequest
from app.models.sensor import (
    AlarmState,
    Sensor,
    SensorType,
)


class SensorService:
    def __init__(
        self,
        repository: SensorRepository,
        publisher: EventPublisher,
        settings: Settings,
    ):
        self.repository = repository
        self.publisher = publisher
        self.settings = settings

    async def ingest(
        self,
        request: SensorReadingRequest,
    ) -> Sensor:
        """
        Process an incoming sensor reading.
        """
        self._validate_sensor_value(
            request.sensor_type,
            request.value,
        )
        await self._validate_timestamp(
            request.sensor_id,
            request.timestamp,
        )

        alarm_state = self._calculate_alarm_state(
            request.sensor_type,
            request.value,
        )
        previous = await self.repository.get(request.sensor_id)
        sensor = Sensor(
            sensor_id=request.sensor_id,
            building_id=request.building_id,
            sensor_type=request.sensor_type,
            value=request.value,
            timestamp=request.timestamp,
            alarm_state=alarm_state,
        )

        await self.repository.save(sensor)
        if previous is not None and previous.alarm_state != sensor.alarm_state:
            await self.publisher.publish(
                SensorAlarmEvent(
                    sensor_id=sensor.sensor_id,
                    building_id=sensor.building_id,
                    previous_state=previous.alarm_state,
                    new_state=sensor.alarm_state,
                    value=sensor.value,
                    timestamp=datetime.utcnow(),
                )
            )
        return sensor


async def _validate_timestamp(
    self,
    sensor_id: str,
    timestamp: datetime,
) -> None:

    existing = await self.repository.get(sensor_id)
    if existing is None:
        return
    if timestamp == existing.timestamp:
        raise DuplicateReadingError("Duplicate timestamp.")
    if timestamp < existing.timestamp:
        raise OutOfOrderReadingError("Out-of-order reading.")

    def _calculate_alarm_state(
        self,
        sensor_type: SensorType,
        value: float,
    ) -> AlarmState:
        thresholds = {
            SensorType.TEMPERATURE: self.settings.temperature_threshold,
            SensorType.HUMIDITY: self.settings.humidity_threshold,
            SensorType.CO2: self.settings.co2_threshold,
            SensorType.SMOKE: self.settings.smoke_threshold,
        }

        if sensor_type == SensorType.MOTION:
            return AlarmState.NORMAL
        limit = thresholds[sensor_type]
        if value > limit:
            return AlarmState.ALARM
        return AlarmState.NORMAL


async def get_sensor(self, sensor_id: str):
    sensor = await self.repository.get(sensor_id)
    if sensor is None:
        raise SensorNotFoundError(f"Sensor '{sensor_id}' not found.")
    return sensor


async def list_sensors(
    self,
    sensor_type=None,
    building_id=None,
    alarm=None,
):
    sensors = await self.repository.list()
    if sensor_type:
        sensors = [s for s in sensors if s.sensor_type.value == sensor_type]
    if building_id:
        sensors = [s for s in sensors if s.building_id == building_id]
    if alarm is not None:
        sensors = [s for s in sensors if (s.alarm_state.name == "ALARM") == alarm]
    return sensors


def _validate_sensor_value(
    self,
    sensor_type: SensorType,
    value: float,
) -> None:
    """
    Validate business rules for sensor values.
    """
    if sensor_type == SensorType.TEMPERATURE:
        if value < -50 or value > 100:
            raise InvalidSensorValueError("Temperature must be between -50 and 100°C.")

    elif sensor_type == SensorType.HUMIDITY:
        if value < 0 or value > 100:
            raise InvalidSensorValueError("Humidity must be between 0 and 100%.")
    elif sensor_type == SensorType.CO2:
        if value < 0:
            raise InvalidSensorValueError("CO₂ cannot be negative.")
    elif sensor_type == SensorType.SMOKE:
        if value < 0:
            raise InvalidSensorValueError("Smoke level cannot be negative.")
