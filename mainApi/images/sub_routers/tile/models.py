from enum import Enum
from typing import Optional

from pydantic import BaseModel, validator


class AlignMethodEnum(str, Enum):
    byRow = "byRow"
    byColumn = "byColumn"


class TileModel(BaseModel):
    absolute_path: str
    file_name: str
    content_type: str  # MIME type
    width_px: int
    height_px: int
    offset_x: Optional[int] = 0
    offset_y: Optional[int] = 0


class AlignedTiledModel(TileModel):
    """ offsets are not optional """
    offset_x: int
    offset_y: int


class AlignRequest(BaseModel):
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
