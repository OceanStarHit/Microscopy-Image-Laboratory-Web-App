from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from pymongo.results import InsertOneResult

from .settings import pwd_context, oauth2_scheme, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from mainApi.config import get_db
from bson import ObjectId
import pyotp

from datetime import datetime, timedelta
from typing import Optional

# from mainApi.config import get_mongo_db
from mainApi.auth.models.user import UserModelDB, CreateUserModel, ShowUserModel, CreateUserReplyModel

db = get_db()

#
# async def create_user(user: CreateUserModel) -> CreateUserReplyModel:
#     # check if another with the same email already exist
#     existing_email = await db["users"].find_one({"email": user.email})
#     if existing_email is not None:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
#
#     # turn user into a dictionary so that we can add keys
#     new_user_dict = user.dict()
#     new_user_dict['created_at'] = datetime.now().strftime("%m/%d/%y %H:%M:%S")
#     new_user_dict['last_login'] = new_user_dict['created_at']  # last login same as created_at
#     new_user_dict['hashed_password'] = get_password_hash(user.password)  # changing plain text password to hash
#     otp_secret = pyotp.random_base32()  # generate secret to be shared with user
#     new_user_dict['otp_secret'] = otp_secret
#     new_user_dict['is_admin'] = False
#     # turn new_user_dict into a UsermodelDB after adding created_at, changing password to hash and adding otp_secret
#     # turning it into a UserModelDB so that we get validation
#     new_user: UserModelDB = UserModelDB.parse_obj(new_user_dict)
#
#     # add user to db
#     # when we insert new_user, _id gets added to new_user
#     insert_user_res: InsertOneResult = await db["users"].insert_one(new_user.dict())
#     if not insert_user_res.acknowledged:
#         raise Exception(f"Failed to add User to Database, :{new_user}")
#
#     created_user = ShowUserModel.parse_obj(new_user)
#
#     otp_uri = pyotp.totp.TOTP(otp_secret).provisioning_uri(name=user.email, issuer_name='IAS App')
#
#     # create access token
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(user_id=str(new_user.id), expires_delta=access_token_expires)
#
#     created_user_reply = CreateUserReplyModel(user=created_user,
#                                               otp_secret=otp_secret,
#                                               otp_uri=otp_uri,
#                                               access_token=access_token,
#                                               token_type="bearer")
#
#     return created_user_reply


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def get_user_by_email(email: str) -> UserModelDB or None:
    user = await db["users"].find_one({"email": email})

    if user is not None:
        return UserModelDB.parse_obj(user)
    else:
        return None


async def get_user_by_id(user_id: str) -> UserModelDB or None:
    user = await db["users"].find_one({"_id": ObjectId(user_id)})

    if user is not None:
        return UserModelDB.parse_obj(user)
    else:
        return None


async def authenticate_user(email, password, otp: str) -> UserModelDB or None:
    # async def authenticate_user(form_data: OAuth2PasswordRequestForm = Depends()) -> UserModel or None:
    user: UserModelDB = await get_user_by_email(email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None

    # check the otp
    totp = pyotp.TOTP(user.otp_secret)
    if not totp.verify(otp):
        return None

    return user


def create_access_token(user_id: str, expires_delta: Optional[timedelta] = None) -> str:
    """ Create the token that the user will include in their header, claims must be json encodable """
    # to_encode = data.copy()
    claims = {"id": user_id}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    claims.update({"exp": expire})
    encode_jwt = jwt.encode(claims=claims, key=SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserModelDB:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        used_id: str = payload.get("id")
        if used_id is None:
            raise credentials_exception
        # token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user_by_id(used_id)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: UserModelDB = Depends(get_current_user)) -> UserModelDB:
    if current_user.is_active:
        return current_user
    else:
        raise HTTPException(status_code=400, detail="Inactive user")


async def get_admin_user(current_user: UserModelDB = Depends(get_current_user)) -> UserModelDB:
    if current_user.is_admin:
        return current_user
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not admin")
