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
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class UserModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    full_name: str
    email: EmailStr
    mobile: int
    password: str

    is_admin: bool = False
    is_active: bool = True
    created_at: str
    last_login: str


    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "full_name": "Jane Doe",
                "email": "jdoe@example.com",
                "mobile": "11112222",
                "password": "fakeHashPassword",

                "is_admin": "false",
                "is_active": "True",
                "created_at": "datetime",
                "last_login": "datetime",
            }
        }

class CreateUserModel(BaseModel):
    full_name: str
    email: EmailStr
    mobile: int
    password: str
    is_admin: Optional[bool] = False
    is_active: Optional[bool] = True

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "full_name": "Jane Doe",
                "email": "jdoe@example.com",
                "mobile": "11112222",
                "password": "fakeHashPassword",
            }
        }


class UpdateUserModel(BaseModel):
    full_name: Optional[str]
    email: Optional[EmailStr]
    mobile: Optional[int]

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
                "mobile": "11112222",

                "is_admin": "false",
                "is_active": "True",
                "created_at": "datetime",
                "last_login": "datetime",
            }
        }

class ShowUserModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    full_name: Optional[str]
    email: Optional[EmailStr]
    mobile: Optional[int]

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
                "mobile": "11112222",

                "is_admin": "false",
                "created_at": "datetime",
                "last_login": "datetime",
            }
        }