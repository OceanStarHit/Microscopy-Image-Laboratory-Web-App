import pytest
from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient

from mainApi.app.auth.models.user import CreateUserModel, ShowUserModel, CreateUserReplyModel
from mainApi.config import MONGO_DB_NAME


@pytest.fixture(scope="class")
def user_to_create():
    test_user = CreateUserModel(
        full_name="Test User",
        email="test@test.com",
        password="password",  # plain text password
    )

    yield test_user


class TestFoo:

    @pytest.mark.asyncio
    async def test_create_user_foo(self, user_to_create, async_client: AsyncClient, db):
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
