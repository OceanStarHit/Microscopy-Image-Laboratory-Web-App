import time

import asyncio

import httpx
import pytest
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient

from mainApi.app.auth.auth import create_user
from mainApi.app.auth.models.user import CreateUserModel, CreateUserReplyModel
from mainApi.app.db.mongodb import get_database
from mainApi.app.db.mongodb_utils import connect_to_mongo, close_mongo_connection
from mainApi.app.main import app
from mainApi.config import MONGO_DB_NAME


class BearerAuth(httpx.Auth):
    def __init__(self, token_type, token):
        self._token_type = token_type
        self._token = token

    def auth_flow(self, request):
        request.headers["Authorization"] = f"{self._token_type} {self._token}"
        yield request

@pytest.fixture(scope="module")
def event_loop():

    loop = asyncio.get_event_loop()

    yield loop


@pytest.fixture(scope="module")
async def async_client() -> AsyncClient:

    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client


@pytest.fixture(scope="function")
async def async_client_auth(async_client, created_user) -> AsyncClient:
# async def async_client_auth(async_client) -> AsyncClient:

    async_client.auth = BearerAuth(token_type="Bearer", token=created_user.access_token)

    yield async_client
    #
    # async with AsyncClient(app=app, base_url="http://testserver") as client:
    #     yield client


@pytest.fixture(scope="function")
async def db() -> AsyncIOMotorClient:
    await connect_to_mongo()
    db = await get_database()
    yield db

    db.drop_database(MONGO_DB_NAME)  # delete testDB after test
    time.sleep(2)  # gotta sleep here for a while so there is time to delete the db before running next test

    await close_mongo_connection()


@pytest.fixture()
def user_to_create(scope="module") -> CreateUserModel:
    test_user = CreateUserModel(
        full_name="Test User",
        email="test@test.com",
        password="password",  # plain text password
    )

    yield test_user


@pytest.fixture(scope="function")
async def created_user(user_to_create, db) -> CreateUserReplyModel:
    print("Created User")
    created_user = await create_user(user_to_create, db)

    yield created_user