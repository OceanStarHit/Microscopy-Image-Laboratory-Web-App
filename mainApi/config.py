import os
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

# ----------------- Database variables (MongoDB) --------------------------
client = AsyncIOMotorClient(os.environ["MONGODB_URL"])
db: AsyncIOMotorDatabase = client.devDB


# mongo_db_client: AsyncIOMotorClient = None
#
# # mongoDb = mongoDbClient.db
#
# def get_mongo_db() -> AsyncIOMotorDatabase:
#     client: AsyncIOMotorClient = get_db_client()
#     return client.get_database("test_db")
#
# async def get_db_client() -> AsyncIOMotorClient:
#     """Return database client instance."""
#     return mongo_db_client
#
# async def connect_db():
#     """Create database connection."""
#     mongo_db_client = AsyncIOMotorClient(os.environ["MONGODB_URL"])
#     return mongo_db_client
#
# async def close_db():
#     """Close database connection."""
#     get_db_client().close()