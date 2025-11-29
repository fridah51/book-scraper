from pydantic import BaseModel, HttpUrl, Field
from typing import Optional
from datetime import datetime

class CrawlMeta(BaseModel):
    last_crawled_at: datetime
    status: str
    source: str
    fingerprint: str

class Book(BaseModel):
    book_id:int
    source_url: HttpUrl
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    price_excl_tax: float = Field(..., ge=0)
    price_incl_tax: float = Field(..., ge=0)
    availability: Optional[str] = None
    num_reviews: int = 0
    image_url: Optional[HttpUrl] = None
    rating: int = Field(..., ge=0, le=5)  # normalized 0-5
    crawl: CrawlMeta
    raw_html: Optional[str] = None
