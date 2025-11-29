import asyncio
from datetime import datetime
import hashlib
import logging
from typing import List
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type, wait_fixed
from bs4 import BeautifulSoup
from motor.motor_asyncio import AsyncIOMotorClient
from models.books import Book
from db.mongo import get_db
from crawler.parser import parse_book_page, list_book_urls_from_listing

BASE = "https://books.toscrape.com"

logger = logging.getLogger(__name__)

timeout = httpx.Timeout(30.0, connect=10.0)
client = httpx.AsyncClient(timeout=30.0, limits=httpx.Limits(max_connections=20))



@retry(stop=stop_after_attempt(3), wait=wait_fixed(2),
       retry=retry_if_exception_type((httpx.HTTPError, asyncio.TimeoutError)))
async def fetch(url: str):
    async with httpx.AsyncClient(timeout=timeout) as client:
        resp = await client.get(url)
        if resp.status_code == 404:
            return None
        resp.raise_for_status()
        return resp



def fingerprint_book(data: dict) -> str:
    # canonicalize fields we care about
    core = f"{data['title']}|{data['price_incl_tax']}|{data.get('availability','')}"
    return hashlib.sha256(core.encode('utf-8')).hexdigest()



async def crawl_book(url: str, db):
    resp = await fetch(url)
    html = resp.text
    parsed = parse_book_page(html, url)  # returns dict with fields matching Book model

    parsed['raw_html'] = html
    parsed['crawl'] = {
        'last_crawled_at': datetime.utcnow(),
        'status': 'ok',
        'source': BASE,
        'fingerprint': fingerprint_book(parsed)
    }

    # upsert by source_url and create change log if fingerprint differs
    existing = await db.books.find_one({"source_url": parsed["source_url"]})
    if existing:
        old_fp = existing.get('crawl', {}).get('fingerprint')
        new_fp = parsed['crawl']['fingerprint']
        if old_fp != new_fp:
            # compute field differences
            diffs = []
            for k in ('price_incl_tax', 'availability', 'rating'):
                if existing.get(k) != parsed.get(k):
                    diffs.append({"field": k, "old": existing.get(k), "new": parsed.get(k)})
            
            # insert change logs
            for d in diffs:
                await db.change_logs.insert_one({
                    "book_id": existing['book_id'],
                    "source_url": parsed['source_url'],
                    "timestamp": datetime.utcnow(),
                    "change": d,
                    "reason": "daily_crawl",
                    "fingerprint_old": old_fp,
                    "fingerprint_new": new_fp
                })
            #update book metadata
            parsed['metadata'] = {
                "last_changed_at": datetime.utcnow()
            }
            parsed['book_id'] = existing['book_id']

        # update crawl metadata and replace
        await db.books.replace_one({"_id": existing["_id"]}, parsed, upsert=True)

    else:
        #Insert new book entry to db 
        last = await db.books.find_one(sort=[("book_id", -1)])
        next_id = 1 if not last else last["book_id"] + 1
        parsed['book_id'] = next_id
        parsed['metadata'] = {"first_seen": datetime.utcnow()}
        res = await db.books.insert_one(parsed)

    logger.info(f"Processed {url}")



async def crawl_all(concurrency:int = 20):
    db = get_db()

    # crawl listing pages, collect book urls, then crawl them concurrently
    book_urls = set()
    # pagination loop
    page = 1
    while True:
        list_url = f"{BASE}/catalogue/page-{page}.html"
        try:
            resp = await fetch(list_url)
            if resp is None:
                print(f"No more pages after page {page-1}")
                break
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                break
            else:
                raise
        urls = list_book_urls_from_listing(resp.text)
        if not urls:
            break
        book_urls.update(urls)
        page += 1

    sem = asyncio.Semaphore(concurrency)
    async def sem_crawl(u):
        async with sem:
            await crawl_book(u, db)

    await asyncio.gather(*[sem_crawl(u) for u in book_urls])
