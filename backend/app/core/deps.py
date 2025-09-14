from fastapi import Depends, HTTPException, Header
from app.core.security import decode_token
from app.db.mongodb import mongodb
from bson import ObjectId

async def get_current_user(authorization: str = Header(...)):
    parts = authorization.split()
    if parts[0].lower() != "bearer" or len(parts) != 2:
        raise HTTPException(status_code=401, detail="Invalid auth header")

    token = parts[1]
    payload = decode_token(token)
    if payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="Invalid token type")

    user_id = payload.get("sub")

    if mongodb.db is None:
        raise HTTPException(status_code=500, detail="Database not initialized")

    user = await mongodb.db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

async def get_current_active_user(user=Depends(get_current_user)):
    if not user.get("isActive", True):
        raise HTTPException(status_code=403, detail="Inactive user")
    return user
