import asyncio
import os

import pytest
from httpx import AsyncClient
#
# from mainApi.auth.models.user import CreateUserModel
# from mainApi.auth.routers import create_user
#

# from mainApi.app import app
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase


@pytest.fixture
def db():
    client = AsyncIOMotorClient(os.environ["MONGODB_URL"])
    # db: AsyncIOMotorDatabase = client.testDB
    db: AsyncIOMotorDatabase = client.devDB
    yield db


class TestAuth:
    @pytest.mark.asyncio
    async def test_create_user(self, db):
        users = await db["users"].find().to_list(None)
        assert len(users) == 0


# @pytest.mark.asyncio
# async def test_coroutine3():
    # from mainApi.config import db

    # res = await asyncio.sleep(5)
    # assert len(users) == 0
# This is the same as using the @pytest.mark.anyio on all test functions in the module
# pytestmark = pytest.mark.anyio
# loop = asyncio.get_event_loop()
# @pytest.mark.asyncio
# # @pytest.mark.anyio
# async def test_root():
#     await asyncio.sleep(5)
#     users = await db["users"].find().to_list(None)
    # assert len(users) == 1, "Single user in db"
    # async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
    #     response = await client.get("/test")
    # assert response.status_code == 200
    # assert response.json() == {"message": "Tomato"}

# class AuthTestCase(unittest.IsolatedAsyncioTestCase):
#
#     user = CreateUserModel(
#         full_name="Test User",
#         email="test@test.com",
#         password="password",  # plain text password
#     )
#
#     async def asyncSetUp(self):
#         """ Set up start by creating a user """
#         self.assertEqual(os.environ.get("IS_PRODUCTION", 'true').lower(), 'false', "Must not be in production mode")
#         self.assertEqual(os.environ.get("IS_TESTING", 'false').lower(), 'true', "Must be in testing mode")
#         # existing_email = await db["users"].find_one({"email": self.user.email})
#         # existing_email = await db["users"].find().to_list(None)
#
#
#     # async def asyncTearDown(self):
#     #     self.widget.dispose()
#
#     async def test_user_is_created(self):
#         # await create_user(self.user)
#         users = await db["users"].find().to_list(None)
#         self.assertEqual(len(users), 1, "Single user in db")
#
#
# if __name__ == '__main__':
#     unittest.main()
