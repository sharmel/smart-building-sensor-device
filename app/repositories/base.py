from __future__ import annotations
from abc import ABC, abstractmethod
from app.models.sensor import Sensor


class SensorRepository(ABC):
    """Abstract repository for sensor state."""

    @abstractmethod
    async def save(self, sensor: Sensor) -> None:
        """Save or update the latest sensor state."""

    @abstractmethod
    async def get(self, sensor_id: str) -> Sensor | None:
        """Return the latest state for a sensor."""

    @abstractmethod
    async def list(self) -> list[Sensor]:
        """Return all sensors."""

    @abstractmethod
    async def exists(self, sensor_id: str) -> bool:
        """Return True if the sensor exists."""

    @abstractmethod
    async def is_newer(
        self,
        sensor_id: str,
        timestamp,
    ) -> bool:
        """Return True if the reading is newer than the stored one."""
