from app.models.sensor import Sensor
from app.repositories.base import SensorRepository
from datetime import datetime


class InMemorySensorRepository(SensorRepository):
    def __init__(self) -> None:
        self._store: dict[str, Sensor] = {}

    async def save(self, sensor: Sensor) -> None:
        self._store[sensor.sensor_id] = sensor

    async def get(self, sensor_id: str) -> Sensor | None:
        return self._store.get(sensor_id)

    async def list(self) -> list[Sensor]:
        return list(self._store.values())

    async def exists(self, sensor_id: str) -> bool:
        return sensor_id in self._store

    async def is_newer(
        self,
        sensor_id: str,
        timestamp: datetime,
    ) -> bool:
        current = self._store.get(sensor_id)
        if current is None:
            return True
        return timestamp > current.timestamp
