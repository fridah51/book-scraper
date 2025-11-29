from pydantic import BaseModel
from datetime import datetime

class Change(BaseModel):
    field: str
    old: str
    new: str
    timestamp: datetime
