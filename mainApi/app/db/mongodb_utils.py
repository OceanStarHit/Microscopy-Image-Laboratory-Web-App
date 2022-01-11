import logging

from motor.motor_asyncio import AsyncIOMotorClient
from app.db.mongodb import db
from config import MONGODB_URL
from config import MONGO_DB_NAME


async def connect_to_mongo():
    # logging.info("Connect to mongo...")
    db.client = AsyncIOMotorClient(MONGODB_URL)
    #print(MONGODB_URL);
    #print(MONGO_DB_NAME);
    # logging.info("Connected to mongo")


async def close_mongo_connection():
    # logging.info("Closing connection to mongo...")
    db.client.close()
    # logging.info("Connection to mongo is closed")