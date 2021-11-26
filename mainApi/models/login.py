from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId


class LoginForm(BaseModel):
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
