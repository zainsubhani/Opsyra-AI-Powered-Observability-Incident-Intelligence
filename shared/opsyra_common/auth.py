from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader

from opsyra_common.config import get_shared_settings


api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def require_api_key(api_key: str | None = Depends(api_key_header)) -> None:
    settings = get_shared_settings()
    if not settings.api_key:
        return
    if api_key == settings.api_key:
        return
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API key.",
    )
