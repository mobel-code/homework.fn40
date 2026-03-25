from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import Category, News


# CATEGORY CRUD
async def create_category(db: AsyncSession, name: str):
    category = Category(name=name)
    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category


async def get_categories(db: AsyncSession):
    result = await db.execute(select(Category))
    return result.scalars().all()


async def get_category(db: AsyncSession, category_id: int):
    result = await db.execute(select(Category).where(Category.id == category_id))
    return result.scalar_one_or_none()


async def delete_category(db: AsyncSession, category_id: int):
    category = await get_category(db, category_id)
    if category:
        await db.delete(category)
        await db.commit()
    return category


# NEWS CRUD
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