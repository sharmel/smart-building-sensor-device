from app.models.event import SensorAlarmEvent
from app.publishers.base import EventPublisher


class InMemoryEventPublisher(EventPublisher):
    def __init__(self) -> None:
        self._events: list[SensorAlarmEvent] = []

    async def publish(
        self,
        event: SensorAlarmEvent,
    ) -> None:
        self._events.append(event)

    async def history(self) -> list[SensorAlarmEvent]:
        return list(self._events)
