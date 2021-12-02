import os

from pathlib import Path

import functools
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

# ----------------- Database variables (MongoDB) --------------------------
from pydantic import BaseSettings, Field, validator


# if os.environ.get("IS_PRODUCTION", 'false').lower() == 'true':
#     db = client.DB
# elif os.environ.get("IS_TESTING", 'false').lower() == 'true':
#     db = client.testDB
# else:
#     db = client.devDB
# db = client.devDB

# db: AsyncIOMotorDatabase = client.devDB

# --------------- Storage/Volume variables, must match the location set in docker-compose.yml -----------------------
# image_path = Path('/image-storage')
# cache_path = Path('/cache-storage')
from starlette.datastructures import CommaSeparatedStrings

ALLOWED_HOSTS = CommaSeparatedStrings(os.getenv("ALLOWED_HOSTS", ""))

MONGODB_URL = os.getenv("MONGODB_URL", "")  # deploying without docker-compose
if not MONGODB_URL:
    MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
    MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
    MONGO_USER = os.getenv("MONGO_USER", "user")
    MONGO_PASS = os.getenv("MONGO_PASSWORD", "pass")

    if os.getenv("IS_PRODUCTION") and os.getenv("IS_PRODUCTION") == 'true':
        MONGO_DB_NAME = os.getenv("MONGO_DB", "db")
    elif os.getenv("IS_TESTING") and os.getenv("IS_TESTING") == 'true':
        MONGO_DB_NAME = os.getenv("MONGO_DB", "test_db")
    else:
        MONGO_DB_NAME = os.getenv("MONGO_DB", "dev_db")

    # MONGODB_URL = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}"
    MONGODB_URL = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}"

#
# class BasicSettings(BaseSettings):
#     mongo_url: str = Field(..., env='MONGODB_URL')
#     mongo_db_name: str = 'db'
#     image_path: Path = Path('/image-storage')
#     cache_path: Path = Path('/cache-storage')
#
#
# class DevSettings(BasicSettings):
#     mongo_db_name: str = 'devDB'
#
#
# class TestSettings(BasicSettings):
#     mongo_db_name: str = 'testDB'


# @functools.lru_cache
# def get_settings() -> BasicSettings:
#     if os.environ.get("IS_PRODUCTION", 'false').lower() == 'true':
#         return BasicSettings()
#     elif os.environ.get("IS_TESTING", 'false').lower() == 'true':
#         return TestSettings()
#     else:
#         return DevSettings()
#

# # @functools.lru_cache
# def get_db() -> AsyncIOMotorDatabase:
#     settings = get_settings()
#
#     client = AsyncIOMotorClient(settings.mongo_url)
#     db: AsyncIOMotorDatabase = client[settings.mongo_db_name]
#
#     return db

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