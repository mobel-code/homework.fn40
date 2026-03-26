from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import uvicorn

from schemas import (CategoryCreate, CategoryResponse,
                     NewsCreate, NewsResponse)
from database import get_db, engine, Base
import crud

async def init_db():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def lifespan(app:FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)



@app.post('/category/', response_model=CategoryResponse)
async def create_category_endpoint(category: CategoryCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_category(category, db)

@app.get('/category/', response_model=list[CategoryResponse])
async def read_categories_endpoint(db: AsyncSession = Depends(get_db)):
    return await crud.read_categories(db)

@app.get('/category/{category_id/}', response_model=CategoryResponse)
async def read_category_endpoint(category_id: int , db: AsyncSession = Depends(get_db)):
    return await crud.read_category(category_id, db)

@app.put('/category/{category_id/}', response_model=CategoryResponse)
async def update_category_endpoint(category_id: int ,category: CategoryCreate, db: AsyncSession = Depends(get_db)):
    return await crud.update_category(category_id, category, db)

@app.delete('/category/{category_id/}', response_model=dict)
async def delete_category_endpoint(category_id: int , db: AsyncSession = Depends(get_db)):
    return await crud.delete_category(category_id, db)

@app.post("/news/", response_model=NewsResponse)
async def create_news(news: NewsCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_news(db, news)


@app.get("/news/", response_model=list[NewsResponse])
async def get_news(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_news(db)


@app.get("/news/{news_id}", response_model=NewsResponse)
async def get_one_news(news_id: int, db: AsyncSession = Depends(get_db)):
    news = await crud.get_news(db, news_id)
    if not news:
        raise HTTPException(status_code=404, detail="Not found")
    return news


@app.delete("/news/{news_id}")
async def delete_news(news_id: int, db: AsyncSession = Depends(get_db)):
    result = await crud.delete_news(db, news_id)
    if not result:
        raise HTTPException(status_code=404, detail="Not found")
    return {"message": "Deleted"}

if __name__ == "__main__":
    uvicorn.run(app)


