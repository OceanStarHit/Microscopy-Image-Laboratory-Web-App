from enum import Enum
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, validator, Field

from mainApi.auth.models.user import PyObjectId


class AlignMethodEnum(str, Enum):
    byRow = "byRow"
    byColumn = "byColumn"


class TileModelDB(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId = Field(default_factory=PyObjectId)  # reference to the user who uploaded the tile
    absolute_path: str
    file_name: str
    content_type: str  # MIME type
    width_px: int
    height_px: int

    offset_x: Optional[int] = 0
    offset_y: Optional[int] = 0

    row_index: Optional[int] = 0  # created by regex of name
    column_index: Optional[int] = 0  # created by regex of name
    channel: Optional[str] = "not specified"

    class Config:
        json_encoders = {ObjectId: str}


class AlignedTiledModel(TileModelDB):
    """ offsets are not optional """
    offset_x: int
    offset_y: int


class AlignNaiveRequest(BaseModel):
    method: AlignMethodEnum
    rows: int

    @validator('rows')
    def greater_than_or_equal_to_one(cls, v):
        assert v >= 1, "'rows' must be greater or equal to 1"
        return v

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "method": "byRow",
                "rows": "5",
            }
        }
