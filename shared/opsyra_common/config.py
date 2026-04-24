from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class SharedSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "sqlite:///./opsyra.db"
    redis_url: str = ""
    api_key: str | None = None
    telemetry_stream_name: str = "telemetry.raw"
    processing_enable_consumer: bool = False
    processing_stream_block_ms: int = 1000
    openai_api_key: str | None = None
    openai_model: str = "gpt-5.4"
    openai_base_url: str = "https://api.openai.com/v1"


@lru_cache
def get_shared_settings() -> SharedSettings:
    return SharedSettings()
