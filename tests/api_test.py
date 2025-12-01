import pytest
from httpx import ASGITransport, AsyncClient
from api.main import app


transport = ASGITransport(app=app)


# test for the main api
@pytest.mark.asyncio
async def test_books_api():
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/books", headers={"x-api-key": "key1"})
        assert response.status_code in (200, 403)
