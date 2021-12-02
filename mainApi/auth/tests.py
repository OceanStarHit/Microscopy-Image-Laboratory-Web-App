import asyncio
import os

import pytest
from bson import ObjectId
from fastapi.encoders import jsonable_encoder

from mainApi.auth.models.user import ShowUserModel


@pytest.fixture
def db():
    from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
    from mainApi.config import get_settings, get_db

    print('before db')
    assert os.environ.get('IS_TESTING', None) == 'true', "Must set 'IS_TESTING' env variable to 'true' before running test"
    os.environ.update({'IS_TESTING': 'true'})  # temporarily sets IS_TESTING environment variable
    settings = get_settings()
    assert settings.mongo_db_name == 'testDB'

    db = get_db()
    assert db.name == 'testDB'

    yield db

    client = AsyncIOMotorClient(settings.mongo_url)

    client.drop_database('testDB')  # delete testDB after test
    print('after db')


class TestAuth:

    @pytest.mark.asyncio
    async def test_create_user(self, db):
        from mainApi.auth.models.user import CreateUserModel, UserModelDB
        from mainApi.auth.routers import create_user

        users = await db["users"].find().to_list(None)
        assert len(users) == 0

        user_to_create = CreateUserModel(
            full_name="Test User",
            email="test@test.com",
            password="password",  # plain text password
        )

        created_user = await create_user(user_to_create)

        # make sure the created user same as user to create, and that the defaults are corrent
        assert created_user.user.full_name == user_to_create.full_name
        assert created_user.user.email == user_to_create.email
        assert created_user.user.is_admin is False
        assert created_user.user.is_active is True

        # look for created user in 'users'...should only be one user..
        users = await db["users"].find().to_list(None)
        assert ShowUserModel.parse_obj(users[0]).id == created_user.user.id

        # search for created user by email
        user_db_by_email = await db["users"].find_one({"email": created_user.user.email})
        assert user_db_by_email['_id'] == str(created_user.user.id)
        assert ShowUserModel.parse_obj(user_db_by_email).id == created_user.user.id

        # search for created user by id
        user_db = await db["users"].find_one({"_id": str(created_user.user.id)})
        assert user_db['_id'] == str(created_user.user.id)
