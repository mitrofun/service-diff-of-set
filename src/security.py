from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader

from src.config import settings

api_key_header_auth = APIKeyHeader(name=settings.api_key_name, auto_error=True)


async def get_api_key(api_key_header: str = Security(api_key_header_auth)):
    if api_key_header != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )
