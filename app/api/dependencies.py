from functools import lru_cache
from app.repositories.memory import InMemorySensorRepository
from app.publishers.memory import InMemoryEventPublisher


@lru_cache
def get_repository() -> InMemorySensorRepository:
    """
    Return a singleton repository.
    """
    return InMemorySensorRepository()


@lru_cache
def get_publisher() -> InMemoryEventPublisher:
    return InMemoryEventPublisher()
