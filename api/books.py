from fastapi import APIRouter, Depends, HTTPException, Query, Request
from typing import Optional

from slowapi import Limiter
from slowapi.util import get_remote_address
from api.auth import get_api_key
from db.mongo import get_db
from models.books import Book

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)



@router.get("/books",
summary="List all books with optional filters",
status_code=200)
@limiter.limit("100/hour")
async def list_books(
    request: Request,
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    rating: Optional[int] = None,
    sort_by: Optional[str] = Query(None, pattern="^(rating|price|reviews)$"),
    page: int = 1, per_page: int = 20,
    api_key = Depends(get_api_key)
):
    db = get_db()
    query = {}
    if category: query["category"] = {"$regex": f"^{category}$", "$options": "i"}
    if rating: query["rating"] = rating
    if min_price or max_price:
        price_filter = {}
        if min_price is not None:
            price_filter["$gte"] = min_price
        if max_price is not None:
            price_filter["$lte"] = max_price
        query["price_incl_tax"] = price_filter
    sort = [("rating",-1)]  # defaults
    if sort_by == "price":
        sort = [("price_incl_tax", 1)]
    elif sort_by == "reviews":
        sort = [("num_reviews", -1)]

    cursor = db.books.find(query).sort(sort).skip((page-1)*per_page).limit(per_page)
    results = await cursor.to_list(length=per_page)
    
    for book in results:
        book["_id"] = str(book["_id"])

    print("Query used:", query)
    print("Count found:", await db.books.count_documents(query))
    print("Total books in DB:", await db.books.count_documents({}))

    return {"page": page, "per_page": per_page, "items": results}



@router.get("/books/{book_id}",
summary="Get one book by book id")
async def get_book(book_id: int, api_key = Depends(get_api_key)):
    db = get_db()
    doc = await db.books.find_one({"book_id": book_id})
    if not doc:
        raise HTTPException(404, "Book Not found")
    doc["_id"] = str(doc["_id"])

    return doc
