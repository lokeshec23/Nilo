# app/db/mongodb.py
from motor.motor_asyncio import AsyncIOMotorClient
from app.core import config

class MongoDB:
    client: AsyncIOMotorClient = None
    db = None

mongodb = MongoDB()

async def connect_to_mongo():
    mongodb.client = AsyncIOMotorClient(config.MONGO_URI)
    mongodb.db = mongodb.client[config.MONGO_DB]
    print("✅ Connected to MongoDB")

async def close_mongo_connection():
    mongodb.client.close()
    print("🛑 MongoDB connection closed")
