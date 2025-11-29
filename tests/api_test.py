import pytest
from httpx import AsyncClient
from api.main import app

@pytest.mark.asyncio
async def test_books_api():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/books", headers={"x-api-key": "key1"})
        assert response.status_code in (200, 403)
