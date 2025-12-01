import pytest
import asyncio
from crawler.crawler import crawl_book
from db.mongo import get_test_db

TEST_URL = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
TEST_BOOK_ID = 9999  # unique for testing


@pytest.mark.asyncio
async def test_crawl_single_book():
    db = get_test_db()

    # Clear test entry if already exists
    await db.books.delete_many({"source_url": TEST_URL})

    # Run crawl
    await crawl_book(TEST_URL, db)

    # Verify book exists in DB
    book = await db.books.find_one({"source_url": TEST_URL})

    assert book is not None, "Book was not inserted"
    assert "price_incl_tax" in book
    assert "category" in book
    assert "rating" in book
    assert "raw_html" in book
    assert "crawl" in book
    assert book["crawl"]["status"] == "ok"

    # Clean up DB after test
    await db.books.delete_many({"source_url": TEST_URL})

