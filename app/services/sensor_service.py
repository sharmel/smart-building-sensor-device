from datetime import datetime
from app.core.config import Settings
from app.core.exceptions import OutOfOrderReadingError
from app.models.event import SensorAlarmEvent
from app.models.sensor import (
    AlarmState,
    Sensor,
    SensorType,
)
from app.publishers.base import EventPublisher
from app.repositories.base import SensorRepository
from app.schemas.requests import SensorReadingRequest


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
        if not await self.repository.is_newer(
            sensor_id,
            timestamp,
        ):
            raise OutOfOrderReadingError(
                "Reading timestamp is older than latest reading."
            )

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
