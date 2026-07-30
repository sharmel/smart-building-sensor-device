from functools import lru_cache
from app.core.config import get_settings
from app.repositories.memory import InMemorySensorRepository
from app.publishers.memory import InMemoryEventPublisher
from app.services.sensor_service import SensorService


@lru_cache
def get_repository() -> InMemorySensorRepository:
    """
    Return a singleton repository.
    """
    return InMemorySensorRepository()


@lru_cache
def get_publisher() -> InMemoryEventPublisher:
    return InMemoryEventPublisher()


@lru_cache
def get_sensor_service():
    return SensorService(
        repository=get_repository(),
        publisher=get_publisher(),
        settings=get_settings(),
    )
