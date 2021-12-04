import time

import pyotp
import pytest
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm

from mainApi.app.auth.auth import create_user, login
from mainApi.app.auth.models.user import ShowUserModel, LoginUserReplyModel, CreateUserModel, CreateUserReplyModel, \
    ChangeUserPasswordModel

from mainApi.app.db.mongodb import get_database
from mainApi.app.db.mongodb_utils import connect_to_mongo, close_mongo_connection
from mainApi.config import MONGO_DB_NAME
from httpx import AsyncClient


class TestAuth:

    @pytest.mark.asyncio
    async def test_create_user(self, user_to_create: CreateUserModel, async_client: AsyncClient, db):
        users = await db[MONGO_DB_NAME]["users"].find().to_list(None)
        assert len(users) == 0

        response = await async_client.post(url="auth/register", json=jsonable_encoder(user_to_create))

        assert response.status_code == 201

        data = response.json()

        created_user = CreateUserReplyModel.parse_obj(data)

        # make sure the created user same as user to create, and that the defaults are correct
        assert created_user.user.full_name == user_to_create.full_name
        assert created_user.user.email == user_to_create.email
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
    async def test_login(self, async_client: AsyncClient,
                         user_to_create: CreateUserModel,
                         created_user: CreateUserReplyModel):

        # start of login
        otp = pyotp.TOTP(created_user.otp_secret)
        login_form = {"username": user_to_create.email, "password": user_to_create.password, "otp": otp.now()}

        response = await async_client.post(url="auth/login", data=login_form)

        assert response.status_code == 200

        data = response.json()

        logged_in_user = LoginUserReplyModel.parse_obj(data)

        assert logged_in_user is not None
        assert logged_in_user.user.email == user_to_create.email
        assert logged_in_user.access_token is not None
        assert logged_in_user.token_type == 'bearer'

    @pytest.mark.asyncio
    async def test_change_password(self, async_client: AsyncClient,
                                   user_to_create: CreateUserModel,
                                   created_user: CreateUserReplyModel):
        # start of login
        otp = pyotp.TOTP(created_user.otp_secret)
        login_form = {"username": user_to_create.email, "password": user_to_create.password, "otp": otp.now()}

        # start of login
        otp = pyotp.TOTP(created_user.otp_secret)

        data = ChangeUserPasswordModel(old_password=user_to_create.password, otp=otp.now(), new_password='new_password')
