from fastapi import APIRouter, Depends
from bson import ObjectId
from datetime import datetime
from app.db.mongodb import mongodb
from app.core.deps import get_current_active_user
from app.schemas.notification import NotificationOut

router = APIRouter()

@router.get("/", response_model=list[NotificationOut])
async def list_notifications(current_user=Depends(get_current_active_user)):
    cursor = mongodb.db.notifications.find({"userId": str(current_user["_id"])}).sort("createdAt", -1)
    results = []
    async for doc in cursor:
        results.append(NotificationOut(id=str(doc["_id"]), **doc))
    return results
