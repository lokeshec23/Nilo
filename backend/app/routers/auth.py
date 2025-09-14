from fastapi import APIRouter, HTTPException
from bson import ObjectId
from datetime import datetime
from app.db.mongodb import mongodb
from app.schemas.user import UserCreate, UserLogin, UserOut
from app.schemas.token import Token
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.core.config import REFRESH_TOKEN_EXPIRE

router = APIRouter()

# ✅ Register endpoint
@router.post("/register", response_model=UserOut)
async def register(user: UserCreate):
    if mongodb.db is None:
        raise HTTPException(status_code=500, detail="Database not initialized")

    existing = await mongodb.db.users.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = {
        "email": user.email,
        "fullName": user.fullName,
        "passwordHash": hash_password(user.password),
        "isActive": True,
        "globalPermissions": [],
    }
    result = await mongodb.db.users.insert_one(new_user)

    return UserOut(
        id=str(result.inserted_id),
        email=user.email,
        fullName=user.fullName,
        isActive=True,
    )

# ✅ Login endpoint (only email + password)
@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):
    if mongodb.db is None:
        raise HTTPException(status_code=500, detail="Database not initialized")

    record = await mongodb.db.users.find_one({"email": credentials.email})
    if not record or not verify_password(credentials.password, record["passwordHash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    sub = str(record["_id"])
    access_token = create_access_token(sub)
    refresh_token, jti = create_refresh_token(sub)

    await mongodb.db.refresh_tokens.insert_one(
        {
            "jti": jti,
            "user_id": ObjectId(sub),
            "issued_at": datetime.utcnow(),
            "revoked": False,
        }
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }

# ✅ Refresh endpoint
@router.post("/refresh", response_model=Token)
async def refresh_token(payload: dict):
    if mongodb.db is None:
        raise HTTPException(status_code=500, detail="Database not initialized")

    token = payload.get("refresh_token")
    if not token:
        raise HTTPException(status_code=400, detail="refresh_token required")

    try:
        data = decode_token(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    if data.get("type") != "refresh" or "jti" not in data:
        raise HTTPException(status_code=401, detail="Invalid token type")

    jti = data["jti"]
    db_record = await mongodb.db.refresh_tokens.find_one({"jti": jti})
    if (
        not db_record
        or db_record.get("revoked")
        or db_record.get("expires_at", datetime.utcnow()) < datetime.utcnow()
    ):
        raise HTTPException(status_code=401, detail="Refresh token expired or revoked")

    user_id = str(db_record["user_id"])
    # issue new access token
    access_token = create_access_token(subject=user_id)
    # rotate refresh token (new one, revoke old)
    new_refresh_token, new_jti = create_refresh_token(subject=user_id)

    # revoke old refresh
    await mongodb.db.refresh_tokens.update_one(
        {"jti": jti}, {"$set": {"revoked": True}}
    )

    # save new refresh
    await mongodb.db.refresh_tokens.insert_one(
        {
            "jti": new_jti,
            "user_id": ObjectId(user_id),
            "issued_at": datetime.utcnow(),
            "expires_at": datetime.utcnow() + REFRESH_TOKEN_EXPIRE,
            "revoked": False,
        }
    )

    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
    }


# ✅ Logout endpoint
@router.post("/logout")
async def logout(payload: dict):
    if mongodb.db is None:
        raise HTTPException(status_code=500, detail="Database not initialized")

    token = payload.get("refresh_token")
    if not token:
        raise HTTPException(status_code=400, detail="refresh_token required")

    try:
        data = decode_token(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    jti = data.get("jti")
    if not jti:
        raise HTTPException(status_code=400, detail="Invalid refresh token payload")

    await mongodb.db.refresh_tokens.update_one(
        {"jti": jti}, {"$set": {"revoked": True}}
    )

    return {"msg": "Logged out successfully"}