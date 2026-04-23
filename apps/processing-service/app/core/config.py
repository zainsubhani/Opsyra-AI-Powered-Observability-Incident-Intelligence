from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "Opsyra Processing Service"
    service_slug: str = "processing-service"
    version: str = "0.1.0"
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"
    openapi_url: str = "/openapi.json"


settings = Settings()
