from fastapi import FastAPI

from app.api.health import router as health_router

app = FastAPI(
    title="Smart Building Sensor Service",
    version="1.0.0",
)

app.include_router(health_router)


@app.get("/")
async def root():
    return {"service": "Smart Building Sensor Service"}
