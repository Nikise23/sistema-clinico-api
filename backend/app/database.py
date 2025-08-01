import os
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional


class Database:
    client: Optional[AsyncIOMotorClient] = None
    database = None


database = Database()


async def get_database() -> AsyncIOMotorClient:
    """Get database instance"""
    return database.database


async def connect_to_mongo():
    """Create database connection"""
    database.client = AsyncIOMotorClient(
        os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    )
    database.database = database.client[
        os.getenv("DATABASE_NAME", "personal_clinic_db")
    ]
    
    # Test connection
    try:
        await database.client.admin.command('ping')
        print("✅ Connected to MongoDB successfully!")
    except Exception as e:
        print(f"❌ Error connecting to MongoDB: {e}")


async def close_mongo_connection():
    """Close database connection"""
    if database.client:
        database.client.close()
        print("🔌 Disconnected from MongoDB")

async def get_collection(collection_name: str):
    """Get a specific collection"""
    db = await get_database()
    return db[collection_name]