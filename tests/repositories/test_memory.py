from datetime import UTC, datetime
import pytest
from app.models.sensor import AlarmState, Sensor, SensorType
from app.repositories.memory import InMemorySensorRepository


@pytest.mark.asyncio
async def test_save_and_get_sensor():
    repository = InMemorySensorRepository()

    sensor = Sensor(
        sensor_id="temp-001",
        building_id="HQ",
        sensor_type=SensorType.TEMPERATURE,
        value=22.5,
        timestamp=datetime.now(UTC),
        alarm_state=AlarmState.NORMAL,
    )

    await repository.save(sensor)
    stored = await repository.get("temp-001")

    assert stored is not None
    assert stored.sensor_id == "temp-001"
    assert stored.value == 22.5


@pytest.mark.asyncio
async def test_list_returns_all_sensors():
    repository = InMemorySensorRepository()

    for index in range(3):
        await repository.save(
            Sensor(
                sensor_id=f"id-{index}",
                building_id="HQ",
                sensor_type=SensorType.TEMPERATURE,
                value=20,
                timestamp=datetime.now(UTC),
                alarm_state=AlarmState.NORMAL,
            )
        )

    sensors = await repository.list()

    assert len(sensors) == 3


@pytest.mark.asyncio
async def test_is_newer():
    repository = InMemorySensorRepository()

    first = datetime(2026, 1, 1, tzinfo=UTC)
    second = datetime(2026, 1, 2, tzinfo=UTC)

    await repository.save(
        Sensor(
            sensor_id="sensor-1",
            building_id="HQ",
            sensor_type=SensorType.TEMPERATURE,
            value=22,
            timestamp=first,
            alarm_state=AlarmState.NORMAL,
        )
    )

    assert await repository.is_newer("sensor-1", second)
    assert not await repository.is_newer("sensor-1", first)
