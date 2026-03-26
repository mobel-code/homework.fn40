from pydantic import BaseModel


class CategoryCreate(BaseModel):
    name: str

class CategoryResponse(CategoryCreate):
    id: int

    class Config:
        from_attributes = True

class BookCreate(BaseModel):
    name: str
    price: int
    author: str
    category_id: int

class BookResponse(BookCreate):
    id: int

    class Config:
        from_attributes = True


class NewsBase(BaseModel):
    title: str
    category_id: int


class NewsCreate(NewsBase):
    pass


class NewsResponse(NewsBase):
    id: int

    class Config:
        from_attributes = True
