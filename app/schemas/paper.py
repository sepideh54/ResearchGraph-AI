from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PaperCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)


class PaperUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=255)


class PaperResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    created_at: datetime