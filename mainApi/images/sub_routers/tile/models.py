from enum import Enum
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


class AlignedTiledModel(TileModel):
    x: int
    y: int

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
