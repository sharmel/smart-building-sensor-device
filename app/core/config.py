from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Smart Building Sensor Service"
    app_version: str = "1.0.0"

    host: str = "0.0.0.0"
    port: int = 8000

    log_level: str = "INFO"

    temperature_threshold: float = 35
    humidity_threshold: float = 80
    co2_threshold: int = 1000
    smoke_threshold: int = 20

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
