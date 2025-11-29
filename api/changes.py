from fastapi import APIRouter, Depends
from datetime import datetime, timedelta
from typing import Optional
from db.mongo import get_db
from api.auth import get_api_key

router = APIRouter(tags=["Changes"])

@router.get("/changes")
async def get_changes(
    days: Optional[int] = 1,
    api_key: str = Depends(get_api_key)
):
    db = get_db()
    since = datetime.utcnow() - timedelta(days=days)

    cursor = db.change_logs.find({"timestamp": {"$gte": since}}).sort("timestamp", -1)
    return await cursor.to_list(length=100)
