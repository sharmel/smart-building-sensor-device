from datetime import UTC, datetime
import pytest
from app.core.config import get_settings
from app.models.sensor import SensorType
from app.publishers.memory import InMemoryEventPublisher
from app.repositories.memory import InMemorySensorRepository
from app.schemas.requests import SensorReadingRequest
from app.services.sensor_service import SensorService


@pytest.mark.asyncio
async def test_ingest_sensor():
    repository = InMemorySensorRepository()
    publisher = InMemoryEventPublisher()
    service = SensorService(
        repository,
        publisher,
        get_settings(),
    )
    reading = SensorReadingRequest(
        sensor_id="temp-001",
        building_id="HQ",
        sensor_type=SensorType.TEMPERATURE,
        value=22,
        timestamp=datetime.now(UTC),
    )
    sensor = await service.ingest(reading)
    assert sensor.value == 22


@pytest.mark.asyncio
async def test_alarm_state():
    repository = InMemorySensorRepository()
    publisher = InMemoryEventPublisher()
    service = SensorService(
        repository,
        publisher,
        get_settings(),
    )
    reading = SensorReadingRequest(
        sensor_id="temp-001",
        building_id="HQ",
        sensor_type=SensorType.TEMPERATURE,
        value=40,
        timestamp=datetime.now(UTC),
    )

    sensor = await service.ingest(reading)
    assert sensor.alarm_state.name == "ALARM"


@pytest.mark.asyncio
async def test_alarm_change_publishes_event():
    repository = InMemorySensorRepository()
    publisher = InMemoryEventPublisher()
    service = SensorService(
        repository,
        publisher,
        get_settings(),
    )
    first = SensorReadingRequest(
        sensor_id="temp-1",
        building_id="HQ",
        sensor_type=SensorType.TEMPERATURE,
        value=20,
        timestamp=datetime(2026, 1, 1, tzinfo=UTC),
    )
    second = SensorReadingRequest(
        sensor_id="temp-1",
        building_id="HQ",
        sensor_type=SensorType.TEMPERATURE,
        value=45,
        timestamp=datetime(2026, 1, 2, tzinfo=UTC),
    )

    await service.ingest(first)
    await service.ingest(second)
    events = await publisher.history()
    assert len(events) == 1
