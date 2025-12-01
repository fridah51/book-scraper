from db.mongo import get_db


# functions to handle resume state of the crawler
async def save_state(page):
    db = get_db()
    await db.state.update_one({"_id": "crawler"}, {"$set": {"page": page}}, upsert=True)


async def load_state():
    db = get_db()
    s = await db.state.find_one({"_id": "crawler"})
    return s["page"] if s else 1
