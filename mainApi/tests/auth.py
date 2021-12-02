import time

import pyotp
import pytest
from fastapi.security import OAuth2PasswordRequestForm

from mainApi.app.auth.auth import create_user, login
from mainApi.app.auth.models.user import ShowUserModel, LoginUserReplyModel, CreateUserModel

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
    time.sleep(2)  # gotta sleep here for a while because so there is time to delete the db before running next test

    await close_mongo_connection()


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

    @pytest.mark.asyncio
    async def test_login(self, test_user, db):
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
