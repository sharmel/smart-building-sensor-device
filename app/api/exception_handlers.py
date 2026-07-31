from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.core.exceptions import (
    DuplicateReadingError,
    InvalidSensorValueError,
    OutOfOrderReadingError,
    SensorNotFoundError,
)


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(SensorNotFoundError)
    async def sensor_not_found(
        request: Request,
        exc: SensorNotFoundError,
    ):
        return JSONResponse(
            status_code=404,
            content={"detail": str(exc)},
        )

    @app.exception_handler(DuplicateReadingError)
    async def duplicate_reading(
        request: Request,
        exc: DuplicateReadingError,
    ):
        return JSONResponse(
            status_code=409,
            content={"detail": str(exc)},
        )

    @app.exception_handler(OutOfOrderReadingError)
    async def out_of_order(
        exc: OutOfOrderReadingError,
    ):
        return JSONResponse(
            status_code=409,
            content={"detail": str(exc)},
        )

    @app.exception_handler(InvalidSensorValueError)
    async def invalid_value(
        exc: InvalidSensorValueError,
    ):
        return JSONResponse(
            status_code=422,
            content={"detail": str(exc)},
        )
