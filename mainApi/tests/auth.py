import os

import asyncio
import time

import pyotp
import pytest
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from motor.motor_asyncio import AsyncIOMotorClient

from mainApi.app.auth.auth import create_user, login
from mainApi.app.auth.models.user import ShowUserModel, LoginUserReplyModel, CreateUserModel


#
# @pytest.yield_fixture
# def event_loop():
#     """Create an instance of the default event loop for each test case."""
#     policy = asyncio.get_event_loop_policy()
#     res = policy.new_event_loop()
#     asyncio.set_event_loop(res)
#     res._close = res.close
#     res.close = lambda: None
#
#     yield res
#
#     res._close()
#
from mainApi.app.db.mongodb import get_database
from mainApi.app.db.mongodb_utils import connect_to_mongo, close_mongo_connection
from mainApi.config import MONGO_DB_NAME


@pytest.fixture(scope="session")
def test_user():
    test_user = CreateUserModel(
        full_name="Test User",
        email="test@test.com",
        password="password",  # plain text password
    )

    yield test_user


@pytest.fixture
async def db():
    await connect_to_mongo()
    db = await get_database()
    yield db

    db.drop_database(MONGO_DB_NAME)  # delete testDB after test
    time.sleep(2)

    await close_mongo_connection()



# @pytest.fixture
# def db():
#     from motor.motor_asyncio import AsyncIOMotorClient
#     from mainApi.config import get_settings, get_db
#
#     print('before db')
#     assert os.environ.get('IS_TESTING', None) == 'true', "Must set 'IS_TESTING' env variable to 'true' before running test"
#     os.environ.update({'IS_TESTING': 'true'})  # temporarily sets IS_TESTING environment variable
#     settings = get_settings()
#     assert settings.mongo_db_name == 'testDB'
#
#     db = get_db()
#     assert db.name == 'testDB'
#
#     yield db
#
#     # client = AsyncIOMotorClient(settings.mongo_url, io_loop=event_loop)
#     client = AsyncIOMotorClient(settings.mongo_url)
#
#     client.drop_database('testDB')  # delete testDB after test
#     print('after db')


# @pytest.fixture
# def db():
#     # from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
#     from mainApi.config import get_settings, get_db
#     settings = get_settings()
#
#     print('before db')
#     assert os.environ.get('IS_TESTING', None) == 'true', "Must set 'IS_TESTING' env variable to 'true' before running test"
#     os.environ.update({'IS_TESTING': 'true'})  # temporarily sets IS_TESTING environment variable
#     assert settings.mongo_db_name == 'testDB'
#
#     client = MongoClient(settings.mongo_url)
#     db = client[settings.mongo_db_name]
#
#     assert db.name == 'testDB'
#
#     yield db
#
#     client.drop_database('testDB')  # delete testDB after test
#     print('after db')

# @pytest.fixture
# def created_user():
#     from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
#     from mainApi.config import get_settings, get_db
#
#
#     yield created_user


class TestAuth:

    @pytest.mark.asyncio
    async def test_create_user(self, test_user, db):

        users = await db[MONGO_DB_NAME]["users"].find().to_list(None)
        assert len(users) == 0

        created_user = await create_user(test_user, db)

        # make sure the created user same as user to create, and that the defaults are correct
        assert created_user.user.full_name == test_user.full_name
        assert created_user.user.email == test_user.email
        assert created_user.user.is_admin is False
        assert created_user.user.is_active is True

        # look for created user in 'users'...should only be one user..
        users = await db[MONGO_DB_NAME]["users"].find().to_list(None)
        assert ShowUserModel.parse_obj(users[0]).id == created_user.user.id

        # search for created user by email
        user_db_by_email = await db[MONGO_DB_NAME]["users"].find_one({"email": created_user.user.email})
        assert user_db_by_email['_id'] == str(created_user.user.id)
        assert ShowUserModel.parse_obj(user_db_by_email).id == created_user.user.id

        # search for created user by id
        user_db = await db[MONGO_DB_NAME]["users"].find_one({"_id": str(created_user.user.id)})
        assert user_db['_id'] == str(created_user.user.id)

    # @pytest.mark.asyncio
    # async def test_login2(self, event_loop):
    #     # start by creating a user, cannot be fixture due to async TODO
    #     from mainApi.app.auth.models.user import CreateUserModel
    #     from mainApi.app.auth.routers import create_user
    #     from mainApi.app.auth.routers import login2
    #
    #     from motor.motor_asyncio import AsyncIOMotorClient
    #     from mainApi.config import get_settings, get_db
    #
    #     print('before db')
    #     assert os.environ.get('IS_TESTING',
    #                           None) == 'true', "Must set 'IS_TESTING' env variable to 'true' before running test"
    #     os.environ.update({'IS_TESTING': 'true'})  # temporarily sets IS_TESTING environment variable
    #     settings = get_settings()
    #     assert settings.mongo_db_name == 'testDB'
    #
    #     db = get_db()
    #     assert db.name == 'testDB'
    #
    #     client = AsyncIOMotorClient(settings.mongo_url, io_loop=event_loop)
    #
    #     client.drop_database('testDB')  # delete testDB after test
    #     print('after db')
    #
    #
    #     user_to_create = CreateUserModel(
    #         full_name="Test User",
    #         email="test@test.com",
    #         password="password",  # plain text password
    #     )
    #
    #     created_user = await create_user(user_to_create)
    #
    #     # start of login
    #     form = OAuth2PasswordRequestForm(username=created_user.user.email, password='password', scope="")
    #     otp = pyotp.TOTP(created_user.otp_secret)
    #
    #     login_reply: LoginUserReplyModel = await login2(form, otp=otp.now())
    #
    #     assert login_reply is not None
    #     assert login_reply.user.email == user_to_create.email
    #     assert login_reply.access_token is not None
    #     assert login_reply.token_type == 'bearer'



    @pytest.mark.asyncio
    async def test_login2(self, test_user, db):
        # start by creating a user, cannot be fixture due to async TODO



        created_user = await create_user(test_user, db)

        # start of login
        form = OAuth2PasswordRequestForm(username=created_user.user.email, password='password', scope="")
        otp = pyotp.TOTP(created_user.otp_secret)

        login_reply: LoginUserReplyModel = await login(form_data=form, otp=otp.now(), db=db)

        assert login_reply is not None
        assert login_reply.user.email == test_user.email
        assert login_reply.access_token is not None
        assert login_reply.token_type == 'bearer'

