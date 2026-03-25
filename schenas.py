from pydantic import BaseModel
from typing import Optional


# CATEGORY
class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: int

    class Config:
        from_attributes = True


# NEWS
class NewsBase(BaseModel):
    title: str
    content: Optional[str] = None
    category_id: int


class NewsCreate(NewsBase):
    pass


class NewsResponse(NewsBase):
    id: int

    class Config:
        from_attributes = True