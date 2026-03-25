from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager

from database import engine, Base, get_db
import crud
from schemas import (
    CategoryCreate, CategoryResponse,
    NewsCreate, NewsResponse
)

# DB init
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)



@app.post("/categories/", response_model=CategoryResponse)
async def create_category(category: CategoryCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_category(db, category.name)


@app.get("/categories/", response_model=list[CategoryResponse])
async def get_categories(db: AsyncSession = Depends(get_db)):
    return await crud.get_categories(db)


@app.delete("/categories/{category_id}")
async def delete_category(category_id: int, db: AsyncSession = Depends(get_db)):
    result = await crud.delete_category(db, category_id)
    if not result:
        raise HTTPException(status_code=404, detail="Not found")
    return {"message": "Deleted"}


# ================= NEWS =================

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