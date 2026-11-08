from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


class PaperCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    filename: str = Field(min_length=1, max_length=255)


class PaperUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=255)


class PaperResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    filename: str
    created_at: datetime