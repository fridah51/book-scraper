from pymongo import ReturnDocument

async def get_next_book_id(db):
    doc = await db.counters.find_one_and_update(
        {"_id": "book_id"},
        {"$inc": {"seq": 1}},
        return_document=ReturnDocument.AFTER,
        upsert=True
    )
    return doc["seq"]
