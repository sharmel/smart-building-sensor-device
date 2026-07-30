from fastapi import APIRouter, Depends
from app.api.dependencies import get_publisher
from app.publishers.base import EventPublisher

router = APIRouter(prefix="/events", tags=["Events"])


@router.get("")
async def list_events(
    publisher: EventPublisher = Depends(get_publisher),
):
    return await publisher.history()
