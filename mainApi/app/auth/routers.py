import pyotp
from bson import ObjectId

from fastapi import (
    APIRouter,
    Depends,
    status,
    HTTPException, Form
)
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.results import InsertOneResult

from .auth import (
    get_current_user,
    authenticate_user,
    create_access_token,
    get_password_hash, get_admin_user, create_user, login, login_swagger
)

# from .settings import ACCESS_TOKEN_EXPIRE_MINUTES, db
from .settings import ACCESS_TOKEN_EXPIRE_MINUTES

from typing import List
from datetime import datetime, timedelta

from mainApi.app.auth.models.user import UserModelDB, ShowUserModel, UpdateUserModel, CreateUserModel, \
    CreateUserReplyModel, LoginUserReplyModel
from mainApi.app.db.mongodb import get_database

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


# ============= Creating path operations ==============
@router.post("/register",
             response_description="Add new user",
             response_model=CreateUserReplyModel,
             status_code=status.HTTP_201_CREATED)
async def register(user: CreateUserModel, db: AsyncIOMotorClient = Depends(get_database)) -> CreateUserReplyModel:
    return await create_user(user, db)


@router.post("/token", response_model=LoginUserReplyModel)
async def _login_swagger(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncIOMotorClient = Depends(get_database)) -> LoginUserReplyModel:
    """
        Login route, returns Bearer Token.
        SWAGGER FRIENDLY.
        Due to the swagger Api not letting me add otp as a required parameter
        the otp needs to be added to the the end of the password
        ex. 'passwordotpotp' .. no space just right after and otp is always 6 digits

        TODO find way to modify swagger to let me add otp separately, no login2 needed
    """
    return await login_swagger(form_data=form_data, db=db)


@router.post("/login", response_model=LoginUserReplyModel)
async def _login(form_data: OAuth2PasswordRequestForm = Depends(),
                 otp: str = Form(...),
                 db: AsyncIOMotorClient = Depends(get_database)) -> LoginUserReplyModel:
    """
    Login route, returns Bearer Token.
    NOT SWAGGER FRIENDLY.
    Separate otp and OAuth2PasswordRequestForm.
    Prettier than the /token function since the requirement of otp is made clear
    """

    return await login(form_data=form_data, otp=otp, db=db)


@router.get("/current", response_description="Current User", response_model=ShowUserModel)
async def current_user(current_user: UserModelDB = Depends(get_current_user)):
    return ShowUserModel.parse_obj(current_user.dict())  # we do not return the full UserModel, only the ShowUserModel


@router.get("/renew_token", response_description=f"Renews token for another {ACCESS_TOKEN_EXPIRE_MINUTES} minutes", response_model=LoginUserReplyModel)
async def renew_token(current_user: UserModelDB = Depends(get_current_user)) -> LoginUserReplyModel:
    # create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(user_id=str(current_user.id), expires_delta=access_token_expires)

    reply = LoginUserReplyModel(
        user=ShowUserModel.parse_obj(current_user),
        access_token=access_token,
        token_type="bearer"
    )

    return reply


@router.get("/admin/list", response_description="List all users", response_model=List[ShowUserModel])
async def list_users(max_entries: int = 1000,
                     admin_user: UserModelDB = Depends(get_admin_user),
                     db: AsyncIOMotorClient = Depends(get_database)):
    users = await db["users"].find().to_list(max_entries)
    # for user in users:
    #     user["is_active"] = "false"
    #     try:
    #         last_login = datetime.strptime(user["last_login"], "%m/%d/%y %H:%M:%S")
    #         my_delta = datetime.now() - last_login
    #         if my_delta <= timedelta(days=30):
    #             user["is_active"] = "true"
    #     except ValueError:
    #         pass

    return users


@router.put("/admin/{user_id}", response_description="Update a user", response_model=UpdateUserModel)
async def update_user(user_id: str, user: UpdateUserModel,
                      admin_user: UserModelDB = Depends(get_admin_user),
                      db: AsyncIOMotorClient = Depends(get_database)) -> ShowUserModel:
    user = {k: v for k, v in user.dict().items() if v is not None}  # todo not sure this is needed

    if len(user) >= 1:
        update_result = await db["users"].update_one({"_id": user_id}, {"$set": user})

        if update_result.modified_count == 1:
            if updated_user := await db["users"].find_one({"_id": user_id}) is not None:
                return updated_user

    if (existing_user := await db["users"].find_one({"_id": user_id})) is not None:
        return existing_user

    raise HTTPException(status_code=404, detail=f"User {user_id} not found")


@router.delete("/admin/{user_id}", response_description="Delete a user")
async def delete_user(user_id: str,
                      admin_user: UserModelDB = Depends(get_admin_user),
                      db: AsyncIOMotorClient = Depends(get_database)):
    delete_result = await db["users"].delete_one({"_id": user_id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"User {user_id} not found")
