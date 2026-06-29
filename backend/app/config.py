from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = Field(
        default="sqlite:///./dealsense.db",
        alias="DATABASE_URL",
    )
    api_title: str = Field(default="DealSense Price API", alias="API_TITLE")
    api_version: str = Field(default="1.0.0", alias="API_VERSION")
    cors_origins: str = Field(default="http://localhost:3000", alias="BACKEND_CORS_ORIGINS")
    enable_scheduler: bool = Field(default=False, alias="ENABLE_SCHEDULER")
    price_refresh_hours: int = Field(default=12, alias="PRICE_REFRESH_HOURS")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
