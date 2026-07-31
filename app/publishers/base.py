from __future__ import annotations
from abc import ABC, abstractmethod
from app.models.event import SensorAlarmEvent


class EventPublisher(ABC):
    @abstractmethod
    async def publish(
        self,
        event: SensorAlarmEvent,
    ) -> None:
        """Publish an event."""

    @abstractmethod
    async def history(self) -> list[SensorAlarmEvent]:
        """Return published events."""
