

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from schemas import (CategoryCreate, CategoryResponse)
from models import Category, News

async def create_category(category: CategoryCreate, db: AsyncSession) -> CategoryResponse:
    db_category = Category(**category.model_dump())
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return CategoryResponse.model_validate(db_category)


async def read_categories(db: AsyncSession) -> list[CategoryResponse]:
    results = await db.execute(select(Category))
    return [CategoryResponse.model_validate(category)for category in results.scalars().all()]


async def read_category(category_id: int, db: AsyncSession) -> CategoryResponse:
    category = await db.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404,detail='hato')
    return CategoryResponse.model_validate(category)


async def update_category(category_id: int, category: CategoryCreate, db: AsyncSession) -> CategoryResponse:
    db_category = await db.get(Category, category_id)
    if not db_category:
        raise HTTPException(status_code=404,detail='hato')
    for attr, value in category.__dict__.items():
        setattr(db_category, attr, value)

    await db.commit()
    await db.refresh(db_category)

    return CategoryResponse.model_validate(db_category)


async def delete_category(category_id: int, db: AsyncSession) -> dict:
    category = await db.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404,detail='hato')

    await db.delete(category)
    await db.commit()

    return {'message': 'deleted'}

async def create_news(db: AsyncSession, news_data):
    news = News(**news_data.dict())
    db.add(news)
    await db.commit()
    await db.refresh(news)
    return news


async def get_all_news(db: AsyncSession):
    result = await db.execute(select(News))
    return result.scalars().all()


async def get_news(db: AsyncSession, news_id: int):
    result = await db.execute(select(News).where(News.id == news_id))
    return result.scalar_one_or_none()


async def delete_news(db: AsyncSession, news_id: int):
    news = await get_news(db, news_id)
    if news:
        await db.delete(news)
        await db.commit()
    return news

