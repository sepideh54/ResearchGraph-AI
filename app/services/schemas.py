from pydantic import BaseModel, Field

class PageData(BaseModel):
    page_number: int = Field(ge=1)
    text: str