from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "Opsyra AI RCA Service"
    service_slug: str = "ai-rca-service"
    version: str = "0.1.0"
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"
    openapi_url: str = "/openapi.json"


settings = Settings()
