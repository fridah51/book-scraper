import asyncio
from crawler.crawler import crawl_all


# a script to run the crawler independently
asyncio.run(crawl_all())
