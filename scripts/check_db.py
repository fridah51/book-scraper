import asyncio
from db.mongo import get_db

async def main():
    db = get_db()
    print(await db.books.count_documents({}))

if __name__ == "__main__":
    asyncio.run(main())
