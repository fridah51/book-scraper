import pytest
from crawler.crawler import crawl_book
from db.mongo import get_db

TEST_URL = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"


@pytest.mark.asyncio
async def test_change_logging():
    db = get_db()

    # Force re-crawl
    await crawl_book(TEST_URL, db)
    await crawl_book(TEST_URL, db)

    logs = await db.change_logs.find({"source_url": TEST_URL}).to_list(10)
    assert isinstance(logs, list)
