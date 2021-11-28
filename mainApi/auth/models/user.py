from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class UserModelDB(BaseModel):
    """
    This is the model as stored on the database
    """
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    full_name: str
    email: EmailStr
    # mobile: int
    hashed_password: str #
    otp_secret: str  # secret to be shared with user, either directly or through a QR code

    is_admin: bool
    is_active: bool
    created_at: str
    last_login: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "_id": "random unique string",
                "full_name": "Jane Doe",
                "email": "jdoe@example.com",
                # "mobile": "11112222",
                "hashed_password": "fakeHashedPassword",

                "is_admin": "false",
                "is_active": "True",
                "created_at": "datetime",
                "last_login": "datetime",
            }
        }


class CreateUserModel(BaseModel):
    full_name: str
    email: EmailStr
    # mobile: int
    password: str # plain text password
    # is_admin: Optional[bool] = False
    is_active: Optional[bool] = True

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "full_name": "Jane Doe",
                "email": "jdoe@example.com",
                # "mobile": "11112222",
                "password": "fakeHashPassword",
            }
        }


class UpdateUserModel(BaseModel):
    full_name: Optional[str]
    email: Optional[EmailStr]
    # mobile: Optional[int]

    is_admin: Optional[bool]
    is_active: Optional[bool]
    created_at: Optional[str]
    last_login: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "full_name": "Jane Doe",
                "email": "jdoe@example.com",
                # "mobile": "11112222",

                "is_admin": "false",
                "is_active": "True",
                "created_at": "datetime",
                "last_login": "datetime",
            }
        }


## REPLIES

class ShowUserModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    full_name: Optional[str]
    email: Optional[EmailStr]
    # mobile: Optional[int]

    is_admin: Optional[bool]
    is_active: Optional[bool]
    created_at: Optional[str]
    last_login: Optional[str]

    class Config:
        arbitrary_types_allowed = False
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "_id": "random unique string",
                "full_name": "Jane Doe",
                "email": "jdoe@example.com",
                # "mobile": "11112222",

                "is_admin": "false",
                "is_active": "true",
                "created_at": "datetime",
                "last_login": "datetime",
            }
        }


class LoginUserReplyModel(BaseModel):
    """ This is what is returned when a user logins """
    user: ShowUserModel
    access_token: str
    token_type: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class CreateUserReplyModel(LoginUserReplyModel):
    """ This is what is returned in the reply when creating a new user, notice that it extends LoginUserReplyModel """
    otp_secret: str
    otp_uri: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        # schema_extra = {
        #     "example": {
        #         "otp_uri": "otpauth://totp/LABEL?PARAMETERS"
        #     }
        # }