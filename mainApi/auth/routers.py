import pyotp

from fastapi import (
    APIRouter,
    Depends,
    status,
    HTTPException, Form
)
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from pymongo.results import InsertOneResult

from .auth import (
    get_current_user,
    authenticate_user,
    create_access_token,
    get_password_hash, get_user_by_email, get_admin_user
)

# from .settings import ACCESS_TOKEN_EXPIRE_MINUTES, db
from .settings import ACCESS_TOKEN_EXPIRE_MINUTES
from mainApi.config import db

from typing import List
from datetime import datetime, timedelta

from mainApi.models.user import UserModelDB, ShowUserModel, UpdateUserModel, CreateUserModel, CreateUserReplyModel

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

# ============= Creating path operations ==============
@router.post("/create_user", response_description="Add new user", response_model=CreateUserReplyModel, status_code=status.HTTP_201_CREATED)
async def create_user(user: CreateUserModel):
    # check if another with the same email already exist
    existing_email = await db["users"].find_one({"email": user.email})
    if existing_email is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")

    # turn user into a dictionary so that we can add keys
    new_user_dict = user.dict()
    new_user_dict['created_at'] = datetime.now().strftime("%m/%d/%y %H:%M:%S")
    new_user_dict['last_login'] = new_user_dict['created_at']  # last login same as created_at
    new_user_dict['hashed_password'] = get_password_hash(user.password)  # changing plain text password to hash
    otp_secret = pyotp.random_base32()  # generate secret to be shared with user
    new_user_dict['otp_secret'] = otp_secret
    # turn new_user_dict into a Usermodel after adding created_at, changing password to hash and adding otp_secret
    new_user: UserModelDB = UserModelDB.parse_obj(new_user_dict)  # turning it into a UserModel so that we get validation

    # add user to db
    # when we insert new_user, _id gets added to new_user
    insert_user_res: InsertOneResult = await db["users"].insert_one(new_user.dict())
    if not insert_user_res.acknowledged:
        raise Exception(f"Failed to add User to Database, :{new_user}")

    created_user = ShowUserModel.parse_obj(new_user)

    otp_uri = pyotp.totp.TOTP(otp_secret).provisioning_uri(name=user.email, issuer_name='IAS App')

    created_user_reply = CreateUserReplyModel(user=created_user, otp_secret=otp_secret, otp_uri=otp_uri)

    return created_user_reply


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login route, returns Bearer Token.
    SWAGGER FRIENDLY.
    Due to the swagger Api not letting me add otp as a required parameter
    the otp needs to be added to the the end of the password
    ex. 'passwordotpotp' .. no space just right after and otp is always 6 digits

    TODO find way to modify swagger to let me add otp separately, no login2 needed
    """
    password = form_data.password[:-6]  # exclude the last 6 digits
    otp = form_data.password[-6:]  # include only the last 6 digits

    user: UserModelDB = await authenticate_user(email=form_data.username, password=password, otp=otp)  # username is email
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect Authentication Data",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(user_id=str(user.id), expires_delta=access_token_expires)
    await db["users"].update_one({"email": form_data.username}, {"$set": {
        "last_login": datetime.now().strftime("%m/%d/%y %H:%M:%S"),
        "is_active": "true"
    }})

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login")
async def login2(form_data: OAuth2PasswordRequestForm = Depends(), otp: str = Form(...)):
    """
    Login route, returns Bearer Token.
    NOT SWAGGER FRIENDLY.
    Separate otp and OAuth2PasswordRequestForm.
    Prettier than the /token function since the requirement of otp is made clear
    """

    form_data.password += otp  # adds the otp to the end of the password to fit the login method

    return await login(form_data=form_data)


@router.get("/current", response_description="Current User", response_model=ShowUserModel)
async def current_user(current_user: UserModelDB = Depends(get_current_user)):
    return ShowUserModel.parse_obj(current_user.dict())  # we do not return the full UserModel, only the ShowUserModel


@router.get("/admin/list", response_description="List all users", response_model=List[ShowUserModel])
async def list_users(max_entries: int = 1000, admin_user: UserModelDB = Depends(get_admin_user)):
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
async def update_user(user_id: str, user: UpdateUserModel, admin_user: UserModelDB = Depends(get_admin_user)) -> ShowUserModel:
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
async def delete_user(user_id: str, admin_user: UserModelDB = Depends(get_admin_user)):
    delete_result = await db["users"].delete_one({"_id": user_id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"User {user_id} not found")
