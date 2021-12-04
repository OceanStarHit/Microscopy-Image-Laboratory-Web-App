import time

import asyncio
import pytest
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient

from mainApi.app.auth.auth import create_user
from mainApi.app.auth.models.user import CreateUserModel, CreateUserReplyModel
from mainApi.app.db.mongodb import get_database
from mainApi.app.db.mongodb_utils import connect_to_mongo, close_mongo_connection
from mainApi.app.main import app
from mainApi.config import MONGO_DB_NAME


@pytest.fixture(scope="module")
def event_loop():

    loop = asyncio.get_event_loop()

    yield loop


@pytest.fixture(scope="module")
async def async_client() -> AsyncClient:

    async with AsyncClient(app=app, base_url="http://testserver") as client:

        yield client


@pytest.fixture
async def db() -> AsyncIOMotorClient:
    await connect_to_mongo()
    db = await get_database()
    yield db

    db.drop_database(MONGO_DB_NAME)  # delete testDB after test
    time.sleep(2)  # gotta sleep here for a while so there is time to delete the db before running next test

    await close_mongo_connection()


@pytest.fixture()
def user_to_create() -> CreateUserModel:
    test_user = CreateUserModel(
        full_name="Test User",
        email="test@test.com",
        password="password",  # plain text password
    )

    yield test_user


@pytest.fixture()
async def created_user(user_to_create, db) -> CreateUserReplyModel:
    created_user = await create_user(user_to_create, db)

    yield created_user