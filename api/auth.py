from fastapi import Header, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
import os

API_KEY_NAME = "x-api-key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if not api_key_header:
        raise HTTPException(403, "Missing API key")
    
    valid_keys = os.getenv("API_KEYS", "").split(",")
    if api_key_header not in valid_keys:
        raise HTTPException(403, "Invalid API key")
    return api_key_header
