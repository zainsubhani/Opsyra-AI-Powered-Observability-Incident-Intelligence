from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "Opsyra Query Service"
    service_slug: str = "query-service"
    version: str = "0.1.0"
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"
    openapi_url: str = "/openapi.json"


settings = Settings()
