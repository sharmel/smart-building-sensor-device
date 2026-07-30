from datetime import UTC, datetime
import pytest
from app.models.event import SensorAlarmEvent
from app.models.sensor import AlarmState
from app.publishers.memory import InMemoryEventPublisher


@pytest.mark.asyncio
async def test_publish_event():
    publisher = InMemoryEventPublisher()

    event = SensorAlarmEvent(
        sensor_id="temp-001",
        building_id="HQ",
        previous_state=AlarmState.NORMAL,
        new_state=AlarmState.ALARM,
        value=38.5,
        timestamp=datetime.now(UTC),
    )

    await publisher.publish(event)

    events = await publisher.history()

    assert len(events) == 1
    assert events[0].sensor_id == "temp-001"


@pytest.mark.asyncio
async def test_publish_multiple_events():
    publisher = InMemoryEventPublisher()

    for index in range(5):
        event = SensorAlarmEvent(
            sensor_id=f"sensor-{index}",
            building_id="HQ",
            previous_state=AlarmState.NORMAL,
            new_state=AlarmState.ALARM,
            value=50,
            timestamp=datetime.now(UTC),
        )

        await publisher.publish(event)

    events = await publisher.history()

    assert len(events) == 5
