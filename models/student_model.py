from pydantic import BaseModel, Field

class StudentCreate(BaseModel):
    name: str = Field(min_length=2)
    math: int = Field(ge=0, le=100)
    science: int = Field(ge=0, le=100)
    english: int = Field(ge=0, le=100)
