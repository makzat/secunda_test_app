from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

from backend.config import get_settings

settings = get_settings()

api_key_header = APIKeyHeader(name=settings.security.api_key_name, auto_error=True)


async def check_api_key(api_key: str = Security(api_key_header)):
    if api_key == settings.security.api_key:
        return api_key
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )
